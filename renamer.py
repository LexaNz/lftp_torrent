#!/usr/bin/env python3

import re
import sys
from pathlib import Path

# Enable dry-run mode (no filesystem changes)
DRY_RUN = False

# Supported video formats
VIDEO_EXTENSIONS = {
    ".mkv", ".mp4", ".avi", ".mov",
    ".m4v", ".ts"
}

# Ignored folders
SKIP_DIRS = {
    "@eaDir",
    "sample",
    "subs",
    "subtitles"
}

# Metadata junk to remove
JUNK = {
    "720p", "1080p", "2160p",
    "x264", "x265", "h264", "h265", "hevc",
    "bluray", "brrip", "bdrip",
    "web-dl", "webrip", "hdtv", "remux",
    "aac", "ac3", "dts", "truehd", "atmos",
    "hdr", "dv", "proper", "repack",
    "multi", "vostfr", "french",
    "nf", "amzn", "dsnp"
}


# Convert filename into clean media name
def clean_name(name):

    name = re.sub(r"[._]+", " ", name).strip()
    tokens = name.split()

    result = []

    for token in tokens:

        low = token.lower()

        # keep episode format
        if re.match(r"s\d{1,2}e\d{1,2}", low):
            result.append(token.upper())
            continue

        # keep year
        if re.match(r"^(19|20)\d{2}$", token):
            result.append(token)
            continue

        # stop at technical metadata
        if low in JUNK:
            break

        result.append(token)

    return " ".join(result).strip()


# Rename safely (file or folder)
def rename_path(path):

    try:

        if path.is_dir():
            ext = ""
            original_name = path.name
        else:
            ext = path.suffix
            original_name = path.stem

        cleaned = clean_name(original_name)

        if not cleaned:
            print(f'SKIPPED: empty -> "{path}"')
            return

        new_name = cleaned + ext

        if new_name == path.name:
            print(f'SKIPPED: unchanged -> "{path.name}"')
            return

        target = path.with_name(new_name)

        if target.exists():
            print(f'ERROR: collision -> "{target.name}"')
            return

        # DRY RUN vs REAL RUN
        if DRY_RUN:
            print(f'DRY_RUN: "{path.name}" -> "{target.name}"')
        else:
            path.rename(target)
            print(f'RENAMED: "{path.name}" -> "{target.name}"')

    except Exception as e:
        print(f'ERROR: "{path}" -> {e}')


# Process full directory tree (deepest first)
def process(base_dir):

    base = Path(base_dir)

    if not base.exists():
        print(f'ERROR: missing path -> "{base}"')
        sys.exit(1)

    paths = sorted(
        base.rglob("*"),
        key=lambda p: len(p.parts),
        reverse=True
    )

    for path in paths:

        if path.is_dir() and path.name.lower() in SKIP_DIRS:
            continue

        rename_path(path)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: rename_media.py <directory> [--dry-run]")
        sys.exit(1)

    # optional CLI flag override
    if "--dry-run" in sys.argv:
        DRY_RUN = True

    process(sys.argv[1])
