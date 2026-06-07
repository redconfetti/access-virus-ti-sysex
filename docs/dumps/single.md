# Single Dump

Part of [Dumps](README.md). **`DUMP_SINGLE`** layout and parameter inventory.

Live edit: [Live Edit README](../live-edit/README.md). Control inventory for
mapping:
[Single parameter map](#single-parameter-map).

## Dump Format

- **Transport**: One MIDI SysEx message per Single.
- **Total length**: 524 bytes including `F0` and `F7`.
- **Wire layout**: `F0` + **522** data bytes + `F7` (checksum is the byte
 before `F7`).

### Message header (offsets in full 524-byte message)

| Offset         | Field             | INIT arrangement (all parts)              | Standalone `-INIT-` single      |
| -------------- | ----------------- | ----------------------------------------- | ------------------------------- |
| `0x00`         | Start             | `F0`                                      | `F0`                            |
| `0x01`–`0x03`  | Manufacturer      | `00 20 33`                                | `00 20 33`                      |
| `0x04`         | Family            | `01`                                      | `01`                            |
| `0x05`         | Device ID         | `00`                                      | `00`                            |
| `0x06`         | Command           | `10` (`DUMP_SINGLE`)                      | `10`                            |
| `0x07`         | **Bank**          | `00` (edit buffer)                        | `00`                            |
| `0x08`         | **Slot / part**   | **`00`–`0F`** = Part 1–16                 | **`7F`** (edit buffer, no part) |
| `0x09`–`0x0B`  | TI extension      | `0C 10 00` (constant in INIT arrangement) | `0C 00 00`                      |
| `0x09`–`0x208` | Payload + trailer | See regions below                         |                                 |
| `0x209`        | Checksum          | `66` (Part 1 in arrangement)              | `44` (standalone baseline)      |
| `0x20A`        | End               | `F7`                                      | `F7`                            |

**Checksum** (confirmed on arrangement Part 1):
`(device + 0x10 + bank + slot + sum(bytes 0x09..0x208)) & 0x7F`.

See [bank.md — Single Request](bank.md#single-request-0x30) for **`30 00 40`**
(Single edit buffer) vs **`30 00 00`–`0F`** (Multi parts).

## Single vs Multi addressing {#single-vs-multi-addressing}

The TI mk2 keeps **separate** single-sound edit buffers for Multi parts and for
Single-mode editing. **Single Request** `slot`, **`DUMP_SINGLE`** header
**`0x08`**, and most live-edit **`<part>`** bytes share this indexing:

| Target             | Typical live edit `<part>`           | Single Request (`30 00 …`) | `DUMP_SINGLE` `@0x08` |
| ------------------ | ------------------------------------ | -------------------------- | --------------------- |
| Multi Part 1–16    | **`0x00`–`0x0F`**                    | **`00`–`0F`**              | **`00`–`0F`**         |
| Single edit buffer | **`0x40`** (`0x70`/`0x71`/`0x6E`, …) | **`40`**                   | **`0x40`**            |

**Exception:** Edit Multi **Bank** / **Program** (**`cmd=0x72`**, params
**`0x20`** / **`0x21`**) always use the **Multi part index**
(**`0x00`–`0x0F`**), even when loading a sound for Part 1 — not **`0x40`**.
See [edit-multi.md — Bank / Program](../live-edit/edit-multi.md#bank-0x20).

Multi Part 1 and the Single edit buffer are **not** the same RAM — SysEx to
**`<part>=00`** does not change the sound returned by **`30 00 40`**, and vice
versa. The synth applies each live edit to the buffer named by **`<part>`**
(Single **`0x40`** vs Multi **`0x00`–`0x0F`**); the panel’s current mode picks
which buffer you are editing, but the wire **`<part>`** byte must match that
target (param IDs such as Ring Mod **`0x32`** stay the same across modes).

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 30 00 40
```

Classic **Single Request** (`0x30`) with `bank=00` uses `slot=00`–`0F` for Multi
parts and `slot=40` for Single-mode buffer — arrangement dumps mirror the
**`00` + part index** scheme.

## Arrangement export (`DUMP_SINGLE` × 16)

Reference capture:
[`artifacts/sysex/init-multi-arrangement.syx`](../artifacts/sysex/init-multi-arrangement.syx)
(INIT MULTI via **Arrangement Request** — `F0 … 34 00 F7`).

| Item          | Value                                   |
| ------------- | --------------------------------------- |
| Total size    | **8651** bytes = **267** + **16 × 524** |
| Message 1     | `DUMP_MULTI` (`0x11`), 267 bytes        |
| Messages 2–17 | `DUMP_SINGLE` (`0x10`), one per part    |

**Part addressing** — order on the wire is **Part 1 first**, then Part 2 …
Part 16:

| Wire order   | Multi part | `DUMP_SINGLE` header `0x08` (slot) |
| ------------ | ---------- | ---------------------------------- |
| 2nd message  | Part 1     | `00`                               |
| 3rd message  | Part 2     | `01`                               |
| …            | …          | …                                  |
| 17th message | Part 16    | `0F`                               |

All sixteen singles in this capture use **bank `0x07` = `00`** (edit buffer),
**slot `0x08` = part index** (zero-based), and the same patch name **`-INIT-`**
at `0xFA`. They are **not** addressed by the Multi’s per-part **program**
bytes at `0x39..0x48` (INIT MULTI has `7F` there — factory placeholder, not
`0x00`–`0x0F`).

```text
# Part 1 (first single after multi)
F0 00 20 33 01 00 10 00 00 0C 10 00 … -INIT- … 66 F7

# Part 16 (last single)
F0 00 20 33 01 00 10 00 0F 0C 10 00 … -INIT- … F7
```

See [Embedded vs Reference
Multis](arrangements.md#embedded-vs-reference-multis).

## High‑level regions (from `-INIT-` baseline)

Using offsets in hexadecimal (0x00 is the `F0` byte):

- **0x00–0x0B – Fixed header**
- Arrangement / per-part: `… 10 00 <slot> 0C 10 00` (`<slot>` = `00`–`0F`).
- Standalone edit buffer: `… 10 00 7F 0C 00 00` (see [message
 header](#message-header-offsets-in-full-524-byte-message)).
- **0x0C–~0xEF – Parameter payload**
- Dense sound data. **Oscillator block** (hardware-verified on `-INIT-` /
 Single edit buffer **`30 00 40`**, live edit **`<part>=0x40`**):
- **`0x00D`** — Portamento (`70`/`05`)
- **`0x019`–`0x01D`** — Osc 1 Classic: Shape, Pulse Width, Wave, Semitone,
 Key Follow (`70`/`11`–`15`)
- **`0x01E`–`0x027`** — Osc 2 Classic: Shape, Pulse Width, Wave, Semitone,
 Detune, FM Amount, Sync, FilterEnv>Pitch, FilterEnv>FM, Key Follow
 (`70`/`16`–`1F`)
- **`0x029`–`0x02F`, `0x03A`** — Mixer / Noise / Ring Mod: Balance (`0x29`),
 Sub Osc vol/shape (`0x2A`/`0x2B`), Osc vol/sat (`0x2C`), Noise vol (`0x2D`),
 Noise color (`0x2F`), Ring Mod (`0x3A`)
- **`0x0AA`–`0x0B4`** — Phase Init, Punch, Osc 2 FM Mode, Osc 3 Mode/Volume/
 Semitone/Detune (`71`/`23`–`29`, `71`/`24`)
- **`0x107`** — Mixer section Osc Volume (`71`/`7F`)
- **`0x127`, `0x12C`** — Osc 1 / Osc 2 mode (`6E`/`1E`, `6E`/`23`)
- **`0x12E`–`0x135`** — Osc 1 **`6E`** params: F-Spread (`0x25`→`0x12E`),
 F-Shift (`0x2A`→`0x133`), Local Detune (`0x2B`→`0x134`), Interpolation
 (`0x2C`→`0x135`)
- **`0x142`–`0x149`** — Osc 2 **`6E`** params: F-Spread (`0x39`→`0x142`),
 F-Shift (`0x3E`→`0x147`), Local Detune (`0x3F`→`0x148`), Interpolation
 (`0x40`→`0x149`)
- **`0x201`–`0x204`** — **Edit Single → Unison** (`6F`/`78`–`7B`): Voices,
 Detune, Pan Spread, LFO Phase
- **`0x030`–`0x047`** — Filters Page A: cutoff/res/env/ADSR/amp (`70`/`28`–`3F`)
- **`0x0A6`–`0x0A7`** — Filter 1 / 2 envelope polarity Page B (`71`/`1E`, `71`/`1F`)
- **`0x0A9`** — Filter Key Follow Base (`71`/`21`)
- **`0x0BE`–`0x0C1`** — Velocity Map filter depths (`71`/`36`–`39`)
- **`0x102`** — Filters SELECT knob target (`71`/`7A`)
- **`0x052`–`0x062`** — LFO 1/2 destination depths (`70`/`4A`–`5A`)
- **`0x057`–`0x05D`** — LFO 2 settings Page A (`70`/`4F`–`55`)
- **`0x08F`–`0x095`** — LFO 3 settings Page B (`71`/`07`–`0D`)
- **`0x09A`–`0x09D`** — LFO 1/2/3 Clock (`71`/`12`, `13`, `15`)
- **`0x0C8`–`0x0D8`, `0x0EF`–`0x0F7`, `0x163`–`0x174`** — Mod Matrix six slots
   (`71`/`40`–`4E`, `67`–`6F`; rows 2–3 on `6E`/`5A`–`6B`)
- **`0x0CC`–`0x0D1`** — LFO 1 settings Page B (`71`/`43`–`49`; **same dump bytes**
   as Mod Matrix slots 2–3 where param bytes overlap)
- **`0x070`–`0x076`** — Chorus Classic Page A (`70`/`67`–`6E`)
- **`0x11C`–`0x11E`** — Filter Bank type/mix/frequency (`6E`/`13`–`15`)
- **`0x123`** — Character type (`6E`/`1A`)
- **`0x14F`–`0x153`** — Distortion treble/high cut/mix/quality/tone (`6E`/`46`–`4A`)
- **`0x11F`–`0x122`** — Filter Bank stereo phase / shapes / resonance (`6E`/`16`–`19`)
- **`0x078`–`0x07F`, `0x113`, `0x115`–`0x117`, `0x11A`, `0x09C`** — Delay
   (`70`/`70`–`77`, `71`/`14`; tape extras on `6E`/`0C`–`0E`, `11`)
- **`0x10A`–`0x112`** — Reverb (`6E`/`01`–`09`)
- **`0x0AE`** — Input Follower Input Select (`71`/`26`)
- **`0x030`–`0x042`** — Vocoder Page A rows + Input Follower attack/release/sensitivity
   (`70`/`28`–`30`, `36`–`3A`, `2B`, `2F`; mode at **`0x0AF`** on `71`/`27`)
- **`0x0B5`–`0x0B6`** — EQ Low / High frequency Page B (`71`/`2D`, `2E`)
- **`0x0DC`–`0x0E2`, `0x0E4`–`0x0E8`, `0x0EC`–`0x0ED`** — Phaser, EQ gains,
   Distortion type/intensity Page B (`71`/`54`–`60`, `5C`–`5F`, `64`–`65`)
- **`0x0E9`–`0x0EA`** — Character Stereo Widener / Speaker Cabinet intensity + frequency (`71`/`61`, `62`)
- **`0x012`** — Panorama (`70`/`0A`)
- **`0x063`** — Patch Volume (`70`/`5B`)
- **`0x065`** — Transpose (`70`/`5D`)
- **`0x066`** — Key Mode (`70`/`5E`)
- **`0x0A1`–`0x0A4`** — Edit Single Common: Smooth Mode, Bend Up/Down, Bender Scale (`71`/`19`–`1C`)
- **`0x0A8`** — Filter Cutoff Link (`71`/`20`)
- **`0x0BB`–`0x0BD`** — Soft Knob 1–3 **Name** (`71`/`33`–`35`)
- **`0x0C2`** — Surround Balance (`71`/`3A`)
- **`0x0C6`–`0x0C8`** — Soft Knob 1–3 **Function As…** (`71`/`3E`–`40`; **`0x0C8`** = Mod Matrix slot 1 Source wire)
- **`0x103`–`0x104`** — Name Cat 1 / 2 (`71`/`7B`, `7C`)
- **`0x159`–`0x162`** — Envelope 3 / 4 (`6E`/`50`–`59`)
- **`0x183`** — Filter Common Pan Spread (`6E`/`7A`, Split routing)
- **`0x0B7`–`0x0C5`** — **Edit Single → Velocity Map** (`71`/`2F`–`32`, `36`–`39`, `3C`–`3D`)
- **`0x08A`–`0x08E`, `0x097`, `0x099`** — **EDIT ARP** settings (`71`/`02`–`06`, `0F`, `11`)
- **~0x184–0x1E9 – User arpeggiator pattern** (when **Pattern** = **User**)
- **`0x189`** — loop length (**1**–**32** steps; `stored = steps − 1`)
- **`0x18A`…`0x1E9`** — **32** step triplets (**length**, **velocity**,
 **enable**; **3** bytes per step) — see
 [Arpeggiator user pattern dump](../live-edit/arpeggiator.md#arpeggiator-user-pattern-dump)
- **~0xF8–0x103 – Patch name, categories, and nearby globals**
- Contains the ASCII patch name `-INIT-` padded with spaces:
- The ASCII sequence `2d 49 4e 49 54 2d 20 20 20`
 (`-INIT-` padded with spaces)
 appears near offset 0xFA.
- Surrounding bytes likely hold category and other global Single attributes.
- **`0x205`–`0x207`** — Input Mode / Select / Atomizer (`6F`/`7C`–`7E`)
- **0x208–0x209 – Trailer metadata + checksum**
- Checksum at **`0x209`**; byte **`0x208`** and following trailer fields vary by
 export context.

## Single parameter map

Parameter inventory (control names and categories). **Excluded:** Flash ROM banks,
Assignable X/Y Pad, and Browser (Patch Saving / Patch Browsing).

Most rows are **Single-program** parameters to correlate with
`DUMP_SINGLE` bytes and live-edit SysEx. Fill **Dump offset** and
**Live edit** as mappings are confirmed. Enum option lists:
[parameter-options.md](../parameter-options.md).

Multi edit parameters are in
[Multi parameter map](arrangements.md#multi-parameter-map).

**403** controls in **11** categories.

### Oscillators

**SubCategory** labels in the parameter inventory below are **not always** TI mk2
**EDIT** menu names. Examples: **Oscillator Common FM** and **Oscillator Common Sync** are
inventory groupings only — there is no **EDIT OSC → Common → FM** page. FM and
sync-related controls live on **Osc 2** sub-menus, **EDIT OSC → Common** (e.g.
**FilterEnv>Sync** when Sync is on), or **Edit Single → Velocity Map**. Rows
for **Edit Single → Unison** are under [Common](#common) — not **EDIT OSC**.

**Dump offsets** in the **Dump offset** column below were confirmed on TI mk2
hardware by: request `DUMP_SINGLE` (`30 00 40`) → one live-edit SysEx
(`<part>=0x40`) → re-request → diff (ignore checksum **`0x209`** and metadata
byte **`0x108`**). Helper script:
[`artifacts/captures/dump-correlate.sh`](../../artifacts/captures/dump-correlate.sh).
Per-mode sweeps (switch **`6E`/`1E`** or **`6E`/`23`**, then test controls from
[oscillators.md](../live-edit/oscillators.md)):
[`dump-correlate-osc-modes.py`](../../artifacts/captures/dump-correlate-osc-modes.py).
Velocity Map + Filters:
[`dump-correlate-velocity-filters.py`](../../artifacts/captures/dump-correlate-velocity-filters.py).
LFO + Mod Matrix + FX 1:
[`dump-correlate-lfo-matrix-fx.py`](../../artifacts/captures/dump-correlate-lfo-matrix-fx.py).

| Control                                | SubCategory                     | Dump offset | Live edit                                                                                                                                                                                |
| -------------------------------------- | ------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sub Oscillator Waveform Shape          | Sub-Osc                         | `0x2B`      | `70` / `0x23` (CC 35; Square `00`, Triangle `01` only)                                                                                                                                   |
| Oscillator 1 Model / Mode              | Oscillator 1                    | `0x127`     | `6E` / `0x1E` (see live-edit by mode)                                                                                                                                                    |
| Oscillator 1 Detune in Semitone        | Oscillator 1                    | `0x1C`      | `70` / `0x14` (−48..+48, `ui+64`)                                                                                                                                                        |
| Oscillator 1 Keyfollow                 | Oscillator 1                    | `0x1D`      | `70` / `0x15` (Classic; Norm @ +32)                                                                                                                                                      |
| Velocity --> Osc1 Waveform Shape       | Oscillator 1                    | `0xB7`      | `71` / `0x2F` (Velocity Map **Osc 1 Shape**; ±100 % — [Velocity Map](../live-edit/edit-single.md#velocity-map-edit-single)                                                               |
| Oscillator 1 Waveform Shape            | Oscillator 1 Classic            | `0x19`      | `70` / `0x11` (`00`–`7F`; see live-edit)                                                                                                                                                 |
| Oscillator 1 Wave Select               | Oscillator 1 Classic            | `0x1B`      | `70` / `0x13` (64 waves `00`–`3F`)                                                                                                                                                       |
| Oscillator 1 Pulsewidth                | Oscillator 1 Classic            | `0x1A`      | `70` / `0x12` — **50.0 %..100 %** when Shape ≥ `40` — [Pulse Width](../live-edit/oscillators.md#pulse-width-shape--sawtooth)                                                             |
| Oscillator 1 Density                   | Oscillator 1 Hypersaw           | `0x19`      | `70` / `0x11` — **1.0..9.0** — [Hypersaw](../live-edit/oscillators.md#oscillator-1--hypersaw)                                                                                            |
| Oscillator 1 Local Detune              | Oscillator 1 Hypersaw           | `0x1A`      | `70` / `0x12` — **0..127** `stored = lcd` (Hypersaw; Classic `12` = Pulse Width)                                                                                                         |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 1 Hypersaw           | `0x23`      | `70` / `0x1B` — **0..127** when Sync On; `stored = lcd`                                                                                                                                  |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable          | `0x1B`      | `70` / `0x13` — Index **0–99** → `00`–`63`; names in [parameter-options.md](../parameter-options.md#wavetable-names)                                                                     |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable          | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd` (mode `02`; not Shape/Density)                                                                                                                 |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable          | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd` (not `70`/`2C` Filter Env)                                                                                                                     |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable PWM      | `0x1B`      | `70` / `0x13` — **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--wavetable-pwm)                                                                                 |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable PWM      | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Pulsewidth                | Oscillator 1 Wavetable PWM      | `0x1A`      | `70` / `0x12` — **0..127** `stored = lcd` (not Classic 50–100 %)                                                                                                                         |
| Oscillator 1 Local Detune              | Oscillator 1 Wavetable PWM      | `0x134`     | `6E` / `0x2B` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable PWM      | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Simple       | `0x1B`      | `70` / `0x13` — **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--grain-simple)                                                                                  |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Simple       | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Simple       | `0x133`     | `6E` / `0x2A` — F-Shift **−64..+63** → `ui+64` (not `70`/`2A` Resonance)                                                                                                                 |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Simple       | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Complex      | `0x1B`      | `70` / `0x13` — **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--grain-complex)                                                                                 |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Complex      | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Complex      | `0x133`     | `6E` / `0x2A` — F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Formant Spread            | Oscillator 1 Grain Complex      | `0x12E`     | `6E` / `0x25` — F-Spread **0..127** → `stored = lcd`                                                                                                                                     |
| Oscillator 1 Local Detune              | Oscillator 1 Grain Complex      | `0x134`     | `6E` / `0x2B` — **0..127** → `stored = lcd`                                                                                                                                              |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Complex      | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Simple     | `0x1B`      | `70` / `0x13` — Same enum as Wavetable mode                                                                                                                                              |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Simple     | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Simple     | `0x133`     | `6E` / `0x2A` — F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Simple     | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Complex    | `0x1B`      | `70` / `0x13` — Same enum as Wavetable mode                                                                                                                                              |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Complex    | `0x19`      | `70` / `0x11` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Complex    | `0x133`     | `6E` / `0x2A` — F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Formant Spread            | Oscillator 1 Formant Complex    | `0x12E`     | `6E` / `0x25` — F-Spread **0..127** → `stored = lcd`                                                                                                                                     |
| Oscillator 1 Local Detune              | Oscillator 1 Formant Complex    | `0x134`     | `6E` / `0x2B` — **0..127** → `stored = lcd`                                                                                                                                              |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Complex    | `0x135`     | `6E` / `0x2C` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Model / Mode              | Oscillator 2                    | `0x12C`     | `6E` / `0x23` (Classic `00`, Hypersaw `01`, Wavetable `02`, Wavetable PWM `03`, Grain Simple `04`, Grain Complex `05`, Formant Simple `06`, Formant Complex `07`)                        |
| Oscillator 2 Detune in Semitone        | Oscillator 2                    | `0x21`      | `70` / `0x19` (−48..+48, `ui+64`)                                                                                                                                                        |
| Oscillator 2 Fine Detune               | Oscillator 2                    | `0x22`      | `70` / `0x1A` (Detune **0..127**, `stored = lcd`)                                                                                                                                        |
| Oscillator 2 Keyfollow                 | Oscillator 2                    | `0x27`      | `70` / `0x1F` (−64..+63, Norm @ +32)                                                                                                                                                     |
| Velocity --> Osc2 Waveform Shape       | Oscillator 2                    | `0xB8`      | `71` / `0x30` (Velocity Map **Osc 2 Shape**; ±100 %)                                                                                                                                     |
| Oscillator 2 Waveform Shape            | Oscillator 2 Classic            | `0x1E`      | `70` / `0x16` — same Classic Shape encoding as Osc 1 (`70`/`11`); Spectral Wave `00`                                                                                                     |
| Oscillator 2 Wave Select               | Oscillator 2 Classic            | `0x20`      | `70` / `0x18` — waves **`00`–`3F`** (Sine `00`; same enum as Osc 1 Wave)                                                                                                                 |
| Oscillator 2 Pulsewidth                | Oscillator 2 Classic            | `0x1F`      | `70` / `0x17` — **50.0 %..100 %** when Shape ≥ `40` (same as Osc 1 Classic PW)                                                                                                           |
| Oscillator 2 Density                   | Oscillator 2 Hypersaw           | `0x1E`      | `70` / `0x16` — **1.0..9.0**, same curve as Osc 1 Hypersaw Density                                                                                                                       |
| Oscillator 2 Local Detune              | Oscillator 2 Hypersaw           | `0x1F`      | `70` / `0x17` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 2 Hypersaw           | `0x23`      | `70` / `0x1B` — **0..127** when Sync On; `stored = lcd`; same slot as Classic FM Amount                                                                                                  |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable          | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable          | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable          | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable PWM      | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable PWM      | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Pulsewidth                | Oscillator 2 Wavetable PWM      | `0x1F`      | `70` / `0x17` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Wavetable PWM      | `0x148`     | `6E` / `0x3F` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable PWM      | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Simple       | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Simple       | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Simple       | `0x147`     | `6E` / `0x3E` — **−64..+63** → `stored = ui + 64`                                                                                                                                        |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Simple       | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Complex      | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Complex      | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Complex      | `0x147`     | `6E` / `0x3E` — **−64..+63** → `stored = ui + 64`                                                                                                                                        |
| Oscillator 2 Formant Spread            | Oscillator 2 Grain Complex      | `0x142`     | `6E` / `0x39` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Grain Complex      | `0x148`     | `6E` / `0x3F` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Complex      | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Simple     | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Simple     | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Simple     | `0x147`     | `6E` / `0x3E` — **−64..+63** → `stored = ui + 64`                                                                                                                                        |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Simple     | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Complex    | `0x20`      | `70` / `0x18` — **`00`–`63`** enum; Sine..Domina7rix                                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Complex    | `0x1E`      | `70` / `0x16` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Complex    | `0x147`     | `6E` / `0x3E` — **−64..+63** → `stored = ui + 64`                                                                                                                                        |
| Oscillator 2 Formant Spread            | Oscillator 2 Formant Complex    | `0x142`     | `6E` / `0x39` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Formant Complex    | `0x148`     | `6E` / `0x3F` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Complex    | `0x149`     | `6E` / `0x40` — **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 3 Model                     | Oscillator 3                    | `0xB1`      | `71` / `0x29` (Mode/Wave; Off `00`, Slave `01`, Saw `02`, Pulse `03`, Sine `04`, Triangle `05`, Wave 3..64 `06`–`43`)                                                                    |
| Oscillator 3 Detune in Semitone        | Oscillator 3                    | `0xB3`      | `71` / `0x2B` (visible for Mode/Wave `02`–`43`; **−48..+48**, `ui+64`)                                                                                                                   |
| Oscillator 3 Fine Detune               | Oscillator 3                    | `0xB4`      | `71` / `0x2C` (visible for Mode/Wave `02`–`43`; panel **0..−127**, `stored = −ui`)                                                                                                       |
| Oscillator 1 Sync (2>1)                | Osc 1 / Osc 2 sub-menus         | `0x24`      | `70` / `0x1C` — **EDIT OSC → Osc 1** (e.g. Hypersaw) and **Osc 2 Classic**; Off `00`, On `01`                                                                                            |
| Filter Envelope --> Oscillator 2 Pitch | Oscillator 2 Classic            | `0x25`      | `70` / `0x1D` — **EDIT OSC → Osc 2** (Classic/Hypersaw/Wavetable/…); **−100 %** `00`, **0 %** `40`, **+100 %** `7F`                                                                      |
| Oscillator Section Initial Phase       | EDIT OSC → Common               | `0xAB`      | `71` / `0x23` — **Phase Init**; Off `00`, **1..127** direct                                                                                                                              |
| Velocity --> Pulsewidth                | Velocity Map                    | `0xB9`      | `71` / `0x31` — **Edit Single → Velocity Map → Pulse Width**; ±100 %                                                                                                                     |
| Patch Common Portamento                | EDIT OSC → Common               | `0x0D`      | `70` / `0x05` (CC 5; Off `00`, **1..127** direct `stored = lcd`)                                                                                                                         |
| Oscillator 2 FM Amount                 | Oscillator 2 Classic            | `0x23`      | `70` / `0x1B` — **EDIT OSC → Osc 2**; **Sync Off:** 0.0..100.0 %; **Sync On:** **Sync Frequency** **0..127**; other Osc 2 modes **0..127** direct                                        |
| Filter Envelope --> FM / X-Sync        | Osc 2 Classic / EDIT OSC Common | `0x26`      | `70` / `0x1E` — one wire; **Sync Off:** **FilterEnv>FM** on **Osc 2 Classic**; **Sync On:** **FilterEnv>Sync** on **EDIT OSC → Common** (and Osc 1 Hypersaw); **−100..+100 %** like `1D` |
| Velocity --> FM Amount                 | Velocity Map                    | `0xBA`      | `71` / `0x32` — **Edit Single → Velocity Map → FM Amount** only (±100 %)                                                                                                                 |
| Oscillator 2 FM Mode                   | Oscillator 2 Classic            | `0xAA`      | `71` / `0x22` — **EDIT OSC → Osc 2**; Classic `00`–`06`, Wavetable/… **FreqMod** `00`, **PhaseMod** `01`                                                                                 |
| ~~Sync Amount / X-Sync Frequency~~     | —                               | —           | Same as **Oscillator 2 FM Amount** — `70` / `0x1B` when **Sync On** (`70`/`1C`=`01`)                                                                                                     |
| ~~Velocity --> FM / Sync~~             | —                               | —           | **N/A** on TI mk2 — Velocity Map has **FM Amount** only (`71`/`32`); no separate **FM/Sync** row                                                                                         |
| ~~Filter Envelope --> X-Sync~~         | —                               | —           | Same wire as **Filter Envelope --> FM / X-Sync** — `70` / `0x1E`; inventory-only duplicate                                                                                               |
| Noise Oscillator Volume                | Noise                           | `0x2D`      | `70` / `0x25` (CC 37; Off `00`, **1..127** direct `stored = lcd`)                                                                                                                        |
| Noise Color                            | Noise                           | `0x2F`      | `70` / `0x27` (**−64..+63** → `stored = ui + 64`)                                                                                                                                        |
| Oscillator Punch Intensity             | Oscillators → Punch             | `0xAC`      | `71` / `0x24` — **EDIT OSC → Punch**; **0.0..100.0 %** (`pct = stored × 100 / 128`)                                                                                                      |
| Oscillator 1/2 Balance                 | Mixer                           | `0x29`      | `70` / `0x21` (−100..+100 %)                                                                                                                                                             |
| Oscillator 3 Volume                    | Mixer                           | `0xB2`      | `71` / `0x2A` (visible for Osc 3 Mode/Wave `02`–`43`; **0..127** `stored = lcd`)                                                                                                         |
| Sub Oscillator Volume                  | Sub-Osc                         | `0x2A`      | `70` / `0x22` (CC 34; **0..127** direct `stored = lcd`)                                                                                                                                  |
| Oscillator Section Volume / Saturation | Mixer                           | `0x2C`      | `70` / `0x24` (Osc Volume / Saturation menu, **−64..+63**); Mixer section volume uses `71` / `0x7F` → dump **`0x107`**                                                                   |
| Ring Modulator Volume                  | Mixer                           | `0x3A`      | `70` / `0x32` (CC 38; **not** param `0x26`; Off `00`, **1..127** direct `stored = lcd`)                                                                                                  |

### Filters

**Filter envelope polarity:** duplicate panel rows under Filter 1 and Filter 2;
separate dump bytes **`0x0A6`** / **`0x0A7`** — see
[filters.md — shared panel menus](../live-edit/filters.md#filter-envelope-polarity-shared).

| Control                               | SubCategory                | Dump offset     | Live edit                                                                                                                                                             |
| ------------------------------------- | -------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Filter 1 Mode                         | Filter 1                   | `0x03B`         | `70` / `0x33`                                                                                                                                                         |
| Filter 1 Envelope Amount              | Filter 1                   | `0x034`         | `70` / `0x2C`                                                                                                                                                         |
| Filter 1 Envelope Polarity            | Filter 1                   | `0x0A6`         | `71`/`1E` `00`/`01`; [shared panel](../live-edit/filters.md#filter-envelope-polarity-shared)                                                                          |
| Filter 1 Cutoff                       | Filter 1                   | `0x030`         | `70` / `0x28`                                                                                                                                                         |
| Filter 1 Resonance                    | Filter 1                   | `0x032`         | `70` / `0x2A` — also **Vocoder Q-Factor** when Vocoder active                                                                                                         |
| Filter 1 Keyfollow                    | Filter 1                   | `0x036`         | `70` / `0x2E` — also **Vocoder Spread** when Vocoder active                                                                                                           |
| ~~Analog Mode On/Off Toggle~~         | —                          | —               | **N/A** — analog types are **Filter 1 Mode** values (`04`–`07` Analog * Pole)                                                                                         |
| Filter 2 Mode                         | Filter 2                   | `0x03C`         | `70` / `0x34` (4 modes `00`–`03` only)                                                                                                                                |
| Filter 2 Envelope Amount              | Filter 2                   | `0x035`         | `70` / `0x2D` (linear %)                                                                                                                                              |
| Filter 2 Envelope Polarity            | Filter 2                   | `0x0A7`         | `71`/`1F` `00`/`01`; [shared panel](../live-edit/filters.md#filter-envelope-polarity-shared)                                                                          |
| ~~Filter 2 Cutoff~~                   | —                          | —               | **N/A** on TI — no separate F2 cutoff; use **Offset** vs F1                                                                                                           |
| Filter 2 Offset                       | Filter 2                   | `0x031`         | `70` / `0x29` (bipolar `ui+64`)                                                                                                                                       |
| Filter 2 Resonance                    | Filter 2                   | `0x033`         | `70` / `0x2B` (direct 0–127)                                                                                                                                          |
| Filter 2 Keyfollow                    | Filter 2                   | `0x037`         | `70` / `0x2F` (bipolar `ui+64`)                                                                                                                                       |
| Oscillator Section Volume             | Filter Common              | `0x02C`         | `70` / `0x24` (Saturation menu; bipolar `ui+64`)                                                                                                                      |
| Filter Routing                        | Filter Common              | `0x03D`         | `70` / `0x35` (4 routing modes)                                                                                                                                       |
| Voice Saturation Type / Curve         | Filter Common              |                 | **N/A** on TI Saturation menu (only Osc Volume)                                                                                                                       |
| Filter knob target (Res / Env Amt)    | Filter Common              | `0x102`         | [`71`/`7A`](../live-edit/filters.md#filters-select) — **SELECT** (`00` F1 … `02` F1+F2)                                                                               |
| Filter Keyfollow Base                 | Filter Common              | `0x0A9`         | `71` / `0x21` (C-1..G9)                                                                                                                                               |
| Filter Cutoff Link toggle             | Filter Common              | `0x0A8`         | `71` / `0x20` — **`00`** Off / **`01`** On (`<part>=0x40`)                                                                                                            |
| Filter Balance                        | Filter Common              | `0x038`         | `70` / `0x30` (bipolar `ui+64`)                                                                                                                                       |
| Pan Spread                            | Filter Common              | `0x183`         | `6E` / `0x7A` (Split routing only)                                                                                                                                    |
| ~~Filter Envelope Select~~            | —                          | —               | **N/A** on TI mk2 — no panel control; use **Filter 1/2 Env Polarity** (`71`/`1E`, `71`/`1F`) and [FILTERS SELECT](../live-edit/filters.md#filters-select) (`71`/`7A`) |
| Filter Envelope Attack                | Filter / Aux Envelopes     | `0x03E`         | `70` / `0x36` (Filter 1 ADSR menu)                                                                                                                                    |
| Filter Envelope Decay                 | Filter / Aux Envelopes     | `0x03F`         | `70` / `0x37`                                                                                                                                                         |
| Filter Envelope Sustain               | Filter / Aux Envelopes     | `0x040`         | `70` / `0x38` (linear %)                                                                                                                                              |
| Filter Envelope Sustain Slope         | Filter / Aux Envelopes     | `0x041`         | `70` / `0x39` (bipolar `ui+64`)                                                                                                                                       |
| Filter Envelope Release               | Filter / Aux Envelopes     | `0x042`         | `70` / `0x3A`                                                                                                                                                         |
| Envelope 3 Attack                     | Filter / Aux Envelopes     | `0x159`         | `6E` / `0x50` (**0..127** `stored = lcd`)                                                                                                                             |
| Envelope 3 Decay                      | Filter / Aux Envelopes     | `0x15A`         | `6E` / `0x51` (**0..127** `stored = lcd`)                                                                                                                             |
| Envelope 3 Sustain                    | Filter / Aux Envelopes     | `0x15B`         | `6E` / `0x52` (**0..100.0 %** → `round(pct × 127 / 100)`)                                                                                                             |
| Envelope 3 Sustain Slope              | Filter / Aux Envelopes     | `0x15C`         | `6E` / `0x53` (**−64..+63** → `ui + 64`)                                                                                                                              |
| Envelope 3 Release                    | Filter / Aux Envelopes     | `0x15D`         | `6E` / `0x54` (**0..127** `stored = lcd`)                                                                                                                             |
| Envelope 4 Attack                     | Filter / Aux Envelopes     | `0x15E`         | `6E` / `0x55` (**0..127** `stored = lcd`)                                                                                                                             |
| Envelope 4 Decay                      | Filter / Aux Envelopes     | `0x15F`         | `6E` / `0x56` (**0..127** `stored = lcd`)                                                                                                                             |
| Envelope 4 Sustain                    | Filter / Aux Envelopes     | `0x160`         | `6E` / `0x57` (**0..100.0 %** → `round(pct × 127 / 100)`)                                                                                                             |
| Envelope 4 Sustain Slope              | Filter / Aux Envelopes     | `0x161`         | `6E` / `0x58` (**−64..+63** → `ui + 64`)                                                                                                                              |
| Envelope 4 Release                    | Filter / Aux Envelopes     | `0x162`         | `6E` / `0x59` (**0..127** `stored = lcd`)                                                                                                                             |
| Amplifier Envelope Attack             | Amplifier Envelope         | `0x043`         | `70` / `0x3B`                                                                                                                                                         |
| Amplifier Envelope Decay              | Amplifier Envelope         | `0x044`         | `70` / `0x3C`                                                                                                                                                         |
| Amplifier Envelope Sustain            | Amplifier Envelope         | `0x045`         | `70` / `0x3D` (linear %)                                                                                                                                              |
| Amplifier Envelope Sustain Slope      | Amplifier Envelope         | `0x046`         | `70` / `0x3E` (bipolar `ui+64`)                                                                                                                                       |
| Amplifier Envelope Release            | Amplifier Envelope         | `0x047`         | `70` / `0x3F`                                                                                                                                                         |
| Velocity --> Filter 1 Envelope Amount | Velocity / Filter Envelope | `0xBE`          | `71` / `0x36` (±100 % — [Velocity Map](../live-edit/edit-single.md#velocity-map-edit-single)                                                                          |
| Velocity --> Filter 1 Resonance       | Velocity / Filter Envelope | `0xC0`          | `71` / `0x38` (±100 %)                                                                                                                                                |
| Velocity --> Filter 2 Envelope Amount | Velocity / Filter Envelope | `0xBF`          | `71` / `0x37` (±100 %)                                                                                                                                                |
| Velocity --> Filter 2 Resonance       | Velocity / Filter Envelope | `0xC1`          | `71` / `0x39` (±100 %)                                                                                                                                                |
| Velocity --> Volume                   | Velocity / Amplifier       | `0xC4`          | `71` / `0x3C` (±100 %)                                                                                                                                                |
| Velocity --> Panorama                 | Velocity / Amplifier       | `0xC5`          | `71` / `0x3D` (±100 %)                                                                                                                                                |
| Patch Volume                          | Amplifier                  |                 | CC 91                                                                                                                                                                 |
| Patch Panorama                        | Amplifier                  |                 | Same as Common **Panorama** — `70` / `0x0A`                                                                                                                           |

### LFO {#lfo}

Live-edit bytes: [modulators.md](../live-edit/modulators.md). **Dump offsets**
(hardware-verified; LFO 1 Page B bytes **overlap** Mod Matrix slots 2–3 — see
[modulation-matrix.md](../live-edit/modulation-matrix.md#page-b-byte-reuse)).

| Control                                            | SubCategory       | Dump offset       | Live edit                                                                                                                 |
| -------------------------------------------------- | ----------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- |
| LFO 1 Rate                                         | LFO 1             | `0x0CB`           | `71` / `0x43` — [LFO Rate](../parameter-options.md#lfo-rate) ( **Clock** = **Off** only)                                  |
| LFO 1 Clock Divider                                | LFO 1             | `0x09A`           | `71` / `0x12` — [LFO Clock](../parameter-options.md#lfo-clock) (**Off** reveals [Rate](../parameter-options.md#lfo-rate)) |
| LFO 1 Keyfollow                                    | LFO 1             | `0x0D0`           | `71` / `0x48` — [LFO Key Follow](../parameter-options.md#key-follow-0x48)                                                 |
| LFO 1 Trigger Phase                                | LFO 1             | `0x0D1`           | `71` / `0x49` — [LFO Trigger Phase](../parameter-options.md#trigger-phase-0x49)                                           |
| LFO 1 Waveform Shape                               | LFO 1             | `0x0CC`           | `71` / `0x44` — [LFO Shape](../parameter-options.md#lfo-shape)                                                            |
| LFO 1 Waveform Contour                             | LFO 1             | `0x0CF`           | `71` / `0x47` — [LFO Contour](../parameter-options.md#contour-0x47)                                                       |
| LFO 1 Mode                                         | LFO 1             | `0x0CE`           | `71` / `0x46` — [LFO Mode](../parameter-options.md#mode-0x46)                                                             |
| LFO 1 Envelope Mode toggle                         | LFO 1             | `0x0CD`           | `71` / `0x45` — [LFO Envelope Mode](../parameter-options.md#envelope-mode-0x45)                                           |
| LFO 1 --> Osc 1                                    | LFO 1 Destination | `0x052`           | `70` / `0x4A` — [Osc 1 Pitch](../parameter-options.md#lfo-1-destination)                                                  |
| LFO 1 --> Osc 2                                    | LFO 1 Destination | `0x053`           | `70` / `0x4B` — [Osc 2 Pitch](../parameter-options.md#lfo-1-destination)                                                  |
| LFO 1 to Oscillator 1&2 lock                       | LFO 1 Destination | `0x052` + `0x053` | linked **`4A`** + **`4B`** (panel **Osc 1+2 Pitch**)                                                                      |
| LFO 1 --> Pulsewidth                               | LFO 1 Destination | `0x054`           | `70` / `0x4C` — [Pulse Width](../parameter-options.md#lfo-1-destination)                                                  |
| LFO 1 --> Filter Resonance 1+2                     | LFO 1 Destination | `0x055`           | `70` / `0x4D` — [Resonance](../parameter-options.md#lfo-1-destination)                                                    |
| LFO 1 --> Filter Envelope Gain / Filter Gain Depth | LFO 1 Destination | `0x056`           | `70` / `0x4E` — [Filter Gain](../parameter-options.md#lfo-1-destination)                                                  |
| LFO 1 User Destination                             | LFO 1 Destination | `0x0D7`           | `71` / `0x4F` — [Assign Target](../parameter-options.md#lfo-1-destination)                                                |
| LFO 1 User Destination Amount                      | LFO 1 Destination | `0x0D8`           | `71` / `0x50` — [Amount](../parameter-options.md#lfo-1-destination)                                                       |
| LFO 2 Rate                                         | LFO 2             | `0x057`           | `70` / `0x4F` — [LFO Rate](../parameter-options.md#lfo-rate) (**Clock** = **Off** only)                                   |
| LFO 2 Clock Divider                                | LFO 2             | `0x09B`           | `71` / `0x13` — [LFO Clock](../parameter-options.md#lfo-clock)                                                            |
| LFO 2 Keyfollow                                    | LFO 2             | `0x05C`           | `70` / `0x54` — [LFO Key Follow](../parameter-options.md#key-follow-0x48)                                                 |
| LFO 2 Trigger Phase                                | LFO 2             | `0x05D`           | `70` / `0x55` — [LFO Trigger Phase](../parameter-options.md#trigger-phase-0x49)                                           |
| LFO 2 Waveform Shape                               | LFO 2             | `0x058`           | `70` / `0x50` — [LFO Shape](../parameter-options.md#lfo-shape)                                                            |
| LFO 2 Waveform Contour                             | LFO 2             | `0x05B`           | `70` / `0x53` — [LFO Contour](../parameter-options.md#contour-0x47)                                                       |
| LFO 2 Mode                                         | LFO 2             | `0x05A`           | `70` / `0x52` — [LFO Mode](../parameter-options.md#mode-0x46)                                                             |
| LFO 2 Envelope Mode toggle                         | LFO 2             | `0x059`           | `70` / `0x51` — [LFO Envelope Mode](../parameter-options.md#envelope-mode-0x45)                                           |
| LFO 2 --> Filter Cutoff 1                          | LFO 2 Destination | `0x060`           | `70` / `0x58` — [Cutoff 1](../parameter-options.md#lfo-2-destination)                                                     |
| LFO 2 --> Filter Cutoff 2                          | LFO 2 Destination | `0x061`           | `70` / `0x59` — [Cutoff 2](../parameter-options.md#lfo-2-destination)                                                     |
| LFO 2 to Filter 1&2 lock                           | LFO 2 Destination | `0x060` + `0x061` | linked **`58`** + **`59`** (panel **Cutoff 1+2**)                                                                         |
| LFO 2 --> Shape 1+2 Depth                          | LFO 2 Destination | `0x05E`           | `70` / `0x56` — [Shape 1+2](../parameter-options.md#lfo-2-destination)                                                    |
| LFO 2 --> Panorama                                 | LFO 2 Destination | `0x062`           | `70` / `0x5A` — [Panorama](../parameter-options.md#lfo-2-destination)                                                     |
| LFO 2 --> FM Amount                                | LFO 2 Destination | `0x05F`           | `70` / `0x57` — [FM Amount](../parameter-options.md#lfo-2-destination)                                                    |
| LFO 2 User Destination                             | LFO 2 Destination | `0x0D9`           | `71` / `0x51` — [Assign Target](../parameter-options.md#lfo-2-destination)                                                |
| LFO 2 User Destination Amount                      | LFO 2 Destination | `0x0DA`           | `71` / `0x52` — [Amount](../parameter-options.md#lfo-2-destination)                                                       |
| LFO 3 Rate                                         | LFO 3             | `0x08F`           | `71` / `0x07` — [LFO Rate](../parameter-options.md#lfo-rate) (**Clock** = **Off** only)                                   |
| LFO 3 Clock Divider                                | LFO 3             | `0x09D`           | `71` / `0x15` — [LFO Clock](../parameter-options.md#lfo-clock)                                                            |
| LFO 3 Keyfollow                                    | LFO 3             | `0x092`           | `71` / `0x0A` — [LFO Key Follow](../parameter-options.md#key-follow-0x48)                                                 |
| LFO 3 Waveform Shape                               | LFO 3             | `0x090`           | `71` / `0x08` — [LFO Shape](../parameter-options.md#lfo-shape)                                                            |
| LFO 3 Mode                                         | LFO 3             | `0x091`           | `71` / `0x09` — [LFO Mode](../parameter-options.md#mode-0x46)                                                             |
| LFO 3 Fade In Time                                 | LFO 3 Destination | `0x095`           | `71` / `0x0D` — [Fade In](../parameter-options.md#fade-in-0x0d) (panel **Fade In**; **`0`–`127`**)                        |
| LFO 3 User Destination                             | LFO 3 Destination | `0x093`           | `71` / `0x0B` — [Assign Target](../parameter-options.md#assign-target-0x0b)                                               |
| LFO 3 User Destination Amount                      | LFO 3 Destination | `0x094`           | `71` / `0x0C` — [Amount](../parameter-options.md#amount-0x0c)                                                             |

### Modulation Matrix {#modulation-matrix}

Live edit: [modulation-matrix.md](../live-edit/modulation-matrix.md). Each slot:
**one** Source; **three** Destination / Amount pairs. **`cmd`** / **param** are
**per slot** (and row) — see doc table. All **42** cells hardware-verified
(`30 00 40` / `<part>=0x40`; [`dump-correlate.sh`](../../artifacts/captures/dump-correlate.sh)).

| Control                         | SubCategory | Dump offset | Live edit                                                                  |
| ------------------------------- | ----------- | ----------- | -------------------------------------------------------------------------- |
| Mod Matrix Slot 1 Source        | Slot 1      | `0x0C8`     | `71`/`40` — [Source](../parameter-options.md#mod-matrix-sources)           |
| Mod Matrix Slot 1 Destination 1 | Slot 1      | `0x0C9`     | `71`/`41` — [Destination](../parameter-options.md#mod-matrix-destinations) |
| Mod Matrix Slot 1 Amount 1      | Slot 1      | `0x0CA`     | `71`/`42` — [Amount](../parameter-options.md#mod-matrix-amount)            |
| Mod Matrix Slot 1 Destination 2 | Slot 1      | `0x163`     | `6E`/`5A`                                                                  |
| Mod Matrix Slot 1 Amount 2      | Slot 1      | `0x164`     | `6E`/`5B`                                                                  |
| Mod Matrix Slot 1 Destination 3 | Slot 1      | `0x165`     | `6E`/`5C`                                                                  |
| Mod Matrix Slot 1 Amount 3      | Slot 1      | `0x166`     | `6E`/`5D`                                                                  |
| Mod Matrix Slot 2 Source        | Slot 2      | `0x0CB`     | `71`/`43`                                                                  |
| Mod Matrix Slot 2 Destination 1 | Slot 2      | `0x0CC`     | `71`/`44`                                                                  |
| Mod Matrix Slot 2 Amount 1      | Slot 2      | `0x0CD`     | `71`/`45`                                                                  |
| Mod Matrix Slot 2 Destination 2 | Slot 2      | `0x0CE`     | `71`/`46`                                                                  |
| Mod Matrix Slot 2 Amount 2      | Slot 2      | `0x0CF`     | `71`/`47`                                                                  |
| Mod Matrix Slot 2 Destination 3 | Slot 2      | `0x167`     | `6E`/`5E`                                                                  |
| Mod Matrix Slot 2 Amount 3      | Slot 2      | `0x168`     | `6E`/`5F`                                                                  |
| Mod Matrix Slot 3 Source        | Slot 3      | `0x0D0`     | `71`/`48`                                                                  |
| Mod Matrix Slot 3 Destination 1 | Slot 3      | `0x0D1`     | `71`/`49`                                                                  |
| Mod Matrix Slot 3 Amount 1      | Slot 3      | `0x0D2`     | `71`/`4A`                                                                  |
| Mod Matrix Slot 3 Destination 2 | Slot 3      | `0x0D3`     | `71`/`4B`                                                                  |
| Mod Matrix Slot 3 Amount 2      | Slot 3      | `0x0D4`     | `71`/`4C`                                                                  |
| Mod Matrix Slot 3 Destination 3 | Slot 3      | `0x0D5`     | `71`/`4D`                                                                  |
| Mod Matrix Slot 3 Amount 3      | Slot 3      | `0x0D6`     | `71`/`4E`                                                                  |
| Mod Matrix Slot 4 Source        | Slot 4      | `0x0EF`     | `71`/`67`                                                                  |
| Mod Matrix Slot 4 Destination 1 | Slot 4      | `0x0F0`     | `71`/`68`                                                                  |
| Mod Matrix Slot 4 Amount 1      | Slot 4      | `0x0F1`     | `71`/`69`                                                                  |
| Mod Matrix Slot 4 Destination 2 | Slot 4      | `0x169`     | `6E`/`60`                                                                  |
| Mod Matrix Slot 4 Amount 2      | Slot 4      | `0x16A`     | `6E`/`61`                                                                  |
| Mod Matrix Slot 4 Destination 3 | Slot 4      | `0x16B`     | `6E`/`62`                                                                  |
| Mod Matrix Slot 4 Amount 3      | Slot 4      | `0x16C`     | `6E`/`63`                                                                  |
| Mod Matrix Slot 5 Source        | Slot 5      | `0x0F2`     | `71`/`6A`                                                                  |
| Mod Matrix Slot 5 Destination 1 | Slot 5      | `0x0F3`     | `71`/`6B`                                                                  |
| Mod Matrix Slot 5 Amount 1      | Slot 5      | `0x0F4`     | `71`/`6C`                                                                  |
| Mod Matrix Slot 5 Destination 2 | Slot 5      | `0x16D`     | `6E`/`64`                                                                  |
| Mod Matrix Slot 5 Amount 2      | Slot 5      | `0x16E`     | `6E`/`65`                                                                  |
| Mod Matrix Slot 5 Destination 3 | Slot 5      | `0x16F`     | `6E`/`66`                                                                  |
| Mod Matrix Slot 5 Amount 3      | Slot 5      | `0x170`     | `6E`/`67`                                                                  |
| Mod Matrix Slot 6 Source        | Slot 6      | `0x0F5`     | `71`/`6D`                                                                  |
| Mod Matrix Slot 6 Destination 1 | Slot 6      | `0x0F6`     | `71`/`6E`                                                                  |
| Mod Matrix Slot 6 Amount 1      | Slot 6      | `0x0F7`     | `71`/`6F`                                                                  |
| Mod Matrix Slot 6 Destination 2 | Slot 6      | `0x171`     | `6E`/`68`                                                                  |
| Mod Matrix Slot 6 Amount 2      | Slot 6      | `0x172`     | `6E`/`69`                                                                  |
| Mod Matrix Slot 6 Destination 3 | Slot 6      | `0x173`     | `6E`/`6A`                                                                  |
| Mod Matrix Slot 6 Amount 3      | Slot 6      | `0x174`     | `6E`/`6B`                                                                  |

### Arpeggiator {#arpeggiator}

Live-edit bytes: [arpeggiator.md](../live-edit/arpeggiator.md). Pattern-editor
dump layout: [user pattern in `DUMP_SINGLE`](../live-edit/arpeggiator.md#arpeggiator-user-pattern-dump).
Settings dump offsets hardware-verified (`30 00 40` / `<part>=0x40`).

| Control                        | SubCategory    | Dump offset               | Live edit                                                                                                                                                                                                                                                                                          |
| ------------------------------ | -------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Arpeggiator Mode               | Settings       | `0x097`                   | [`71`/`0F`](../live-edit/arpeggiator.md#arpeggiator-mode-cmd0x71-param-0x0f) — [enum](../parameter-options.md#arpeggiator-mode)                                                                                                                                                                    |
| Arpeggiator Pattern            | Settings       | `0x08A`                   | [`71`/`02`](../live-edit/arpeggiator.md#arpeggiator-pattern-cmd0x71-param-0x02) — [enum](../parameter-options.md#arpeggiator-pattern); hidden when **Mode** Off                                                                                                                                    |
| Arpeggiator Range In Octaves   | Settings       | `0x08B`                   | [`71`/`03`](../live-edit/arpeggiator.md#arpeggiator-octaves-cmd0x71-param-0x03) — [enum](../parameter-options.md#arpeggiator-octaves); hidden when **Mode** Off                                                                                                                                    |
| Arpeggiator Clock / Resolution | Settings       | `0x099`                   | [`71`/`11`](../live-edit/arpeggiator.md#arpeggiator-resolution-cmd0x71-param-0x11) — [enum](../parameter-options.md#arpeggiator-resolution)                                                                                                                                                        |
| Arpeggiator Note Length        | Settings       | `0x08D`                   | [`71`/`05`](../live-edit/arpeggiator.md#arpeggiator-note-length-cmd0x71-param-0x05) — [LCD](../parameter-options.md#arpeggiator-note-length-lcd)                                                                                                                                                   |
| Arpeggiator Swing Factor       | Settings       | `0x08E`                   | [`71`/`06`](../live-edit/arpeggiator.md#arpeggiator-swing-factor-cmd0x71-param-0x06) — [LCD](../parameter-options.md#arpeggiator-swing-factor-lcd)                                                                                                                                                 |
| Arpeggiator Hold Mode          | Settings       | `0x08C`                   | [`71`/`04`](../live-edit/arpeggiator.md#arpeggiator-hold-cmd0x71-param-0x04) — [enum](../parameter-options.md#arpeggiator-hold); panel **Hold**; hidden when **Mode** Off                                                                                                                          |
| Arpeggiator User Pattern Step  | Pattern Editor | `0x18A` + (step−1)×3 … +2 | Step triplet — [length](../live-edit/arpeggiator.md#arpeggiator-step-length-cmd0x6f) / [velocity](../live-edit/arpeggiator.md#arpeggiator-step-velocity-cmd0x6f) / [enable](../live-edit/arpeggiator.md#arpeggiator-step-enable-cmd0x6f) — [map](../parameter-options.md#arpeggiator-step-triplet) |
| Arpeggiator Loop Length        | Pattern Editor | `0x189`                   | [`6E`/`7F`](../live-edit/arpeggiator.md#arpeggiator-loop-length-cmd0x6e-param-0x7f) — [enum](../parameter-options.md#arpeggiator-loop-length); **1**–**32** steps                                                                                                                                  |

### FX 1

Live-edit bytes: [effects.md](../live-edit/effects.md). Dump offsets
hardware-verified on clean **`-INIT-`**
([`dump-correlate-fx.sh`](../../artifacts/captures/dump-correlate-fx.sh),
[`dump-correlate-fx-remaining.sh`](../../artifacts/captures/dump-correlate-fx-remaining.sh)).
Shared Page A chorus bytes (`0x070`–`0x076`) apply across chorus types; type at
**`0x06F`** (`70`/`67`).

| Control                         | SubCategory                   | Dump offset       | Live edit                                                                                                                                                                                                                                                                                                 |
| ------------------------------- | ----------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Character Type                  | Characters                    | `0x123`           | [`6E`/`1A`](../live-edit/effects.md#character-type-cmd0x6e-param-0x1a) — preset types **`01`–`06`** change **Type** only (no other **EDIT FX** rows)                                                                                                                                                      |
| Character Intensity             | Characters                    | `0x01D` / `0x0E9` | Analog Boost [`70`/`15`](../live-edit/effects.md#character-intensity-cmd0x70-param-0x15) → **`0x01D`**; Stereo Widener / Speaker Cabinet [`71`/`61`](../live-edit/effects.md#character-intensity-stereo-widener-cmd0x71-param-0x61) → **`0x0E9`**; [LCD](../parameter-options.md#character-intensity-lcd) |
| Character Tune / Frequency      | Characters                    | `0x029` / `0x0EA` | Analog Boost [`70`/`21`](../live-edit/effects.md#character-frequency-cmd0x70-param-0x21) → **`0x029`**; Stereo Widener / Speaker Cabinet [`71`/`62`](../live-edit/effects.md#character-frequency-stereo-widener-cmd0x71-param-0x62) → **`0x0EA`**                                                         |
| Chorus Type                     | Chorus                        | `0x06F`           | [`70`/`67`](../live-edit/effects.md#chorus-type-cmd0x70-param-0x67) — **`01`–`06`** ([enum](../parameter-options.md#chorus-type))                                                                                                                                                                         |
| Chorus Mix                      | Chorus Classic                | `0x071`           | [`70`/`69`](../live-edit/effects.md#chorus-mix-cmd0x70-param-0x69)                                                                                                                                                                                                                                        |
| Chorus Delay                    | Chorus Classic                | `0x074`           | [`70`/`6C`](../live-edit/effects.md#chorus-delay-cmd0x70-param-0x6c)                                                                                                                                                                                                                                      |
| Chorus Feedback                 | Chorus Classic                | `0x075`           | [`70`/`6D`](../live-edit/effects.md#chorus-feedback-cmd0x70-param-0x6d)                                                                                                                                                                                                                                   |
| Chorus LFO Rate                 | Chorus Classic                | `0x072`           | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                                                                                                                                                                                       |
| Chorus LFO Depth                | Chorus Classic                | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                                                                                                                                                                                      |
| Chorus LFO Shape                | Chorus Classic                | `0x076`           | [`70`/`6E`](../live-edit/effects.md#chorus-lfo-wave-cmd0x70-param-0x6e)                                                                                                                                                                                                                                   |
| Chorus Mix                      | Chorus Vintage                | `0x070`           | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68)                                                                                                                                                                                                                                |
| Chorus X Over                   | Chorus Vintage                | `0x077`           | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                                                                                                                                                                                     |
| Chorus LFO Rate                 | Chorus Vintage                | `0x072`           | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                                                                                                                                                                                       |
| Chorus LFO Depth                | Chorus Vintage                | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                                                                                                                                                                                      |
| Chorus Mix                      | Chorus Hyper                  | `0x070`           | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68)                                                                                                                                                                                                                                |
| Chorus X Over                   | Chorus Hyper                  | `0x077`           | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                                                                                                                                                                                     |
| Chorus Amount                   | Chorus Hyper                  | `0x074`           | [`70`/`6C`](../live-edit/effects.md#chorus-amount-cmd0x70-param-0x6c) — [LCD](../parameter-options.md#chorus-amount-lcd)                                                                                                                                                                                  |
| Chorus LFO Depth                | Chorus Hyper                  | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                                                                                                                                                                                      |
| Chorus X Over                   | Chorus Air                    | `0x077`           | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                                                                                                                                                                                     |
| Chorus LFO Depth                | Chorus Air                    | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                                                                                                                                                                                      |
| Chorus X Over                   | Chorus Vibrato                | `0x077`           | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                                                                                                                                                                                     |
| Chorus LFO Rate                 | Chorus Vibrato                | `0x072`           | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                                                                                                                                                                                       |
| Chorus LFO Depth                | Chorus Vibrato                | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-depth-vibrato-cmd0x70-param-0x6b)                                                                                                                                                                                                                              |
| Chorus Mix                      | Chorus Rotary Speaker         | `0x070`           | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68) — **`0`–`127`**                                                                                                                                                                                                                |
| Chorus Speed                    | Chorus Rotary Speaker         | `0x072`           | [`70`/`6A`](../live-edit/effects.md#chorus-speed-rotary-cmd0x70-param-0x6a)                                                                                                                                                                                                                               |
| Chorus Low/High Balance         | Chorus Rotary Speaker         | `0x075`           | [`70`/`6D`](../live-edit/effects.md#chorus-low-high-balance-rotary-cmd0x70-param-0x6d) — [LCD](../parameter-options.md#chorus-rotary-low-high-balance-lcd)                                                                                                                                                |
| Chorus Mic Angle                | Chorus Rotary Speaker         | `0x074`           | [`70`/`6C`](../live-edit/effects.md#chorus-mic-angle-rotary-cmd0x70-param-0x6c) — [LCD](../parameter-options.md#chorus-rotary-mic-angle-lcd)                                                                                                                                                              |
| Chorus Distance                 | Chorus Rotary Speaker         | `0x073`           | [`70`/`6B`](../live-edit/effects.md#chorus-distance-rotary-cmd0x70-param-0x6b) — [LCD](../parameter-options.md#chorus-rotary-distance-lcd)                                                                                                                                                                |
| Distortion Type                 | Distortion                    | `0x0EC`           | [`71`/`64`](../live-edit/effects.md#distortion-type-cmd0x71-param-0x64) — [enum](../parameter-options.md#distortion-type)                                                                                                                                                                                 |
| Distortion Mix                  | Distortion                    | `0x151`           | [`6E`/`48`](../live-edit/effects.md#distortion-mix-cmd0x6e-param-0x48) — [panel](../parameter-options.md#distortion-panel-visibility)                                                                                                                                                                     |
| Distortion Intensity            | Distortion                    | `0x0ED`           | [`71`/`65`](../live-edit/effects.md#distortion-intensity-cmd0x71-param-0x65) — **Drive** on overdrive **`14`–`19`**                                                                                                                                                                                       |
| Distortion Treble Booster       | Distortion                    | `0x14F`           | [`6E`/`46`](../live-edit/effects.md#distortion-treble-boost-cmd0x6e-param-0x46)                                                                                                                                                                                                                           |
| Distortion High Cut             | Distortion                    | `0x150`           | [`6E`/`47`](../live-edit/effects.md#distortion-high-cut-cmd0x6e-param-0x47) — standard + overdrive                                                                                                                                                                                                        |
| Distortion Quality              | Distortion                    | `0x152`           | [`6E`/`49`](../live-edit/effects.md#distortion-quality-cmd0x6e-param-0x49) — **Bit** / **Rate Reducer**                                                                                                                                                                                                   |
| Distortion Tone                 | Distortion Overdrives         | `0x153`           | [`6E`/`4A`](../live-edit/effects.md#distortion-tone-cmd0x6e-param-0x4a) — **Mint** / **Saffron** / **Onion** / **Pepper**                                                                                                                                                                                 |
| Phaser Mix                      | Phaser                        | `0x0DD`           | [`71`/`55`](../live-edit/effects.md#phaser-mix-cmd0x71-param-0x55) — [LCD](../parameter-options.md#phaser-mix-lcd)                                                                                                                                                                                        |
| Phaser Stages                   | Phaser                        | `0x0DC`           | [`71`/`54`](../live-edit/effects.md#phaser-stages-cmd0x71-param-0x54) — Mix ≠ Off                                                                                                                                                                                                                         |
| Phaser Frequency                | Phaser                        | `0x0E0`           | [`71`/`58`](../live-edit/effects.md#phaser-frequency-cmd0x71-param-0x58) — Mix ≠ Off                                                                                                                                                                                                                      |
| Phaser Feedback (FB)            | Phaser                        | `0x0E1`           | [`71`/`59`](../live-edit/effects.md#phaser-feedback-cmd0x71-param-0x59) — Mix ≠ Off                                                                                                                                                                                                                       |
| Phaser Spread                   | Phaser                        | `0x0E2`           | [`71`/`5A`](../live-edit/effects.md#phaser-spread-cmd0x71-param-0x5a) — Mix ≠ Off                                                                                                                                                                                                                         |
| Phaser LFO Rate                 | Phaser                        | `0x0DE`           | [`71`/`56`](../live-edit/effects.md#phaser-mod-rate-cmd0x71-param-0x56) — **Mod Rate**; Mix ≠ Off                                                                                                                                                                                                         |
| Phaser LFO Depth                | Phaser                        | `0x0DF`           | [`71`/`57`](../live-edit/effects.md#phaser-mod-depth-cmd0x71-param-0x57) — **Mod Depth**; Mix ≠ Off                                                                                                                                                                                                       |
| Filter Bank Type                | Filter Bank                   | `0x11C`           | [`6E`/`13`](../live-edit/effects.md#filter-bank-type-cmd0x6e-param-0x13) — [enum](../parameter-options.md#filter-bank-type)                                                                                                                                                                               |
| Filter Bank Mix / Amount        | Filter Bank                   | `0x11D`           | [`6E`/`14`](../live-edit/effects.md#filter-bank-mix-cmd0x6e-param-0x14) — [LCD](../parameter-options.md#filter-bank-mix-lcd)                                                                                                                                                                              |
| Filter Bank Frequency           | Filter Bank                   | `0x11E`           | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-bipolar-cmd0x6e-param-0x15) bipolar; [Vowel](../live-edit/effects.md#filter-bank-vowel-frequency-cmd0x6e-param-0x15)                                                                                                                            |
| Filter Bank Stereo Phase        | Filter Bank                   | `0x11F`           | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                                                                                                                                                                          |
| Frequency Shifter Left Shape    | Filter Bank Frequency Shifter | `0x120`           | [`6E`/`17`](../live-edit/effects.md#filter-bank-shape-l-cmd0x6e-param-0x17) — **Shape L**                                                                                                                                                                                                                 |
| Frequency Shifter Right Shape   | Filter Bank Frequency Shifter | `0x121`           | [`6E`/`18`](../live-edit/effects.md#filter-bank-shape-r-cmd0x6e-param-0x18) — **Shape R**                                                                                                                                                                                                                 |
| Filter Bank Frequency / Vowel   | Filter Bank Vowel Filter      | `0x11E`           | [`6E`/`15`](../live-edit/effects.md#filter-bank-vowel-frequency-cmd0x6e-param-0x15) — [glyphs](../parameter-options.md#filter-bank-vowel-frequency)                                                                                                                                                       |
| Filter Bank Resonance           | Filter Bank Vowel Filter      | `0x122`           | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19) — [LCD](../parameter-options.md#filter-bank-resonance-lcd)                                                                                                                                                                  |
| Filter Bank Stereo Phase        | Filter Bank Vowel Filter      | `0x11F`           | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                                                                                                                                                                          |
| Filter Bank Frequency           | Filter Bank Comb Filter       | `0x11E`           | [`6E`/`15`](../live-edit/effects.md#filter-bank-comb-frequency-cmd0x6e-param-0x15) — [C0..C8](../parameter-options.md#filter-bank-comb-frequency)                                                                                                                                                         |
| Filter Bank Resonance           | Filter Bank Comb Filter       | `0x122`           | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19) — [LCD](../parameter-options.md#filter-bank-resonance-lcd)                                                                                                                                                                  |
| Filter Bank Stereo Phase        | Filter Bank Comb Filter       | `0x11F`           | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                                                                                                                                                                          |
| Filter Bank Frequency           | Filter Bank 1-6 Pole XFade    | `0x11E`           | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-direct-cmd0x6e-param-0x15) — **`0`–`127`**                                                                                                                                                                                                      |
| Filter Bank Resonance           | Filter Bank 1-6 Pole XFade    | `0x122`           | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19)                                                                                                                                                                                                                             |
| Filter Type                     | Filter Bank 1-6 Pole XFade    | `0x120`           | [`6E`/`17`](../live-edit/effects.md#filter-bank-filter-type-cmd0x6e-param-0x17) — [XFade type](../parameter-options.md#filter-bank-xfade-filter-type)                                                                                                                                                     |
| Filter Bank Frequency           | Filter Bank VariSlopes        | `0x11E`           | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-direct-cmd0x6e-param-0x15)                                                                                                                                                                                                                      |
| Filter Bank Resonance           | Filter Bank VariSlopes        | `0x122`           | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19)                                                                                                                                                                                                                             |
| Filter Bank Filter Poles        | Filter Bank VariSlopes        | `0x120`           | [`6E`/`17`](../live-edit/effects.md#filter-bank-poles-cmd0x6e-param-0x17) — [Poles LCD](../parameter-options.md#filter-bank-varislope-poles-lcd)                                                                                                                                                          |
| Filter Bank Filter Slope        | Filter Bank VariSlopes        | `0x121`           | [`6E`/`18`](../live-edit/effects.md#filter-bank-slope-cmd0x6e-param-0x18) — [Slope](../parameter-options.md#filter-bank-varislope-slope)                                                                                                                                                                  |
| EQ Low Gain (db)                | Equalizer                     | `0x0E7`           | [`71`/`5F`](../live-edit/effects.md#eq-low-gain-cmd0x71-param-0x5f) — **−16..+16 dB**, **Off** @ **`40`**                                                                                                                                                                                                 |
| EQ Low Frequency (Hz)           | Equalizer                     | `0x0B5`           | [`71`/`2D`](../live-edit/effects.md#eq-low-frequency-cmd0x71-param-0x2d) — **32..458 Hz**                                                                                                                                                                                                                 |
| EQ Mid Gain (db)                | Equalizer                     | `0x0E4`           | [`71`/`5C`](../live-edit/effects.md#eq-mid-gain-cmd0x71-param-0x5c) — same as [Low Gain](../parameter-options.md#eq-low-gain)                                                                                                                                                                             |
| EQ Mid Frequency (Hz)           | Equalizer                     | `0x0E5`           | [`71`/`5D`](../live-edit/effects.md#eq-mid-frequency-cmd0x71-param-0x5d) — **19 Hz..24.0 kHz**                                                                                                                                                                                                            |
| EQ Mid Q-Factor                 | Equalizer                     | `0x0E6`           | [`71`/`5E`](../live-edit/effects.md#eq-mid-q-factor-cmd0x71-param-0x5e) — **0.28..15.4**                                                                                                                                                                                                                  |
| EQ High Gain (db)               | Equalizer                     | `0x0E8`           | [`71`/`60`](../live-edit/effects.md#eq-high-gain-cmd0x71-param-0x60) — same as [Low Gain](../parameter-options.md#eq-low-gain)                                                                                                                                                                            |
| EQ High Frequency (Hz)          | Equalizer                     | `0x0B6`           | [`71`/`2E`](../live-edit/effects.md#eq-high-frequency-cmd0x71-param-0x2e) — **1831 Hz..24.0 kHz**                                                                                                                                                                                                         |
| Input Follower Select           | Envelope Follower             | `0x0AE`           | [`71`/`26`](../live-edit/effects.md#input-follower-input-select-cmd0x71-param-0x26) — [enum](../parameter-options.md#input-follower-input-select)                                                                                                                                                         |
| Input Follower Sensitivity      | Envelope Follower             | `0x040`           | [`70`/`38`](../live-edit/effects.md#input-follower-sensitivity-cmd0x70-param-0x38) — **0..100 %** when **Input Select** ≠ Off                                                                                                                                                                             |
| Input Follower Envelope Attack  | Envelope Follower             | `0x03E`           | [`70`/`36`](../live-edit/effects.md#input-follower-attack-cmd0x70-param-0x36) — **0..127** when **Input Select** ≠ Off                                                                                                                                                                                    |
| Input Follower Envelope Release | Envelope Follower             | `0x042`           | [`70`/`3A`](../live-edit/effects.md#input-follower-release-cmd0x70-param-0x3a) — **0..127** when **Input Select** ≠ Off                                                                                                                                                                                   |
| Input Mode                      | Input                         | `0x205`           | `6F` / `0x7C` (Off `00`, Dynamic `01`, Static `02`; visible when Atomizer Off)                                                                                                                                                                                                                            |
| Input Select                    | Input                         | `0x206`           | `6F` / `0x7D` (Left `00`, L+R `01`, Right `02`; when Mode Dynamic/Static)                                                                                                                                                                                                                                 |
| Input Atomizer                  | Input                         | `0x207`           | `6F` / `0x7E` (beat-synced input looper preset; Off `00`, On `01`, **2**–**16** `02`–`10`) — [Inputs](../live-edit/edit-single.md#inputs-edit-single)                                                                                                                                                     |

### FX 2

Live-edit bytes: [effects.md](../live-edit/effects.md). Dump offsets
hardware-verified on clean **`-INIT-`** (`30 00 40` / `<part>=0x40`;
[`dump-correlate-fx.sh`](../../artifacts/captures/dump-correlate-fx.sh)).

| Control                            | SubCategory        | Dump offset | Live edit                                                                                                                                       |
| ---------------------------------- | ------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Delay Send                         | Delay              | `0x079`     | [`70`/`71`](../live-edit/effects.md#delay-send-cmd0x70-param-0x71) — [LCD](../parameter-options.md#delay-send-lcd)                              |
| Delay Type                         | Delay              | `0x113`     | [`6E`/`0A`](../live-edit/effects.md#delay-type-cmd0x6e) — [enum](../parameter-options.md#delay-type)                                            |
| Delay Mode                         | Delay              | `0x078`     | [`70`/`70`](../live-edit/effects.md#delay-mode-cmd0x70-param-0x70) — [Mode](../parameter-options.md#delay-mode); **`01`–`16`**                  |
| Delay Clock                        | Delay              | `0x09C`     | [`71`/`14`](../parameter-options.md#delay-clock) — Simple/Ping Pong modes                                                                       |
| Delay Time (ms)                    | Delay              | `0x07A`     | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — Classic + **Clock** Off; tape **Time**                                |
| Delay Feedback                     | Delay              | `0x07B`     | [`70`/`73`](../live-edit/effects.md#delay-feedback) — Classic **0..100 %**, Tape **0..200 %**                                                   |
| Delay Coloration                   | Delay              | `0x07F`     | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — [Coloration](../parameter-options.md#delay-coloration) (Classic) |
| Delay LFO Rate                     | Delay              | `0x07C`     | [`70`/`74`](../live-edit/effects.md#delay-lfo-rate-cmd0x70-param-0x74)                                                                          |
| Delay LFO Depth                    | Delay              | `0x07D`     | [`70`/`75`](../live-edit/effects.md#delay-lfo-depth-cmd0x70-param-0x75)                                                                         |
| Delay LFO Shape                    | Delay              | `0x07E`     | [`70`/`76`](../live-edit/effects.md#delay-lfo-wave-cmd0x70-param-0x76)                                                                          |
| Delay Tape Delay Clock Left        | Delay Tape Clocked | `0x116`     | [`6E`/`0D`](../live-edit/effects.md#delay-tape-left-clock-cmd0x6e) — [Left Clock](../parameter-options.md#delay-tape-left-clock)                |
| Delay Tape Delay Clock Right       | Delay Tape Clocked | `0x117`     | [`6E`/`0E`](../live-edit/effects.md#delay-tape-right-clock-cmd0x6e) — [Right Clock](../parameter-options.md#delay-tape-right-clock)             |
| Delay Tape Delay Feedback          | Delay Tape Clocked | `0x07B`     | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                              |
| Delay Tape Delay Center Frequency  | Delay Tape Clocked | `0x07F`     | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — **`0`–`127`**                                                    |
| Delay Tape Delay Bandwidth         | Delay Tape Clocked | `0x11A`     | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                    |
| Delay Tape Delay Modulation        | Delay Tape Clocked | `0x07D`     | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75)                                                                   |
| Delay Tape Delay Ratio             | Delay Tape Free    | `0x115`     | [`6E`/`0C`](../live-edit/effects.md#delay-tape-ratio-cmd0x6e) — [Ratio](../parameter-options.md#delay-tape-ratio)                               |
| Delay Tape Delay Time (ms)         | Delay Tape Free    | `0x07A`     | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — [Time](../parameter-options.md#delay-tape-time)                       |
| Delay Tape Delay Feedback          | Delay Tape Free    | `0x07B`     | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                              |
| Delay Tape Delay Center Frequency  | Delay Tape Free    | `0x07F`     | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — **`0`–`127`**                                                    |
| Delay Tape Delay Bandwidth         | Delay Tape Free    | `0x11A`     | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                    |
| Delay Tape Delay Modulation        | Delay Tape Free    | `0x07D`     | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75)                                                                   |
| Delay Tape Delay Ratio             | Delay Tape Doppler | `0x115`     | [`6E`/`0C`](../live-edit/effects.md#delay-tape-ratio-cmd0x6e) — same as Tape Free                                                               |
| Delay Tape Delay Time (ms)         | Delay Tape Doppler | `0x07A`     | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — [Time](../parameter-options.md#delay-tape-time)                       |
| Delay Tape Delay Feedback          | Delay Tape Doppler | `0x07B`     | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                              |
| Delay Tape Delay Center Frequency  | Delay Tape Doppler | `0x07F`     | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — [Frequency](../parameter-options.md#delay-tape-frequency)        |
| Delay Tape Delay Bandwidth         | Delay Tape Doppler | `0x11A`     | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11) — [Bandwidth](../parameter-options.md#delay-tape-bandwidth)        |
| Delay Tape Delay Modulation        | Delay Tape Doppler | `0x07D`     | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75) — [Modulation](../parameter-options.md#delay-tape-modulation)     |
| Reverb Send                        | Reverb             | `0x10B`     | [`6E`/`02`](../live-edit/effects.md#reverb-send-cmd0x6e) — [LCD](../parameter-options.md#reverb-send-lcd)                                       |
| Reverb Mode                        | Reverb             | `0x10A`     | [`6E`/`01`](../live-edit/effects.md#reverb-mode-cmd0x6e) — **`00`–`03`**                                                                        |
| Reverb Type                        | Reverb             | `0x10C`     | [`6E`/`03`](../live-edit/effects.md#reverb-type-cmd0x6e)                                                                                        |
| Reverb Time                        | Reverb             | `0x10D`     | [`6E`/`04`](../live-edit/effects.md#reverb-time-cmd0x6e) — **0..127**                                                                           |
| Reverb Damping                     | Reverb             | `0x10E`     | [`6E`/`05`](../live-edit/effects.md#reverb-damping-cmd0x6e) — **0..100.0 %**                                                                    |
| Reverb Coloration                  | Reverb             | `0x10F`     | [`6E`/`06`](../live-edit/effects.md#reverb-coloration-cmd0x6e) — **−64..+63**                                                                   |
| Reverb Predelay                    | Reverb             | `0x110`     | [`6E`/`07`](../live-edit/effects.md#reverb-predelay-cmd0x6e) — **0.0..500.0 ms**; **Clock** Off                                                 |
| Reverb Feedback                    | Reverb             | `0x112`     | [`6E`/`09`](../live-edit/effects.md#reverb-feedback-cmd0x6e) — **Feedback 1/2** only                                                            |
| Reverb Clock                       | Reverb             | `0x111`     | [`6E`/`08`](../live-edit/effects.md#reverb-clock-cmd0x6e) — same map as [Delay Clock](../parameter-options.md#delay-clock)                      |
| Vocoder Mode                       | Vocoder            | `0x0AF`     | [`71`/`27`](../live-edit/effects.md#vocoder-mode-cmd0x71-param-0x27) — [enum](../parameter-options.md#vocoder-mode)                             |
| Vocoder Amount of Synthesis Bands  | Vocoder            | `0x042`     | [`70`/`3A`](../live-edit/effects.md#vocoder-bands-cmd0x70-param-0x3a) — [Bands](../parameter-options.md#vocoder-bands)                          |
| Vocoder Balance (Dry-Wet)          | Vocoder            | `0x038`     | [`70`/`30`](../live-edit/effects.md#vocoder-balance-cmd0x70-param-0x30) — modes **`01`–`06`                                                     |
| Vocoder Spectral Balance           | Vocoder            | `0x041`     | [`70`/`39`](../live-edit/effects.md#vocoder-spectral-balance-cmd0x70-param-0x39)                                                                |
| Vocoder Envelope Attack            | Vocoder            | `0x03E`     | [`70`/`36`](../live-edit/effects.md#vocoder-carrier-attack-cmd0x70-param-0x36) — **Carrier Attack**                                             |
| Vocoder Envelope Release           | Vocoder            | `0x03F`     | [`70`/`37`](../live-edit/effects.md#vocoder-carrier-release-cmd0x70-param-0x37) — **Carrier Release**                                           |
| Vocoder Carrier Center Frequency   | Vocoder            | `0x030`     | [`70`/`28`](../live-edit/effects.md#vocoder-center-freq-cmd0x70-param-0x28) — **Center Freq**                                                   |
| Vocoder Carrier Frequency Spread   | Vocoder            | `0x037`     | [`70`/`2F`](../live-edit/effects.md#vocoder-spread-cmd0x70-param-0x2f) — **Spread**                                                             |
| Vocoder Carrier Q-Factor           | Vocoder            | `0x033`     | [`70`/`2B`](../live-edit/effects.md#vocoder-q-factor-cmd0x70-param-0x2b) — **Q-Factor**                                                         |
| Vocoder Modulator Frequency Offset | Vocoder            | `0x031`     | [`70`/`29`](../live-edit/effects.md#vocoder-mod-offset-cmd0x70-param-0x29) — **Mod Offset**                                                     |
| Vocoder Modulator Input            | Vocoder            | `0x0AF`     | [Mode](../parameter-options.md#vocoder-mode) **`04`** In L / **`05`** In L+R / **`06`** In R — same byte as **Mode**                            |

### Common

| Control                            | SubCategory          | Dump offset            | Live edit                                                                                                                              |
| ---------------------------------- | -------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Unison Voices                      | Edit Single → Unison | `0x201`                | `6F` / `0x78` — **Edit Single → Unison → Voices**; Off `00`, Twin `01`, **3**–**8** `02`–`07` (**not** `70`/`61` / CC-as-param)        |
| Unison Detune                      | Edit Single → Unison | `0x202`                | `6F` / `0x79` — panel visible when Voices ≥ Twin; **0..127** `stored = lcd`                                                            |
| Unison Pan Spread                  | Edit Single → Unison | `0x203`                | `6F` / `0x7A` — **0.0..100.0 %** (`× 100 / 128`, `7F` → 100 %)                                                                         |
| Unison LFO Phase Offset            | Edit Single → Unison | `0x204`                | `6F` / `0x7B` — **−64..+63** → `ui+64`                                                                                                 |
| Transpose / Patch Transpose        | Common Parameters    | `0x065`                | `70` / `0x5D` (CC 93) — **−64..+63** → `ui+64` — [Transpose](edit-single.md#transpose--patch-transpose-0x5d-cmd0x70--cc-93)            |
| ~~Part Detune~~                    | —                    | —                      | **Multi** detune (`0x72`/`0x26`) — not Edit Single; CSV lists VC Common access only                                                    |
| Multi Tempo / Master Clock         | Common Parameters    | `0x18` in `DUMP_MULTI` | `72` / `0x0F` — **63..190** bpm → `stored = bpm - 63` — [Multi Tempo](edit-single.md#multi-tempo--master-clock-0x0f-cmd0x72)           |
| Parameter Smooth Mode              | Common Parameters    | `0x0A1`                | `71` / `0x19` — [Control Smooth Mode / clock quantize](../parameter-options.md#control-smooth-mode--clock-quantize)                    |
| Oscillator Section Keyboard Mode   | Common Parameters    | `0x066`                | `70`/`0x5E` or CC 94                                                                                                                   |
| Patch Volume                       | Common Parameters    | `0x063`                | `70` / `0x5B` (CC 91) — **0..127** direct — [Patch Volume](edit-single.md#patch-volume-0x5b-cmd0x70--cc-91)                            |
| Panorama                           | Common Parameters    | `0x012`                | `70` / `0x0A` (CC 10) — **−64..+63** → `ui+64` — [Panorama](edit-single.md#panorama-0x0a-cmd0x70--cc-10)                               |
| Bend Down                          | Pitch Bender         | `0x0A3`                | `71` / `0x1B` — **−64..+63** → `ui+64` — [Bend Down](edit-single.md#bend-down-0x1b-cmd0x71)                                            |
| Bend Up                            | Pitch Bender         | `0x0A2`                | `71` / `0x1A` — same encoding — [Bend Up](edit-single.md#bend-up-0x1a-cmd0x71)                                                         |
| Bender Scale                       | Pitch Bender         | `0x0A4`                | `71` / `0x1C` — [Bender Scale](../parameter-options.md#bender-scale) — [live](edit-single.md#bender-scale-0x1c-cmd0x71)                |
| Patch Category 1                   | Category             | `0x103`                | `71` / `0x7B` — [Patch name categories](../parameter-options.md#patch-name-categories) (**Name Cat 1**)                                |
| Patch Category 2                   | Category             | `0x104`                | `71` / `0x7C` — same list (**Name Cat 2**) — [Categories](edit-single.md#categories-edit-single)                                       |
| Surround Channel Balance           | Output               | `0x0C2`                | `71` / `0x3A` (−64..+63, `ui+64`) — [Surround Balance](edit-single.md#balance-0x3a-cmd0x71; also mod dest **116**)                     |
| Multi Part Parameter Output Select | Output               | **Not in dump**        | **`73` / `0x2D`** — **Edit Single → Surround → Output** — [Secondary output routing](../parameter-options.md#secondary-output-routing) |
| Soft Knob 1 Function As…           | Soft Knobs           | `0x0C6`                | `71` / `0x3E` — [Soft Knob Destinations](../parameter-options.md#soft-knob-destinations) (wire `<value>` ≠ index)                      |
| Soft Knob 1 Name                   | Soft Knobs           | `0x0BB`                | `71` / `0x33` — [Soft Knob Names](../parameter-options.md#soft-knob-names); LCD label above knob 1                                     |
| Soft Knob 2 Function As…           | Soft Knobs           | `0x0C7`                | `71` / `0x3F` — same destination list — [Soft Knobs](edit-single.md#soft-knobs-edit-single)                                            |
| Soft Knob 2 Name                   | Soft Knobs           | `0x0BC`                | `71` / `0x34` — [Soft Knob Names](../parameter-options.md#soft-knob-names)                                                             |
| Soft Knob 3 Function As…           | Soft Knobs           | `0x0C8`                | `71` / `0x40` — same wire as [Mod Matrix slot 1 Source](#modulation-matrix) (`71`/`40`)                                                |
| Soft Knob 3 Name                   | Soft Knobs           | `0x0BD`                | `71` / `0x35` — [Soft Knob Names](../parameter-options.md#soft-knob-names)                                                             |

### Patch Utility - Config

Patch utility / I/O config; likely not in `DUMP_SINGLE`.

| Control         | SubCategory                  | Dump offset     | Live edit                                                                                      |
| --------------- | ---------------------------- | -----------     | ---------                                                                                      |
| USB Audio Mode  | Input / Output Configuration | **Not in dump** | `73` / `0x09` — [USB Audio Mode](../live-edit/edit-config.md#usb-audio-mode-0x09); **RX** only |
| Surround Output | Input / Output Configuration |                 |                                                                                                |
| Master Volume   | Input / Output Configuration |                 |                                                                                                |

### Patch Utility - Remote

Remote template UI; not a synth parameter.

| Control                               | SubCategory      | Dump offset | Live edit |
| ------------------------------------- | ---------------- | ----------- | --------- |
| Remote Template Configuration Ability | Remote Templates |             |           |

### Global

Global settings — see [edit-config.md](../live-edit/edit-config.md). Not stored
in `DUMP_SINGLE`. Rows below are legacy inventory placeholders; **panel-only**
CONFIG (no SysEx on TI mk2) is omitted — documented only when a wire byte is
confirmed in `edit-config.md`.

| Control                                    | SubCategory    | Dump offset     | Live edit                                                                                                                           |
| ------------------------------------------ | -------------- | -----------     | --------------------------------------------------------------------------------------                                              |
| LED Mode                                   | Hardware Panel |                 |                                                                                                                                     |
| LED Brightness (Lux) - TI Series Only      | Hardware Panel |                 |                                                                                                                                     |
| BPM Brightness (Lux) - TI Series Only      | Hardware Panel |                 |                                                                                                                                     |
| LCD Contrast                               | Hardware Panel |                 |                                                                                                                                     |
| Memory Protect                             | Memory / RAM   |                 |                                                                                                                                     |
| Sync Clock to External Host toggle         | MIDI           |                 |                                                                                                                                     |
| Master Clock / Global Tempo                | MIDI           |                 |                                                                                                                                     |
| MIDI Clock Source                          | MIDI           |                 |                                                                                                                                     |
| MIDI Destination                           | MIDI           |                 |                                                                                                                                     |
| MIDI Device ID                             | MIDI           |                 |                                                                                                                                     |
| Global MIDI Channel                        | MIDI           |                 |                                                                                                                                     |
| MIDI Volume Receive (RX) toggle            | MIDI           | **Not in dump** | `73` / `0x57` — [Global MIDI Volume RX](../live-edit/edit-config.md#global-midi-volume-rx-0x57); **RX** only                        |
| Program Change Receive (RX) toggle         | MIDI           |                 |                                                                                                                                     |
| MIDI Control Page A toggle                 | MIDI           |                 |                                                                                                                                     |
| MIDI Control Page B toggle                 | MIDI           |                 |                                                                                                                                     |
| Arpeggiator to MIDI Out / Note Send toggle | MIDI           |                 |                                                                                                                                     |
| All Argpeggiators toggle                   | FX             |                 |                                                                                                                                     |
| All Delays                                 | FX             |                 |                                                                                                                                     |
| All Reverbs                                | FX             |                 |                                                                                                                                     |
| All EQs                                    | FX             |                 |                                                                                                                                     |
| Knob Response                              | Knobs          |                 | [`73`/`75`](../live-edit/edit-config.md#knob-response-0x75) — **RX** only; no panel TX                                              |
| Keyboard Local Mode / Control              | Global         |                 |                                                                                                                                     |
| Keyboard Channel Mode                      | Global         |                 |                                                                                                                                     |
| Keyboard Transpose                         | Global         |                 |                                                                                                                                     |
| Keyboard Aftertouch Sensitivity            | Global         |                 |                                                                                                                                     |
| Modwheel Assign                            | Global         |                 |                                                                                                                                     |
| Pedal 1 Assign                             | Global         |                 |                                                                                                                                     |
| Pedal 2 Assign                             | Global         |                 |                                                                                                                                     |
| Master Tuning                              | Global         |                 |                                                                                                                                     |
| Pure Tuning                                | Global         |                 |                                                                                                                                     |
| Input Source                               | In / Out       | **Not in dump** | `73` / `0x2B` — [Input Source](../live-edit/edit-config.md#input-source-0x2b); **RX** only                                          |
| Input Characteristic                       | In / Out       | **Not in dump** | `73` / `0x1D` — [Input Characteristic](../live-edit/edit-config.md#input-characteristic-0x1d); **RX** only                          |
| Input Direct Thru                          | In / Out       | **Not in dump** | `73` / `0x5A` — **`0`–`127`** `stored = lcd` — [Input Direct Thru](../live-edit/edit-config.md#input-direct-thru-0x5a); **RX** only |
| Input Boost                                | In / Out       | **Not in dump** | `73` / `0x5B` — **`00`** Off, **`01`–`7F`** level — [Input Boost](../live-edit/edit-config.md#input-boost-0x5b); **RX** only        |
| Input Sensitivity (CONFIG)                 | In / Out       | **Not in dump** | `73` / `0x1F` — [Input Sensitivity](../live-edit/edit-config.md#input-sensitivity-0x1f); **RX** only                                |

## Known / unknowns at this stage

- **Known**
- Single dumps are **fixed‑size 524‑byte** SysEx messages.
- **Arrangement** exports: **16** singles after the multi; **slot `0x08`**
 = zero-based part index **`0x00`–`0x0F`** (confirmed on
 `init-multi-arrangement.syx`).
- Checksum at **`0x209`**; sum payload from **`0x09`** per formula above.
- The **patch name** appears as an ASCII sequence near offset 0xFA, padded to
 a fixed length with spaces.
- The final byte before `F7` behaves like a **checksum byte**.
- **405** UI controls are listed in [Single parameter
 map](#single-parameter-map)
 for byte /
 live-edit correlation (Multi parameters →
 [arrangements.md](arrangements.md#multi-parameter-map); excluding Flash ROM,
 X/Y Pad, and Browser).
- **Unknown (to be refined with more examples)**
- Exact mapping from payload offsets to GUI parameters.
- Meaning of **`0x09`–`0x0B`** (`0C 10 00` vs `0C 00 00`) beyond “TI header”.
- Trailer bytes at **`0x204`–`0x208`** (`7F 40 00 01 00 00`).

Future work: compare additional Single dumps (small, targeted parameter
changes) and record byte deltas in the parameter map.
