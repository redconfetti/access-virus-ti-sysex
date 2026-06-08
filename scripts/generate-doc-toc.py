#!/usr/bin/env python3
"""Insert a ## Contents TOC into markdown guides.

Requires Node and markdownlint (once): npm install --no-save markdownlint@0.40.0

Usage:
  python3 scripts/generate-doc-toc.py [path ...]

With no paths, updates default doc sets (live-edit, dumps, parameter-options).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG_SCRIPT = ROOT / "scripts" / "extract-heading-slugs.mjs"
CONTENTS_RE = re.compile(r"\n## Contents\n.*?\n---\n\n?", re.DOTALL)

DEFAULT_TARGETS: list[tuple[Path, int]] = [
    (ROOT / "docs" / "reference" / "parameter-options.md", 3),
    *( (path, 5) for path in sorted((ROOT / "docs" / "dumps").glob("*.md")) ),
    *( (path, 4) for path in sorted((ROOT / "docs" / "live-edit").rglob("*.md")) ),
]

MAX_LEVEL_BY_PATH: dict[str, int] = {
    str(ROOT / "docs" / "reference" / "parameter-options.md"): 3,
}


def max_level_for(path: Path) -> int:
    key = str(path.resolve())
    if key in MAX_LEVEL_BY_PATH:
        return MAX_LEVEL_BY_PATH[key]
    if "docs/dumps" in path.as_posix():
        return 5
    if "docs/live-edit" in path.as_posix():
        return 4
    return 4


def strip_existing_toc(content: str) -> str:
    return CONTENTS_RE.sub("\n", content, count=1)


def list_marker(content: str) -> str:
    """Match MD004 to the dominant list style in the document body."""
    dash = len(re.findall(r"^-\s", content, re.MULTILINE))
    star = len(re.findall(r"^\*\s", content, re.MULTILINE))
    if dash > star:
        return "-"
    if star > dash:
        return "*"
    match = re.search(r"^## ", content, re.MULTILINE)
    intro = content[: match.start()] if match else content
    return "-" if re.search(r"^-\s", intro, re.MULTILINE) else "*"


def extract_headings(path: Path, content: str, max_level: int) -> list[tuple[int, str, str]]:
    stripped = strip_existing_toc(content)
    proc = subprocess.run(
        ["node", str(SLUG_SCRIPT), "-", str(max_level)],
        input=stripped,
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    rows = json.loads(proc.stdout)
    return [(row["level"], row["text"], row["slug"]) for row in rows]


def build_toc(headings: list[tuple[int, str, str]], marker: str) -> str:
    lines = ["## Contents", ""]
    for level, text, slug in headings:
        if text == "Contents":
            continue
        indent = "  " * (level - 2)
        lines.append(f"{indent}{marker} [{text}](#{slug})")
    lines.extend(["", "---"])
    return "\n".join(lines) + "\n\n"


def insert_toc(content: str, toc: str) -> str:
    content = strip_existing_toc(content)
    match = re.search(r"^## ", content, re.MULTILINE)
    if not match:
        return content.rstrip() + "\n\n" + toc
    pos = match.start()
    return content[:pos] + toc + content[pos:]


def process_file(path: Path, max_level: int | None = None) -> bool:
    level = max_level if max_level is not None else max_level_for(path)
    original = path.read_text()
    stripped = strip_existing_toc(original)
    headings = extract_headings(path, original, level)
    updated = insert_toc(original, build_toc(headings, list_marker(stripped)))
    if updated != original:
        path.write_text(updated)
        return True
    return False


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        paths = [Path(arg).resolve() for arg in argv[1:]]
        targets = [(path, max_level_for(path)) for path in paths]
    else:
        targets = DEFAULT_TARGETS

    changed: list[Path] = []
    for path, max_level in targets:
        if not path.is_file():
            print(f"skip missing: {path}", file=sys.stderr)
            continue
        if process_file(path, max_level):
            changed.append(path)

    for path in changed:
        print(path.relative_to(ROOT))
    print(f"Updated {len(changed)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
