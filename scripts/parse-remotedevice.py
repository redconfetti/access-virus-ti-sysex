#!/usr/bin/env python3
"""Parse Access's own Virus Control `remotedevice.xml` into a parameter address table.

`remotedevice.xml` ships inside the Virus TI Software Suite installer
(`Virus Control.bundle/Contents/Resources/`). It is Access's own model of the
synth's remote-control surface: one <Parameter> per addressable parameter, each
carrying the SysEx bank it lives in (via `defaultmessage`), its index within
that bank (`controllerindex`), its range, and a named value list.

This script reads it and emits a flat `(bank, index) -> name/range/valuelist`
table. It is a *reading* tool — the XML is Access's copyrighted data and is not
committed; point --xml at a locally extracted copy.

Extraction: see docs/reference/extracting-parameter-data.md for macOS, Windows
and Linux recipes. The XML is Access's copyrighted data -- extract it from your own
copy of the installer; it is deliberately not committed here.

Caveat that matters: this is the *editor's* model of the synth, not the
firmware's. Where the two disagree, the firmware wins.

Usage:
    parse_vc_remotedevice.py --xml <remotedevice.xml> [--format table|csv|json]
    parse_vc_remotedevice.py --xml <...> --dumps      # dump-layout templates
    parse_vc_remotedevice.py --xml <...> --valuelist "Filter Mode"
"""

import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET

# `defaultmessage` names the MIDIMessage template a parameter is sent with.
# The seven SysEx templates carry an explicit bank byte; `cc` and `pp` are the
# MIDI shortcuts the Virus accepts for banks $70 and $71 respectively (a plain
# Control Change and a Poly Pressure message, neither of which carries a bank
# byte at all). Verified against the templates' own byte lists.
SHORTCUT_BANKS = {"cc": 0x70, "pp": 0x71}


def bank_of_template(msg):
    """Return the SysEx bank byte a MIDIMessage template addresses, or None."""
    bytes_ = list(msg)
    # A bank-addressing template looks like:
    #   F0 00 20 33 01 <deviceid> <bank> <part> <controllerid> <value> F7
    # i.e. the literal byte immediately after <deviceid>.
    for i, b in enumerate(bytes_):
        if b.get("content") == "deviceid":
            nxt = bytes_[i + 1] if i + 1 < len(bytes_) else None
            if nxt is not None and nxt.get("content") == "byte":
                # A single-parameter template ends <controllerid> <value> F7.
                contents = [x.get("content") for x in bytes_]
                if "controllerid" in contents and "value" in contents:
                    return int(nxt.get("tag"))
            return None
    return None


def load(path):
    root = ET.parse(path).getroot()

    banks = {}
    for msg in root.find("MIDIMessages"):
        mid = msg.get("id")
        bank = bank_of_template(msg)
        if bank is not None:
            banks[mid] = bank
    banks.update(SHORTCUT_BANKS)

    valuelists = {}
    for vl in root.find("Valuelists"):
        entries = {}
        for e in vl:
            # The display string is the element's *text*; the `value` attribute
            # (present on only ~8% of entries) carries a numeric override used
            # by the tabular value lists, not the name.
            entries[int(e.get("index"))] = (e.text or "").strip() or e.get("value")
        valuelists[vl.get("name")] = {"type": vl.get("type"), "entries": entries}

    params = []
    for pset in root.find("ParameterSets"):
        for p in pset.findall("Parameter"):
            msg = p.get("defaultmessage")
            idx = p.get("controllerindex")
            params.append(
                {
                    "set": pset.get("name"),
                    "name": p.get("name"),
                    "qualified": "%s/%s" % (pset.get("name"), p.get("name")),
                    "shortname": p.get("shortname"),
                    "displayname": p.get("displayname"),
                    "message": msg,
                    "bank": banks.get(msg),
                    "index": int(idx) if idx not in (None, "") else None,
                    "min": p.get("minValue"),
                    "max": p.get("maxValue"),
                    "default": p.get("defaultValue"),
                    "valuelist": p.get("valuelist"),
                    "part": p.get("part"),
                    "automatable": p.get("automatable"),
                    "condition": p.get("condition"),
                }
            )

    return root, banks, valuelists, params


def dump_templates(root):
    """Print the multi-byte dump templates as index -> parameter maps."""
    for msg in root.find("MIDIMessages"):
        bytes_ = list(msg)
        if len(bytes_) <= 12:
            continue  # single-parameter template, not a dump layout
        print("=== %s (%d bytes) ===" % (msg.get("id"), len(bytes_)))
        for b in bytes_:
            content = b.get("content")
            if content == "byte":
                content = "0x%02X" % int(b.get("tag"))
            extra = ""
            if b.get("mask"):
                extra = " mask=%s shift=%s" % (b.get("mask"), b.get("shift"))
            print("  [%3s] %s%s" % (b.get("index"), content, extra))
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xml", required=True)
    ap.add_argument("--format", choices=("table", "csv", "json"), default="table")
    ap.add_argument("--bank", help="filter to one bank, e.g. 0x6E")
    ap.add_argument("--dumps", action="store_true", help="print dump-layout templates")
    ap.add_argument("--valuelist", help="print one value list by name")
    ap.add_argument("--valuelists", action="store_true", help="list all value lists")
    args = ap.parse_args()

    root, banks, valuelists, params = load(args.xml)

    if args.dumps:
        dump_templates(root)
        return
    if args.valuelists:
        for name, vl in sorted(valuelists.items()):
            print("%-40s type=%-10s entries=%d" % (name, vl["type"], len(vl["entries"])))
        return
    if args.valuelist:
        vl = valuelists.get(args.valuelist)
        if vl is None:
            sys.exit("no such value list: %s" % args.valuelist)
        for i in sorted(vl["entries"]):
            print("%4d  %s" % (i, vl["entries"][i]))
        return

    rows = params
    if args.bank:
        want = int(args.bank, 0)
        rows = [r for r in rows if r["bank"] == want]
    rows.sort(key=lambda r: (r["bank"] if r["bank"] is not None else 999, r["index"]))

    if args.format == "json":
        json.dump(rows, sys.stdout, indent=2)
    elif args.format == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    else:
        print("%-5s %-5s %-46s %-5s %-5s %s" % ("bank", "idx", "parameter", "min", "max", "valuelist"))
        for r in rows:
            print(
                "%-5s %-5s %-46s %-5s %-5s %s"
                % (
                    "0x%02X" % r["bank"] if r["bank"] is not None else "-",
                    r["index"],
                    r["qualified"],
                    r["min"],
                    r["max"],
                    r["valuelist"] or "",
                )
            )
        print("\n%d parameters" % len(rows))


if __name__ == "__main__":
    main()
