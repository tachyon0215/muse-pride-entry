#!/usr/bin/env python3
"""Write the entry line to entry.txt. Deterministic, stdlib only.

Entry for make.fun 'One Line of Earned Pride': one line of 1 to 240
characters, a quiet earned moment of pride in a concrete scene.
"""
import os
from pathlib import Path

LINE = "The night janitor who studied between shifts for six years opened the exam envelope, read 'pass' twice, and quietly mopped the last corridor like it was his."
TEXT = LINE + "\n"
MAX_CHARS = 240


def validate(text: str) -> None:
    # The gate counts characters of the line itself, newline excluded.
    if not (1 <= len(text.rstrip("\n")) <= MAX_CHARS):
        raise ValueError("entry length out of range")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    body = text[:-1] if text.endswith("\n") else text
    if "\n" in body or "\r" in body:
        raise ValueError("entry must be exactly one line")


def main() -> None:
    validate(TEXT)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(TEXT.encode("utf-8"))
    if target.read_bytes() != TEXT.encode("utf-8"):
        raise IOError("read-back mismatch")


if __name__ == "__main__":
    main()
