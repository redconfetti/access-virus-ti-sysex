# Edit Multi

Part of [Documentation](../../README.md#documentation). Paging:
[virus.md](../misc/virus.md#paging).

Live SysEx notes for Multi edit behavior on Virus TI mk2.

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7
```

Some parameters use **`cmd=0x71`** instead of **`0x72`** (same byte layout):

```text
F0 00 20 33 01 00 71 <part> <param> <value> F7
```

- `<part>` — zero-based part index (`00` = Part 1, `0F` = Part 16)
- `<param>` — Multi edit parameter ID
- `<value>` — parameter value (encoding depends on parameter)

Single-related live edits (`cmd=0x6E`, `cmd=0x10`) are in
[single.md](single/single.md).

Enumerated options: [parameter-options.md](../reference/parameter-options.md).

## Summary

| Param ID | Memory / Target | Parameter | Description |
| -------- | ---------------------------- | ---------------- | -------------------------------------------- |
| `0x0F` | Global (`0x18` in dump) | Master Clock | Global Multi tempo |
| `0x23` | `0x59 + part` | Low Key | Part low key limit |
| `0x24` | `0x69 + part` | High Key | Part high key limit |
| `0x25` | `0x79 + part` | Transpose | Part transposition |
| `0x26` | `0x89 + part` | Detune | Part detune |
| `0x1A` | **Not in dump** | Bend Up | Pitch bend up limit (`cmd=0x71`) |
| `0x1B` | **Not in dump** | Bend Down | Pitch bend down limit (`cmd=0x71`) |
| `0x27` | `0x99 + (part−1)` | Volume | Part level (Part 16 at `0xA8`) |
| `0x20` | `0x29 + (part−1)` | Bank | Single bank index (P1 at `0x29`) |
| `0x21` | `0x39 + (part−1)` | Program | Single program 0–127 (P1 at `0x39`) |
| `0x22` | `0x49 + (part−1)` | MIDI Channel | Part MIDI channel 1–16 (P1 at `0x49`) |
| `0x28` | `0xA9 + (part−1)` | Init Volume | MIDI volume on multi select (Part 16 `0xB8`) |
| `0x29` | `0xC8 + part` | Output Routing | Part output bus and channel |
| `0x2D` | **Not in dump** (`cmd=0x73`) | Secondary Output | Second output bus (`cmd=0x73`) |
| `0x2B` | `0xD8 + part` | Panorama | Part pan position |
| `0x40` | **Not in dump** (desktop) | Keyboard-related | Keyboard global behavior control |
| `0x48` | `0xF8 + part` (packed flags) | Enable | Part on/off |
| `0x49` | `0xF8 + part` (packed flags) | Volume RX | Receive MIDI CC#7 |
| `0x4A` | `0xF8 + part` (packed flags) | Hold Pedal | Sustain pedal behavior |
| `0x4D` | `0xF8 + part` (packed flags) | Priority | Note-steal priority |
| `0x4E` | `0xF8 + part` (packed flags) | Program Change | Program Change response |

**Not in this table (not in Multi Dump):** **Secondary Output** (`73` /
`0x2D`), **Bend Up/Down** (`71` / `0x1A`, `0x1B` — in **Single Dump**
only), **Direct Monitoring** (VC **Live**). See
[Runtime-only Edit Multi](../dumps/multi.md#runtime-only-edit-multi).
**Solo** in some host UIs manipulates **`0x48` Enable** on other parts.

## Parameters

### Master Clock Tempo

**Live edit:** param `0x0F`.

- Global parameter.
- Dump correlation: `0x18` in Multi Dump (follows 10-byte name at `0x0D`–`0x16`
  and null at `0x17`).
- Supported values: see [Tempo (`bpm - 63`)](#tempo-bpm---63).

### Low Key

**Live edit:** param `0x23`.

- Per-part note-range lower bound.
- Dump correlation: `0x59 + part`.
- Supported values: see [Key Range (direct 7-bit)](#key-range-direct-7-bit).

### High Key

**Live edit:** param `0x24`.

- Per-part note-range upper bound.
- Dump correlation: `0x69 + part`.
- Supported values: see [Key Range (direct 7-bit)](#key-range-direct-7-bit).

### Transpose

**Live edit:** param `0x25`.

- Per-part transpose in live edit.
- Dump correlation: `0x79 + part`.
- Note: live and dump use different value mapping for TI UI range.
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Detune

**Live edit:** param `0x26`.

- Per-part detune in live edit.
- Dump correlation: `0x89 + part`.
- Live/dump values align (`00` = minimum, `40` = center-ish, `7F` = maximum).
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Bend Up

**Live edit:** `cmd=0x71`, param `0x1A`.

- Per-part **pitch bend up** limit (Edit Single → Common).
- Sent via **`cmd=0x71`**, not `0x72`:

 ```text
 F0 00 20 33 01 00 71 <part> <param> <value> F7
 ```

- **Not in Multi Dump** — eliminated on TI mk2 desktop (identical dump vs
  INIT baseline; values live in **Single Dump** when editing that part’s
  Single). See
  [multi.md — Bend limits](../dumps/multi.md#bend-limits-not-in-multi-dump).
- Encoding: **`stored = ui + 64`** (center `0x40` = 0); UI **−64..+63** →
 `0x00..0x7F`.

| UI | `<value>` (Part 1) |
| --- | ------------------ |
| −64 | `00` |
| −2 | `3E` |
| 0 | `40` |
| +2 | `42` |
| +63 | `7F` |

```text
F0 00 20 33 01 00 71 00 1A 00 F7 # −64
F0 00 20 33 01 00 71 00 1A 3E F7 # −2
F0 00 20 33 01 00 71 00 1A 40 F7 # 0
F0 00 20 33 01 00 71 00 1A 42 F7 # +2
F0 00 20 33 01 00 71 00 1A 7F F7 # +63
```

### Bend Down

**Live edit:** `cmd=0x71`, param `0x1B`.

- Per-part **pitch bend down** limit (Edit Single → Common).
- Same transport and encoding as [Bend Up](#bend-up) (`cmd=0x71`,
 **`stored = ui + 64`**, UI **−64..+63**).
- **Not in Multi Dump** — eliminated (hardware-tested: `71 00 1B` at
  `00` / `7F` — no dump change). Stored in **Single Dump** for the part
  Single, not the multi block.

| UI | `<value>` (Part 1) |
| --- | ------------------ |
| −64 | `00` |
| −2 | `3E` |
| 0 | `40` |
| +2 | `42` |
| +63 | `7F` |

```text
F0 00 20 33 01 00 71 00 1B 00 F7 # −64
F0 00 20 33 01 00 71 00 1B 3E F7 # −2
F0 00 20 33 01 00 71 00 1B 40 F7 # 0
F0 00 20 33 01 00 71 00 1B 42 F7 # +2
F0 00 20 33 01 00 71 00 1B 7F F7 # +63
```

### Volume

**Live edit:** param `0x27`.

- Per-part volume / level.
- Dump correlation: `0x99 + (part−1)` — Parts **1–16** at `0x99..0xA8`.
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Init Volume

**Live edit:** param `0x28`.

- Per-part init MIDI volume when Multi is selected.
- Dump correlation: `0xA9 + (part−1)` — Parts **1–16** at `0xA9..0xB8`.
- Supported values: see **Value Reference → Init Volume (direct 7-bit)**.

### Bank

**Live edit:** param `0x20`.

- Per-part Single **bank** for the part.
- Message: **`72 <part> 20 <bank_index>`** — **`<part>`** = Multi part
 **`0x00`–`0x0F`** (Part 1 = **`0x00`**), not Single-mode scope **`0x40`**.
- Dump correlation: **`0x29 + (part−1)`** — see
 [Part bank index](../dumps/multi.md#part-bank-index) in
 `multi.md`.
- Live value = dump bank index (`0x00` = RAM A, `0x01` = RAM B, `0x04` =
 ROM A, etc.).
- Virus Part 1: live `72 00 20 01` → LCD **RAM-B** (confirmed).

### Program

**Live edit:** param `0x21`.

- Per-part Single **program** number.
- Message: **`72 <part> 21 <program>`** — same **`<part>`** rule as Bank.
- Dump correlation: **`0x39 + (part−1)`** — stored byte = UI program
 number on LCD (`0x00` = 0, `0x40` = 64, `0x41` = 65).
- Virus Part 1: `21 41` → program **65**; `21 00` → program **0** (dump
 confirmed).

**Load from RAM/ROM (Multi mode, Part 1)** — set bank/program via **`0x72`**, then
upload with **Single Dump** (`0x10`); hardware load-from-bank via **`0x72` alone**
is **not confirmed** on TI mk2:

```text
F0 00 20 33 01 00 72 00 20 00 F7  # Part 1 → RAM A
F0 00 20 33 01 00 72 00 21 40 F7  # Part 1 → program 64 (wire 0x40)
```

### MIDI Channel

**Live edit:** param `0x22`.

- Per-part MIDI channel assignment.
- Dump correlation: `0x49 + (part−1)` — Part 1 at **`0x49`**.
- Live value is **zero-based** channel index: `0x00` = channel 1 …
 `0x0F` = channel 16 (Part 1: all 16 steps confirmed on Virus LCD).
- Supported values: see [MIDI Channel (zero-based)](#midi-channel-zero-based).

### Output Routing

**Live edit:** param `0x29`.

- Per-part output routing selection.
- Dump correlation: `0xC8 + part`.
- Supported values: see [Output Routing Enum
(`0x29`)](#output-routing-enum).

### Secondary Output

**Live edit:** param `0x2D`.

- Per-part **secondary** output routing (Edit Multi). On TI mk2 the same
 setting appears as **Edit Single → Surround → Output** (rear/surround bus);
 see [Surround (Edit Single)](single/single.md#surround-edit-single).
- Sent via **`cmd=0x73`**, not `0x72`:

 ```text
 F0 00 20 33 01 00 73 00 2D <value> F7   # Edit Multi Part 1
 F0 00 20 33 01 00 73 40 2D <value> F7   # Single edit buffer
 ```

 Part 1 captures confirmed; Single mode uses **`<part>=0x40`**. Whether other
 Multi parts use a different part byte with the same param is **not confirmed**.

- **Not in Multi Dump** — eliminated (hardware-tested: `73 00 2D` and
  `72 00 2D` — no dump change vs INIT baseline). Same class as Edit Single
  Surround **Output** (also absent from **Single Dump**). See
  [multi.md](../dumps/multi.md#secondary-output-not-in-multi-dump).
- Supported values: see
 [Secondary Output Enum (`0x2D`)](#secondary-output-enum).

### Panorama

**Live edit:** param `0x2B`.

- Per-part panorama setting.
- Dump correlation: `0xD8 + part`.
- Supported values: see [Panorama (special direct)](#panorama-special-direct).

### Keyboard-related (`0x40`) — global

- Observed as global control (`part=00`).
- Keyboard local / global keyboard behavior (label TBD on panel).
- On TI desktop module, **`72 00 40` on/off does not change Multi Dump**
 (hardware-tested).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Enable

**Live edit:** param `0x48`.

- Per-part packed-flag control (dump bit **`0x01`**: `0x44` off / `0x45` on
 at INIT).
- Dump correlation: `0xF8 + part`.
- Host **Mute** / **Solo** UIs may toggle this flag.
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Volume RX

**Live edit:** param `0x49`.

- Per-part receive MIDI CC#7.
- Dump correlation: packed flag at `0xF8 + part` (`+2` when enabled).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Hold Pedal

**Live edit:** param `0x4A`.

- Per-part sustain pedal behavior (MIDI CC#64).
- Dump correlation: packed flags at `0xF8 + part`.
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Priority

**Live edit:** param `0x4D`.

- Per-part voice priority.
- Dump correlation: packed flag at `0xF8 + part` (`+0x20` for High).
- Supported values: see [Priority Enum](#priority-enum).

### Program Change

**Live edit:** param `0x4E`.

- Per-part Program Change response.
- Dump correlation: packed flag at `0xF8 + part` (`±0x40` behavior).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Keyboard settings context (manual)

The TI manual distinguishes:

- **Keyboard to MIDI** (Edit Multi field).
- **Keyboard Local / Mode** (global CONFIG keyboard settings).

Current live mapping does not fully disambiguate these on all hardware
variants, so `0x40` remains keyboard-related with target TBD.

### Example messages

**Live edit:** param `0x72`.

- `F0 00 20 33 01 00 72 00 25 00 F7` — Part 1 transpose minimum
- `F0 00 20 33 01 00 72 01 25 7F F7` — Part 2 transpose maximum
- `F0 00 20 33 01 00 72 0F 24 7F F7` — Part 16 High Key G9
- `F0 00 20 33 01 00 72 00 24 00 F7` / `... 0F 24 00 F7` — Part 1 / Part 16
 High Key C1
- `F0 00 20 33 01 00 72 00 49 00 F7` / `... 49 01 F7` — Part 1 Volume RX
 off / on
- `F0 00 20 33 01 00 72 00 20 01 F7` / `... 21 41 F7` — Part 1 Bank RAM B /
 Program 65
- `F0 00 20 33 01 00 72 00 22 01 F7` / `... 22 0F F7` — Part 1 MIDI
 channel 2 / 16 (`0x01` / `0x0F` at dump `0x49`)
- `F0 00 20 33 01 00 72 00 4A 00 F7` / `... 4A 01 F7` — Part 1 Hold Pedal
 off / on
- `F0 00 20 33 01 00 72 0F 4A 00 F7` / `... 4A 01 F7` — Part 16 Hold Pedal
 off / on
- `F0 00 20 33 01 00 72 0F 49 00 F7` / `... 49 01 F7` — Part 16 Volume RX
 off / on
- `F0 00 20 33 01 00 72 0F 4E 00 F7` / `... 4E 01 F7` — Part 16 Program
 Change off / on
- `F0 00 20 33 01 00 72 0F 4D 01 F7` — Part 16 Priority High
- `F0 00 20 33 01 00 72 00 0F 3D F7` — Master Clock 124 bpm (`0x3D` = 124 −

 1)

- `F0 00 20 33 01 00 72 00 48 00 F7` / `... 48 01 F7` — Part 1 Enable
 off / on
- `F0 00 20 33 01 00 72 07 48 00 F7` — Part 8 Enable off (dump `0x100`
 `0x45`→`0x44`)
- `F0 00 20 33 01 00 72 0F 48 00 F7` / `... 48 01 F7` — Part 16 Enable
 off / on
- `F0 00 20 33 01 00 72 00 40 00 F7` / `... 40 01 F7` — keyboard-related
 global toggle

## Value Reference

### Boolean On/Off

| Value | Meaning |
| ----- | ------- |
| `00` | Off |
| `01` | On |

Used by: `0x40`, `0x48`, `0x49`, `0x4A`, `0x4E`.

### Bipolar `-63..+64` (live encoding)

| Value range | Meaning |
| ----------- | ---------- |
| `00`..`7F` | `-63..+64` |
| `00` | `-63` |
| `40` | `+1` |
| `7F` | `+64` |

Used by: `0x25` (live transpose), `0x27` (volume).

### Init Volume (direct 7-bit)

| Value range | Meaning |
| ----------- | ------------- |
| `00` | Off |
| `01`..`7F` | UI `1`..`127` |

Used by: `0x28`.

### MIDI Channel (zero-based)

| Value | MIDI channel |
| ----- | ------------ |
| `00` | 1 |
| `01` | 2 |
| `0F` | 16 |

Stored the same way in Multi Dump at `0x49 + (part−1)`. Used by: `0x22`.

### Key Range (direct 7-bit)

| Value range | Meaning |
| ----------- | ------------------ |
| `00`..`7F` | C1..G9 note domain |

Used by: `0x23` (Low Key), `0x24` (High Key).

### Output Routing Enum

**Live edit:** param `0x29`.

| Value | Routing |
| --------- | ---------------- |
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R |
| `06`–`08` | Out 3: L, L+R, R |
| `09`–`0B` | USB 1: L, L+R, R |
| `0C`–`0E` | USB 2: L, L+R, R |
| `0F`–`11` | USB 3: L, L+R, R |

Used by: `0x29`.

### Secondary Output Enum

**Live edit:** param `0x2D`.

Full panel labels: [Secondary output
routing](../reference/parameter-options.md#secondary-output-routing).
**`00`** = Off; otherwise same routes as
[primary output](#output-routing-enum), **`stored = primary_index + 1`**
(through **`12`** = USB 3 R).

Part 1 captures (`cmd=0x73`):

```text
F0 00 20 33 01 00 73 00 2D 00 F7 # Off
F0 00 20 33 01 00 73 00 2D 01 F7 # Out 1 L
F0 00 20 33 01 00 73 00 2D 02 F7 # Out 1 L+R
F0 00 20 33 01 00 73 00 2D 0A F7 # USB 1 L
F0 00 20 33 01 00 73 00 2D 11 F7 # USB 3 L+R
```

Used by: `0x2D` with **`cmd=0x73`**.

### Priority Enum

| Value | Meaning |
| ----- | ------- |
| `00` | Low |
| `01` | High |

Used by: `0x4D`.

### Panorama (special direct)

| Value | Meaning |
| ----- | ------- |
| `00` | Off |
| `40` | Center |

Used by: `0x2B`.

### Tempo (`bpm - 63`)

| BPM range | Stored value |
| --------- | ------------ |
| 63..190 | `00`..`7F` |

Used by: `0x0F`.
