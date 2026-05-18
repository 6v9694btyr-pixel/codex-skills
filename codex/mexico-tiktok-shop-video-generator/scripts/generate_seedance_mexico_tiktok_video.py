from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_TASKS_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
DEFAULT_MODEL = "doubao-seedance-2-0-260128"


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


def submit_task(endpoint: str, api_key: str, model: str, spec: dict) -> str:
    duration = int(spec.get("duration", spec.get("duration_seconds", 15)))
    if duration > 15:
        raise ValueError("Seedance 2.0 supports a maximum of 15 seconds per single task. Confirm compression or segmentation first.")
    body = {
        "model": model,
        "content": [{"type": "text", "text": spec["prompt"]}],
        "resolution": spec.get("resolution", "720p"),
        "ratio": spec.get("ratio", "9:16"),
        "duration": duration,
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
        status_file.write_text(json.dumps({"task_id": task_id, "latest_response": status}, ensure_ascii=False, indent=2), encoding="utf-8")
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
            "-shortest",
            str(output),
        ],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one confirmed Mexico TikTok Shop video with Seedance 2.0.")
    parser.add_argument("--spec", required=True, help="Path to confirmed generation spec JSON.")
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
    model = env.get("SEEDANCE_VIDEO_MODEL") or spec.get("model") or DEFAULT_MODEL

    out_root = Path(args.out).resolve()
    slug = spec.get("output_slug", "mexico_tiktok_shop_video")
    run_dir = out_root / slug
    task_file = run_dir / "seedance_task.json"
    silent_video = run_dir / f"{slug}_silent.mp4"
    voiceover_file = run_dir / f"{slug}_voiceover.mp3"
    final_video = run_dir / f"{slug}_with_voice.mp4"
    run_dir.mkdir(parents=True, exist_ok=True)

    task_id = ""
    if task_file.exists():
        try:
            task_id = json.loads(task_file.read_text(encoding="utf-8")).get("task_id", "")
        except json.JSONDecodeError:
            task_id = ""

    if not silent_video.exists() or silent_video.stat().st_size <= 1000:
        if not task_id:
            print(f"Submitting one Seedance task with model={model}, duration={spec.get('duration', spec.get('duration_seconds', 15))}s")
            task_id = submit_task(endpoint, api_key, model, spec)
            task_file.write_text(json.dumps({"task_id": task_id}, ensure_ascii=False, indent=2), encoding="utf-8")
        result = wait_and_download(endpoint, api_key, task_id, silent_video, task_file)
    else:
        print(f"Using existing video: {silent_video}")
        result = {"status": "existing", "output": str(silent_video)}

    awaitable = make_voiceover(spec, voiceover_file)
    asyncio.run(awaitable)

    if voiceover_file.exists() and voiceover_file.stat().st_size > 1000:
        add_voiceover(silent_video, voiceover_file, final_video)
        output = final_video
    else:
        output = silent_video

    summary = {
        "final_video": str(output),
        "silent_video": str(silent_video),
        "voiceover": str(voiceover_file) if voiceover_file.exists() else "",
        "result": result,
    }
    (run_dir / "generation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
