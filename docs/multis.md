# Multis

Byte reference for Virus TI/TI2 Multi SysEx messages (`DUMP_MULTI`, 267 bytes).

**Official multi parameters:** Virus TI **Edit Multi** fields in [README.md](../README.md). Everything below maps those fields to **stored** multi dumps.

**Live edits** (`cmd=0x72`, `0x6E`, etc.) are documented in [live-sysex.md](live-sysex.md). Prefer **Virus LCD changes + hardware `DUMP_MULTI`** for mapping; use live traffic for param IDs only.

## Multi parameter map

Status of README fields in the 267-byte `DUMP_MULTI`. Live param IDs: [live-sysex.md](live-sysex.md).

| Parameter (TI Edit Multi) | Dump offset | Live param | Status |
|---|---|---|---|
| **Global** | | | |
| Multi Program Name | `0x0D..` | — | Dump confirmed |
| Master Clock Tempo | `0x17` | `0x0F` | `stored = bpm - 63` (`120`→`0x39`, `124`→`0x3D`); Virus clean baseline |
| Keyboard to MIDI | **Not in dump** | `0x40` | Global; live `part=00`; **not** in `DUMP_MULTI` on desktop (enable/disable dumps identical) |
| **Part** | | | |
| Part Enable | `0xF8 + part` | `0x48` | `0x44` off / `0x45` on at `0xF8` (Part 1, Virus) |
| Bank (reference multi) | `0x29 + part` | TBD | Sequential index; full table below; Virus Part 1 |
| Program (reference multi) | `0x39 + part` | TBD | `0x00..0x7F` direct; Virus Part 1 |
| Volume | `0x99 + (part−1)` | `0x27` | Parts **1–15** at `0x99..0xA7`; `stored = ui + 64`; Part 16 not stored |
| Panorama | `0xD8 + part` | `0x2B` | Dump + live confirmed; Part 1 at `0xD8` (Virus) |
| MIDI Channel | `0x49 + part` | — | Dump confirmed |
| Output | `0xB8 + part` | `0x29` | `0xB8..0xC7`; P1: `00`=Out 1 L, `03`=Out 2 L (Virus + live `72 00 29 03`) |
| Transpose | `0x79 + part` | `0x25` | `stored = ui + 64` (center `0x40` = 0); UI −48..+48 → `0x10..0x70`; Virus P1, P3 |
| Detune | `0x89 + part` | — | Dump confirmed (Parts 1–2) |
| Priority | `0xF8 + part` (flag) | `0x4D` | Low: no `+0x20`; High: **`+0x20`** (`0x41`→`0x61` with Hold off); Virus Part 1 |
| Init Volume | `0xA8 + (part−1)` | TBD | Parts **1–15** at **`0xA8..0xB6`**; UI direct; **`0xB7` unused**; Part **16** not stored |
| Low Key | `0x59 + part` | `0x23` | Dump + live confirmed (Part 1) |
| High Key | `0x69 + part` | `0x24` | Dump + live confirmed (Part 1) |
| Hold Pedal | `0xF8 + part` (flag) | `0x4A` | `0x41` off / `0x45` on (AURA + Virus, Part 1) |
| Volume RX | `0xF8 + part` (flag) | `0x49` | **`+2`** when enabled; Virus Part 1; AURA couples RX off when Init Vol → 0 |
| Program Change | `0xF8 + part` (flag) | `0x4E` | Off: **`-0x40`** → `0x05`; On: `0x45` (AURA INIT, Part 1) |

## Beyond Edit Multi

Controls that affect Multi mode but are **not** on the TI **Edit Multi** screen (or not in `DUMP_MULTI` yet). Mapping target remains the [README](../README.md) Edit Multi list above.

### Live / part-edit only

| Control | In `DUMP_MULTI`? | Notes |
|---|---|---|
| Reverb Send | **No** | [Live `0x6E`](live-sysex.md#reverb-send--not-in-multi-dump); part-edit buffer; captured via AURA only so far |
| Delay send (per part) | Not confirmed | May share Reverb encoding |

### CONFIG / device settings (not on Edit Multi)

Seen in **Multi / CONFIG** on TI; **not** found in the 267-byte multi payload (other message or unmapped):

- Global MIDI channel  
- Multi Program Change enable  
- Global Program Change enable  
- MIDI Clock receive / transmit  
- Soft Thru  

**Master Clock Tempo** *is* Edit Multi global and **is** in the dump at **`0x17`** (separate from MIDI Clock enable above).

### Shared Multi Delay (OS4 manual)

The **OS4** manual describes a **shared Multi Delay** block in the multi (not per-part), including:

Delay On/Off, Time, Feedback, Rate, Depth, Shape, Color, **Output Assignment**, Clock Division.

None of these offsets are confirmed in `DUMP_MULTI` yet. Capturing **Delay On** vs **Off** with all parts otherwise at INIT would be the first step.

### Effect Send vs Reverb Send (TI 5.1.7)

**Reverb Send** is live-only (`cmd=0x6E`, param `0x02`) — see [live-sysex.md](live-sysex.md). It has **not** appeared in any `DUMP_MULTI` diff. Older/OS4 docs may say “Effect Send”.

### Snow manual (secondary)

The Virus **Snow** manual lists a similar multi set plus vague **“Global routing settings”** and **Patch Volume** as a separate name — on TI, routing is per-part Output / Volume / Pan (all on Edit Multi and in the dump). Use Snow only as a cross-check, not as the project checklist.

### Part bank index (`0x29 + part`)

One byte per part (`0x29..0x38`). **Formula:** RAM A–D = `0x00`–`0x03`; ROM *letter* = `0x04 + (letter - 'A')` for ROM A–Z.

| Index | Bank | Confirmed |
|---:|---|:---:|
| `0x00` | RAM A | ✓ |
| `0x01` | RAM B | ✓ |
| `0x02` | RAM C | inferred |
| `0x03` | RAM D | ✓ |
| `0x04` | ROM A | ✓ |
| `0x05` | ROM B | inferred |
| … | … | |
| `0x0B` (11) | ROM H | ✓ |
| … | … | |
| `0x10` (16) | ROM M | ✓ |
| … | … | |
| `0x1D` (29) | ROM Z | ✓ |

Program number at `0x39 + part`: direct `0x00`–`0x7F` (UI program = stored byte).

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

## Capture baseline

Working baseline for dump diffs: **INIT MULTI, all parts enabled** (`0xF8..0x107` = `0x45`), exported from AURA. Part enable: `0x45` = On, `0x44` = Off at **`0xF8 + part`** (Part 1, Virus).

AURA persistence issues: see [aura-bugs.md](aura-bugs.md). When AURA does not save a field, capture dumps from the Virus after editing on hardware.

**Virus vs AURA header noise** (ignore when diffing against an AURA INIT baseline): `0x08` slot (`0x00` AURA / `0x7F` Virus panel), `0x0C`, `0x26` (edited-part context).

When a diff shows **more than one payload byte** changed for a single parameter edit — or any change that does not match what we expect for that parameter — **stop and ask**:

1. **Confirm panel state** for the unexpected byte(s) (e.g. Hold Pedal, Priority, Prog Change, Output — especially anything touching **`0xF8` flags**).
2. **Re-capture** after loading a known baseline (INIT MULTI) and changing **only** the target parameter.

Do not document ambiguous offsets until a clean one-parameter diff is confirmed. Known pitfalls: packed flags at **`0xF8 + part`** (several settings share one byte; `0x61` is not unique), and Virus header bytes listed above.

## Confirmed payload fields (offsets in full 267-byte `DUMP_MULTI`)

| Offset(s) | Field | Encoding | Supported values |
|---|---|---|---|
| `0x0D..0x16` | Multi name | ASCII + `0x00` | `"INIT MULTI"` + null; tempo follows at **`0x17`** |
| `0x17` | Master Clock Tempo | `stored = bpm - 63` | UI `63..190` → `0x00..0x7F`; default **`0x39`** (120 bpm); live param `0x0F` |
| `0x29..0x38` | Part bank (16 bytes) | Sequential bank index | See [Part bank index](#part-bank-index-0x29--part); Parts 2–16 `0x00` in captures |
| `0x39..0x48` | Part program (16 bytes) | Direct `0..127` | Part 1 at `0x39`: UI `64` → `0x40`, UI `65` → `0x41`; Parts 2–16 often `0x7F` in baseline |
| `0x49..0x58` | Part MIDI channels (16 bytes) | Zero-based channel index | `0x00..0x0F` -> MIDI channels `1..16` |
| `0x59..0x68` | Part low key (16 bytes) | Direct 7-bit note value | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x59` confirmed); live param `0x23` |
| `0x69..0x78` | Part high key (16 bytes) | Direct 7-bit note value | `0x00` = C1, `0x7F` = G9 (Part 1 at `0x69` confirmed); live param `0x24` |
| `0x79..0x88` | Part transpose (16 bytes) | Bipolar centered at `0x40` | UI −48..+48 → `stored = ui + 64` (`0x10`..`0x70`); `0x40` = 0; Part 1 at `0x79`; live `0x25` uses **different** encoding — [live-sysex.md](live-sysex.md) |
| `0x89..0x98` | Part detune (16 bytes) | Bipolar centered at `0x40` | `0x00..0x7F` -> UI `-64..+63` (`stored = ui + 64`); Part 1 confirmed at `0x89`, Part 2 confirmed at `0x8A` |
| `0x99..0xA7` | Part volume (**15** bytes) | Bipolar centered at `0x40` | Parts **1–15**; `stored = ui + 64`; Part 1 at `0x99`; Part 16 not stored |
| `0xA8..0xB6` | Part Init Volume (**15** bytes) | Direct 7-bit | Parts **1–15**; P1 at **`0xA8`** (`64`→`0x40`); P15 at **`0xB6`**; **`0xB7` unused**; Part 16 not stored |
| `0xB8..0xC7` | Part output routing (16 bytes) | [Output enum](live-sysex.md#part-output-routing-enum-0x29) | Part 1 at **`0xB8`**: `00` = Out 1 L, `03` = Out 2 L |
| `0xC8..0xD7` | *(unmapped)* | — | All `0x00` in captures |
| `0xD8..0xE7` | Part panorama (16 bytes) | Direct `0..127` | Part 1 at `0xD8`: `0x00` = Off, `0x40` = Center |
| `0xE8..0xF7` | *(unmapped)* | — | All `0x00` in captures |
| `0xF8..0x107` | Part packed flags (16 bytes) | Packed flags | `0x44` Off; `0x45` On + defaults; live `0x48` at **`0xF8`** (Part 1) |

### Packed flags at `0xF8 + part`

Several Edit Multi booleans share one byte. **Diff from INIT** (`0x45`) when possible; other flags must be at defaults or confirmed on the panel.

| Toggle | Delta from `0x45` | Example (`0xF8`, Part 1) | Source |
|---|---|---|---|
| Part Off | — | `0x44` | AURA + Virus |
| Default On | — | `0x45` | AURA INIT |
| Program Change off | `-0x40` | `0x05` | AURA INIT |
| Hold Pedal off | `-0x04` | `0x41` | AURA + Virus |
| Volume RX on and/or Init Vol ≠ 0 | `+0x02` | `0x47` (from `0x45`) | AURA; Virus P1 Init Vol **64** did **not** set `0xF8` +2 (Vol RX may be required) |
| Priority High | `+0x20` | `0x41` → `0x61` (Hold off) | Virus |

Earlier Virus Prog Change captures (`0x21` / `0x61`) likely had **Hold / Priority not at INIT** — use AURA pair above for Prog Change.

## Unmapped payload (elimination)

**Hypothesis:** `DUMP_MULTI` may reserve a byte for **Keyboard to MIDI** (and other globals); the **desktop module** ignores it on save/export, so live `0x72` / `0x40` does not change a Virus-requested dump.

**Unmapped regions** in the 256-byte payload (everything else is assigned in the table above):

| Offset(s) | INIT MULTI (typical) | Notes |
|---|---|---|
| `0x09..0x0C` | `02 00 00 20` | Message/payload header; `0x0A` toggles on edit |
| `0x19..0x28` | `01 3C 00 10 00 01 01 00` + 8 bytes | Between name/tempo and bank table; `0x26` = edited part (`00`–`0F`) |
| `0xC8..0xD7` | **16 × `0x00`** | Between **Output** and **Pan** |
| `0xE8..0xF7` | **16 × `0x00`** | Between **Pan** and **flags** (`0xF8..`) |

A **global** bool (Keyboard to MIDI) would most likely be **`0xC8`** or **`0xE8`** (`00` / `01`) in the remaining zero blocks.

### Elimination captures (Virus LCD → one change → dump)

Reload **INIT MULTI** first. Each row should move **only** the listed offset(s); if a gap byte changes too, note it.

| Change | Should touch | Confirms gap |
|---|---|---|
| Part 1 **Pan** Off ↔ Center | `0xD8` only | `0xC8..0xD7` unchanged |
| Part 1 **Output** Out 1 L → Out 2 L | `0xB8` only | `0xC8..0xD7` unchanged |
| Part 1 **Enable** Off | `0xF8` `45`→`44` | `0xE8..0xF7` unchanged |
| **Master Clock** 120 → 124 bpm | `0x17` only (`0x39`→`0x3D`) | `0x19..0x28` unchanged |
| **Multi name** (one character) | `0x0D..` | Name block isolated |
| **OS4 Multi Delay On** (if on CONFIG/multi UI) | TBD in `0xC9..` or `0x19..` | May share “zero” block |

**Cannot eliminate Keyboard to MIDI on desktop** via dump (enable/disable dumps are identical). Options: TI **Keyboard** panel toggle + dump; compare **AURA file export** vs Virus dump after kbd local (does AURA embed a byte the hardware omits?); compare two **factory** multis that differ only in keyboard-related behavior.

## Candidate / partially understood bytes

| Offset | Status | Current interpretation |
|---|---|---|
| `0x0A` | Candidate | Likely state/version/edit flag byte |
| `0x26` | Candidate | Likely selected/edited-part context or state marker |

## Dump capture notes

Single-parameter `DUMP_MULTI` diffs (Virus panel preferred). Live `0x72` examples: [live-sysex.md](live-sysex.md).

- AURA INIT, Part 1 **Hold Pedal** off: only `0xF9` `0x45` → `0x41` + checksum.
- Virus Part 1 Hold Pedal on/off (panel): only `0xF9` `0x45` ↔ `0x41` + checksum (header `0x0A` may toggle).
- Virus Part 1 **Priority** Low vs High (Hold off): only `0xF9` `0x41` → `0x61` (`+0x20`) + checksum.
- AURA INIT, Part 1 **Prog Change** off/on: only `0xF9` `0x05` ↔ `0x45` (`±0x40`) + checksum.
- Virus Part 1 **Init Volume** 64: only **`0xA8`** `0x00` → `0x40` + checksum; **`0xF8` unchanged** (`0x45`).
- **Part 15 Init Vol** (Virus, clean baseline): only **`0xB6`** — `0x00` / `0x7F` (127) / `0x14` (20); **`0xB7` stays `0`**; Part 15 flag **`0x106` unchanged** (`0x45`); `0x26` = `0x0E` (edited part).
- AURA INIT, Part 1 **Init Volume** 64: `0xA9` `0x00` → `0x40`; `0xF9` `0x45` → `0x47` (`+2`) — AURA offset/export may differ from Virus **`0xA8`**.
- AURA **Part Level** at `0x99`: INIT `0x40`; UI `-64` → `0x00`; UI `+36` → `0x64`.
- Virus Part 1 **Program** 64→65: only `0x39` `0x40` → `0x41` + checksum.
- Virus Part 1 **Bank** RAM-A→RAM-B (P65): `0x29` `0x00` → `0x01`; `0x39` unchanged vs program-only diff.
- Virus bank index (P65): RAM D `0x03`, ROM A `0x04`, ROM Z `0x1D`; ROM H P66 `0x0B`/`0x42`; ROM M P127 `0x10`/`0x7F`.
- Virus **Master Clock** at **`0x17`**: 120/`124` bpm → `0x39`/`0x3D`; only byte + checksum (clean baseline).
- Virus Prog Change captures (`0x21`/`0x61`) — **superseded** (mixed `0xF9` flags).
- **Reverb Send:** no `DUMP_MULTI` byte change in any capture; live-only — [live-sysex.md](live-sysex.md#reverb-send--not-in-multi-dump).
- Virus INIT MULTI, Part 1 **Transpose** only: `0x79` `0x40` (+0), `0x70` (+48), `0x10` (−48), `0x34` (−12); header `0x0A` often `0x01` when edited; Part 3 +48: `0x7B` `0x70`, `0x26` `0x02`.
- Virus Part 1 **Output** Out 1 L → Out 2 L: only `0xB8` `00` → `03` + checksum; live `72 00 29 03`; `0xC8..0xD7` unchanged.
- Virus Part 1 **Pan** Off vs Center: only `0xD8` `00` ↔ `0x40` + checksum; `0xC8..0xD7` unchanged.
- Virus Part 1 **Enable** Off: only `0xF8` `0x45` → `0x44` + checksum; `0xE8..0xF7` unchanged.
- **Part 15 Init Vol** (Virus, clean baseline): only **`0xB6`** — `0x00` / `0x7F` (127) / `0x14` (20); **`0xB7` stays `0`**; Part 15 flag **`0x106` unchanged** (`0x45`); `0x26` = `0x0E` (edited part).
- **Part 16 Init Vol** — not in dump (`0xB7` unused; `0xB8` = Part 1 Output).
- **Keyboard to MIDI** (AURA kbd local, live `72 00 40 00/01`): two `DUMP_MULTI` captures from **TI desktop module** — **identical** (no payload/checksum change).

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
