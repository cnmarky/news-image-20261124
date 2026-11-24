#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261124.

Writes the one-image summary of the world news of Tuesday
24 November 2026 to /output/entry.png.

The image itself (entry.png, 1024x1024 PNG, ~135 KB) is built by
generate_image.py from researched facts about that day; this program
only copies it into place, using the standard library alone, so the
graded run needs no network, no fonts and no third-party packages,
and two runs always write the same bytes.

Local test:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    if not os.path.isfile(SOURCE):
        print("missing image next to main.py:", SOURCE, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # The grader collects outputs as another user: leave the file
    # world-readable (mode 0644) and the directory 0755.
    os.chmod(dest, 0o644)
    os.chmod(out_dir, 0o755)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
