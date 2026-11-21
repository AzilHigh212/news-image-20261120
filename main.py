#!/usr/bin/env python3
"""make.fun entry: "Sum up 20 November's world news in one image".

The front page is rendered ahead of time by render_frontpage.py into
entry.png (1024x1024). This entry point only places that image where the
grader expects it: $MAKEFUN_OUTPUT_DIR/entry.png.

Pure standard library, so it runs in the grader's sandbox with no extra
packages. The copy is byte-for-byte, so repeated runs produce identical
output.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def output_path():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return (Path(base) if base else HERE / "output") / "entry.png"


def main():
    src = HERE / "entry.png"
    dst = output_path()
    if not src.is_file():
        raise SystemExit("entry.png is missing next to main.py")
    data = src.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("entry.png is not a valid PNG")
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    print(f"wrote {dst} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
