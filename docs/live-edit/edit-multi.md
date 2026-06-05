# Edit Multi

Part of [Live Edit](README.md).

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
[edit-single.md](edit-single.md).

Enumerated options: [parameter-options.md](../parameter-options.md).

## Summary

| Param ID | Memory / Target              | Parameter        | Description                                  |
| -------- | ---------------------------- | ---------------- | -------------------------------------------- |
| `0x0F`   | Global (`0x17` in dump)      | Master Clock     | Global Multi tempo                           |
| `0x23`   | `0x59 + part`                | Low Key          | Part low key limit                           |
| `0x24`   | `0x69 + part`                | High Key         | Part high key limit                          |
| `0x25`   | `0x79 + part`                | Transpose        | Part transposition                           |
| `0x26`   | `0x89 + part`                | Detune           | Part detune                                  |
| `0x1A`   | **Not in dump**              | Bend Up          | Pitch bend up limit (`cmd=0x71`)             |
| `0x1B`   | **Not in dump**              | Bend Down        | Pitch bend down limit (`cmd=0x71`)           |
| `0x27`   | `0x99 + (part−1)`            | Volume           | Part level (Part 16 at `0xA8`)               |
| `0x20`   | `0x29 + (part−1)`            | Bank             | Single bank index (P1 at `0x29`)             |
| `0x21`   | `0x39 + (part−1)`            | Program          | Single program 0–127 (P1 at `0x39`)          |
| `0x22`   | `0x49 + (part−1)`            | MIDI Channel     | Part MIDI channel 1–16 (P1 at `0x49`)        |
| `0x28`   | `0xA9 + (part−1)`            | Init Volume      | MIDI volume on multi select (Part 16 `0xB8`) |
| `0x29`   | `0xC8 + part`                | Output Routing   | Part output bus and channel                  |
| `0x2D`   | **Not in dump** (`cmd=0x73`) | Secondary Output | Second output bus (`cmd=0x73`)               |
| `0x2B`   | `0xD8 + part`                | Panorama         | Part pan position                            |
| `0x40`   | **Not in dump** (desktop)    | Keyboard-related | Keyboard global behavior control             |
| `0x48`   | `0xF8 + part` (packed flags) | Enable           | Part on/off                                  |
| `0x49`   | `0xF8 + part` (packed flags) | Volume RX        | Receive MIDI CC#7                            |
| `0x4A`   | `0xF8 + part` (packed flags) | Hold Pedal       | Sustain pedal behavior                       |
| `0x4D`   | `0xF8 + part` (packed flags) | Priority         | Note-steal priority                          |
| `0x4E`   | `0xF8 + part` (packed flags) | Program Change   | Program Change response                      |

**Not in this table:** **Direct Monitoring** (VC-only; dump byte
unmapped — [arrangements.md](../dumps/arrangements.md#direct-monitoring)).
**Solo** in some host UIs manipulates **`0x48` Enable** on other parts — see
[aura-notes.md](../aura-notes.md#multi-mixer-ui-host-software).

## Parameters

### Master Clock Tempo (`0x0F`)

- Global parameter.
- Dump correlation: `0x17` in `DUMP_MULTI`.
- Supported values: see [Tempo (`bpm - 63`)](#tempo-bpm---63).

### Low Key (`0x23`)

- Per-part note-range lower bound.
- Dump correlation: `0x59 + part`.
- Supported values: see [Key Range (direct 7-bit)](#key-range-direct-7-bit).

### High Key (`0x24`)

- Per-part note-range upper bound.
- Dump correlation: `0x69 + part`.
- Supported values: see [Key Range (direct 7-bit)](#key-range-direct-7-bit).

### Transpose (`0x25`)

- Per-part transpose in live edit.
- Dump correlation: `0x79 + part`.
- Note: live and dump use different value mapping for TI UI range.
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Detune (`0x26`)

- Per-part detune in live edit.
- Dump correlation: `0x89 + part`.
- Live/dump values align (`00` = minimum, `40` = center-ish, `7F` = maximum).
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Bend Up (`0x1A`, `cmd=0x71`)

- Per-part **pitch bend up** limit (Edit Single → Common).
- Sent via **`cmd=0x71`**, not `0x72`:

  ```text
  F0 00 20 33 01 00 71 <part> <param> <value> F7
  ```

- Dump correlation: **not in `DUMP_MULTI`** (edit buffer; hardware-tested:
  `71 00 1A` at `00` / `7F` — identical dump vs INIT baseline).
- Encoding: **`stored = ui + 64`** (center `0x40` = 0); UI **−64..+63** →
  `0x00..0x7F`.

| UI  | `<value>` (Part 1) |
| --- | ------------------ |
| −64 | `00`               |
| −2  | `3E`               |
| 0   | `40`               |
| +2  | `42`               |
| +63 | `7F`               |

```text
F0 00 20 33 01 00 71 00 1A 00 F7   # −64
F0 00 20 33 01 00 71 00 1A 3E F7   # −2
F0 00 20 33 01 00 71 00 1A 40 F7   # 0
F0 00 20 33 01 00 71 00 1A 42 F7   # +2
F0 00 20 33 01 00 71 00 1A 7F F7   # +63
```

### Bend Down (`0x1B`, `cmd=0x71`)

- Per-part **pitch bend down** limit (Edit Single → Common).
- Same transport and encoding as [Bend Up](#bend-up-0x1a-cmd0x71) (`cmd=0x71`,
  **`stored = ui + 64`**, UI **−64..+63**).
- Dump correlation: **not in `DUMP_MULTI`** (hardware-tested: `71 00 1B` at
  `00` / `7F` — no dump change).

| UI  | `<value>` (Part 1) |
| --- | ------------------ |
| −64 | `00`               |
| −2  | `3E`               |
| 0   | `40`               |
| +2  | `42`               |
| +63 | `7F`               |

```text
F0 00 20 33 01 00 71 00 1B 00 F7   # −64
F0 00 20 33 01 00 71 00 1B 3E F7   # −2
F0 00 20 33 01 00 71 00 1B 40 F7   # 0
F0 00 20 33 01 00 71 00 1B 42 F7   # +2
F0 00 20 33 01 00 71 00 1B 7F F7   # +63
```

### Volume (`0x27`)

- Per-part volume / level.
- Dump correlation: `0x99 + (part−1)` — Parts **1–16** at `0x99..0xA8`.
- Supported values: see **Value Reference → Bipolar `-63..+64` (live
encoding)**.

### Init Volume (`0x28`)

- Per-part init MIDI volume when Multi is selected.
- Dump correlation: `0xA9 + (part−1)` — Parts **1–16** at `0xA9..0xB8`.
- Supported values: see **Value Reference → Init Volume (direct 7-bit)**.

### Bank (`0x20`)

- Per-part Single **bank** for the part.
- Dump correlation: **`0x29 + (part−1)`** — see
  [Part bank index](../dumps/arrangements.md#part-bank-index) in
  `arrangements.md`.
- Live value = dump bank index (`0x00` = RAM A, `0x01` = RAM B, `0x04` =
  ROM A, etc.).
- Virus Part 1: live `72 00 20 01` → LCD **RAM-B** (confirmed).

### Program (`0x21`)

- Per-part Single **program** number.
- Dump correlation: **`0x39 + (part−1)`** — stored byte = UI program
  number on LCD (`0x00` = 0, `0x40` = 64, `0x41` = 65).
- Virus Part 1: `21 41` → program **65**; `21 00` → program **0** (dump
  confirmed).

### MIDI Channel (`0x22`)

- Per-part MIDI channel assignment.
- Dump correlation: `0x49 + (part−1)` — Part 1 at **`0x49`**.
- Live value is **zero-based** channel index: `0x00` = channel 1 …
  `0x0F` = channel 16 (Part 1: all 16 steps confirmed on Virus LCD).
- Supported values: see [MIDI Channel (zero-based)](#midi-channel-zero-based).

### Output Routing (`0x29`)

- Per-part output routing selection.
- Dump correlation: `0xC8 + part`.
- Supported values: see [Output Routing Enum
(`0x29`)](#output-routing-enum-0x29).

### Secondary Output (`0x2D`)

- Per-part **secondary** output routing (Edit Multi). On TI mk2 the same
  setting appears as **Edit Single → Surround → Output** (rear/surround bus);
  see [Surround (Edit Single)](edit-single.md#surround-edit-single).
- Sent via **`cmd=0x73`**, not `0x72`:

  ```text
  F0 00 20 33 01 00 73 00 2D <value> F7
  ```

  Part 1 captures confirmed; whether other parts use a part selector byte
  with the same param is **not confirmed**.
- Dump correlation: **not in `DUMP_MULTI`** (hardware-tested: `73 00 2D`
  Off/`01`, and `72 00 2D 01` — no dump change vs INIT baseline).
- Supported values: see
  [Secondary Output Enum (`0x2D`)](#secondary-output-enum-0x2d).

### Panorama (`0x2B`)

- Per-part panorama setting.
- Dump correlation: `0xD8 + part`.
- Supported values: see [Panorama (special direct)](#panorama-special-direct).

### Keyboard-related (`0x40`) — global

- Observed as global control (`part=00`).
- Keyboard local / global keyboard behavior (label TBD on panel).
- On TI desktop module, **`72 00 40` on/off does not change `DUMP_MULTI`**
  (hardware-tested).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Enable (`0x48`)

- Per-part packed-flag control (dump bit **`0x01`**: `0x44` off / `0x45` on
  at INIT).
- Dump correlation: `0xF8 + part`.
- Host **Mute** / **Solo** UIs may toggle this flag —
[aura-notes.md](../aura-notes.md).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Volume RX (`0x49`)

- Per-part receive MIDI CC#7.
- Dump correlation: packed flag at `0xF8 + part` (`+2` when enabled).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Hold Pedal (`0x4A`)

- Per-part sustain pedal behavior (MIDI CC#64).
- Dump correlation: packed flags at `0xF8 + part`.
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Priority (`0x4D`)

- Per-part voice priority.
- Dump correlation: packed flag at `0xF8 + part` (`+0x20` for High).
- Supported values: see [Priority Enum](#priority-enum).

### Program Change (`0x4E`)

- Per-part Program Change response.
- Dump correlation: packed flag at `0xF8 + part` (`±0x40` behavior).
- Supported values: see [Boolean On/Off](#boolean-onoff).

### Keyboard settings context (manual)

The TI manual distinguishes:

- **Keyboard to MIDI** (Edit Multi field).
- **Keyboard Local / Mode** (global CONFIG keyboard settings).

Current live mapping does not fully disambiguate these on all hardware
variants, so `0x40` remains keyboard-related with target TBD.

### Example messages (`0x72`)

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
  63)
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
| `00`  | Off     |
| `01`  | On      |

Used by: `0x40`, `0x48`, `0x49`, `0x4A`, `0x4E`.

### Bipolar `-63..+64` (live encoding)

| Value range | Meaning    |
| ----------- | ---------- |
| `00`..`7F`  | `-63..+64` |
| `00`        | `-63`      |
| `40`        | `+1`       |
| `7F`        | `+64`      |

Used by: `0x25` (live transpose), `0x27` (volume).

### Init Volume (direct 7-bit)

| Value range | Meaning       |
| ----------- | ------------- |
| `00`        | Off           |
| `01`..`7F`  | UI `1`..`127` |

Used by: `0x28`.

### MIDI Channel (zero-based)

| Value | MIDI channel |
| ----- | ------------ |
| `00`  | 1            |
| `01`  | 2            |
| `0F`  | 16           |

Stored the same way in `DUMP_MULTI` at `0x49 + (part−1)`. Used by: `0x22`.

### Key Range (direct 7-bit)

| Value range | Meaning            |
| ----------- | ------------------ |
| `00`..`7F`  | C1..G9 note domain |

Used by: `0x23` (Low Key), `0x24` (High Key).

### Output Routing Enum (`0x29`)

| Value     | Routing          |
| --------- | ---------------- |
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R |
| `06`–`08` | Out 3: L, L+R, R |
| `09`–`0B` | USB 1: L, L+R, R |
| `0C`–`0E` | USB 2: L, L+R, R |
| `0F`–`11` | USB 3: L, L+R, R |

Used by: `0x29`.

### Secondary Output Enum (`0x2D`)

Full panel labels: [Secondary output
routing](../parameter-options.md#secondary-output-routing).
**`00`** = Off; otherwise same routes as
[primary output](#output-routing-enum-0x29), **`stored = primary_index + 1`**
(through **`12`** = USB 3 R).

Part 1 captures (`cmd=0x73`):

```text
F0 00 20 33 01 00 73 00 2D 00 F7   # Off
F0 00 20 33 01 00 73 00 2D 01 F7   # Out 1 L
F0 00 20 33 01 00 73 00 2D 02 F7   # Out 1 L+R
F0 00 20 33 01 00 73 00 2D 0A F7   # USB 1 L
F0 00 20 33 01 00 73 00 2D 11 F7   # USB 3 L+R
```

Used by: `0x2D` with **`cmd=0x73`**.

### Priority Enum

| Value | Meaning |
| ----- | ------- |
| `00`  | Low     |
| `01`  | High    |

Used by: `0x4D`.

### Panorama (special direct)

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `40`  | Center  |

Used by: `0x2B`.

### Tempo (`bpm - 63`)

| BPM range | Stored value |
| --------- | ------------ |
| 63..190   | `00`..`7F`   |

Used by: `0x0F`.
