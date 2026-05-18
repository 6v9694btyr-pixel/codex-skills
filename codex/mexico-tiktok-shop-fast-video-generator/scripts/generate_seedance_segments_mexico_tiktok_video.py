from __future__ import annotations

import argparse
import asyncio
import base64
import json
import mimetypes
import os
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_TASKS_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "ep-20260511103248-tcqpx"


def load_env(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    env: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def tasks_endpoint(value: str) -> str:
    base = (value or DEFAULT_TASKS_URL).rstrip("/")
    if base.endswith("/contents/generations/tasks"):
        return base
    if base.endswith("/api/v3"):
        return f"{base}/contents/generations/tasks"
    return f"{base}/api/v3/contents/generations/tasks"


def request_json(url: str, api_key: str, method: str = "GET", body: dict | None = None) -> dict:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def extract_task_id(payload: dict) -> str:
    return (
        payload.get("id")
        or payload.get("task_id")
        or payload.get("data", {}).get("id")
        or payload.get("data", {}).get("task_id")
        or ""
    )


def extract_video_url(payload: dict) -> str:
    content = payload.get("content") or payload.get("data", {}).get("content") or {}
    if isinstance(content, dict):
        for key in ("video_url", "url"):
            if content.get(key):
                return content[key]
    for key in ("video_url", "url"):
        if payload.get(key):
            return payload[key]
        if isinstance(payload.get("data"), dict) and payload["data"].get(key):
            return payload["data"][key]
    return ""


def valid_image_url(value: str) -> bool:
    return value.startswith(("http://", "https://", "data:image/"))


def local_image_data_url(value: str, base_dir: Path | None = None) -> str:
    path = Path(value)
    if not path.is_absolute() and base_dir:
        path = base_dir / path
    if not path.exists() or not path.is_file():
        return ""
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    if not mime.startswith("image/"):
        return ""
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def reference_image_urls(spec: dict, base_dir: Path | None = None) -> list[str]:
    urls: list[str] = []
    for key in ("reference_image_urls", "image_urls", "reference_images", "image_paths"):
        values = spec.get(key)
        if isinstance(values, str):
            values = [values]
        if isinstance(values, list):
            for value in values:
                if not isinstance(value, str):
                    continue
                value = value.strip()
                if valid_image_url(value):
                    urls.append(value)
                    continue
                data_url = local_image_data_url(value, base_dir)
                if data_url:
                    urls.append(data_url)
    return list(dict.fromkeys(urls))


def submit_task(endpoint: str, api_key: str, model: str, spec: dict) -> str:
    content = [{"type": "text", "text": spec["prompt"]}]
    for url in reference_image_urls(spec):
        content.append({"type": "image_url", "image_url": {"url": url}, "role": "first_frame"})
    body = {
        "model": spec.get("model") or model,
        "content": content,
        "resolution": spec.get("resolution", "720p"),
        "ratio": spec.get("ratio", "9:16"),
        "duration": int(spec.get("duration", spec.get("duration_seconds", 8))),
        "watermark": bool(spec.get("watermark", False)),
        "generate_audio": bool(spec.get("generate_audio", False)),
    }
    created = request_json(endpoint, api_key, "POST", body)
    task_id = extract_task_id(created)
    if not task_id:
        raise RuntimeError(f"No task id returned: {json.dumps(created, ensure_ascii=False)}")
    return task_id


def wait_and_download(endpoint: str, api_key: str, task_id: str, output: Path, status_file: Path) -> dict:
    status_url = f"{endpoint}/{task_id}"
    for attempt in range(360):
        status = request_json(status_url, api_key)
        state = (status.get("status") or status.get("data", {}).get("status") or "").lower()
        status_file.write_text(
            json.dumps({"task_id": task_id, "latest_response": status}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"{output.name}: poll {attempt + 1}, {state or 'unknown'}")

        if state in {"succeeded", "completed", "success"}:
            video_url = extract_video_url(status)
            if not video_url:
                raise RuntimeError(f"Task succeeded but no video URL: {json.dumps(status, ensure_ascii=False)}")
            with urlopen(video_url, timeout=180) as response:
                output.write_bytes(response.read())
            return {"task_id": task_id, "status": state, "output": str(output)}

        if state in {"failed", "cancelled", "canceled", "expired"}:
            raise RuntimeError(f"Task {task_id} ended with {state}: {json.dumps(status, ensure_ascii=False)}")

        time.sleep(10 if attempt else 4)

    raise RuntimeError(f"Task {task_id} still running after extended polling. Re-run later to resume.")


def normalized_segments(spec: dict, base_dir: Path | None = None) -> list[dict]:
    segments = spec.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("Spec must include exactly 3 segments for shots 1-3, 4-6, and 7-9.")
    if len(segments) != 3:
        raise ValueError("Expected exactly 3 segments, each covering 3 of the 9 shots.")

    normalized: list[dict] = []
    for index, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict):
            raise ValueError(f"Segment {index} must be an object.")
        prompt = str(segment.get("prompt", "")).strip()
        if not prompt:
            raise ValueError(f"Segment {index} is missing prompt.")
        normalized.append(
            {
                **segment,
                "segment": segment.get("segment", index),
                "duration": int(segment.get("duration", spec.get("segment_duration", 8))),
                "resolution": segment.get("resolution", spec.get("resolution", "720p")),
                "ratio": segment.get("ratio", spec.get("ratio", "9:16")),
                "watermark": segment.get("watermark", spec.get("watermark", False)),
                "generate_audio": segment.get("generate_audio", spec.get("generate_audio", False)),
                "model": segment.get("model", spec.get("model")),
                "reference_image_urls": reference_image_urls(spec, base_dir) + reference_image_urls(segment, base_dir),
                "prompt": prompt,
            }
        )
    return normalized


def generate_segment(endpoint: str, api_key: str, model: str, run_dir: Path, segment: dict, index: int) -> dict:
    stem = f"segment_{index:02d}"
    task_file = run_dir / f"{stem}_task.json"
    video_file = run_dir / f"{stem}_silent.mp4"

    task_id = ""
    if task_file.exists():
        try:
            task_id = json.loads(task_file.read_text(encoding="utf-8")).get("task_id", "")
        except json.JSONDecodeError:
            task_id = ""

    if video_file.exists() and video_file.stat().st_size > 1000:
        print(f"Using existing segment: {video_file}")
        return {"segment": index, "status": "existing", "output": str(video_file), "task_id": task_id}

    if not task_id:
        print(f"Submitting segment {index}/3 with model={segment.get('model') or model}, duration={segment['duration']}s")
        task_id = submit_task(endpoint, api_key, model, segment)
        task_file.write_text(json.dumps({"task_id": task_id, "segment": index}, ensure_ascii=False, indent=2), encoding="utf-8")

    result = wait_and_download(endpoint, api_key, task_id, video_file, task_file)
    return {"segment": index, **result}


def concat_videos(segment_paths: list[Path], output: Path, list_file: Path) -> None:
    lines = []
    for path in segment_paths:
        escaped = path.as_posix().replace("'", "'\\''")
        lines.append(f"file '{escaped}'")
    list_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(output),
        ],
        check=True,
    )


async def make_voiceover(spec: dict, output: Path) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError("Missing edge-tts. Install it with: python -m pip install edge-tts") from exc

    voiceover = spec.get("voiceover", "").strip()
    if not voiceover:
        return
    voice = spec.get("voice", "es-MX-DaliaNeural")
    rate = spec.get("voice_rate", "+12%")
    pitch = spec.get("voice_pitch", "+2Hz")
    communicate = edge_tts.Communicate(voiceover, voice, rate=rate, pitch=pitch)
    await communicate.save(str(output))


def add_voiceover(video: Path, audio: Path, output: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-filter:a",
            "volume=1.2",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            str(output),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate three Seedance 1.5 Pro segments and stitch one Mexico TikTok Shop video.")
    parser.add_argument("--spec", required=True, help="Path to generation spec JSON with 3 segments.")
    parser.add_argument("--env", default=".env.local", help="Path to .env.local containing Seedance credentials.")
    parser.add_argument("--out", default="outputs", help="Output directory.")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    env = {**os.environ, **load_env(Path(args.env).resolve())}

    api_key = env.get("SEEDANCE_API_KEY") or env.get("ARK_API_KEY") or ""
    if not api_key:
        raise SystemExit("Missing SEEDANCE_API_KEY or ARK_API_KEY.")

    endpoint = tasks_endpoint(env.get("SEEDANCE_BASE_URL") or env.get("ARK_BASE_URL") or DEFAULT_TASKS_URL)
    model = env.get("SEEDANCE_VIDEO_MODEL") or env.get("ARK_VIDEO_MODEL") or spec.get("model") or DEFAULT_MODEL

    out_root = Path(args.out).resolve()
    slug = spec.get("output_slug", "mexico_tiktok_shop_video")
    run_dir = out_root / slug
    run_dir.mkdir(parents=True, exist_ok=True)

    segments = normalized_segments(spec, spec_path.parent)
    results = [generate_segment(endpoint, api_key, model, run_dir, segment, index) for index, segment in enumerate(segments, start=1)]
    segment_paths = [Path(result["output"]) for result in results]

    stitched_video = run_dir / f"{slug}_stitched_silent.mp4"
    voiceover_file = run_dir / f"{slug}_voiceover.mp3"
    final_video = run_dir / f"{slug}_with_voice.mp4"
    concat_list = run_dir / "concat_segments.txt"

    output = stitched_video
    try:
        concat_videos(segment_paths, stitched_video, concat_list)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        summary = {
            "final_video": "",
            "stitched_video": "",
            "segment_videos": [str(path) for path in segment_paths],
            "voiceover": "",
            "results": results,
            "error": f"Unable to stitch segments with ffmpeg: {exc}",
        }
        (run_dir / "generation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    try:
        asyncio.run(make_voiceover(spec, voiceover_file))
        if voiceover_file.exists() and voiceover_file.stat().st_size > 1000:
            add_voiceover(stitched_video, voiceover_file, final_video)
            output = final_video
    except Exception as exc:
        print(f"Voiceover step skipped: {exc}")

    summary = {
        "final_video": str(output),
        "stitched_video": str(stitched_video),
        "segment_videos": [str(path) for path in segment_paths],
        "voiceover": str(voiceover_file) if voiceover_file.exists() else "",
        "results": results,
    }
    (run_dir / "generation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
