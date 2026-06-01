# Multis

Byte reference for Virus TI/TI2 Multi SysEx messages.

## Message-level structure

- `REQUEST_MULTI` message length: 11 bytes
- `DUMP_MULTI` message length: 267 bytes
- `DUMP_MULTI` command: `0x11`
- `REQUEST_MULTI` command: `0x31`
- Reference-style transfer: one `DUMP_MULTI` only
- Arrangement-style transfer: one `DUMP_MULTI` + 16 `DUMP_SINGLE` messages

## `REQUEST_MULTI` byte table

| Offset | Bytes | Meaning | Value range / notes |
|---|---|---|---|
| `0x00` | `F0` | SysEx start | Fixed |
| `0x01..0x03` | `00 20 33` | Access manufacturer ID | Fixed |
| `0x04` | `01` | Virus family marker | Fixed in observed TI/TI2 messages |
| `0x05` | `device_id` | Device ID | `00` observed |
| `0x06` | `31` | Request Multi command | Fixed for `REQUEST_MULTI` |
| `0x07` | `bank` | Multi bank selector | `01` observed in examples |
| `0x08` | `slot` | Multi slot/program index | `00..7F` (confirmed) |
| `0x09` | `checksum` | Checksum byte | Algorithm not fully documented here |
| `0x0A` | `F7` | SysEx end | Fixed |

## `DUMP_MULTI` byte table (267 bytes)

| Offset | Bytes | Meaning | Value range / notes |
|---|---|---|---|
| `0x00` | `F0` | SysEx start | Fixed |
| `0x01..0x03` | `00 20 33` | Access manufacturer ID | Fixed |
| `0x04` | `01` | Virus family marker | Fixed in observed TI/TI2 messages |
| `0x05` | `device_id` | Device ID | `00` observed |
| `0x06` | `11` | Dump Multi command | Fixed for `DUMP_MULTI` |
| `0x07` | `bank` | Multi bank selector | Echoes request bank |
| `0x08` | `slot` | Multi slot/program index | Echoes request slot |
| `0x09..0x108` | payload | Multi payload bytes | 256-byte payload block |
| `0x109` | checksum | Checksum byte | Changes with payload |
| `0x10A` | `F7` | SysEx end | Fixed |

## Confirmed payload fields (offsets in full 267-byte `DUMP_MULTI`)

| Offset(s) | Field | Encoding | Supported values |
|---|---|---|---|
| `0x0D..` | Multi name | ASCII text | Zero-padded/trailing spaces observed |
| `0x49..0x58` | Part MIDI channels (16 bytes) | Zero-based channel index | `0x00..0x0F` -> MIDI channels `1..16` |
| `0x89..0x98` | Part detune (16 bytes) | Bipolar centered at `0x40` | `0x00..0x7F` -> UI `-64..+63` (`stored = ui + 64`); Part 1 confirmed at `0x89`, Part 2 confirmed at `0x8A` |
| `0x99..0xA8` | Part levels (16 bytes) | Bipolar centered at `0x40` | `stored = ui + 64` (`0x00` = `-64`, `0x40` = `0`, `0x4C` = `+12`, `0x7F` = `+63`); Part 1–3 at `0x99`–`0x9B`; live param `0x27` |

## Candidate / partially understood bytes

| Offset | Status | Current interpretation |
|---|---|---|
| `0x0A` | Candidate | Likely state/version/edit flag byte |
| `0x26` | Candidate | Likely selected/edited-part context or state marker |

## Live parameter-change map (`cmd=0x72`)

Observed format:

`F0 00 20 33 01 00 72 <part> <param> <value> F7`

- `<part>` is zero-based part index (`00` = Part 1, `01` = Part 2)
- `<param>` is a parameter ID within this page
- `<value>` is the new value for that parameter

| Param ID | Field | Value encoding | Confirmed examples |
|---|---|---|---|
| `0x23` | Part Low Key (key range low note) | Direct 7-bit note value | `00` = C1, `01` = C#1, `7E` = F#9, `7F` = G9 |
| `0x24` | Part High Key (key range high note) | Direct 7-bit note value | `00` = C1, `7F` = G9; confirmed for Part 1 (`part=00`) and Part 16 (`part=0F`) |
| `0x25` | Part Transpose | Direct unsigned `0..127` mapped to bipolar UI | `00` = `-63`, `7F` = `+64` |
| `0x27` | Part Level | Bipolar centered at `0x40` | `stored = ui + 64`: `00` = `-64`, `40` = `0`, `4C` = `+12`, `4D` = `+13`, `7F` = `+63`; confirmed Parts 1, 8, 16; dump offset `0x99 + part` |
| `0x29` | Part Output routing | Enum (sequential) | Per output: L, L+R, R; order: Out 1–3, USB 1–3. Confirmed: `00` Out 1 L, `01` Out 1 L+R, `02` Out 1 R, `03` Out 2 L, `0D` USB 2 L+R, `10` USB 3 L+R, `11` USB 3 R; Parts 1, 8, 16 |
| `0x2B` | Part Panorama (Pan) | Direct unsigned `0..127` | `00` = Off; `40` = Center; `01` = Left 100%; `63` = Left 1%; `65` = Right 1%; `42` = Right 3%; `7F` = Right 100%; confirmed Parts 1, 2, 5 (`part=04`) |
| `0x4E` | Part Program Change (Prog Change) | Boolean | `00` = Disabled, `01` = Enabled; confirmed Parts 1, 2, 16 |
| `0x4D` | Part Note Priority | Boolean / enum | `00` = Low, `01` = High (Part 1 confirmed) |

### Part Output routing enum (`0x29`)

Each physical/USB output group uses three consecutive values: **L**, **L+R**, **R**.

| Value | Routing (confirmed or inferred) |
|---|---|
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R (`03` = Out 2 L confirmed) |
| `06`–`08` | Out 3: L, L+R, R (inferred) |
| `09`–`0B` | USB 1: L, L+R, R (inferred) |
| `0C`–`0E` | USB 2: L, L+R, R (`0D` = USB 2 L+R confirmed) |
| `0F`–`11` | USB 3: L, L+R, R (`10`, `11` confirmed) |

Notes:

- `F0 00 20 33 01 00 72 00 25 00 F7` confirms Part 1 (`part=00`) transpose minimum.
- `F0 00 20 33 01 00 72 01 25 7F F7` confirms Part 2 (`part=01`) transpose maximum.
- `F0 00 20 33 01 00 72 0F 24 7F F7` confirms `part=0F` maps to Part 16.

## AURA behavior: part enable sends `DUMP_SINGLE`

When a part track is disabled then re-enabled in AURA, a full **524-byte** message is sent with `cmd=0x10` (`DUMP_SINGLE`). This loads that part's single program into the synth (multi-mode per-part edit buffer), not a multi dump.

| Offset | Field | Encoding | Confirmed |
|---|---|---|---|
| `0x06` | Command | `0x10` = `DUMP_SINGLE` | Yes |
| `0x08` | Part index | Zero-based | `0x00`..`0x0F` for Parts 1..16 (confirmed: 1, 2, 8, 9, 16) |
| `0x09` | Context byte | Fixed `0x0C` in observed AURA loads | Yes |
| `0x0A..0x0B` | Context bytes | Two patterns observed | Parts 1–2: `10 00`; Parts 8, 9, 16: `00 01`; arrangement: `01 00` |

Parts 1 vs 2, and Parts 8 vs 9, differ only in part index (`0x08`) plus checksum and minor part-slot payload bytes.

Header bytes `0x0A..0x0B` split into two AURA patterns; meaning not yet mapped.

Arrangement-style exports use the same `DUMP_SINGLE` message type for each of 16 parts after the multi header message; arrangement singles use header pattern `00 <part> 0C 01 00`.

## Notes

- Offsets above are in the full SysEx message (including `F0` at offset `0x00`).
- The same fields can also be expressed as payload-relative offsets by subtracting `0x09`.
