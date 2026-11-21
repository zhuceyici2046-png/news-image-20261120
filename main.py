#!/usr/bin/env python3
"""Entry program for news-image-20261120.

draw_entry.py renders entry.png, a newspaper front page summing up
Friday 20 November 2026 world news. This program puts that image
where the grader expects it: /output/entry.png, or
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set.
"""
import os
import shutil
from pathlib import Path

source = Path(__file__).resolve().parent / "entry.png"
target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
target_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target_dir / "entry.png")
print(f"wrote {target_dir / 'entry.png'}")
