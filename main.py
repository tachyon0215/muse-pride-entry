#!/usr/bin/env python3
"""Place this entry's single line into ``entry.txt``.

Competition: make.fun "One Line of Earned Pride". The brief asks for
one line, between 1 and 240 characters, holding a quiet moment of
pride that was earned rather than announced. Mine stays with a night
janitor who studied between shifts for six years: the envelope says
"pass", he reads it twice, and then he goes back to mopping — except
the last corridor is suddenly his in a way it never was before.

The program uses only the standard library, never touches the
network, and writes byte-identical output on every run.
"""

import os
from pathlib import Path

# The line itself, exactly as it will be judged. The file adds one
# trailing newline, which is formatting, not part of the line.
LINE = "The night janitor who studied between shifts for six years opened the exam envelope, read 'pass' twice, and quietly mopped the last corridor like it was his."
SHEET = LINE + "\n"

# Upper bound from the brief; the line must also be non-empty.
BOUND = 240


def vet(line: str) -> None:
    """Make sure the line still qualifies as one earned line.

    Three checks, three distinct ways to fail: nothing written at
    all, more written than the brief allows, or a line break hiding
    inside what is supposed to be a single line.
    """
    if not line.strip():
        raise ValueError("line must not be blank")
    if len(line) > BOUND:
        raise ValueError(f"line is {len(line)} chars, bound is {BOUND}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")


def entry_file() -> Path:
    """Find the file the grader expects inside the output folder."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(folder) / "entry.txt"


def deliver(target: Path, sheet: str) -> None:
    """Write the sheet, then read it back and hold it up to the light.

    A byte-for-byte comparison catches a truncated write; decoding
    the result and confirming the envelope's verdict survived proves
    the file on disk is still the same small story, not a fragment.
    """
    data = sheet.encode("utf-8")
    target.write_bytes(data)
    landed = target.read_bytes()
    if landed != data:
        raise IOError(
            f"read-back mismatch: wrote {len(data)} bytes, "
            f"read {len(landed)} bytes"
        )
    text = landed.decode("utf-8")
    if "read 'pass' twice" not in text or text.count("\n") != 1:
        raise IOError("written line lost its verdict or its shape")


def main() -> None:
    vet(LINE)
    target = entry_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    deliver(target, SHEET)


if __name__ == "__main__":
    main()
