# Hardware testing (Virus TI mk2 desktop)

Guide for **agents** (and humans) verifying SysEx documentation against a
real **Access Virus TI mk2 desktop** using `sendmidi` / `receivemidi`.

Scope: **desktop module** via **`Virus TI USB Plugin I/O`**. Keyboard/Polar
and **External I/O** routing are out of scope unless the user says otherwise.

## Prerequisites

1. Virus TI mk2 powered on, USB connected, **Virus TI plugin / AURA** path
   active so **`Virus TI USB Plugin I/O`** appears in port lists.
2. Tools installed (see [README Setup](../README.md#setup)):

   ```bash
   brew install sendmidi receivemidi
   ```

3. Agent shell: MIDI needs **full host access** — run commands with
   `required_permissions: ["all"]`. Workspace sandbox allows **`/tmp`**
   for capture files.

## MIDI port

| Direction    | Command       | Port name                 |
| ------------ | ------------- | ------------------------- |
| Host → Virus | `sendmidi`    | `Virus TI USB Plugin I/O` |
| Virus → Host | `receivemidi` | `Virus TI USB Plugin I/O` |

Verify names have not changed:

```bash
sendmidi list
receivemidi list
```

Set a shell variable for repeat use:

```bash
VIRUS_DEV='Virus TI USB Plugin I/O'
```

## Critical: `sendmidi` SysEx syntax (v1.3+)

From `sendmidi` help:

- **`syx`** — payload bytes only; **do not** pass `F0` or `F7` (the tool
  adds start/end).
- **`hex`** — interpret following numbers as hexadecimal (required).
- Default mode is **decimal**; `0x20` is **not** valid hex syntax and is
  read as **0**, which produces all-zero bodies like
  `F0 00 00 … 00 F7`.

| Mistake              | On the wire (symptom)        |
| -------------------- | ---------------------------- |
| `syx 0xf0 … 0xf7`    | Zeros / unknown manufacturer |
| `syx 20 33` (no hex) | `14 21` instead of `20 33`   |
| `hex syx 00 20 33 …` | Correct Access message       |

Correct live edit (Part 1 Hold Pedal off):

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 72 00 4a 00
```

On the wire:

```text
F0 00 20 33 01 00 72 00 4A 00 F7
```

## Message types

| Purpose            | Cmd  | Length    | Doc                                                              |
| ------------------ | ---- | --------- | ---------------------------------------------------------------- |
| Live multi edit    | `72` | 11 bytes  | [multis-live-edit.md](multis-live-edit.md)                       |
| Request multi dump | `31` | 11 bytes  | [multis-dump.md](multis-dump.md#request_multi-byte-table)        |
| Multi dump reply   | `11` | 267 bytes | [multis-dump.md](multis-dump.md#dump_multi-byte-table-267-bytes) |

Live edit template:

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7
```

- `<part>`: **0-based** (`0x00` = Part 1, `0x0F` = Part 16).
- Boolean live params (`0x48`–`0x4E`): `0x00` = off, `0x01` = on.

Example — Part 1 Hold Pedal **disabled**:

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 72 00 4a 00
```

Re-enable:

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 72 00 4a 01
```

## Interactive single-parameter capture (panel → host)

Use this loop when the **user** turns a control on the Virus and the agent
listens with `receivemidi syx`.

### Agent setup

```bash
VIRUS_DEV='Virus TI USB Plugin I/O'
receivemidi dev "$VIRUS_DEV" syx 2>&1 | tee /tmp/virus-live-capture.txt
```

Run with `required_permissions: ["all"]`. Work **one parameter at a time**
from [single-dump.md — Single parameter map](single-dump.md#single-parameter-map).
Skip **Easy / Quick Edit** — those are VC panel shortcuts to parameters listed
under other categories.

### User / agent rules

1. Agent names the **category** and **parameter** before each capture.
2. User edits that control on the Virus (Edit Single context, Part 1 unless
   noted).
3. **Knob turns** often produce **many SysEx messages** — use the **last
   message** in the burst as the landing value. The user states the **final
   UI value** they landed on (not every intermediate step).
4. After capture, agent records **`cmd`**, **param**, **value** encoding
   from the last message and updates docs.
5. Toggle/switch controls may send a single message; knobs and sliders may
   send a stream.
6. Some Easy-page controls send **MIDI CC only** (no SysEx) — e.g. **Sub
   Oscillator Volume** = **CC 34**; see [control-change.md](control-change.md).
7. **Before a SysEx mapping session**, set globals **MIDI Controller Page A**
   and **Page B** to **SysEx** (not Controller Data) so panel edits emit
   Access SysEx instead of CC — see
   [global-live-edit.md — Page A / B](global-live-edit.md#midi-controller-page-a-0x5e).
   With Page A = **SysEx**, Page A parameters use **`cmd=0x70`** (see
   [waf80.md](waf80.md)); with **Controller Data**, they use **MIDI CC**
   (CC number = Page A index).

### Parse template (11-byte live edit)

```text
F0 00 20 33 01 00 <cmd> <part> <param> <value> F7
```

Confirm `<part>` on the first few captures (Part 1 is often `0x00` but
hardware may use other scope bytes — note anomalies in docs).

Use this loop to confirm a **single** documented mapping at a time.

### 1. Load a known baseline

On the Virus: load **INIT MULTI** (e.g. multi **#32** from memory) into the
**Multi edit buffer**. Packed flags should be **`0x45`** per part at INIT
(Part 1 at offset **`0xF9`**, Part 16 at **`0x108`** in the full 267-byte
message).

Tell the user which baseline you loaded if you cannot operate the panel.

### 2. Send one live edit

Pick **one** parameter from
[multis-live-edit.md](multis-live-edit.md). Send exactly one `hex syx`
message (no `F0`/`F7` in the argument list).

**Tell the user** which part, menu field, and value you set so they can
confirm on the hardware (e.g. “Part 1 → Hold Pedal → Disabled”).

### 3. Confirm on hardware

Wait for user confirmation that the Edit Multi screen shows the expected
value.

Do **not** document new offsets from automation alone if the panel does not
match.

### 4. Capture `DUMP_MULTI`

**Option A — User / panel (reliable today)**  
Ask the user to dump the multi from the Virus while `receivemidi` is
listening:

```bash
receivemidi dev "$VIRUS_DEV" dump | tee /tmp/virus-dump.txt
```

Stop capture after the **267-byte** `F0 … 11 … F7` message (`cmd` byte
`0x11` at index `0x06`). Arrangement dumps may add sixteen `0x10`
(`DUMP_SINGLE`, 524 bytes each); keep only the multi dump for mapping work.

**Option B — `REQUEST_MULTI` (edit buffer)**  
With `receivemidi` running:

```bash
sendmidi dev "$VIRUS_DEV" hex syx 00 20 33 01 00 31 00 7f 7c
```

Replies with **`cmd=0x11`**, **267 bytes**, bank/slot **`00 7F`**. Checksum
`0x7C` = `(128 - (sum & 0x7F)) & 0x7F` over `00 20 33 01 00 31 00 7F`.

**Option C — Stored Multi bank slot**  
Bank **`01`**, slot = slot number (`09`, `30`, …). **No checksum** (AURA
format). See [multis-dump.md — Stored Multi bank request](multis-dump.md#request_multi-byte-table).

### 5. Diff against baseline

Save hex to a file or parse from `/tmp/virus-dump.txt`. Compare to a stored
INIT baseline; **only** the documented offset(s) should change for a single
parameter edit.

Example — Part 1 Hold off should change **`0xF9`** only (`0x45` → `0x41`),
plus often **`0x0A`** and the checksum byte **`0x109`**.

Ignore when diffing Virus panel vs AURA export baselines:

- `0x08` slot (`0x7F` vs `0x00`)
- `0x0C`, `0x26` (edited-part context)

Python one-liner (two full messages as space-separated hex strings):

```python
def parse(s):
    return [int(x, 16) for x in s.split()]

a = parse(open("/tmp/baseline.txt").read())
b = parse(open("/tmp/after.txt").read())
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print(f"0x{i:02X}: {x:02X} -> {y:02X}")
```

### 6. Update documentation

Record results in [multis-dump.md](multis-dump.md) and/or
[multis-live-edit.md](multis-live-edit.md): offset, encoding, example hex,
and whether the source was **Virus hardware** vs AURA.

## Suggested smoke tests

Run in order after any setup change (port name, OS update, plugin path).

| #   | Live message (summary) | Panel check              |
| --- | ---------------------- | ------------------------ |
| 1   | P1 Hold `4A` `00`      | Part 1 Hold **Disabled** |
| 2   | P1 Hold `4A` `01`      | Hold **Enabled**         |
| 3   | P16 Enable `48` `00`   | Part 16 **Off**          |
| 4   | P1 Vol `27` `48` (+8)  | Part 1 Vol **+8**        |

## Unmapped-region correlation tests

After loading **INIT MULTI** in the edit buffer, send a live edit and
`REQUEST_MULTI` (`31 00 7F 7C`); diff against baseline. Sanity check:
Part 1 Volume (`72 00 27 48`) changes **`0x99`** only (+ checksum).

Tested **2026-06-02** on TI mk2 desktop — **no** `DUMP_MULTI` change in
`0x09..0x0C`, `0x19..0x28`, `0xB9..0xC7`, or `0xE8..0xF7` for:

| Live message (summary)         | Notes                         |
| ------------------------------ | ----------------------------- |
| Bend Up `71 00 1A` `00`/`7F`   | Part 1                        |
| Bend Down `71 00 1B` `00`/`7F` | Part 1                        |
| Secondary Out `73 00 2D`/`01`  | AURA path                     |
| Secondary Out `72 00 2D 01`    | Alternate cmd — still no dump |
| Keyboard `72 00 40` `00`/`01`  | Desktop                       |
| All Delays `73 00 1B 01`       | Global — not in multi dump    |

Use `receivemidi syx` (not `dump`) for hex capture.

Expected single-byte dump changes: (1) `0xF9` `0x45` to `0x41`; (2) back to
`0x45`; (3) `0x108` `0x45` to `0x44`; (4) `0x99` `0x40` to `0x48`.

Packed-flag INIT byte **`0x45`** = `0b01000101`: enable, Hold on, Prog
Change on, Vol RX off, Priority low. See
[multis-dump.md — Packed flags](multis-dump.md#packed-flags-at-0xf8--part).

## Running `receivemidi` as an agent

`receivemidi dump` runs until killed. Typical pattern:

1. Start capture in a **background** shell writing to `/tmp/virus-midi.txt`.
2. Send live edit (and/or user triggers panel dump).
3. Wait 2–5 s, stop `receivemidi` (`pkill -f 'receivemidi dev'` or kill the
   background job).
4. Inspect `/tmp/virus-midi.txt` for `F0 00 20 33 … 11 …`.

macOS may not have `timeout`; do not rely on it.

## AURA vs hardware

Some fields do not appear in AURA-exported `DUMP_MULTI` files. Prefer
**Virus panel edits + hardware dump** for mapping. See
[aura-notes.md](aura-notes.md).

## When to stop and ask the user

- `sendmidi` was not invoked as `hex syx …` (wrong wire format).
- Dump diff touches **multiple** payload bytes for one edit.
- Packed flag byte is not at INIT **`0x45`** (another toggle still on).
- `REQUEST_MULTI` never returns `0x11` / 267 bytes.
- Plugin port missing (use External I/O only if user directs).

## References

- [README Setup](../README.md#setup) — install and minimal examples
- [virus.md](virus.md) — dump types and Multi bank slots
- [multis-live-edit.md](multis-live-edit.md) — `0x72` param IDs
- [multis-dump.md](multis-dump.md) — payload offsets and capture rules
