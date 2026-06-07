#!/usr/bin/env python3
"""Align markdown pipe tables for markdownlint MD060 (style: aligned)."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_table_row(line: str) -> list[str] | None:
    stripped = line.rstrip("\n")
    if not stripped.lstrip().startswith("|"):
        return None
    body = stripped.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [cell.strip() for cell in body.split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def format_row(cells: list[str], widths: list[int], separator: bool = False) -> str:
    parts: list[str] = []
    for cell, width in zip(cells, widths):
        if separator:
            dash = max(width, 3)
            parts.append("-" * dash)
        else:
            parts.append(cell.ljust(width))
    return "| " + " | ".join(parts) + " |"


def align_table(lines: list[str]) -> list[str]:
    rows: list[list[str]] = []
    for line in lines:
        parsed = parse_table_row(line)
        if parsed is None:
            break
        rows.append(parsed)

    if len(rows) < 2:
        return lines

    col_count = len(rows[0])
    if col_count == 0 or any(len(row) != col_count for row in rows):
        return lines

    widths = [max(len(row[i]) for row in rows) for i in range(col_count)]
    out: list[str] = []
    for idx, row in enumerate(rows):
        out.append(format_row(row, widths, separator=is_separator_row(row)))
    return out


def process_text(text: str) -> str:
    lines = text.splitlines(keepends=True)
    result: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if parse_table_row(line.rstrip("\n")) is not None:
            block: list[str] = []
            while i < len(lines) and parse_table_row(lines[i].rstrip("\n")) is not None:
                block.append(lines[i].rstrip("\n"))
                i += 1
            aligned = align_table(block)
            for al in aligned:
                result.append(al + "\n")
            continue
        result.append(line)
        i += 1
    return "".join(result)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    paths = sorted(root.rglob("*.md"))
    changed = 0
    for path in paths:
        original = path.read_text(encoding="utf-8")
        updated = process_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Aligned tables in {changed} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
