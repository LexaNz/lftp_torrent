#!/usr/bin/env python3

import tempfile
import subprocess
import sys
from pathlib import Path


TEST_EXPECTATIONS = [
    "Movie Name 2024.mkv",
    "The Last of Us S01E01.mkv",
    "Dune Part Two 2024.mkv",
    "Show Name S01E01.mkv",
    "Show Name S01E02.mkv",
]


def create_fake_structure(base: Path):

    # LEVEL 1: movie folder
    (base / "Movie.Name.2024.1080p").mkdir()
    (base / "Movie.Name.2024.1080p" /
     "Movie.Name.2024.1080p.mkv").touch()

    # LEVEL 2: TV show structure
    (base / "Show.Name.S01" /
     "Season.01").mkdir(parents=True)

    (base / "Show.Name.S01" /
     "Season.01" /
     "Show.Name.S01E01.mkv").touch()

    # LEVEL 3: nested release folder
    (base / "Show.Name.S01" /
     "Season.01" /
     "Release.Group.X265").mkdir(parents=True)

    (base / "Show.Name.S01" /
     "Season.01" /
     "Release.Group.X265" /
     "Show.Name.S01E02.mkv").touch()

    # standalone files
    (base / "Dune.Part.Two.2024.REMUX.mkv").touch()
    (base / "The.Last.of.Us.S01E01.2160p.WEB-DL.mkv").touch()


def run_renamer(base: Path):

    # IMPORTANT: no capture_output (prevents hanging)
    result = subprocess.run(
        ["python3", "renamer.py", str(base)]
    )

    if result.returncode != 0:
        print("Renamer failed")
        sys.exit(1)


def validate(base: Path):

    print("\nVALIDATION:")

    failed = False

    for expected in TEST_EXPECTATIONS:

        matches = list(base.rglob(expected))

        if not matches:
            print(f"FAIL: missing -> {expected}")
            failed = True
        else:
            print(f"OK: {expected}")

    if failed:
        sys.exit(1)

    print("\nALL TESTS PASSED")


def main():

    with tempfile.TemporaryDirectory() as tmp:

        base = Path(tmp)

        create_fake_structure(base)

        run_renamer(base)

        validate(base)


if __name__ == "__main__":
    main()
