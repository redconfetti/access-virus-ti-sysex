# Multis Dump

Multi mode on the Virus TI: program types, **Edit Multi** parameters, and
byte-level `DUMP_MULTI` mapping.

Live-edit traffic (`cmd=0x72`) is documented in
[multis-live-edit.md](multis-live-edit.md).

## Multi Dump

### Virus TI multis

The TI adds a **Multi bank** (128 slots). Slots **1–16** are
**embedded multis** (multi settings plus all 16 Singles). From OS **1.1**,
slots **17–128** are **reference multis** (multi settings plus
bank/program per part only). See
[virus.md](virus.md#multi-bank-ti-series).

Both types share the same **267-byte** `DUMP_MULTI` multi-settings block;
embedded programs additionally include sixteen `DUMP_SINGLE` messages
when exported as an **arrangement**.

### Edit Multi parameters

**Official parameter list for this project.** Fields match the **Virus TI
Edit Multi** screen (TI manual). They are the target set for mapping
the 256-byte multi payload inside `DUMP_MULTI`.

Dump offsets and confirmed deltas are in
[Multi parameter map](#multi-parameter-map) and
[Confirmed payload fields](#confirmed-payload-fields-offsets-in-full-267-byte-dump_multi).

### Global

- **Multi Program Name**
- **Master Clock Tempo:** 63–190 bpm — tempo for all parts in the Multi,
overriding Single-program Master Clock settings
- **Keyboard to MIDI:** Disabled / Enabled — whether keyboard notes are
  **also sent to MIDI OUT** (Edit Multi global; **not** the same as
  CONFIG **Local** or **Mode** — [keyboard settings](multis-live-edit.md#keyboard-settings-ti-keyboard--polar)).
  **TI Keyboard and Polar** on the panel; desktop module has no keyboard.
  Live `0x72` param `0x40` exists (AURA); dump byte **not confirmed** on
  desktop (identical enable/disable dumps).

### Part

- **Part Enable:** On/Off
- **Bank** — reference multis: bank from which a Single is copied into the part
- **Program:** 0–127 — reference multis: program number to copy into the part
- **Volume:** −64 to +63 — balance between parts (AURA: **Part Level**)
- **Panorama:** −64 to +63 — overrides the Single pan
- **MIDI Channel:** 1–16
- **Output:** Out 1 L … Out 3 R on **Virus Edit Multi** (analog only);
  full protocol also includes USB 1–3 (`09`–`11`) — see
  [Output enum](multis-live-edit.md#part-output-routing-enum-0x29)
- **Transpose:** −48 to +48 semitones — adds to the Single transpose
- **Detune:** −64 to +63
- **Priority:** Low / High — note stealing when voices are exhausted
- **Init Volume:** Off, 1–127 — MIDI volume (CC#7) when the Multi is selected
- **Low Key / High Key:** C−2 to G8 — part note range (inverted range =
  outside range enabled)
- **Hold Pedal:** Disabled / Enabled — MIDI CC#64 (sustain)
- **Volume RX:** Disabled / Enabled — MIDI CC#7
- **Program Change:** Disabled / Enabled — part responds to MIDI
  Program Change; CONFIG “Program Change” global is ignored for parts

### `DUMP_MULTI` byte reference

Byte reference for Virus TI/TI2 Multi SysEx messages (`DUMP_MULTI`, 267
bytes). Everything below maps **Edit Multi** fields to **stored** multi
dumps.

**Live edits** (`cmd=0x72`) are documented in [multis-live-edit.md](multis-live-edit.md).
Single-edit notes (`cmd=0x6E`, `cmd=0x10`) are in
[single-live-edit.md](single-live-edit.md). Prefer **Virus LCD changes +
hardware `DUMP_MULTI`** for mapping; paste captures in chat and record
deltas here.

### Multi parameter map

Live param IDs are in [multis-live-edit.md](multis-live-edit.md).

#### Summary

| Parameter (TI Edit Multi) | Dump offset               | Live param |
| ------------------------- | ------------------------- | ---------- |
| Multi Program Name        | `0x0D..`                  | —          |
| Master Clock Tempo        | `0x17`                    | `0x0F`     |
| Keyboard to MIDI          | **Not in dump** (desktop) | `0x40`     |
| Part Enable               | `0xF8 + part`             | `0x48`     |
| Bank (reference multi)    | `0x29 + part`             | TBD        |
| Program (reference multi) | `0x39 + part`             | TBD        |
| Volume                    | `0x99 + (part−1)`         | `0x27`     |
| Panorama                  | `0xD8 + part`             | `0x2B`     |
| MIDI Channel              | `0x49 + part`             | —          |
| Output                    | `0xC8 + part`             | `0x29`     |
| Transpose                 | `0x79 + part`             | `0x25`     |
| Detune                    | `0x89 + part`             | `0x26`     |
| Priority                  | `0xF8 + part` (flag)      | `0x4D`     |
| Init Volume               | `0xA9 + (part−1)`         | `0x28`     |
| Low Key                   | `0x59 + part`             | `0x23`     |
| High Key                  | `0x69 + part`             | `0x24`     |
| Hold Pedal                | `0xF8 + part` (flag)      | `0x4A`     |
| Volume RX                 | `0xF8 + part` (flag)      | `0x49`     |
| Program Change            | `0xF8 + part` (flag)      | `0x4E`     |

#### Parameters

##### Multi Program Name

Dump confirmed.

##### Master Clock Tempo

`stored = bpm - 63` (`120`→`0x39`, `124`→`0x3D`); Virus clean baseline.

##### Keyboard to MIDI

Edit Multi field; distinct from CONFIG **Local** / **Mode**; live `0x40`
target **unverified** (AURA “kbd local”).

##### Part Enable

Bit **`0x01`**: `0x44` off / `0x45` on at INIT (`±0x01` from the other
state). Virus Part 8 at **`0x100`** (`0x45`→`0x44`); Part 16 at **`0x108`**
(`0x45`→`0x44`, checksum unchanged `0x20`); live `72 0F 48 00/01`.

##### Bank (reference multi)

Sequential index; full table below; Virus Part 1.

##### Program (reference multi)

`0x00..0x7F` direct; Virus Part 1.

##### Volume

Parts **1–16** at `0x99..0xA8`; `stored = ui + 64`; P1 at `0x99`, P16 at
`0xA8` (e.g. UI `+46` → `0x6E`).

##### Panorama

Dump + live confirmed; Part 1 at `0xD8` (Virus).

##### MIDI Channel

Dump confirmed.

##### Output

`0xC8..0xD7`; P1: `00`=Out 1 L, `03`=Out 2 L (Virus + live `72 00 29 03`).

##### Transpose

`stored = ui + 64` (center `0x40` = 0); UI −48..+48 → `0x10..0x70`;
Virus P1, P3.

##### Detune

Dump + live confirmed. `0x89 + part` with `stored = ui + 64`:
Part 1 (`0x89`) and Part 8 (`0x90`) verified across min/max captures;
Part 16 fully verified (`0x98`: `0x00` = −64, `0x40` = +0, `0x7F` = +63).

##### Priority

Low: no `+0x20`; High: **`+0x20`** (`0x41`→`0x61` with Hold off);
Virus Part 1 and Part 16 (`0x108`: `0x45`→`0x65` at INIT defaults).

##### Init Volume

Parts **1–16** at **`0xA9..0xB8`**; UI direct; P1 at **`0xA9`** (UI `64` →
`0x40`); P16 at **`0xB8`** (`Off`→`0x00`, `1`→`0x01`, `64`→`0x40`); live
`0x28` and dump values align.

##### Low Key

Dump + live confirmed (Part 1).

##### High Key

Dump + live confirmed (Part 1).

##### Hold Pedal

Off: **`-0x04`** → `0x41`; On (INIT): `0x45` (AURA + Virus Part 1;
Part 16 at `0x108` same delta).

##### Volume RX

**`+2`** when enabled (`0x45`→`0x47` at INIT); Virus Part 1 and Part 16
(`0x108`); AURA couples RX off when Init Vol → 0.

##### Program Change

Off: **`-0x40`** → `0x05`; On (INIT): `0x45` (AURA + Virus Part 1;
Part 16 at `0x108` same delta).

### Part bank index (`0x29 + part`)

One byte per part (`0x29..0x38`). **Formula:** RAM A–D = `0x00`–`0x03`;
ROM *letter* = `0x04 + (letter - 'A')` for ROM A–Z.

| Index       | Bank  | Confirmed |
| ----------- | ----- | --------- |
| `0x00`      | RAM A | ✓         |
| `0x01`      | RAM B | ✓         |
| `0x02`      | RAM C | inferred  |
| `0x03`      | RAM D | ✓         |
| `0x04`      | ROM A | ✓         |
| `0x05`      | ROM B | inferred  |
| …           | …     |           |
| `0x0B` (11) | ROM H | ✓         |
| …           | …     |           |
| `0x10` (16) | ROM M | ✓         |
| …           | …     |           |
| `0x1D` (29) | ROM Z | ✓         |

Program number at `0x39 + part`: direct `0x00`–`0x7F` (UI program = stored byte).

### Message-level structure

- `REQUEST_MULTI` message length: 11 bytes
- `DUMP_MULTI` message length: 267 bytes
- `DUMP_MULTI` command: `0x11`
- `REQUEST_MULTI` command: `0x31`
- Reference-style transfer: one `DUMP_MULTI` only
- Arrangement-style transfer: one `DUMP_MULTI` + 16 `DUMP_SINGLE` messages

### `REQUEST_MULTI` byte table

| Offset       | Bytes       | Meaning                  | Value range / notes                 |
| ------------ | ----------- | ------------------------ | ----------------------------------- |
| `0x00`       | `F0`        | SysEx start              | Fixed                               |
| `0x01..0x03` | `00 20 33`  | Access manufacturer ID   | Fixed                               |
| `0x04`       | `01`        | Virus family marker      | Fixed in observed TI/TI2 messages   |
| `0x05`       | `device_id` | Device ID                | `00` observed                       |
| `0x06`       | `31`        | Request Multi command    | Fixed for `REQUEST_MULTI`           |
| `0x07`       | `bank`      | Multi bank selector      | **`00 7F`** = Multi **edit buffer** (Virus); `01 00` = stored slot |
| `0x08`       | `slot`      | Multi slot/program index | `00..7F` (confirmed)                |
| `0x09`       | `checksum`  | Checksum byte            | **`0x7C`** for edit-buffer request (see below) |
| `0x0A`       | `F7`        | SysEx end                | Fixed                               |

**Edit buffer request** (Virus TI, confirmed): body
`00 20 33 01 00 31 00 7F 7C` → 267-byte `DUMP_MULTI` with `00 7F` echoed at
`0x07`–`0x08`. Checksum on bytes `0x01..0x08` (manufacturer through slot):
`checksum = (128 - (sum(bytes) & 0x7F)) & 0x7F` → **`0x7C`** for `00 7F`.

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 31 00 7f 7c
```

### `DUMP_MULTI` byte table (267 bytes)

| Offset        | Bytes       | Meaning                  | Value range / notes               |
| ------------- | ----------- | ------------------------ | --------------------------------- |
| `0x00`        | `F0`        | SysEx start              | Fixed                             |
| `0x01..0x03`  | `00 20 33`  | Access manufacturer ID   | Fixed                             |
| `0x04`        | `01`        | Virus family marker      | Fixed in observed TI/TI2 messages |
| `0x05`        | `device_id` | Device ID                | `00` observed                     |
| `0x06`        | `11`        | Dump Multi command       | Fixed for `DUMP_MULTI`            |
| `0x07`        | `bank`      | Multi bank selector      | Echoes request bank               |
| `0x08`        | `slot`      | Multi slot/program index | Echoes request slot               |
| `0x09..0x108` | payload     | Multi payload bytes      | 256-byte payload block            |
| `0x109`       | checksum    | Checksum byte            | Changes with payload              |
| `0x10A`       | `F7`        | SysEx end                | Fixed                             |

### Capture baseline

Working baseline for dump diffs: **INIT MULTI, all parts enabled**
(`0xF8..0x107` = `0x45`), exported from AURA. Part enable:
`0x45` = On, `0x44` = Off at **`0xF8 + part`** (Part 1, Virus).

AURA persistence issues: see [aura-bugs.md](aura-bugs.md).
When AURA does not save a field, capture dumps from the Virus
after editing on hardware.

**Virus vs AURA header noise** (ignore when diffing against an AURA
INIT baseline): `0x08` slot (`0x00` AURA / `0x7F` Virus panel), `0x0C`,
`0x26` (edited-part context).

When a diff shows **more than one payload byte** changed for a single
parameter edit — or any change that does not match what we expect for
that parameter — **stop and ask**:

1. **Confirm panel state** for the unexpected byte(s) (e.g. Hold Pedal,
   Priority, Prog Change, Output — especially anything touching
   **`0xF8` flags**).
2. **Re-capture** after loading a known baseline (INIT MULTI) and
   changing **only** the target parameter.

Do not document ambiguous offsets until a clean one-parameter diff is
confirmed. Known pitfalls: packed flags at **`0xF8 + part`** (several
settings share one byte; `0x61` is not unique), and Virus header bytes
listed above.

### Confirmed payload fields (offsets in full 267-byte `DUMP_MULTI`)

| Offset(s)     | Field                           | Encoding                                                         | Supported values                                                                                                                                                      |
| ------------- | ------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0x0D..0x16`  | Multi name                      | ASCII + `0x00`                                                   | `"INIT MULTI"` + null; tempo follows at **`0x17`**                                                                                                                    |
| `0x17`        | Master Clock Tempo              | `stored = bpm - 63`                                              | UI `63..190` → `0x00..0x7F`; default **`0x39`** (120 bpm); live param `0x0F`                                                                                          |
| `0x29..0x38`  | Part bank (16 bytes)            | Sequential bank index                                            | See [Part bank index](#part-bank-index-0x29--part); Parts 2–16 `0x00` in captures                                                                                     |
| `0x39..0x48`  | Part program (16 bytes)         | Direct `0..127`                                                  | Part 1 at `0x39`: UI `64` → `0x40`, UI `65` → `0x41`; Parts 2–16 often `0x7F` in baseline                                                                             |
| `0x49..0x58`  | Part MIDI channels (16 bytes)   | Zero-based channel index                                         | `0x00..0x0F` -> MIDI channels `1..16`                                                                                                                                 |
| `0x59..0x68`  | Part low key (16 bytes)         | Direct 7-bit note value                                          | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x59` confirmed); live param `0x23`                                                                                              |
| `0x69..0x78`  | Part high key (16 bytes)        | Direct 7-bit note value                                          | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x69` confirmed); live param `0x24`                                                                                              |
| `0x79..0x88`  | Part transpose (16 bytes)       | Bipolar centered at `0x40`                                       | UI −48..+48 → `stored = ui + 64` (`0x10`..`0x70`); `0x40` = 0; Part 1 at `0x79`; live `0x25` uses **different** encoding — [multis-live-edit.md](multis-live-edit.md) |
| `0x89..0x98`  | Part detune (16 bytes)          | Bipolar centered at `0x40`                                       | `0x00..0x7F` -> UI `-64..+63` (`stored = ui + 64`); Part 1 confirmed at `0x89`, Part 2 at `0x8A`, Part 8 at `0x90`, Part 16 full set at `0x98` (`00/40/7F`)           |
| `0x99..0xA8`  | Part volume (16 bytes)          | Bipolar centered at `0x40`                                       | Parts **1–16**; `stored = ui + 64`; P1 at `0x99`, P16 at `0xA8` (`+46`→`0x6E`)                                                                                        |
| `0xA9..0xB8`  | Part Init Volume (16 bytes)     | Direct 7-bit                                                     | Parts **1–16**; P1 at **`0xA9`** (UI `64`→`0x40`); P16 at **`0xB8`**                                                                                                  |
| `0xB9..0xC7`  | *(unmapped)*                    | —                                                                | All `0x00` in current captures                                                                                                                                        |
| `0xC8..0xD7`  | Part output routing (16 bytes)  | [Output enum](multis-live-edit.md#part-output-routing-enum-0x29) | Same bytes as live `0x29`; P1: `00`–`03` dump confirmed; `06`–`08` Out 3 live (Virus)                                                                                 |
| `0xD8..0xE7`  | Part panorama (16 bytes)        | Direct `0..127`                                                  | Part 1 at `0xD8`: `0x00` = Off, `0x40` = Center                                                                                                                       |
| `0xE8..0xF7`  | *(unmapped)*                    | —                                                                | All `0x00` in captures                                                                                                                                                |
| `0xF8..0x107` | Part packed flags (16 bytes)    | Packed flags                                                     | `0x44` Off; `0x45` On + defaults; live `0x48`; Part 1 at **`0xF9`**, Part 16 at **`0x108`**                                                                           |

### Packed flags at `0xF8 + part`

Several Edit Multi booleans share one byte per part (**1-based** part
index: Part 1 = `0xF9`, Part 16 = `0x108`). **Diff from INIT** (`0x45`)
when possible; other flags must be at defaults or confirmed on the panel.

**INIT MULTI defaults** (`0x45` = `0b01000101`):

| Mask   | Meaning when set        | INIT state |
| ------ | ----------------------- | ---------- |
| `0x01` | Part enabled            | On         |
| `0x02` | Volume RX               | Off        |
| `0x04` | Hold Pedal              | On         |
| `0x20` | Priority High           | Off (Low)  |
| `0x40` | Program Change          | On         |

| Toggle                           | Delta from `0x45` | Example (Part 1 / Part 16) | Source   |
| -------------------------------- | ----------------- | ---------------------------- | -------- |
| Part Enable off                  | `-0x01`           | `0x44` (P8 `0x100`, P16 `0x108`) | AURA + Virus |
| Default On                       | —                 | `0x45` / `0x45` at `0x108`   | AURA + Virus |
| Program Change off               | `-0x40`           | `0x05` / `0x05` at `0x108`   | AURA + Virus |
| Hold Pedal off                   | `-0x04`           | `0x41` / `0x41` at `0x108`   | AURA + Virus |
| Volume RX on                     | `+0x02`           | `0x47` / `0x47` at `0x108`   | AURA + Virus |
| Priority High                    | `+0x20`           | `0x65` at `0x108` (Hold on)  | Virus    |
| Priority High (Hold off)         | `+0x20`           | `0x41` → `0x61`              | Virus P1 |

Part 16 sweep (reset multi, INIT defaults, one toggle each): clean
single-byte diffs at **`0x108`** only (+ `0x0A` header noise and checksum).
Live: `72 0F` + `48`/`49`/`4A`/`4E`/`4D` + `00`/`01`. Re-baseline from
INIT before flag diffs if Priority High was left on (`0x65` at `0x108`).

Earlier Virus Prog Change captures (`0x21` / `0x61`) likely had
**Hold / Priority not at INIT** — use table above.

### Unmapped payload (elimination)

**Hypothesis:** `DUMP_MULTI` may reserve a byte for **Keyboard to MIDI**
(per-multi on keyboard models). The **desktop module** may ignore it on
save/export, so live `0x72` / `0x40` does not change a Virus-requested
dump. CONFIG **Local** / **Mode** are separate globals and are unlikely
to live in the same byte without keyboard-hardware captures.

**Unmapped regions** in the 256-byte payload
(everything else is assigned in the table above):

| Offset(s)    | INIT MULTI (typical)                | Notes                                                               |
| ------------ | ----------------------------------- | ------------------------------------------------------------------- |
| `0x09..0x0C` | `02 00 00 20`                       | Message/payload header; `0x0A` toggles on edit                      |
| `0x19..0x28` | `01 3C 00 10 00 01 01 00` + 8 bytes | Between name/tempo and bank table; `0x26` = edited part (`00`–`0F`) |
| `0xB9..0xC7` | **15 × `0x00`**                     | Between **Init Volume** and **Output**                              |
| `0xE8..0xF7` | **16 × `0x00`**                     | Between **Pan** and **flags** (`0xF8..`)                            |

A **global** bool (**Keyboard to MIDI**, if stored on keyboard
hardware) would most likely be in **`0xB9..0xC7`** or **`0xE8`**
(`00` / `01`) in the remaining zero blocks.

### Elimination captures (Virus LCD → one change → dump)

Reload **INIT MULTI** first. Each row should move **only** the listed
offset(s); if a gap byte changes too, note it.

| Change                                         | Should touch                | Confirms gap           |
| ---------------------------------------------- | --------------------------- | ---------------------- |
| Part 1 **Pan** Off ↔ Center                    | `0xD8` only                 | `0xC8..0xD7` unchanged |
| Part 1 **Output** Out 1 L → Out 2 L            | `0xC8` only                 | `0xB9..0xC7` unchanged |
| Part 1 **Enable** Off                          | `0xF9` `45`→`44`            | `0xE8..0xF7` unchanged |
| **Master Clock** 120 → 124 bpm                 | `0x17` only (`0x39`→`0x3D`) | `0x19..0x28` unchanged |
| **Multi name** (one character)                 | `0x0D..`                    | Name block isolated    |

**Cannot eliminate Keyboard to MIDI on desktop** via dump
(enable/disable dumps are identical). On **TI Keyboard / Polar**:
toggle **Keyboard to MIDI** on Edit Multi and dump (vs CONFIG **Local**
/ **Mode** separately); compare **AURA export** vs hardware dump;
compare factory multis that differ only in keyboard-related behavior.

### Candidate / partially understood bytes

| Offset | Status    | Current interpretation                              |
| ------ | --------- | --------------------------------------------------- |
| `0x0A` | Candidate | Likely state/version/edit flag byte                 |
| `0x26` | Candidate | Likely selected/edited-part context or state marker |

### Dump capture notes

Single-parameter `DUMP_MULTI` diffs (Virus panel preferred).
Live `0x72` examples: [multis-live-edit.md](multis-live-edit.md).

- AURA INIT, Part 1 **Hold Pedal** off:
  only `0xF9` `0x45` → `0x41` + checksum.
- Virus Part 1 Hold Pedal on/off (panel):
  only `0xF9` `0x45` ↔ `0x41` + checksum (header `0x0A` may toggle).
- Virus Part 1 **Priority** Low vs High (Hold off):
  only `0xF9` `0x41` → `0x61` (`+0x20`) + checksum.
- AURA INIT, Part 1 **Prog Change** off/on:
  only `0xF9` `0x05` ↔ `0x45` (`±0x40`) + checksum.
- Virus Part 1 **Init Volume** 64:
  only **`0xA9`** `0x00` → `0x40` + checksum;
  **`0xF8` unchanged** (`0x45`).
- **Part 15 Init Vol** (Virus, clean baseline):
  only **`0xB7`** — `0x00` / `0x51` (81); checksum changes.
- AURA INIT, Part 1 **Init Volume** 64:
  `0xA9` `0x00` → `0x40`; `0xF9` `0x45` → `0x47` (`+2`) — AURA may
  couple Volume RX when Init Vol changes.
- Virus Part 1 **Init Volume** 37/127:
  **`0xA9`** `0x00` → `0x25` / `0x7F`; live `72 00 28 26/7E`.
- Virus Part 2 **Init Volume** 37/0:
  **`0xAA`** `0x00` ↔ `0x25`; live `72 01 28 25/00`.
- Virus Part 1 **Volume** +8 / +0:
  only **`0x99`** `0x40` ↔ `0x48`; live `72 00 27 40/48`.
- Virus Part 2 **Volume** +31:
  only **`0x9A`** `0x40` → `0x5F`; live `72 01 27 5F`.
- Virus Part 16 **Volume** +46 / +0:
  only **`0xA8`** `0x40` ↔ `0x6E`; live `72 0F 27 40/6E`.
- Virus Part 16 **Init Volume** Off / 1 / 64 / Off:
  only **`0xB8`** `0x00` ↔ `0x01` ↔ `0x40` ↔ `0x00`; live `72 0F 28
  00/01/40/00`; **`0xA8` unchanged** (Volume block separate).
- AURA **Part Level** at `0x99`:
  INIT `0x40`; UI `-64` → `0x00`; UI `+36` → `0x64`.
- Virus Part 1 **Program** 64→65: only `0x39` `0x40` → `0x41` + checksum.
- Virus Part 1 **Bank** RAM-A→RAM-B (P65):
  `0x29` `0x00` → `0x01`; `0x39` unchanged vs program-only diff.
- Virus bank index (P65):
  RAM D `0x03`, ROM A `0x04`, ROM Z `0x1D`;
  ROM H P66 `0x0B`/`0x42`; ROM M P127 `0x10`/`0x7F`.
- Virus **Master Clock** at **`0x17`**:
  120/`124` bpm → `0x39`/`0x3D`; only byte + checksum (clean baseline).
- Virus Prog Change captures (`0x21`/`0x61`) — **superseded** (mixed `0xF9` flags).
- **Reverb Send:** no `DUMP_MULTI` byte change in any capture; live-only —
  [single-live-edit.md#reverb-send-cmd0x6e](single-live-edit.md#reverb-send-cmd0x6e).
- Virus INIT MULTI, Part 1 **Transpose** only:
  `0x79` `0x40` (+0), `0x70` (+48), `0x10` (−48), `0x34` (−12);
  header `0x0A` often `0x01` when edited; Part 3 +48:
  `0x7B` `0x70`, `0x26` `0x02`.
- Virus Part 1 **Output** Out 1 L ↔ L+R ↔ R:
  `0xC8` `00` ↔ `01` ↔ `02` + checksum; live `72 00 29 00/01/02`.
- Virus Part 1 **Output** Out 3 L / L+R / R (Edit Multi menu):
  live `72 00 29 06` / `07` / `08` only (no dump captures in this session).
- Virus Part 1 **Pan** Off vs Center:
  only `0xD8` `00` ↔ `0x40` + checksum; `0xC8..0xD7` unchanged.
- Virus Part 1 **Enable** Off:
  only `0xF9` `0x45` → `0x44` + checksum; `0xE8..0xF7` unchanged.
- Virus INIT, Part 16 **Enable** Off:
  only `0x108` `0x45` → `0x44` (+ `0x0A`); checksum **unchanged** `0x20`.
- **Part 15 Init Vol** (`0xB7`) and **Part 16 Init Vol** (`0xB8`) are stored:
  P15 `81`→`0x51`; P16 `0/81/127`→`0x00/0x51/0x7F`; live `0x28`.
- **Keyboard / live `0x40`** (AURA “kbd local”, `72 00 40 00/01`):
  two `DUMP_MULTI` captures from **TI desktop module** —
  **identical** (no payload/checksum change). Does **not** prove whether
  `0x40` is **Keyboard to MIDI**, **Local**, or another keyboard global.

### AURA behavior: part enable sends `DUMP_SINGLE`

When a part track is disabled then re-enabled in AURA, a full
**524-byte** message is sent with `cmd=0x10` (`DUMP_SINGLE`).
This loads that part's single program into the synth
(multi-mode per-part edit buffer), not a multi dump.

| Offset       | Field         | Encoding                            | Confirmed                                                         |
| ------------ | ------------- | ----------------------------------- | ----------------------------------------------------------------- |
| `0x06`       | Command       | `0x10` = `DUMP_SINGLE`              | Yes                                                               |
| `0x08`       | Part index    | Zero-based                          | `0x00`..`0x0F` for Parts 1..16 (confirmed: 1, 2, 8, 9, 16)        |
| `0x09`       | Context byte  | Fixed `0x0C` in observed AURA loads | Yes                                                               |
| `0x0A..0x0B` | Context bytes | Two patterns observed               | Parts 1–2: `10 00`; Parts 8, 9, 16: `00 01`; arrangement: `01 00` |

Parts 1 vs 2, and Parts 8 vs 9, differ only in part index (`0x08`)
plus checksum and minor part-slot payload bytes.

Header bytes `0x0A..0x0B` split into two AURA patterns; meaning not yet mapped.

Arrangement-style exports use the same `DUMP_SINGLE` message type for
each of 16 parts after the multi header message; arrangement singles use
header pattern `00 <part> 0C 01 00`.

### Notes

- Offsets above are in the full SysEx message
  (including `F0` at offset `0x00`).
- The same fields can also be expressed as payload-relative offsets
  by subtracting `0x09`.
