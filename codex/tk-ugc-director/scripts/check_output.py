#!/usr/bin/env python3
"""Check whether a TK UGC Director output contains required sections."""

from __future__ import annotations

import argparse
import locale
import sys
from pathlib import Path


REQUIRED = {
    "product positioning": ["product positioning", "产品定位", "产品一句话定位"],
    "target audience": ["target audience", "目标人群", "目标受众"],
    "pain point analysis": ["pain point", "痛点分析", "功能痛点", "情绪痛点", "身份痛点"],
    "hook": ["hook", "钩子"],
    "ugc script": ["ugc script", "ugc短视频脚本", "口播脚本", "脚本"],
    "storyboard": ["storyboard", "分镜"],
    "voiceover": ["voiceover", "口播"],
    "image prompts": ["image prompts", "image prompt", "图片提示词", "图生成提示词"],
    "video prompts": ["video prompts", "video prompt", "视频提示词", "视频生成提示词"],
    "compliance check": ["compliance check", "合规自查", "合规检查"],
}


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    if sys.stdin.isatty():
        raise SystemExit("Provide an output file path or pipe text through stdin.")
    data = sys.stdin.buffer.read()
    encodings = ["utf-8-sig", locale.getpreferredencoding(False), "gb18030", "utf-16"]
    for encoding in dict.fromkeys(encodings):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a UGC output for required structural keywords."
    )
    parser.add_argument("path", nargs="?", help="Path to a text/markdown output file.")
    args = parser.parse_args()

    text = read_input(args.path).lower()
    missing = [
        key
        for key, aliases in REQUIRED.items()
        if not any(alias.lower() in text for alias in aliases)
    ]

    if missing:
        print("Missing required keywords:")
        for key in missing:
            print(f"- {key}")
        return 1

    print("OK: all required keywords found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
