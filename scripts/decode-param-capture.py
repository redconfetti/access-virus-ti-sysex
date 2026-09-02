#!/usr/bin/env python3
"""Decode an `amidi -d` capture of a Virus TI front-panel sweep into a per-parameter report.

Turning a knob on the TI's CONFIG (or any) page makes the synth emit an ordinary
live-edit SysEx, so a passive capture is enough to confirm a parameter's `cmd`,
index and observed value set -- no bytes need to be sent to the instrument.

Every message carries its own index, so a single capture of many knobs
self-separates; there is no need to isolate one control per run.

Wire format:  F0 00 20 33 01 <dev> <cmd> <part> <index> <value> F7

With --xml, each index is named from Access's own parameter database
(`remotedevice.xml`; see docs/reference/extracting-parameter-data.md) and the observed
value set is checked against the declared min/max -- which is the cross-check
that makes a passive capture worth something: two independent sources agreeing
on the same index.

Usage:
  scripts/decode-param-capture.py CAPTURE [--xml remotedevice.xml] [--cmd 73]
  scripts/decode-param-capture.py CAPTURE --from-byte N   # only bytes past N
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BANKS = {0x6E: "0x6E", 0x6F: "0x6F", 0x70: "0x70", 0x71: "0x71",
         0x72: "0x72", 0x73: "0x73", 0x74: "0x74"}


def load_names(xml: Path) -> dict[tuple[int, int], dict]:
    """(bank, index) -> parameter record, via the sibling XML reader."""
    reader = Path(__file__).resolve().parent / "parse-remotedevice.py"
    out = subprocess.run(
        [sys.executable, str(reader), "--xml", str(xml), "--format", "csv"],
        capture_output=True, text=True, check=True).stdout
    import csv
    names = {}
    for row in csv.DictReader(out.splitlines()):
        if row["bank"] and row["index"]:
            names[(int(row["bank"]), int(row["index"]))] = row
    return names


def parse(capture: str) -> list[tuple[int, int, int, int]]:
    """-> list of (cmd, part, index, value) from every well-formed live-edit message."""
    tokens = re.findall(r"[0-9A-Fa-f]{2}", capture)
    data = bytes(int(t, 16) for t in tokens)
    found = []
    for m in re.finditer(rb"\xf0\x00\x20\x33\x01(.)(.)(.)(.)(.)\xf7", data, re.DOTALL):
        _dev, cmd, part, index, value = (b[0] for b in m.groups())
        found.append((cmd, part, index, value))
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("capture", type=Path)
    ap.add_argument("--xml", type=Path, help="remotedevice.xml, to name each index")
    ap.add_argument("--cmd", type=lambda s: int(s, 16), default=None,
                    help="only report this cmd/bank byte, hex (e.g. 73)")
    ap.add_argument("--from-byte", type=int, default=0,
                    help="ignore the first N bytes of the capture file")
    args = ap.parse_args()

    text = args.capture.read_text(errors="replace")[args.from_byte:]
    msgs = parse(text)
    if not msgs:
        print("no live-edit SysEx found in that capture")
        return

    names = load_names(args.xml) if args.xml else {}

    by_key: dict[tuple[int, int], list[int]] = {}
    order: list[tuple[int, int]] = []
    for cmd, _part, index, value in msgs:
        if args.cmd is not None and cmd != args.cmd:
            continue
        key = (cmd, index)
        if key not in by_key:
            by_key[key] = []
            order.append(key)
        by_key[key].append(value)

    print(f"{len(msgs)} live-edit messages, {len(by_key)} distinct (cmd, index) pairs")
    print("(listed in order of first appearance)\n")
    hdr = f"{'cmd':>4} {'idx':>5} {'msgs':>5} {'distinct':>8} {'observed values':<34}"
    print(hdr + ("  check  name" if names else ""))
    for cmd, index in order:
        vals = by_key[(cmd, index)]
        uniq = sorted(set(vals))
        shown = " ".join(f"{v:02x}" for v in uniq)
        if len(shown) > 33:
            shown = shown[:30] + "..."
        line = f"  {cmd:02x} {index:5} {len(vals):5} {len(uniq):8} {shown:<34}"
        rec = names.get((cmd, index))
        if names:
            if not rec:
                line += "  ????   (not in XML)"
            else:
                lo, hi = int(rec["min"]), int(rec["max"])
                inside = all(lo <= v <= hi for v in uniq)
                # a 2-valued declaration observed with a 3rd value is the interesting case
                mark = "OK  " if inside else "OUT!"
                line += f"  {mark}   {rec['qualified']}  [{lo}..{hi}]"
        print(line)

    if names:
        outs = [(c, i) for (c, i) in order
                if (rec := names.get((c, i))) and
                any(not (int(rec["min"]) <= v <= int(rec["max"]))
                    for v in set(by_key[(c, i)]))]
        print()
        if outs:
            print("VALUES OUTSIDE THE DECLARED RANGE -- the XML understates these:")
            for c, i in outs:
                rec = names[(c, i)]
                bad = sorted(v for v in set(by_key[(c, i)])
                             if not int(rec["min"]) <= v <= int(rec["max"]))
                print(f"  cmd {c:02x} idx {i} ({rec['qualified']}): "
                      f"declared {rec['min']}..{rec['max']}, saw "
                      + " ".join(f"0x{v:02x}" for v in bad))
        else:
            print("every observed value falls inside its declared range")


if __name__ == "__main__":
    main()
