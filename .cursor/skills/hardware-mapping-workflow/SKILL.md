---
name: hardware-mapping-workflow
description: >-
 Maps Access Virus TI mk2 SysEx by hardware capture with sendmidi/receivemidi.
 Use when confirming parameters, live-edit bytes, dump offsets,
 work, panel-to-host capture, or MIDI SysEx testing.
disable-model-invocation: true
---

# Hardware mapping workflow

Maps **Virus TI mk2 desktop** SysEx against real hardware. Use the MIDI port
from `sendmidi list` / `receivemidi list`. See also
[OsTIrus](../../docs/misc/ostirus.md).

Install and first message: [README — Setup](../../README.md#setup).

## Prerequisites

1. Virus TI powered on, USB connected, target port visible in `sendmidi list`.
2. `brew install sendmidi receivemidi` (see [README — Setup](../../README.md#setup)).
3. Agent commands need `required_permissions: ["all"]` (MIDI + `/tmp` capture).

```bash
MIDI_DEV='<MIDI port>'
sendmidi list && receivemidi list
```

## sendmidi SysEx (critical)

- Use **`hex syx`** — payload only; **omit `F0`/`F7`** (tool adds them).
- Without **`hex`**, decimals corrupt the body (`20` → `0x14`).

```bash
sendmidi dev "$MIDI_DEV" hex syx 00 20 33 01 00 72 00 4a 00
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

| Section | Live edit | Values (confirmed) |
| ----------- | --------- | --------------------------------------------------------------------------------------------------------------------- |
| Oscillators | `71`/`7F` | `00` Osc 1 … `02` Osc 3 — [oscillators.md](../../docs/live-edit/single/oscillators.md#oscillators-select) |
| Filters | `71`/`7A` | `00` F1 … `02` F1+F2 — [filters.md](../../docs/live-edit/single/filters.md#filters-select); **disabled** when Vocoder active |
| Effects g1 | `6E`/`75` | `00` Delay … `04` High EQ |
| Effects g2 | `6E`/`76` | `00` Distortion … `04` Others — [effects.md](../../docs/live-edit/single/effects.md#effects-select) |

```bash
sendmidi dev "$MIDI_DEV" hex syx 00 20 33 01 00 71 00 7F 01 # Osc 2
sendmidi dev "$MIDI_DEV" hex syx 00 20 33 01 00 71 00 7A 02 # Filter 1 + 2
sendmidi dev "$MIDI_DEV" hex syx 00 20 33 01 00 6E 00 76 02 # Chorus
```

## Before mapping

Set global **MIDI Controller Page A/B** to **SysEx** when capturing or testing
live-edit bytes — [Paging](../../docs/misc/virus.md#midi-controller-page-a).

## Interactive capture (panel → host)

**Agent** runs persistent capture; **user** turns controls and reports **final
LCD values only**.

```bash
LOG=/tmp/virus-live-capture.txt
: > "$LOG"
receivemidi dev "$MIDI_DEV" syx 2>&1 | tee -a "$LOG"
```

Background shell, `required_permissions: ["all"]`. After each edit: `tail -n 20
"$LOG"` — use **last** line of a burst; ignore empty `F0 F7`-only unless alone.

## Dump correlation batches (send → re-dump → diff)

Automated or scripted runs that send live edits and diff **Single Dump**
(edit buffer: `30 00 40`, part **`0x40`**) or **Multi Dump**.

1. Start from a **clean baseline** (e.g. RAM-A slot 127 **`-INIT-`**). A dirty
   edit buffer makes **NONE** look like failure when the sent value already
   equals the dump byte.
2. Every `send_param` must include **`00 20 33 01 00`** before `<cmd>`.
3. For each parameter: send → request dump → diff payload (ignore checksum /
   header drift bytes documented in capture scripts).
4. **NONE** = no payload change. Before counting a failure, retry once with a
   contrasting value (`0x00` vs `0x7F`) if the first send may have matched
   baseline.

### Stop at 10 failures (user rule)

**If ≥ 10 parameters in one batch return NONE (no dump offset), stop the batch
immediately.** Do not finish the script, do not bulk-update markdown.

Report to the user a table of every failure so far:

| Parameter | Live edit (`cmd` / `param`) | Sent value | Notes |
| --------- | --------------------------- | ---------- | ----- |

Include brief notes where useful (e.g. prerequisite not set, shares wire byte
with another menu, **MULTI** diff instead of single byte).

**Wait for corrective data** from the user (correct `cmd`/`param`, required
panel state, or confirmation that a control is not stored in the dump) before
continuing the batch or documenting offsets.

Scratch capture files and helper scripts belong in `artifacts/` during mapping
work (not committed; see `.gitignore`).

## Single-parameter verify (send → dump)

1. Load baseline (e.g. **INIT MULTI** #32); note packed flags **`0x45`** per
 part at `0xF9` / `0x108` in 267-byte dump.
2. Send **one** `hex syx` live edit; user confirms panel.
3. Capture Multi Dump:
 - Panel: `receivemidi dev "$MIDI_DEV" dump`
 - Request buffer: `sendmidi … 31 00 7f 7c`
 - Bank slot: bank `01`, slot byte, no checksum — see
 [multi.md](../../docs/dumps/multi.md)
4. Diff payload — **one** offset should change (+ checksum). Prefer Virus
 panel dumps over host export when diffing.

```python
def parse(s):
 return [int(x, 16) for x in s.split()]
a, b = parse(open("/tmp/baseline.txt").read()), parse(open("/tmp/after.txt").read())
for i, (x, y) in enumerate(zip(a, b)):
 if x != y:
 print(f"0x{i:02X}: {x:02X} -> {y:02X}")
```

## Smoke tests

| # | Message (summary) | Panel check |
| --- | -------------------- | ------------- |
| 1 | P1 Hold `4A` `00` | Hold Disabled |
| 2 | P1 Hold `4A` `01` | Hold Enabled |
| 3 | P16 Enable `48` `00` | Part 16 Off |
| 4 | P1 Vol `27` `48` | Part 1 Vol +8 |

## Stop and ask the user when

- **≥ 10 NONE** in one dump-correlation batch — list failures; wait for
  corrective data (see [Dump correlation batches](#dump-correlation-batches-send--re-dump--diff)).
- Wrong `sendmidi` syntax (not `hex syx`).
- Dump diff touches **multiple** bytes for one edit.
- Packed flags not INIT **`0x45`**.
- No `0x11` / 267-byte reply to `REQUEST_MULTI`.
- MIDI port missing.

## Doc targets after confirm

| Work | Update |
| --------------- | ------------------------------------------------------------ |
| Live edit bytes | [Documentation](../../README.md#documentation) |
| Dump offsets | [Documentation](../../README.md#documentation) |
| Enum tables | [docs/reference/parameter-options.md](../../docs/reference/parameter-options.md) |

Follow [documentation-standards](../documentation-standards/SKILL.md) when
writing markdown.
