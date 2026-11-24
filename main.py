#!/usr/bin/env python3
"""Write one short apology line to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The apology is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

ENTRY = "Sorry, I deleted the production database. I have rebuilt it as a spreadsheet called final_final_v2.xlsx, and I am quietly confident about the customers tab."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("entry is only white space")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Write the entry, failing cleanly when the path cannot be written.

    A directory given as the output path exits with a plain message
    instead of a traceback.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot write {path}: {exc.strerror or exc}") from exc


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        write_entry(path, ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
