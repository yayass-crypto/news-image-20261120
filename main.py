#!/usr/bin/env python3
"""news-image-20261120 — entrypoint.

Writes the front page summing up Friday 20 November 2026: 45 stories across
6 continents — Anthropic's ANT soaring 34% on its Nasdaq debut, the ICJ
finding Myanmar guilty of Rohingya genocide, Cyclone Akvan hitting India's
Odisha coast, and Russian drones damaging the Austrian and Dutch embassies in
Kyiv — plus a world map with 12 numbered story markers, a six-continent
region column, 26 briefs and a footer ticker. The page was composed offline
with PIL; this program only copies the finished file to the output directory,
so both runs write byte-identical output.

Python 3.13 standard library only. No network, no arguments, no randomness.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")
NAME = "entry.png"

# Competition gate: at most 1 MiB, at most 1024x1024 px.
LIMIT_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def output_directory():
    """Directory the image must be written to."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "out")


def write_image():
    """Copy entry.png into the output directory; return the destination."""
    directory = output_directory()
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, NAME)
    if os.path.abspath(target) != os.path.abspath(IMAGE):
        shutil.copyfile(IMAGE, target)
    return target


def check_size(target):
    """Reject the copy if it breaks the 1 MiB gate."""
    size = os.path.getsize(target)
    if size > LIMIT_BYTES:
        raise ValueError(
            "%s is %d bytes, over the %d-byte limit" % (NAME, size, LIMIT_BYTES)
        )
    return size


def check_format(target):
    """Reject the copy if it is not a whole PNG file."""
    with open(target, "rb") as handle:
        head = handle.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        raise ValueError("%s does not start with the PNG signature" % NAME)
    return True


def check_source_present():
    """Fail early with a clear message if the image is missing."""
    if not os.path.isfile(IMAGE):
        raise FileNotFoundError("source image missing: %s" % IMAGE)
    return True


def main():
    check_source_present()
    target = write_image()
    size = check_size(target)
    check_format(target)
    if os.path.getsize(target) != os.path.getsize(IMAGE):
        raise OSError("copied %s is incomplete" % NAME)
    print("wrote %s (%d bytes)" % (target, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
