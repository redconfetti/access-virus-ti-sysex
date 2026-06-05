---
name: hardware-mapping-workflow
description: >-
  Maps Access Virus TI mk2 SysEx by hardware capture with sendmidi/receivemidi.
  Use when confirming parameters, live-edit bytes, dump offsets, WAF80 queue
  work, panel-to-host capture, or Virus TI USB MIDI testing.
disable-model-invocation: true
---

# Hardware mapping workflow

Maps **Virus TI mk2 desktop** SysEx against real hardware. Scope: **`Virus TI
USB Plugin I/O`** via the TI plugin unless the user says otherwise. **OsTIrus:**
same bytes, different port — [docs/ostirus.md](../../docs/ostirus.md).

Install and first message: [docs/setup.md](../../docs/setup.md).

## Prerequisites

1. Virus TI powered on, USB connected, **`Virus TI USB Plugin I/O`** in port
   lists.
2. `brew install sendmidi receivemidi` (see Setup doc).
3. Agent commands need `required_permissions: ["all"]` (MIDI + `/tmp` capture).

```bash
VIRUS_DEV='Virus TI USB Plugin I/O'
sendmidi list && receivemidi list
```

## sendmidi SysEx (critical)

- Use **`hex syx`** — payload only; **omit `F0`/`F7`** (tool adds them).
- Without **`hex`**, decimals corrupt the body (`20` → `0x14`).

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 72 00 4a 00
# → F0 00 20 33 01 00 72 00 4A 00 F7
```

Live edit template:

```text
F0 00 20 33 01 00 <cmd> <part> <param> <value> F7
```

`<part>` is **0-based** (`00` = Part 1). Booleans on `0x48`–`0x4E`: `00` off,
`01` on.

## SELECT buttons (section focus)

Front-panel **SELECT** switches which sub-page the shared knobs edit. **`stored =
index`**. Pause **≥ 1 s** between probe messages. For **EFFECTS**, documents
**`6E`/`75`** / **`6E`/`76`** focus only — not physical knob routing.

| Section      | Live edit   | Values (confirmed) |
| ------------ | ----------- | ------------------ |
| Oscillators  | `71`/`7F`   | `00` Osc 1 … `02` Osc 3 — [oscillators.md](../../docs/live-edit/oscillators.md#oscillators-select) |
| Filters      | `71`/`7A`   | `00` F1 … `02` F1+F2 — [filters.md](../../docs/live-edit/filters.md#filters-select); **disabled** when Vocoder active |
| Effects g1   | `6E`/`75`   | `00` Delay … `04` High EQ |
| Effects g2   | `6E`/`76`   | `00` Distortion … `04` Others — [effects.md](../../docs/live-edit/effects.md#effects-select) |

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 71 00 7F 01   # Osc 2
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 71 00 7A 02   # Filter 1 + 2
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 6E 00 76 02   # Chorus
```

## Before mapping

Set global **MIDI Controller Page A/B** to **SysEx** (not Controller Data) so
panel edits emit Access SysEx — [edit-config.md](../../docs/live-edit/edit-config.md).

## Confirmation queue (WAF80 → TI)

1. Use [waf80.md](../../docs/waf80.md) as **hypothesis**.
2. Confirm on **TI mk2 desktop**; record in TI docs.
3. Work **one LCD menu** at a time — align with [single.md](../../docs/dumps/single.md) categories.
4. Finish a menu group before flushing markdown.

Report captures as **`Mode: …` / `Shape: …` / `Control: …` → value`** for
nested osc menus. Use **+/−** for single steps when possible.

## Interactive capture (panel → host)

**Agent** runs persistent capture; **user** turns controls and reports **final
LCD values only**.

```bash
LOG=/tmp/virus-live-capture.txt
: > "$LOG"
receivemidi dev "$VIRUS_DEV" syx 2>&1 | tee -a "$LOG"
```

Background shell, `required_permissions: ["all"]`. After each edit: `tail -n 20
"$LOG"` — use **last** line of a burst; ignore empty `F0 F7`-only unless alone.

### User / agent rules

1. Agent names **category** + **parameter** before each capture.
2. User edits on Virus (Edit Single, Part 1 unless noted).
3. **Knob** = many messages → **last** = landing value.
4. **Ranged** params: capture **several LCD landings** (0 %, 50 %, 100 %, …).
5. Session notes in chat; **flush to markdown when a menu group is done**.
6. CC vs SysEx: some controls differ by Page A mode — check
   [control-change.md](../../docs/control-change.md).
7. **Duplicate LCD / adjacent wire bytes** is normal — document every wire
   `00`–`7F` detent; do not assume one LCD ↔ one byte.
8. Ignore spurious **Noise Volume** (`70`/`25`) when using VALUE +/− near that
   knob.

## Single-parameter verify (send → dump)

1. Load baseline (e.g. **INIT MULTI** #32); note packed flags **`0x45`** per
   part at `0xF9` / `0x108` in 267-byte dump.
2. Send **one** `hex syx` live edit; user confirms panel.
3. Capture `DUMP_MULTI`:
   - Panel: `receivemidi dev "$VIRUS_DEV" dump`
   - Request buffer: `sendmidi … 31 00 7f 7c`
   - Bank slot: bank `01`, slot byte, no checksum — see
     [arrangements.md](../../docs/dumps/arrangements.md)
4. Diff payload — **one** offset should change (+ checksum). Plugin export
   quirks: [aura-notes.md](../../docs/aura-notes.md).

```python
def parse(s):
    return [int(x, 16) for x in s.split()]
a, b = parse(open("/tmp/baseline.txt").read()), parse(open("/tmp/after.txt").read())
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print(f"0x{i:02X}: {x:02X} -> {y:02X}")
```

## Smoke tests

| #   | Message (summary)    | Panel check   |
| --- | -------------------- | ------------- |
| 1   | P1 Hold `4A` `00`    | Hold Disabled |
| 2   | P1 Hold `4A` `01`    | Hold Enabled  |
| 3   | P16 Enable `48` `00` | Part 16 Off   |
| 4   | P1 Vol `27` `48`     | Part 1 Vol +8 |

## Stop and ask the user when

- Wrong `sendmidi` syntax (not `hex syx`).
- Dump diff touches **multiple** bytes for one edit.
- Packed flags not INIT **`0x45`**.
- No `0x11` / 267-byte reply to `REQUEST_MULTI`.
- Plugin port missing.

## Doc targets after confirm

| Work            | Update                                                       |
| --------------- | ------------------------------------------------------------ |
| Live edit bytes | [docs/live-edit/](../../docs/live-edit/README.md)            |
| Dump offsets    | [docs/dumps/](../../docs/dumps/README.md)                    |
| Enum tables     | [docs/parameter-options.md](../../docs/parameter-options.md) |

Follow [documentation-standards](../documentation-standards/SKILL.md) when
writing markdown.
