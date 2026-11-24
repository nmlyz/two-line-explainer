#!/usr/bin/env python3
"""Write two lines explaining a traffic jam to a 10-year-old to /output/entry.txt.

Line 1 explains the everyday thing in one vivid sentence built on a single
analogy; line 2 says in one sentence what that analogy maps and what it
leaves out. Standard library only, no network. Deterministic: the text is a
constant, so every run writes byte-identical output.
"""

import os

ENTRY = (
    "A traffic jam is a parking lot that forgot it was a road.\n"
    "It maps rows of cars standing still, but leaves out that the cars all "
    "want to move and are stuck because too many of them are trying to use "
    "one road."
)

MAX_CHARS = 400


def check(text):
    if not text or text != text.strip() or len(text) > MAX_CHARS:
        raise ValueError("entry must be 1-400 non-blank characters")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines")
    for line in lines:
        if not line or line != line.strip():
            raise ValueError("each line must be non-blank")
        if line.count(".") != 1 or not line.endswith("."):
            raise ValueError("each line must be a single sentence")
    return text


def main():
    text = check(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the file is the two lines, nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, 0o644)
    # Read it back and verify the bytes on disk are exactly what was checked.
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        raise ValueError("entry.txt on disk differs from the checked text")
    if os.stat(path).st_mode & 0o777 != 0o644:
        raise ValueError("entry.txt must be readable by every user (0644)")
    print(f"wrote {len(text)} characters to {path}")


if __name__ == "__main__":
    main()
