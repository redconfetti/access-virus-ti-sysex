# Hardware testing (Virus TI mk2 desktop)

Guide for **agents** (and humans) verifying SysEx documentation against a
real **Access Virus TI mk2 desktop** using `sendmidi` / `receivemidi`.

Scope: **desktop module** via **`Virus TI USB Plugin I/O`**. Keyboard/Polar
and **External I/O** routing are out of scope unless the user says otherwise.

## Prerequisites

1. Virus TI mk2 powered on, USB connected, **Virus TI plugin** active so
   **`Virus TI USB Plugin I/O`** appears in port lists.
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

## Confirmation queue (WAF80 → TI)

Use [waf80.md](waf80.md) as the **1999 hypothesis**. Confirm on the **Virus TI
mk2 desktop**, record in the TI docs, then trim the matching WAF80 rows.

**Work by LCD menu**, aligned with [single-dump.md](single-dump.md) categories
— finish one menu before switching (e.g. all **Filters** controls, then
**Oscillators**).

| Status          | Category    | Virus LCD (typical)                 | Doc section                                        |
| --------------- | ----------- | ----------------------------------- | -------------------------------------------------- |
| Done            | **Filters** | **FILTERS** (F1/F2/Common/F1 ADSR)  | [single-dump.md — Filters](single-dump.md#filters) |
| Done            | **Amplifier** | **Amp Envelope** ADSR             | [single-live-edit.md — Amplifier envelope](single-live-edit.md#amplifier-envelope-adsr) |
| **In progress** | **Oscillator 1** | **OSCILLATORS** → Osc 1 — panel order | [single-dump.md — Oscillators](single-dump.md#oscillators) |

### Filters — order (Filter 1 first)

Confirm in this order (stay on the **FILTERS** menu):

| #   | Parameter                              | SubCategory | WAF80 Page A # (hypothesis) |
| --- | -------------------------------------- | ----------- | --------------------------- |
| 1   | ~~Filter 1 Cutoff~~                    | Filter 1    | **40** — ✓ `70 00 28`       |
| 2   | ~~Filter 1 Resonance~~                 | Filter 1    | **42** — ✓ `70 00 2A`       |
| 3   | ~~Filter 1 Mode~~                      | Filter 1    | **51** — ✓ 8 modes `00`–`07` |
| 4   | ~~Filter 1 Envelope Amount~~           | Filter 1    | **44** — ✓ linear %         |
| 5   | ~~Filter 1 Keyfollow~~                 | Filter 1    | **46** — ✓ `ui + 64`        |
| …   | (remaining Filter 1 / 2 / Common rows) |             | see parameter map           |

**Current step:** **OSCILLATORS → Oscillator 1**. Osc params are a **nested tree**:

1. **Mode** (Classic, Wavetable, Grain Simple, …) — changes which sub-menus exist
   (Classic **1–2**, Wavetable/Grain Simple/Formant Simple **1–3**, Grain/Formant
   Complex **1–4**).
2. **Shape** (within many modes) — changes which controls appear on those menus.

Report captures as **`Mode: …` / `Shape: …` / `Control: …` → LCD value** so session
notes stay unambiguous. Use **+/−** for single steps when possible (cleaner log than
long knob sweeps). Session notes until Osc 1 is done; then Osc 2, Common, Mixer.

**Shape / Saw>Pulse:** Value byte is **hex** on the `70 00 11` line (`0x44`…`0x5A`…`0x7E`).
`receivemidi`’s trailing **`dec`** is decimal equivalent only (e.g. `5A` hex = 90 dec).
Do not use a decimal **44–66** index column — use **hex `44`–`5A`** (see live-edit table).

**WAF80 Page A hypotheses (Osc 1, `cmd=0x70` unless capture says otherwise):**

| A# | `param` | Classic name | Range (WAF80) |
| -- | ------- | ------------ | ------------- |
| 17 | `11` | Shape | TI: **enum** on `70`/`11` (not classic bipolar) |
| 18 | `12` | Pulsewidth | 0–127 |
| 19 | `13` | Wave Select | 0–64 |
| 20 | `14` | Semitone | −64..+63 |
| 21 | `15` | Keyfollow | −64..+63 |

**Mode:** `6E`/`1E` — Classic = `00` ✓. **Classic / Spectral Wave** in progress.
See [single-live-edit.md — Oscillator 1](single-live-edit.md#oscillators).

**Key Follow “Norm” (done):** Stored Single with Key Follow **−21**; after reload,
**Norm** still = **+32** / wire **`0x60`** — fixed scale marker, not per-patch default.

| Status | Category | Notes |
| ------ | -------- | ----- |
| Done | Filter 1 | Cutoff, Resonance, Mode (8), Env Amt, Keyfollow, Env Polarity (`1E`) |
| Done | Filter 2 | Offset, Resonance, Mode (4), Env Amt, Keyfollow, Env Polarity (`1F`); Cutoff **N/A** |
| Done | Filter Common | Routing, Balance, Cutoff Link, Key Follow Base, Pan Spread (Split only) |
| Done | Filter 1 envelope | `36`–`3A` ADSR (FILTERS → Filter Envelope menu) |
| Done | Amp Envelope | `3B`–`3F` ADSR (same encodings as Filter 1 env) |
| Done | Saturation (Filters) | Osc Volume `70`/`24`; knob target `71`/`7A` |

## Interactive single-parameter capture (panel → host)

Use this loop when the **user** turns a control on the Virus and the agent
listens with `receivemidi syx`.

### Agent setup (persistent log)

The **agent** keeps **`receivemidi`** running for the whole mapping session and
**tails** the log after each user edit — the user does **not** paste SysEx hex.

```bash
VIRUS_DEV='Virus TI USB Plugin I/O'
LOG=/tmp/virus-live-capture.txt
: > "$LOG"
receivemidi dev "$VIRUS_DEV" syx 2>&1 | tee -a "$LOG"
```

Run with `required_permissions: ["all"]`. Leave this process running in a
background shell until the session ends; then `pkill -f 'receivemidi dev'`.

After the user reports a landing UI value, the agent reads the **last**
non-empty line from **`$LOG`** (e.g. `tail -n 20 "$LOG"`). Ignore empty
`F0 F7`-only lines unless that is the only traffic for that action.

Follow [Confirmation queue](#confirmation-queue-waf80--ti)
when doing WAF80-driven mapping; otherwise pick one row from
[single-dump.md — Single parameter map](single-dump.md#single-parameter-map).

### User / agent rules

1. Agent names the **category** and **parameter** before each capture.
2. User edits that control on the Virus (Edit Single context, Part 1 unless
   noted).
3. **Knob turns** often produce **many SysEx messages** — use the **last
   message** in the burst as the landing value.
4. The **user** reports only the **final UI value** (not every intermediate
   step). The **agent** tails **`/tmp/virus-live-capture.txt`** and uses the
   last relevant SysEx line — no need to copy hex from a MIDI monitor.
5. **Ranged parameters** (percent, bipolar, tempo, etc.): the agent prompts for
   **several LCD landing values** (e.g. **0 %**, **50 %**, **100 %**) until the
   encoding is clear — not only one endpoint.
6. Agent records **`cmd`**, **param**, **value** encoding in **session notes**
   (chat) as captures arrive; **flush to markdown only when a menu group is
   done** (e.g. all Filter 2 rows, or Filters complete) — not after every
   single landing.
7. Toggle/switch controls may send a single message; knobs and sliders may
   send a stream.
8. Some controls send **MIDI CC only** (no SysEx) — e.g. **Sub Oscillator
   Volume** = **CC 34**; see [control-change.md](control-change.md).
9. **Before a SysEx mapping session**, set globals **MIDI Controller Page A**
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
Bank **`01`**, slot = slot number (`09`, `30`, …). **No checksum** on the
request. See [multis-dump.md — Stored Multi bank request](multis-dump.md#request_multi-byte-table).

### 5. Diff against baseline

Save hex to a file or parse from `/tmp/virus-dump.txt`. Compare to a stored
INIT baseline; **only** the documented offset(s) should change for a single
parameter edit.

Example — Part 1 Hold off should change **`0xF9`** only (`0x45` → `0x41`),
plus often **`0x0A`** and the checksum byte **`0x109`**.

When diffing against a host-plugin export baseline, see
[aura-notes.md — Export and diff baselines](aura-notes.md#export-and-diff-baselines).

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
[multis-live-edit.md](multis-live-edit.md): offset, encoding, and example
hex from **Virus hardware** captures.

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
| Secondary Out `73 00 2D`/`01`  | `cmd=0x73`                    |
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

**Parameter mapping (panel → host):** one long-running `receivemidi syx` →
`/tmp/virus-live-capture.txt`; tail the log per step (see [Agent setup](#agent-setup-persistent-log)).

**One-shot dump capture** (`receivemidi dump` for `DUMP_MULTI`):

1. Start `receivemidi dump` in a background shell → `/tmp/virus-midi.txt`.
2. User triggers panel dump or agent sends `REQUEST_MULTI`.
3. Wait 2–5 s, stop `receivemidi` (`pkill -f 'receivemidi dev'`).
4. Inspect `/tmp/virus-midi.txt` for `F0 00 20 33 … 11 …`.

macOS may not have `timeout`; do not rely on it.

Host plugin quirks (export gaps, UI labels): [aura-notes.md](aura-notes.md).

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
