# Arrangements & Multis

Part of [Documentation](../../../README.md#documentation). Multi mode on the Virus TI: program types, **Edit
Multi** parameters, and
byte-level Multi Dump mapping.

## Multi Dump

### Multi Dump byte reference

Byte reference for Multi SysEx messages (Multi Dump, 267
bytes). **Edit Multi** parameters are mapped in
[Multi parameter map](#multi-parameter-map) and
[Confirmed payload
fields](#confirmed-payload-fields-offsets-in-full-267-byte-multi-dump).
Remaining gaps: **Keyboard to MIDI** (no dump byte on the desktop module) and
payload metadata in [Unmapped payload](#unmapped-payload). **Secondary Output**,
**Bend Up/Down** (Multi), and **Direct Monitoring** are **not** in this
267-byte block — see [Runtime-only Edit Multi](#runtime-only-edit-multi).

## Embedded vs Reference Multis

The TI **Multi bank** has **128 slots**. Every slot — and the **Multi edit
buffer** — uses the same **267-byte** Multi Dump layout, including
per-part **Bank** and **Program** bytes at `0x29..` / `0x39..`.

| Slots | Storage model | Typical MIDI export |
| ---------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1–16** | **Embedded** | **Type: Arrangement** — one Multi Dump plus **sixteen Single Dump** messages (524 bytes each). Slots 1–16 hold **full Single program data** for all sixteen parts, matching those sixteen singles. |
| **17–128** | **Reference** | **Multi Dump only** — multi settings and bank/program pointers per part; Singles remain in RAM/ROM banks. |

**Requesting a dump**

- **Multi edit buffer** — from the Virus panel, or SysEx
 **`REQUEST_MULTI`** bank **`00`** slot **`7F`** (checksum **`7C`**).
- **Stored Multi bank slot** — SysEx **`REQUEST_MULTI`** bank **`01`**, slot
 = slot number (`9`→`0x09`, `48`→`0x30`; no checksum byte). See
 [`REQUEST_MULTI`](#request_multi-byte-table).

A **`REQUEST_MULTI`** reply is always the **267-byte** multi block first;
**Arrangement**-style export (edit buffer or slots **1–16**) adds the
sixteen singles in **part order** — see
[Arrangement export](single.md#arrangement-export-single-dump--16).

### Multi parameter map

Fields match the **Edit Multi** screen.

#### Summary

| Parameter (TI Edit Multi) | Scope | Dump offset |
| ------------------------- | ------------- | ------------------------- |
| Multi Program Name | Global | `0x0D..0x16` (+ null `0x17`) |
| Master Clock Tempo | Global | `0x18` |
| Keyboard to MIDI | Global | **Not in dump** (desktop) |
| Enable | Part-specific | `0xF8 + part` |
| Direct Monitoring | Part-specific | **Not in dump** |
| Bank | Part-specific | `0x29 + (part−1)` |
| Program | Part-specific | `0x39 + (part−1)` |
| Volume | Part-specific | `0x99 + (part−1)` |
| Panorama | Part-specific | `0xD8 + part` |
| MIDI Channel | Part-specific | `0x49 + (part−1)` |
| Output | Part-specific | `0xC8 + part` |
| Transpose | Part-specific | `0x79 + part` |
| Detune | Part-specific | `0x89 + part` |
| Priority | Part-specific | `0xF8 + part` (flag) |
| Init Volume | Part-specific | `0xA9 + (part−1)` |
| Low Key | Part-specific | `0x59 + part` |
| High Key | Part-specific | `0x69 + part` |
| Hold Pedal | Part-specific | `0xF8 + part` (flag) |
| Volume RX | Part-specific | `0xF8 + part` (flag) |
| Program Change | Part-specific | `0xF8 + part` (flag) |

#### Parameters

##### Multi Program Name

ASCII name for the multi — **10 bytes** at **`0x0D`–`0x16`** (case as entered on
the panel), null at **`0x17`**. **No live-edit SysEx** on desktop (panel
rename → **Multi Dump** only; **`receivemidi`** capture empty on rename).

Hardware-verified (edit buffer, INIT MULTI baseline → **`Init Mult4`**):

| Offset | `INIT MULTI` | `Init Mult4` |
| -------- | ------------ | ------------ |
| `0x0D` | `49` (`I`) | `49` (`I`) |
| `0x0E` | `4E` (`N`) | `6E` (`n`) |
| `0x0F` | `49` (`I`) | `69` (`i`) |
| `0x10` | `54` (`T`) | `74` (`t`) |
| `0x11` | `20` (sp) | `20` (sp) |
| `0x12` | `4D` (`M`) | `4D` (`M`) |
| `0x13` | `55` (`U`) | `75` (`u`) |
| `0x14` | `4C` (`L`) | `6C` (`l`) |
| `0x15` | `54` (`T`) | `74` (`t`) |
| `0x16` | `49` (`I`) | `34` (`4`) |
| `0x17` | `00` | `00` |

Edit flag **`0x0A`** also toggles (`00` → `01`) on rename.

##### Master Clock Tempo

Global tempo for all parts in the Multi (**63–190** bpm), overriding
Single-program Master Clock settings. Dump at **`0x18`**
(`stored = bpm - 63`; `120`→`0x39`, `124`→`0x3D`); INIT MULTI baseline.
Live edit: **`72` / `0x0F`** — see [multis.md](../live-edit/multis.md).

##### Keyboard to MIDI

Disabled / Enabled — whether keyboard notes are **also sent to MIDI OUT**.
Distinct from CONFIG **Local** / **Mode** (TI Keyboard / Polar panel).
Desktop module has no keyboard.

##### Enable

On / Off. Bit **`0x01`**: `0x44` off / `0x45` on at INIT (`±0x01` from
the other state). Part 8 at **`0x100`** (`0x45`→`0x44`); Part 16 at
**`0x108`** (`0x45`→`0x44`, checksum unchanged `0x20`).

**Mute** and **Solo** in host software are mixer UI controls, not separate
dump fields. Solo may disable other parts by toggling **Enable**.

##### Direct Monitoring

Per-part Edit Multi setting (VC **Live** / direct monitoring). When enabled,
that part’s audio is routed from the **analog outputs** directly, bypassing
the USB return path through the DAW (avoids USB buffer latency for live
performance). Not all host apps expose this control.

**Not in Multi Dump.** Treat as **runtime / VC state** — same class as
[Secondary Output](#secondary-output-not-in-multi-dump) and Multi **Bend
Up/Down** (stored in **Single Dump** when editing a Single, not in the
267-byte multi block). Do not map to [unmapped payload](#unmapped-payload)
regions.

##### Secondary Output (not in Multi Dump) {#secondary-output-not-in-multi-dump}

Per-part **secondary** output routing — live edit only (`73` / `0x2D`; same
param as Edit Single → Surround → Output). Hardware-tested:
**no** change to **Multi Dump** vs baseline. See
[multis.md](../live-edit/multis.md#secondary-output).

##### Bend Up / Down (Multi — not in Multi Dump) {#bend-limits-not-in-multi-dump}

Edit Multi exposes the same pitch-bend limit controls as Edit Single
(`71` / `0x1A`, `0x1B`). Values live in **Single Dump** when editing a
part’s Single; they do **not** appear in **Multi Dump**. Hardware-tested:
identical multi dump vs INIT after `71 00 1A` / `1B` sweeps. See
[multis.md](../live-edit/multis.md).

##### Bank

Bank from which a Single is loaded into the part. Sequential index at
**`0x29 + (part−1)`**. Part 1: RAM B → index **`0x01`** at **`0x29`**
confirmed.

##### Program

Program number for that bank (**0–127**). Direct **`0x00..0x7F`** at
**`0x39 + (part−1)`**. Part 1: LCD **65** → stored **`0x41`** at
**`0x39`** confirmed.

##### Volume

Part balance (**−64..+63**). Parts **1–16** at
`0x99..0xA8`; `stored = ui + 64`; P1 at `0x99`, P16 at `0xA8` (e.g. UI
`+46` → `0x6E`).

##### Panorama

**−64..+63**; overrides the Single pan. Part 1 at `0xD8` confirmed.

##### MIDI Channel

**1–16**. Parts **1–16** at **`0x49..0x58`**; zero-based channel index
(`0x00` = ch 1, `0x0F` = ch 16). Part 1: ch 2 → `0x01`, ch 16 →
`0x0F` at **`0x49`**. All channels **`0x00`–`0x0F`** verified.

##### Output

Out 1 L … Out 3 R on **Edit Multi** (analog only); USB 1–3 also in
protocol (`09`–`11`). **`0xC8..0xD7`**, one byte per part:

| Value | Routing |
| --------- | ---------------- |
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R |
| `06`–`08` | Out 3: L, L+R, R |
| `09`–`0B` | USB 1: L, L+R, R |
| `0C`–`0E` | USB 2: L, L+R, R |
| `0F`–`11` | USB 3: L, L+R, R |

Part 1: `00` = Out 1 L, `03` = Out 2 L confirmed.

##### Transpose

**−48..+48** semitones; adds to the Single transpose. `stored = ui + 64`
(center `0x40` = 0); UI −48..+48 → `0x10..0x70`; Parts 1 and 3 confirmed.

##### Detune

**−64..+63**. `0x89 + part` with
`stored = ui + 64`: Part 1 (`0x89`) and Part 8 (`0x90`) verified across
min/max captures; Part 16 fully verified (`0x98`: `0x00` = −64, `0x40` =
+0, `0x7F` = +63).

##### Priority

Low / High — note stealing when voices are exhausted. Low: no `+0x20`;
High: **`+0x20`** (`0x41`→`0x61` with Hold off); Part 1 and Part 16
(`0x108`: `0x45`→`0x65` at INIT defaults).

##### Init Volume

Off, **1–127** — MIDI volume (CC#7) when the Multi is selected. Parts
**1–16** at **`0xA9..0xB8`**; UI direct; P1 at **`0xA9`** (UI `64` →
`0x40`); P16 at **`0xB8`**.

##### Low Key

**C−2..G8** — part low note limit (inverted range = outside range
enabled). Part 1 at `0x59` confirmed.

##### High Key

**C−2..G8** — part high note limit (inverted range = outside range
enabled). Part 1 at `0x69` confirmed.

##### Hold Pedal

Disabled / Enabled — MIDI CC#64 (sustain). Off: **`-0x04`** → `0x41`; On
(INIT): `0x45` (Part 1; Part 16 at `0x108` same delta).

##### Volume RX

Disabled / Enabled — receive MIDI CC#7. **`+2`** when enabled
(`0x45`→`0x47` at INIT); Part 1 and Part 16 (`0x108`).

##### Program Change

Disabled / Enabled — part responds to MIDI Program Change; CONFIG
“Program Change” global is ignored for parts. Off: **`-0x40`** → `0x05`;
On (INIT): `0x45` (Part 1; Part 16 at `0x108` same delta).

### Part bank index

One byte per part (`0x29..0x38`) in **every** Multi Dump. **Formula:** RAM
A–D = `0x00`–`0x03`; ROM *letter* = `0x04 + (letter - 'A')` for ROM A–Z.

| Index | Bank |
| ----------- | ----- |
| `0x00` | RAM A |
| `0x01` | RAM B |
| `0x02` | RAM C |
| `0x03` | RAM D |
| `0x04` | ROM A |
| `0x05` | ROM B |
| … | … |
| `0x0B` (11) | ROM H |
| … | … |
| `0x10` (16) | ROM M |
| … | … |
| `0x1D` (29) | ROM Z |

Program number at **`0x39 + (part−1)`**: direct `0x00`–`0x7F` (LCD program =
stored byte); same for all multi bank slots.

### Message-level structure

- `REQUEST_MULTI` message length: 11 bytes
- Multi Dump message length: 267 bytes
- Multi Dump command: `0x11`
- `REQUEST_MULTI` command: `0x31`
- Slots **1–16** export: one Multi Dump + 16 Single Dump messages
- Slots **17–128** (and typical bank requests): one Multi Dump only

### `REQUEST_MULTI` byte table

| Offset | Bytes | Meaning | Value range / notes |
| ------------ | ----------- | ------------------------ | -------------------------------------------------------------------------------- |
| `0x00` | `F0` | SysEx start | Fixed |
| `0x01..0x03` | `00 20 33` | Access manufacturer ID | Fixed |
| `0x04` | `01` | Virus family marker | Fixed in observed messages |
| `0x05` | `device_id` | Device ID | `00` observed |
| `0x06` | `31` | Request Multi command | Fixed for `REQUEST_MULTI` |
| `0x07` | `bank` | Multi bank selector | **`00`** + slot **`7F`** = edit buffer; **`01`** + slot = Multi bank |
| `0x08` | `slot` | Multi slot/program index | **`0x01`–`0x7F`** = Multi bank slots **1–127** (slot *N* → byte *N*) |
| `0x09` | `checksum` | Checksum byte | **`0x7C`** for edit buffer only (see below); **omitted** on stored-slot requests |
| `0x0A` | `F7` | SysEx end | Fixed (stored slot: message may be **10 bytes**, no checksum) |

**Edit buffer request** (Virus TI, confirmed): body
`00 20 33 01 00 31 00 7F 7C` → 267-byte Multi Dump with `00 7F` echoed at
`0x07`–`0x08`. Checksum on bytes `0x01..0x08` (manufacturer through slot):
`checksum = (128 - (sum(bytes) & 0x7F)) & 0x7F` → **`0x7C`** for `00 7F`.

```bash
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 31 00 7f 7c
```

**Stored Multi bank request** (confirmed): bank **`01`**,
slot = **slot number** as one byte (`1`→`0x01`, `9`→`0x09`, `48`→`0x30`).
**No checksum byte** before `F7` (10-byte message).

```bash
# Slot 9
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 31 01 09
# Slot 48
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 31 01 30
```

Reply: 267-byte Multi Dump with `0x07`/`0x08` echoing **`01`** / slot byte.
All slots use the same **`0x29..0x38`** (bank) and **`0x39..0x48`**
(program) layout (examples below).

### Multi bank slot examples (Multi Dump only)

Captured via `REQUEST_MULTI` bank **`01`** (267-byte reply only; slots
**1–16** may also stream sixteen Single Dump on full export):

| Slot | Name (example) | Bank bytes (16 parts) | Program bytes (notes) |
| ---- | -------------- | --------------------- | --------------------- |
| 1 | `RC1` | all `0x00` (RAM A) | varied per part |
| 9 | `Init Multi` | all `0x00` | `0x00..0x0F` per part |
| 16 | `Ref-Multi1` | all `0x00` | `0x00..0x0F` per part |
| 17 | `Ref2` | mixed (RAM/ROM) | mixed per part |
| 48 | `Multi` | all `0x00` | `0x00..0x0F` per part |

### Multi Dump byte table (267 bytes)

| Offset | Bytes | Meaning | Value range / notes |
| ------------- | ----------- | ------------------------ | --------------------------------- |
| `0x00` | `F0` | SysEx start | Fixed |
| `0x01..0x03` | `00 20 33` | Access manufacturer ID | Fixed |
| `0x04` | `01` | Virus family marker | Fixed in observed messages |
| `0x05` | `device_id` | Device ID | `00` observed |
| `0x06` | `11` | Dump Multi command | Fixed for Multi Dump |
| `0x07` | `bank` | Multi bank selector | Echoes request bank |
| `0x08` | `slot` | Multi slot/program index | Echoes request slot |
| `0x09..0x108` | payload | Multi payload bytes | 256-byte payload block |
| `0x109` | checksum | Checksum byte | Changes with payload |
| `0x10A` | `F7` | SysEx end | Fixed |

### Confirmed payload fields (offsets in full 267-byte Multi Dump)

| Offset(s) | Field | Encoding | Supported values |
| ------------- | ------------------------------ | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `0x0D..0x16` | Multi name | 10 × ASCII | `"INIT MULTI"` or `"Init Mult4"`; panel truncates/pads to 10 chars |
| `0x17` | Name terminator | `0x00` | Null after name field |
| `0x18` | Master Clock Tempo | `stored = bpm - 63` | UI `63..190` → `0x00..0x7F`; default **`0x39`** (120 bpm) |
| `0x29..0x38` | Part bank (16 bytes) | Sequential bank index | See [Part bank index](#part-bank-index); Parts 2–16 `0x00` in captures |
| `0x39..0x48` | Part program (16 bytes) | Direct `0..127` | Part 1 at `0x39`: UI `64` → `0x40`, UI `65` → `0x41`; Parts 2–16 often `0x7F` in baseline |
| `0x49..0x58` | Part MIDI channels (16 bytes) | Zero-based channel index | `0x00..0x0F` -> MIDI channels `1..16` |
| `0x59..0x68` | Part low key (16 bytes) | Direct 7-bit note value | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x59` confirmed) |
| `0x69..0x78` | Part high key (16 bytes) | Direct 7-bit note value | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x69` confirmed) |
| `0x79..0x88` | Part transpose (16 bytes) | Bipolar centered at `0x40` | UI −48..+48 → `stored = ui + 64` (`0x10`..`0x70`); `0x40` = 0; Part 1 at `0x79` |
| `0x89..0x98` | Part detune (16 bytes) | Bipolar centered at `0x40` | `0x00..0x7F` -> UI `-64..+63` (`stored = ui + 64`); Part 1 at `0x89`, Part 8 at `0x90`, Part 16 at `0x98` (`00/40/7F`) |
| `0x99..0xA8` | Part volume (16 bytes) | Bipolar centered at `0x40` | Parts **1–16**; `stored = ui + 64`; P1 at `0x99`, P16 at `0xA8` (`+46`→`0x6E`) |
| `0xA9..0xB8` | Part Init Volume (16 bytes) | Direct 7-bit | Parts **1–16**; P1 at **`0xA9`** (UI `64`→`0x40`); P16 at **`0xB8`** |
| `0xB9..0xC7` | *(unmapped)* | — | All `0x00` in current captures |
| `0xC8..0xD7` | Part output routing (16 bytes) | Per-part enum (see [Output](#output)) | P1: `00`–`03` confirmed; `06`–`08` = Out 3 L/L+R/R |
| `0xD8..0xE7` | Part panorama (16 bytes) | Direct `0..127` | Part 1 at `0xD8`: `0x00` = Off, `0x40` = Center |
| `0xE8..0xF7` | *(unmapped)* | — | All `0x00` in captures |
| `0xF8..0x107` | Part packed flags (16 bytes) | Packed flags | `0x44` Off; `0x45` On + defaults; Part 1 at **`0xF9`**, Part 16 at **`0x108`** |

### Packed flags at `0xF8 + part`

Several Edit Multi booleans share one byte per part (**1-based** part
index: Part 1 = `0xF9`, Part 16 = `0x108`). **Diff from INIT** (`0x45`)
when possible; other flags must be at defaults or confirmed on the panel.

**INIT MULTI defaults** (`0x45` = `0b01000101`):

| Mask | Meaning when set | INIT state |
| ------ | ---------------- | ---------- |
| `0x01` | Part enabled | On |
| `0x02` | Volume RX | Off |
| `0x04` | Hold Pedal | On |
| `0x20` | Priority High | Off (Low) |
| `0x40` | Program Change | On |

| Toggle | Delta from `0x45` | Example (Part 1 / Part 16) |
| ------------------------ | ----------------- | -------------------------------- |
| Enable off | `-0x01` | `0x44` (P8 `0x100`, P16 `0x108`) |
| Default On | — | `0x45` / `0x45` at `0x108` |
| Program Change off | `-0x40` | `0x05` / `0x05` at `0x108` |
| Hold Pedal off | `-0x04` | `0x41` / `0x41` at `0x108` |
| Volume RX on | `+0x02` | `0x47` / `0x47` at `0x108` |
| Priority High | `+0x20` | `0x65` at `0x108` (Hold on) |
| Priority High (Hold off) | `+0x20` | `0x41` → `0x61` |

Part 16 sweep (reset multi, INIT defaults, one toggle each): clean
single-byte diffs at **`0x108`** only (+ `0x0A` and checksum). Re-baseline
from INIT before flag diffs if Priority High was left on (`0x65` at
`0x108`).

Several booleans share one byte; **`0x61` is not unique** (Priority High
with Hold off). Diff from INIT (`0x45`) when toggling one flag.

### Runtime-only Edit Multi

These panel / host controls have live SysEx (where documented) but **no**
byte in **Multi Dump** — confirmed by edit → re-dump
diffs (INIT MULTI baseline):

| Control | Live edit | In Multi Dump |
| -------------------- | ---------------------- | --------------- |
| Secondary Output | `73` / `0x2D` | **No** |
| Bend Up / Down | `71` / `0x1A`, `0x1B` | **No** (in Single Dump for the part Single) |
| Direct Monitoring | VC **Live** (VC-only) | **No** |

Do not assign these to unmapped payload offsets below.

### Unmapped payload

All **dump-resident** Edit Multi fields are mapped above except **Keyboard to
MIDI** (desktop: identical enable/disable dumps). Remaining bytes are
metadata or unknown storage — **not** Secondary Output, Multi bend limits, or
Direct Monitoring.

| Offset(s) | INIT MULTI (typical) | Notes |
| ------------ | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0x09..0x0C` | `02 00 00 20` | Payload header; `0x0A` toggles on edit |
| `0x19..0x28` | `01 3C 00 10 00 01 01 00 40 40 40 40 40 0F 40 40` | 16 bytes between tempo and bank; `0x26` = edited part (`00`–`0F`); remainder **uninterpreted** — see [slot 32 INIT](#init-multi-slot-32-reference) |
| `0xB9..0xC7` | **15 × `0x00`** | Between Init Volume and Output — candidate for Keyboard to MIDI |
| `0xE8..0xF7` | **16 × `0x00`** | Between Pan and flags — candidate for Keyboard to MIDI |

Elimination captures confirmed **`0xB9..0xC7`** and **`0xE8..0xF7`** do
not hold Pan, Output, Enable, or Master Clock.

**Hardware correlation (edit buffer, INIT MULTI):** live edits for **Bend
Up/Down**, **Secondary Output**, **Direct Monitoring** (where available), and
**Keyboard** (`0x72`, `0x40`) produced **identical** Multi Dump vs
baseline — none of the unmapped regions changed. These settings are
**runtime-only** on the desktop module (or stored outside this 267-byte
block). Global **`0x73`** settings (e.g. All Delays `0x1B`) also did not
alter the multi dump.

**Keyboard to MIDI** cannot be probed on the desktop module (enable/disable
dumps are identical). On **TI Keyboard / Polar**, toggle Edit Multi
**Keyboard to MIDI** and dump. CONFIG **Local** / **Mode** are separate
globals — see [global.md](../live-edit/global.md).

#### INIT MULTI slot 32 reference

Stored **`REQUEST_MULTI`** bank **`01`** slot **`0x20`** (slot 32), full
267-byte message (checksum `0x42`). Name is null-terminated at **`0x17`**;
Master Clock tempo at **`0x18`** (`0x39` = 120 bpm).

Unmapped block **`0x19..0x28`** (16 bytes):

```text
01 3C 00 10 00 01 01 00 40 40 40 40 40 0F 40 40
```

Notable: **`0x26`** = `0x0F` (edited-part index, Part 16). Remaining
non-zero bytes (`0x3C`, `0x10`, six × `0x40`) are **uninterpreted** — not
yet tied to Edit Multi or **`0x73`** globals.

### Notes

- Offsets above are in the full SysEx message
 (including `F0` at offset `0x00`).
- The same fields can also be expressed as payload-relative offsets
 by subtracting `0x09`.
