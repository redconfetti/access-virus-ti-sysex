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
`(device + 0x10 + bank + slot + sum(bytes 0x09..0x208)) & 0x7F`  
(same as [waf80.md](../waf80.md) classic formula with payload starting at
`0x09`).

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
  - Dense, non‑ASCII data, assumed to contain:
    - Oscillator, mixer, filter, envelope, LFO and matrix parameters
    - FX / EQ / reverb / chorus / global edit‑menu parameters
  - Exact field boundaries within this block are not yet mapped, but this block
    is where most sound‑shaping values live.
- **~0xF8–0x103 – Patch name and nearby globals**
  - Contains the ASCII patch name `-INIT-` padded with spaces:
    - The ASCII sequence `2d 49 4e 49 54 2d 20 20 20`
      (`-INIT-` padded with spaces)
      appears near offset 0xFA.
  - Surrounding bytes likely hold category and other global Single attributes.
- **0x204–0x209 – Trailer metadata + checksum**
  - Checksum at **`0x209`**; trailer bytes before it include `7F 40 00 01 00 00`
    (arrangement Part 1: `… 66 F7`).

## Single parameter map

Parameter inventory (control names and categories). **Excluded:** Flash ROM banks,
Assignable X/Y Pad, and Browser (Patch Saving / Patch Browsing).

Most rows are **Single-program** parameters to correlate with
`DUMP_SINGLE` bytes and live-edit SysEx. Fill **Dump offset** and
**Live edit** as mappings are confirmed. Enum option lists:
[parameter-options.md](../parameter-options.md).

Multi edit parameters are in
[Multi parameter map](arrangements.md#multi-parameter-map).

**413** controls in **11** categories.

### Oscillators

| Control                                | SubCategory                  | Dump offset   | Live edit                                                                                                                                                                |
| -------------------------------------- | ---------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sub Oscillator Waveform Shape          | Sub-Osc                      |               | `70` / `0x23` (CC 35; Square `00`, Triangle `01` only)                                                                                                                   |
| Oscillator 1 Model / Mode              | Oscillator 1                 |               | `6E` / `0x1E` (see live-edit by mode)                                                                                                                                    |
| Oscillator 1 Detune in Semitone        | Oscillator 1                 |               | `70` / `0x14` (−48..+48, `ui+64`)                                                                                                                                        |
| Oscillator 1 Keyfollow                 | Oscillator 1                 |               | `70` / `0x15` (Classic; Norm @ +32)                                                                                                                                      |
| Velocity --> Osc1 Waveform Shape       | Oscillator 1                 |               | `71` / `0x2F` (Velocity Map **Osc 1 Shape**; ±100 % — [Velocity Map](../live-edit/edit-single.md#velocity-map-edit-single)                                               |
| Oscillator 1 Waveform Shape            | Oscillator 1 Classic         |               | `70` / `0x11` (`00`–`7F`; see live-edit)                                                                                                                                 |
| Oscillator 1 Wave Select               | Oscillator 1 Classic         |               | `70` / `0x13` (64 waves `00`–`3F`)                                                                                                                                       |
| Oscillator 1 Pulsewidth                | Oscillator 1 Classic         |               |                                                                                                                                                                          |
| Oscillator 1 Density                   | Oscillator 1 Hypersaw        |               |                                                                                                                                                                          |
| Oscillator 1 Local Detune              | Oscillator 1 Hypersaw        | `70` / `0x12` | **0..127** `stored = lcd` (Hypersaw; Classic `12` = Pulse Width)                                                                                                         |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 1 Hypersaw        | `70` / `0x1B` | **0..127** when Sync On; `stored = lcd`                                                                                                                                  |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable       | `70` / `0x13` | Index **0–99** → `00`–`63`; names in [parameter-options.md](../parameter-options.md#wavetable-names)                                                                     |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable       | `70` / `0x11` | **0..127** `stored = lcd` (mode `02`; not Shape/Density)                                                                                                                 |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable       | `6E` / `0x2C` | **0..127** `stored = lcd` (not `70`/`2C` Filter Env)                                                                                                                     |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable PWM   | `70` / `0x13` | **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--wavetable-pwm)                                                                                 |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable PWM   | `70` / `0x11` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Pulsewidth                | Oscillator 1 Wavetable PWM   | `70` / `0x12` | **0..127** `stored = lcd` (not Classic 50–100 %)                                                                                                                         |
| Oscillator 1 Local Detune              | Oscillator 1 Wavetable PWM   | `6E` / `0x2B` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable PWM   | `6E` / `0x2C` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Simple    | `70` / `0x13` | **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--grain-simple)                                                                                  |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Simple    | `70` / `0x11` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Simple    | `6E` / `0x2A` | F-Shift **−64..+63** → `ui+64` (not `70`/`2A` Resonance)                                                                                                                 |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Simple    | `6E` / `0x2C` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Complex   | `70` / `0x13` | **`00`–`63`** enum; [live-edit](../live-edit/oscillators.md#oscillator-1--grain-complex)                                                                                 |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Complex   | `70` / `0x11` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Complex   | `6E` / `0x2A` | F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Formant Spread            | Oscillator 1 Grain Complex   | `6E` / `0x25` | F-Spread **0..127** → `stored = lcd`                                                                                                                                     |
| Oscillator 1 Local Detune              | Oscillator 1 Grain Complex   | `6E` / `0x2B` | **0..127** → `stored = lcd`                                                                                                                                              |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Complex   | `6E` / `0x2C` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Simple  | `70` / `0x13` | Same enum as Wavetable mode                                                                                                                                              |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Simple  | `70` / `0x11` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Simple  | `6E` / `0x2A` | F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Simple  | `6E` / `0x2C` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Complex | `70` / `0x13` | Same enum as Wavetable mode                                                                                                                                              |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Complex | `70` / `0x11` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Complex | `6E` / `0x2A` | F-Shift **−64..+63** → `ui+64`                                                                                                                                           |
| Oscillator 1 Formant Spread            | Oscillator 1 Formant Complex | `6E` / `0x25` | F-Spread **0..127** → `stored = lcd`                                                                                                                                     |
| Oscillator 1 Local Detune              | Oscillator 1 Formant Complex | `6E` / `0x2B` | **0..127** → `stored = lcd`                                                                                                                                              |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Complex | `6E` / `0x2C` | **0..127** `stored = lcd`                                                                                                                                                |
| Oscillator 2 Model / Mode              | Oscillator 2                 |               | `6E` / `0x23` (Classic `00`, Hypersaw `01`, Wavetable `02`, Wavetable PWM `03`, Grain Simple `04`, Grain Complex `05`, Formant Simple `06`, Formant Complex `07`)        |
| Oscillator 2 Detune in Semitone        | Oscillator 2                 |               | `70` / `0x19` (−48..+48, `ui+64`)                                                                                                                                        |
| Oscillator 2 Fine Detune               | Oscillator 2                 |               | `70` / `0x1A` (Detune **0..127**, `stored = lcd`)                                                                                                                        |
| Oscillator 2 Keyfollow                 | Oscillator 2                 |               | `70` / `0x1F` (−64..+63, Norm @ +32)                                                                                                                                     |
| Velocity --> Osc2 Waveform Shape       | Oscillator 2                 |               | `71` / `0x30` (Velocity Map **Osc 2 Shape**; ±100 %)                                                                                                                     |
| Oscillator 2 Waveform Shape            | Oscillator 2 Classic         |               | `70` / `0x16` (Spectral Wave `00`; expected Classic Shape table)                                                                                                         |
| Oscillator 2 Wave Select               | Oscillator 2 Classic         |               | `70` / `0x18` (Sine `00`; expected 64 waves `00`–`3F`)                                                                                                                   |
| Oscillator 2 Pulsewidth                | Oscillator 2 Classic         |               | `70` / `0x17` (expected Classic PW when Shape ≥ `40`)                                                                                                                    |
| Oscillator 2 Density                   | Oscillator 2 Hypersaw        |               | `70` / `0x16` (Hypersaw; **1.0..9.0**, same curve as Osc 1 Hypersaw Density)                                                                                             |
| Oscillator 2 Local Detune              | Oscillator 2 Hypersaw        |               | `70` / `0x17` (Hypersaw; **0..127** `stored = lcd`)                                                                                                                      |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 2 Hypersaw        |               | `70` / `0x1B` (**0..127** when Sync On; `stored = lcd`; same slot as Classic FM Amount)                                                                                  |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable       |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable       |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable       |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable PWM   |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable PWM   |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Pulsewidth                | Oscillator 2 Wavetable PWM   |               | `70` / `0x17` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Wavetable PWM   |               | `6E` / `0x3F` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable PWM   |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Simple    |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Simple    |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Simple    |               | `6E` / `0x3E` (**−64..+63** → `stored = ui + 64`)                                                                                                                        |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Simple    |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Complex   |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Complex   |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Complex   |               | `6E` / `0x3E` (**−64..+63** → `stored = ui + 64`)                                                                                                                        |
| Oscillator 2 Formant Spread            | Oscillator 2 Grain Complex   |               | `6E` / `0x39` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Grain Complex   |               | `6E` / `0x3F` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Complex   |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Simple  |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Simple  |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Simple  |               | `6E` / `0x3E` (**−64..+63** → `stored = ui + 64`)                                                                                                                        |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Simple  |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Complex |               | `70` / `0x18` (**`00`–`63`** enum; Sine..Domina7rix)                                                                                                                     |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Complex |               | `70` / `0x16` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Complex |               | `6E` / `0x3E` (**−64..+63** → `stored = ui + 64`)                                                                                                                        |
| Oscillator 2 Formant Spread            | Oscillator 2 Formant Complex |               | `6E` / `0x39` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Local Detune              | Oscillator 2 Formant Complex |               | `6E` / `0x3F` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Complex |               | `6E` / `0x40` (**0..127** `stored = lcd`)                                                                                                                                |
| Oscillator 3 Model                     | Oscillator 3                 |               | `71` / `0x29` (Mode/Wave; Off `00`, Slave `01`, Saw `02`, Pulse `03`, Sine `04`, Triangle `05`, Wave 3..64 `06`–`43`)                                                    |
| Oscillator 3 Detune in Semitone        | Oscillator 3                 |               | `71` / `0x2B` (visible for Mode/Wave `02`–`43`; **−48..+48**, `ui+64`)                                                                                                   |
| Oscillator 3 Fine Detune               | Oscillator 3                 |               | `71` / `0x2C` (visible for Mode/Wave `02`–`43`; panel **0..−127**, `stored = −ui`)                                                                                       |
| Oscillator 1 Sync (2>1)                | Oscillator Common            |               | `70` / `0x1C` (Osc 2 Classic Sync; Off `00`, On `01`)                                                                                                                    |
| Filter Envelope --> Oscillator 2 Pitch | Oscillator Common            |               | `70` / `0x1D` (Osc 2 Classic/Hypersaw/Wavetable/Wavetable PWM/Grain Simple/Grain Complex/Formant Simple/Formant Complex; **−100 %** `00`, **0 %** `40`, **+100 %** `7F`) |
| Oscillator Section Initial Phase       | Oscillator Common            |               | `71` / `0x23` (Phase Init; Off `00`, **1..127** direct)                                                                                                                  |
| Velocity --> Pulsewidth                | Oscillator Common            |               | `71` / `0x31` (Velocity Map **Pulse Width**; ±100 %)                                                                                                                     |
| Patch Common Portamento                | Oscillator Common            |               | `70` / `0x05` (CC 5; Off `00`, **1..127** direct `stored = lcd`)                                                                                                         |
| Oscillator 2 FM Amount                 | Oscillator Common FM         |               | `70` / `0x1B` (Classic **Sync Off:** 0.0..100.0 %; **Sync On:** Sync Frequency **0..127**; other modes **0..127** direct)                                                |
| Filter Envelope --> FM                 | Oscillator Common FM         |               | `70` / `0x1E` (**Sync Off** / no Sync: **FilterEnv>FM**; Classic/Hypersaw **Sync On:** same wire = **FilterEnv>Sync**; **−100..+100 %** like `1D`)                       |
| Velocity --> FM Amount                 | Oscillator Common FM         |               | `71` / `0x32` (Velocity Map **FM Amount**; ±100 %)                                                                                                                       |
| Oscillator 2 FM Mode                   | Oscillator Common FM         |               | `71` / `0x22` enum; Classic `00`–`06`, Wavetable/Wavetable PWM/Grain Simple/Grain Complex/Formant Simple/Formant Complex **FreqMod** `00`, **PhaseMod** `01`             |
| Sync Amount / X-Sync Frequency         | Oscillator Common Sync       |               |                                                                                                                                                                          |
| Velocity --> FM / Sync                 | Oscillator Common Sync       |               |                                                                                                                                                                          |
| Filter Envelope --> X-Sync             | Oscillator Common Sync       |               | `70` / `0x1E` when **Sync On** (panel **FilterEnv>Sync**; same wire as FilterEnv>FM)                                                                                     |
| Unison Mode                            | Unison                       |               | `70` / `0x61` (CC 97 **Voices**; Off `00`, Twin `01`, **3**–**8** `02`–`07`)                                                                                             |
| Unison Detune                          | Unison                       |               | `70` / `0x62` (CC 98; **0..127** when Voices ≥ Twin; `stored = lcd`)                                                                                                     |
| Unison Panorama Spread                 | Unison                       |               | `70` / `0x63` (CC 99 **Pan Spread**; **0.0..100.0 %**, always visible; likely `× 100 / 128`, `7F` → 100 %)                                                               |
| Unison LFO Phase Offset                | Unison                       |               | `70` / `0x64` (CC 100; **−64..+63** → `ui+64`; panel TBD)                                                                                                                |
| Noise Oscillator Volume                | Noise                        |               | `70` / `0x25` (CC 37; Off `00`, **1..127** direct `stored = lcd`)                                                                                                        |
| Noise Color                            | Noise                        |               | `70` / `0x27` (**−64..+63** → `stored = ui + 64`)                                                                                                                        |
| Oscillator Punch Intensity             | Punch                        |               | `71` / `0x24` (**0.0..100.0 %**; `pct = stored × 100 / 128`, `7F` → 100.0 %; LCD swap at `04`/`05`)                                                                      |
| Oscillator 1/2 Balance                 | Mixer                        |               | `70` / `0x21` (−100..+100 %)                                                                                                                                             |
| Oscillator 3 Volume                    | Mixer                        |               | `71` / `0x2A` (visible for Osc 3 Mode/Wave `02`–`43`; **0..127** `stored = lcd`)                                                                                         |
| Sub Oscillator Volume                  | Sub-Osc                      |               | `70` / `0x22` (CC 34; **0..127** direct `stored = lcd`)                                                                                                                  |
| Oscillator Section Volume / Saturation | Mixer                        |               | `70` / `0x24` (Osc Volume / Saturation menu, **−64..+63**); Mixer section volume uses `71` / `0x7F`                                                                      |
| Ring Modulator Volume                  | Mixer                        |               | `70` / `0x26` (CC 38; Off `00`, **1..127** direct `stored = lcd`)                                                                                                        |

### Filters

| Control                               | SubCategory                | Dump offset | Live edit                                                                       |
| ------------------------------------- | -------------------------- | ----------- | ------------------------------------------------------------------------------- |
| Filter 1 Mode                         | Filter 1                   |             | `70` / `0x33`                                                                   |
| Filter 1 Envelope Amount              | Filter 1                   |             | `70` / `0x2C`                                                                   |
| Filter 1 Envelope Polarity            | Filter 1                   |             | `71` / `0x1E`                                                                   |
| Filter 1 Cutoff                       | Filter 1                   |             | `70` / `0x28`                                                                   |
| Filter 1 Resonance                    | Filter 1                   |             | `70` / `0x2A`                                                                   |
| Filter 1 Keyfollow                    | Filter 1                   |             | `70` / `0x2E`                                                                   |
| ~~Analog Mode On/Off Toggle~~         | —                          | —           | **N/A** — analog types are **Filter 1 Mode** values (`04`–`07` Analog * Pole)   |
| Filter 2 Mode                         | Filter 2                   |             | `70` / `0x34` (4 modes `00`–`03` only)                                          |
| Filter 2 Envelope Amount              | Filter 2                   |             | `70` / `0x2D` (linear %)                                                        |
| Filter 2 Envelope Polarity            | Filter 2                   |             | `71` / `0x1F`                                                                   |
| ~~Filter 2 Cutoff~~                   | —                          | —           | **N/A** on TI — no separate F2 cutoff; use **Offset** vs F1                     |
| Filter 2 Offset                       | Filter 2                   |             | `70` / `0x29` (bipolar `ui+64`)                                                 |
| Filter 2 Resonance                    | Filter 2                   |             | `70` / `0x2B` (direct 0–127)                                                    |
| Filter 2 Keyfollow                    | Filter 2                   |             | `70` / `0x2F` (bipolar `ui+64`)                                                 |
| Oscillator Section Volume             | Filter Common              |             | `70` / `0x24` (Saturation menu; bipolar `ui+64`)                                |
| Filter Routing                        | Filter Common              |             | `70` / `0x35` (4 routing modes)                                                 |
| Voice Saturation Type / Curve         | Filter Common              |             | **N/A** on TI Saturation menu (only Osc Volume)                                 |
| Filter knob target (Res / Env Amt)    | Filter Common              |             | [`71`/`7A`](../live-edit/filters.md#filters-select) — **SELECT** (`00` F1 … `02` F1+F2) |
| Filter Keyfollow Base                 | Filter Common              |             | `71` / `0x21` (C-1..G9)                                                         |
| Filter Cutoff Link toggle             | Filter Common              |             | `71` / `0x20`                                                                   |
| ~~Filter Link toggle~~                | Filter Common              | —           | Unconfirmed — may differ from **knob target** `7A`                              |
| Filter Balance                        | Filter Common              |             | `70` / `0x30` (bipolar `ui+64`)                                                 |
| Pan Spread                            | Filter Common              |             | `6E` / `0x7A` (Split routing only)                                              |
| Filter Envelope Select                | Filter / Aux Envelopes     |             |                                                                                 |
| Filter Envelope Attack                | Filter / Aux Envelopes     |             | `70` / `0x36` (Filter 1 ADSR menu)                                              |
| Filter Envelope Decay                 | Filter / Aux Envelopes     |             | `70` / `0x37`                                                                   |
| Filter Envelope Sustain               | Filter / Aux Envelopes     |             | `70` / `0x38` (linear %)                                                        |
| Filter Envelope Sustain Slope         | Filter / Aux Envelopes     |             | `70` / `0x39` (bipolar `ui+64`)                                                 |
| Filter Envelope Release               | Filter / Aux Envelopes     |             | `70` / `0x3A`                                                                   |
| Envelope 3 Attack                     | Filter / Aux Envelopes     |             | `6E` / `0x50` (**0..127** `stored = lcd`)                                       |
| Envelope 3 Decay                      | Filter / Aux Envelopes     |             | `6E` / `0x51` (**0..127** `stored = lcd`)                                       |
| Envelope 3 Sustain                    | Filter / Aux Envelopes     |             | `6E` / `0x52` (**0..100.0 %** → `round(pct × 127 / 100)`)                       |
| Envelope 3 Sustain Slope              | Filter / Aux Envelopes     |             | `6E` / `0x53` (**−64..+63** → `ui + 64`)                                        |
| Envelope 3 Release                    | Filter / Aux Envelopes     |             | `6E` / `0x54` (**0..127** `stored = lcd`)                                       |
| Envelope 4 Attack                     | Filter / Aux Envelopes     |             | `6E` / `0x55` (**0..127** `stored = lcd`)                                       |
| Envelope 4 Decay                      | Filter / Aux Envelopes     |             | `6E` / `0x56` (**0..127** `stored = lcd`)                                       |
| Envelope 4 Sustain                    | Filter / Aux Envelopes     |             | `6E` / `0x57` (**0..100.0 %** → `round(pct × 127 / 100)`)                       |
| Envelope 4 Sustain Slope              | Filter / Aux Envelopes     |             | `6E` / `0x58` (**−64..+63** → `ui + 64`)                                        |
| Envelope 4 Release                    | Filter / Aux Envelopes     |             | `6E` / `0x59` (**0..127** `stored = lcd`)                                       |
| Amplifier Envelope Attack             | Amplifier Envelope         |             | `70` / `0x3B`                                                                   |
| Amplifier Envelope Decay              | Amplifier Envelope         |             | `70` / `0x3C`                                                                   |
| Amplifier Envelope Sustain            | Amplifier Envelope         |             | `70` / `0x3D` (linear %)                                                        |
| Amplifier Envelope Sustain Slope      | Amplifier Envelope         |             | `70` / `0x3E` (bipolar `ui+64`)                                                 |
| Amplifier Envelope Release            | Amplifier Envelope         |             | `70` / `0x3F`                                                                   |
| Velocity --> Filter 1 Envelope Amount | Velocity / Filter Envelope |             | `71` / `0x36` (±100 % — [Velocity Map](edit-single.md#velocity-map-edit-single) |
| Velocity --> Filter 1 Resonance       | Velocity / Filter Envelope |             | `71` / `0x38` (±100 %)                                                          |
| Velocity --> Filter 2 Envelope Amount | Velocity / Filter Envelope |             | `71` / `0x37` (±100 %)                                                          |
| Velocity --> Filter 2 Resonance       | Velocity / Filter Envelope |             | `71` / `0x39` (±100 %)                                                          |
| Velocity --> Volume                   | Velocity / Amplifier       |             | `71` / `0x3C` (±100 %)                                                          |
| Velocity --> Panorama                 | Velocity / Amplifier       |             | `71` / `0x3D` (±100 %)                                                          |
| Patch Volume                          | Amplifier                  |             | CC 91                                                                           |
| Patch Panorama                        | Amplifier                  |             | Same as Common **Panorama** — `70` / `0x0A`                                     |

### LFO

| Control                                            | SubCategory      | Dump offset | Live edit |
| -------------------------------------------------- | ---------------- | ----------- | --------- |
| LFO 1 Rate                                         | LFO 1            |             |           |
| LFO 1 Clock Divider                                | LFO 1            |             |           |
| LFO 1 Clock Switch toggle                          | LFO 1            |             |           |
| LFO 1 Keyfollow                                    | LFO 1            |             |           |
| LFO 1 Trigger Phase                                | LFO 1            |             |           |
| LFO 1 Waveform Shape                               | LFO 1            |             |           |
| LFO 1 Waveform Contour                             | LFO 1            |             |           |
| LFO 1 Mode                                         | LFO 1            |             |           |
| LFO 1 Envelope Mode toggle                         | LFO 1            |             |           |
| LFO 1 --> Osc 1                                    | LFO Modulation 1 |             |           |
| LFO 1 --> Osc 2                                    | LFO Modulation 1 |             |           |
| LFO 1 to Oscillator 1&2 lock                       | LFO Modulation 1 |             |           |
| LFO 1 --> Pulsewidth                               | LFO Modulation 1 |             |           |
| LFO 1 --> Filter Resonance 1+2                     | LFO Modulation 1 |             |           |
| LFO 1 --> Filter Envelope Gain / Filter Gain Depth | LFO Modulation 1 |             |           |
| LFO 1 User Destination                             | LFO Modulation 1 |             |           |
| LFO 1 User Destination Amount                      | LFO Modulation 1 |             |           |
| LFO 2 Rate                                         | LFO 2            |             |           |
| LFO 2 Clock Divider                                | LFO 2            |             |           |
| LFO 2 Clock Switch toggle                          | LFO 2            |             |           |
| LFO 2 Keyfollow                                    | LFO 2            |             |           |
| LFO 2 Trigger Phase                                | LFO 2            |             |           |
| LFO 2 Waveform Shape                               | LFO 2            |             |           |
| LFO 2 Waveform Contour                             | LFO 2            |             |           |
| LFO 2 Mode                                         | LFO 2            |             |           |
| LFO 2 Envelope Mode toggle                         | LFO 2            |             |           |
| LFO 2 --> Filter Cutoff 1                          | LFO Modulation 2 |             |           |
| LFO 2 --> Filter Cutoff 2                          | LFO Modulation 2 |             |           |
| LFO 2 to Filter 1&2 lock                           | LFO Modulation 2 |             |           |
| LFO 2 --> Shape 1+2 Depth                          | LFO Modulation 2 |             |           |
| LFO 2 --> Panorama                                 | LFO Modulation 2 |             |           |
| LFO 2 --> FM Amount                                | LFO Modulation 2 |             |           |
| LFO 2 User Destination                             | LFO Modulation 2 |             |           |
| LFO 2 User Destination Amount                      | LFO Modulation 2 |             |           |
| LFO 3 Rate                                         | LFO 3            |             |           |
| LFO 3 Clock Divider                                | LFO 3            |             |           |
| LFO 3 Clock Switch toggle                          | LFO 3            |             |           |
| LFO 3 Keyfollow                                    | LFO 3            |             |           |
| LFO 3 Waveform Shape                               | LFO 3            |             |           |
| LFO 3 Mode                                         | LFO 3            |             |           |
| LFO 3 Fade In Time                                 | LFO 3            |             |           |
| LFO 3 User Destination                             | LFO Modulation 3 |             |           |
| LFO 3 User Destination Amount                      | LFO Modulation 3 |             |           |

### Modulation Matrix

| Control                           | SubCategory | Dump offset | Live edit |
| --------------------------------- | ----------- | ----------- | --------- |
| Mod Matrix Slot 1-6 Source        | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Destination 1 | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Amount 1      | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Destination 2 | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Amount 2      | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Destination 3 | Slot 1-6    |             |           |
| Mod Matrix Slot 1-6 Amount 3      | Slot 1-6    |             |           |

### Arpeggiator {#arpeggiator}

Live-edit bytes: [arpeggiator.md](../live-edit/arpeggiator.md). **Dump offsets**:
**TBD**.

| Control                              | SubCategory    | Dump offset | Live edit |
| ------------------------------------ | -------------- | ----------- | --------- |
| Arpeggiator Mode                     | Settings       |             | [`71`/`0F`](../live-edit/arpeggiator.md#arpeggiator-mode-cmd0x71-param-0x0f) — [enum](../parameter-options.md#arpeggiator-mode) |
| Arpeggiator Pattern                  | Settings       |             | [`71`/`02`](../live-edit/arpeggiator.md#arpeggiator-pattern-cmd0x71-param-0x02) — [enum](../parameter-options.md#arpeggiator-pattern); hidden when **Mode** Off |
| Arpeggiator Range In Octaves         | Settings       |             | [`71`/`03`](../live-edit/arpeggiator.md#arpeggiator-octaves-cmd0x71-param-0x03) — [enum](../parameter-options.md#arpeggiator-octaves); hidden when **Mode** Off |
| Arpeggiator Clock / Resolution       | Settings       |             | [`71`/`11`](../live-edit/arpeggiator.md#arpeggiator-resolution-cmd0x71-param-0x11) — [enum](../parameter-options.md#arpeggiator-resolution) |
| Arpeggiator Note Length              | Settings       |             | [`71`/`05`](../live-edit/arpeggiator.md#arpeggiator-note-length-cmd0x71-param-0x05) — [LCD](../parameter-options.md#arpeggiator-note-length-lcd) |
| Arpeggiator Swing Factor             | Settings       |             | [`71`/`06`](../live-edit/arpeggiator.md#arpeggiator-swing-factor-cmd0x71-param-0x06) — [LCD](../parameter-options.md#arpeggiator-swing-factor-lcd) |
| Arpeggiator Hold Mode                | Settings       |             | [`71`/`04`](../live-edit/arpeggiator.md#arpeggiator-hold-cmd0x71-param-0x04) — [enum](../parameter-options.md#arpeggiator-hold); panel **Hold**; hidden when **Mode** Off |
| Arpeggiator User Pattern Step        | Pattern Editor |             |           |
| Arpeggiator Offset Direction Buttons | Pattern Editor |             |           |
| Arpeggiator Step Random Button       | Pattern Editor |             |           |
| Arpeggiator Velocity Random Button   | Pattern Editor |             |           |
| Arpeggiator Length Random Button     | Pattern Editor |             |           |
| Arpeggiator Loop Length              | Pattern Editor |             |           |

### FX 1

Live-edit bytes: [effects.md](../live-edit/effects.md). **Dump offsets** for FX
rows: still **TBD**.

| Control                         | SubCategory                   | Dump offset | Live edit                                                                                                                                        |
| ------------------------------- | ----------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Character Type                  | Characters                    |             | [`6E`/`1A`](../live-edit/effects.md#character-type-cmd0x6e-param-0x1a)                                                                          |
| Character Intensity             | Characters                    |             | Analog Boost [`70`/`15`](../live-edit/effects.md#character-intensity-cmd0x70-param-0x15); Stereo Widener / Speaker Cabinet [`71`/`61`](../live-edit/effects.md#character-intensity-stereo-widener-cmd0x71-param-0x61); [LCD](../parameter-options.md#character-intensity-lcd) |
| Character Tune / Frequency      | Characters                    |             | Analog Boost [`70`/`21`](../live-edit/effects.md#character-frequency-cmd0x70-param-0x21); Stereo Widener / Speaker Cabinet [`71`/`62`](../live-edit/effects.md#character-frequency-stereo-widener-cmd0x71-param-0x62) |
| Chorus Type                     | Chorus                        |             | [`70`/`67`](../live-edit/effects.md#chorus-type-cmd0x70-param-0x67) — **`01`–`06`** ([enum](../parameter-options.md#chorus-type))               |
| Chorus Mix                      | Chorus Classic                |             | [`70`/`69`](../live-edit/effects.md#chorus-mix-cmd0x70-param-0x69)                                                                               |
| Chorus Delay                    | Chorus Classic                |             | [`70`/`6C`](../live-edit/effects.md#chorus-delay-cmd0x70-param-0x6c)                                                                            |
| Chorus Feedback                 | Chorus Classic                |             | [`70`/`6D`](../live-edit/effects.md#chorus-feedback-cmd0x70-param-0x6d)                                                                         |
| Chorus LFO Rate                 | Chorus Classic                |             | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                              |
| Chorus LFO Depth                | Chorus Classic                |             | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                             |
| Chorus LFO Shape                | Chorus Classic                |             | [`70`/`6E`](../live-edit/effects.md#chorus-lfo-wave-cmd0x70-param-0x6e)                                                                          |
| Chorus Mix                      | Chorus Vintage                |             | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68)                                                                        |
| Chorus X Over                   | Chorus Vintage                |             | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                            |
| Chorus LFO Rate                 | Chorus Vintage                |             | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                              |
| Chorus LFO Depth                | Chorus Vintage                |             | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                             |
| Chorus Mix                      | Chorus Hyper                  |             | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68)                                                                        |
| Chorus X Over                   | Chorus Hyper                  |             | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                            |
| Chorus Amount                   | Chorus Hyper                  |             | [`70`/`6C`](../live-edit/effects.md#chorus-amount-cmd0x70-param-0x6c) — [LCD](../parameter-options.md#chorus-amount-lcd)                          |
| Chorus LFO Depth                | Chorus Hyper                  |             | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                             |
| Chorus X Over                   | Chorus Air                    |             | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                            |
| Chorus LFO Depth                | Chorus Air                    |             | [`70`/`6B`](../live-edit/effects.md#chorus-depth-cmd0x70-param-0x6b)                                                                             |
| Chorus X Over                   | Chorus Vibrato                |             | [`70`/`6F`](../live-edit/effects.md#chorus-x-over-cmd0x70-param-0x6f)                                                                            |
| Chorus LFO Rate                 | Chorus Vibrato                |             | [`70`/`6A`](../live-edit/effects.md#chorus-rate-cmd0x70-param-0x6a)                                                                              |
| Chorus LFO Depth                | Chorus Vibrato                |             | [`70`/`6B`](../live-edit/effects.md#chorus-depth-vibrato-cmd0x70-param-0x6b)                                                                     |
| Chorus Mix                      | Chorus Rotary Speaker         |             | [`70`/`68`](../live-edit/effects.md#chorus-mix-vintage-cmd0x70-param-0x68) — **`0`–`127`**                                                         |
| Chorus Speed                    | Chorus Rotary Speaker         |             | [`70`/`6A`](../live-edit/effects.md#chorus-speed-rotary-cmd0x70-param-0x6a)                                                                      |
| Chorus Low/High Balance         | Chorus Rotary Speaker         |             | [`70`/`6D`](../live-edit/effects.md#chorus-low-high-balance-rotary-cmd0x70-param-0x6d) — [LCD](../parameter-options.md#chorus-rotary-low-high-balance-lcd) |
| Chorus Mic Angle                | Chorus Rotary Speaker         |             | [`70`/`6C`](../live-edit/effects.md#chorus-mic-angle-rotary-cmd0x70-param-0x6c) — [LCD](../parameter-options.md#chorus-rotary-mic-angle-lcd)       |
| Chorus Distance                 | Chorus Rotary Speaker         |             | [`70`/`6B`](../live-edit/effects.md#chorus-distance-rotary-cmd0x70-param-0x6b) — [LCD](../parameter-options.md#chorus-rotary-distance-lcd)         |
| Distortion Type                 | Distortion                    |             | [`71`/`64`](../live-edit/effects.md#distortion-type-cmd0x71-param-0x64) — [enum](../parameter-options.md#distortion-type)                         |
| Distortion Mix                  | Distortion                    |             | [`6E`/`48`](../live-edit/effects.md#distortion-mix-cmd0x6e-param-0x48) — [panel](../parameter-options.md#distortion-panel-visibility)              |
| Distortion Intensity            | Distortion                    |             | [`71`/`65`](../live-edit/effects.md#distortion-intensity-cmd0x71-param-0x65) — **Drive** on overdrive **`14`–`19`**                                 |
| Distortion Treble Booster       | Distortion                    |             | [`6E`/`46`](../live-edit/effects.md#distortion-treble-boost-cmd0x6e-param-0x46)                                                                     |
| Distortion High Cut             | Distortion                    |             | [`6E`/`47`](../live-edit/effects.md#distortion-high-cut-cmd0x6e-param-0x47) — standard + overdrive                                                   |
| Distortion Quality              | Distortion                    |             | [`6E`/`49`](../live-edit/effects.md#distortion-quality-cmd0x6e-param-0x49) — **Bit** / **Rate Reducer**                                             |
| Distortion Tone                 | Distortion Overdrives         |             | [`6E`/`4A`](../live-edit/effects.md#distortion-tone-cmd0x6e-param-0x4a) — **Mint** / **Saffron** / **Onion** / **Pepper**                          |
| Phaser Mix                      | Phaser                        |             | [`71`/`55`](../live-edit/effects.md#phaser-mix-cmd0x71-param-0x55) — [LCD](../parameter-options.md#phaser-mix-lcd)                                 |
| Phaser Stages                   | Phaser                        |             | [`71`/`54`](../live-edit/effects.md#phaser-stages-cmd0x71-param-0x54) — Mix ≠ Off                                                                |
| Phaser Frequency                | Phaser                        |             | [`71`/`58`](../live-edit/effects.md#phaser-frequency-cmd0x71-param-0x58) — Mix ≠ Off                                                             |
| Phaser Feedback (FB)            | Phaser                        |             | [`71`/`59`](../live-edit/effects.md#phaser-feedback-cmd0x71-param-0x59) — Mix ≠ Off                                                                |
| Phaser Spread                   | Phaser                        |             | [`71`/`5A`](../live-edit/effects.md#phaser-spread-cmd0x71-param-0x5a) — Mix ≠ Off                                                                 |
| Phaser LFO Rate                 | Phaser                        |             | [`71`/`56`](../live-edit/effects.md#phaser-mod-rate-cmd0x71-param-0x56) — **Mod Rate**; Mix ≠ Off                                                 |
| Phaser LFO Depth                | Phaser                        |             | [`71`/`57`](../live-edit/effects.md#phaser-mod-depth-cmd0x71-param-0x57) — **Mod Depth**; Mix ≠ Off                                                |
| Filter Bank Type                | Filter Bank                   |             | [`6E`/`13`](../live-edit/effects.md#filter-bank-type-cmd0x6e-param-0x13) — [enum](../parameter-options.md#filter-bank-type)                      |
| Filter Bank Mix / Amount        | Filter Bank                   |             | [`6E`/`14`](../live-edit/effects.md#filter-bank-mix-cmd0x6e-param-0x14) — [LCD](../parameter-options.md#filter-bank-mix-lcd)                      |
| Filter Bank Frequency           | Filter Bank                   |             | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-bipolar-cmd0x6e-param-0x15) bipolar; [Vowel](../live-edit/effects.md#filter-bank-vowel-frequency-cmd0x6e-param-0x15) |
| Filter Bank Stereo Phase        | Filter Bank                   |             | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                   |
| Frequency Shifter Left Shape    | Filter Bank Frequency Shifter |             | [`6E`/`17`](../live-edit/effects.md#filter-bank-shape-l-cmd0x6e-param-0x17) — **Shape L**                                                          |
| Frequency Shifter Right Shape   | Filter Bank Frequency Shifter |             | [`6E`/`18`](../live-edit/effects.md#filter-bank-shape-r-cmd0x6e-param-0x18) — **Shape R**                                                         |
| Filter Bank Frequency / Vowel   | Filter Bank Vowel Filter      |             | [`6E`/`15`](../live-edit/effects.md#filter-bank-vowel-frequency-cmd0x6e-param-0x15) — [glyphs](../parameter-options.md#filter-bank-vowel-frequency) |
| Filter Bank Resonance           | Filter Bank Vowel Filter      |             | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19) — [LCD](../parameter-options.md#filter-bank-resonance-lcd)          |
| Filter Bank Stereo Phase        | Filter Bank Vowel Filter      |             | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                   |
| Filter Bank Frequency           | Filter Bank Comb Filter       |             | [`6E`/`15`](../live-edit/effects.md#filter-bank-comb-frequency-cmd0x6e-param-0x15) — [C0..C8](../parameter-options.md#filter-bank-comb-frequency) |
| Filter Bank Resonance           | Filter Bank Comb Filter       |             | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19) — [LCD](../parameter-options.md#filter-bank-resonance-lcd)          |
| Filter Bank Stereo Phase        | Filter Bank Comb Filter       |             | [`6E`/`16`](../live-edit/effects.md#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                                   |
| Filter Bank Frequency           | Filter Bank 1-6 Pole XFade    |             | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-direct-cmd0x6e-param-0x15) — **`0`–`127`**                                                |
| Filter Bank Resonance           | Filter Bank 1-6 Pole XFade    |             | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19)                                                                      |
| Filter Type                     | Filter Bank 1-6 Pole XFade    |             | [`6E`/`17`](../live-edit/effects.md#filter-bank-filter-type-cmd0x6e-param-0x17) — [XFade type](../parameter-options.md#filter-bank-xfade-filter-type) |
| Filter Bank Frequency           | Filter Bank VariSlopes        |             | [`6E`/`15`](../live-edit/effects.md#filter-bank-frequency-direct-cmd0x6e-param-0x15)                                                                 |
| Filter Bank Resonance           | Filter Bank VariSlopes        |             | [`6E`/`19`](../live-edit/effects.md#filter-bank-resonance-cmd0x6e-param-0x19)                                                                      |
| Filter Bank Filter Poles        | Filter Bank VariSlopes        |             | [`6E`/`17`](../live-edit/effects.md#filter-bank-poles-cmd0x6e-param-0x17) — [Poles LCD](../parameter-options.md#filter-bank-varislope-poles-lcd)   |
| Filter Bank Filter Slope        | Filter Bank VariSlopes        |             | [`6E`/`18`](../live-edit/effects.md#filter-bank-slope-cmd0x6e-param-0x18) — [Slope](../parameter-options.md#filter-bank-varislope-slope)         |
| EQ Low Gain (db)                | Equalizer                     |             | [`71`/`5F`](../live-edit/effects.md#eq-low-gain-cmd0x71-param-0x5f) — **−16..+16 dB**, **Off** @ **`40`**                                          |
| EQ Low Frequency (Hz)           | Equalizer                     |             | [`71`/`2D`](../live-edit/effects.md#eq-low-frequency-cmd0x71-param-0x2d) — **32..458 Hz**                                                          |
| EQ Mid Gain (db)                | Equalizer                     |             | [`71`/`5C`](../live-edit/effects.md#eq-mid-gain-cmd0x71-param-0x5c) — same as [Low Gain](../parameter-options.md#eq-low-gain)                       |
| EQ Mid Frequency (Hz)           | Equalizer                     |             | [`71`/`5D`](../live-edit/effects.md#eq-mid-frequency-cmd0x71-param-0x5d) — **19 Hz..24.0 kHz**                                                      |
| EQ Mid Q-Factor                 | Equalizer                     |             | [`71`/`5E`](../live-edit/effects.md#eq-mid-q-factor-cmd0x71-param-0x5e) — **0.28..15.4**                                                            |
| EQ High Gain (db)               | Equalizer                     |             | [`71`/`60`](../live-edit/effects.md#eq-high-gain-cmd0x71-param-0x60) — same as [Low Gain](../parameter-options.md#eq-low-gain)                      |
| EQ High Frequency (Hz)          | Equalizer                     |             | [`71`/`2E`](../live-edit/effects.md#eq-high-frequency-cmd0x71-param-0x2e) — **1831 Hz..24.0 kHz**                                                   |
| Input Follower Select           | Envelope Follower             |             | [`6E`/`26`](../live-edit/effects.md#input-follower-input-select-cmd0x6e-param-0x26) — [enum](../parameter-options.md#input-follower-input-select) |
| Input Follower Sensitivity      | Envelope Follower             |             | [`6E`/`38`](../live-edit/effects.md#input-follower-sensitivity-cmd0x6e-param-0x38) — **0..100 %** when **Input Select** ≠ Off                  |
| Input Follower Envelope Attack  | Envelope Follower             |             | [`6E`/`36`](../live-edit/effects.md#input-follower-attack-cmd0x6e-param-0x36) — **0..127** when **Input Select** ≠ Off                          |
| Input Follower Envelope Release | Envelope Follower             |             | [`6E`/`3A`](../live-edit/effects.md#input-follower-release-cmd0x6e-param-0x3a) — **0..127** when **Input Select** ≠ Off                          |
| Input Mode                      | Input                         |             | `6F` / `0x7C` (Off `00`, Dynamic `01`, Static `02`; visible when Atomizer Off)                                                                   |
| Input Select                    | Input                         |             | `6F` / `0x7D` (Left `00`, L+R `01`, Right `02`; when Mode Dynamic/Static)                                                                        |
| Input Atomizer                  | Input                         |             | `6F` / `0x7E` (beat-synced input looper preset; Off `00`, On `01`, **2**–**16** `02`–`10`) — [Inputs](../live-edit/edit-single.md#inputs-edit-single) |

### FX 2

Live-edit bytes: [effects.md](../live-edit/effects.md). **Dump offsets**: **TBD**.

| Control                                 | SubCategory        | Dump offset | Live edit                                                                                                                                          |
| --------------------------------------- | ------------------ | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| FX Delay Switch                         | Delay              |             | No TI mk2 **EDIT FX** control                                                                                                                        |
| Delay Send                              | Delay              |             | [`70`/`71`](../live-edit/effects.md#delay-send-cmd0x70-param-0x71) — [LCD](../parameter-options.md#delay-send-lcd)                              |
| Delay Type                              | Delay              |             | [`6E`/`0A`](../live-edit/effects.md#delay-type-cmd0x6e) — [enum](../parameter-options.md#delay-type)                                              |
| Delay Mode                              | Delay              |             | [`70`/`70`](../live-edit/effects.md#delay-mode-cmd0x70-param-0x70) — [Mode](../parameter-options.md#delay-mode); **`01`–`16`**                    |
| Delay Clock                             | Delay              |             | [`71`/`14`](../parameter-options.md#delay-clock) — Simple/Ping Pong modes                                                                        |
| Delay Time (ms)                         | Delay              |             | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — Classic + **Clock** Off; tape **Time**                                 |
| Delay Feedback                          | Delay              |             | [`70`/`73`](../live-edit/effects.md#delay-feedback) — Classic **0..100 %**, Tape **0..200 %**                                                     |
| Delay Coloration                        | Delay              |             | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — [Coloration](../parameter-options.md#delay-coloration) (Classic) |
| Delay LFO Rate                          | Delay              |             | [`70`/`74`](../live-edit/effects.md#delay-lfo-rate-cmd0x70-param-0x74)                                                                           |
| Delay LFO Depth                         | Delay              |             | [`70`/`75`](../live-edit/effects.md#delay-lfo-depth-cmd0x70-param-0x75)                                                                           |
| Delay LFO Shape                         | Delay              |             | [`70`/`76`](../live-edit/effects.md#delay-lfo-wave-cmd0x70-param-0x76)                                                                           |
| Delay Tape Delay Clock Left             | Delay Tape Clocked |             | [`6E`/`0D`](../live-edit/effects.md#delay-tape-left-clock-cmd0x6e) — [Left Clock](../parameter-options.md#delay-tape-left-clock)                  |
| Delay Tape Delay Clock Right            | Delay Tape Clocked |             | [`6E`/`0E`](../live-edit/effects.md#delay-tape-right-clock-cmd0x6e) — [Right Clock](../parameter-options.md#delay-tape-right-clock)               |
| Delay Tape Delay Feedback               | Delay Tape Clocked |             | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                                |
| Delay Tape Delay Center Frequency       | Delay Tape Clocked |             | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — **`0`–`127`**                                                      |
| Delay Tape Delay Bandwidth              | Delay Tape Clocked |             | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                      |
| Delay Tape Delay Modulation             | Delay Tape Clocked |             | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75)                                                                     |
| Delay Tape Delay Ratio                  | Delay Tape Free    |             | [`6E`/`0C`](../live-edit/effects.md#delay-tape-ratio-cmd0x6e) — [Ratio](../parameter-options.md#delay-tape-ratio)                                 |
| Delay Tape Delay Time (ms)              | Delay Tape Free    |             | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — [Time](../parameter-options.md#delay-tape-time)                        |
| Delay Tape Delay Feedback               | Delay Tape Free    |             | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                                |
| Delay Tape Delay Center Frequency       | Delay Tape Free    |             | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — **`0`–`127`**                                                      |
| Delay Tape Delay Bandwidth              | Delay Tape Free    |             | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                      |
| Delay Tape Delay Modulation             | Delay Tape Free    |             | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75)                                                                     |
| Delay Tape Delay Ratio                  | Delay Tape Doppler |             | [`6E`/`0C`](../live-edit/effects.md#delay-tape-ratio-cmd0x6e) — same as Tape Free                                                                 |
| Delay Tape Delay Time (ms)              | Delay Tape Doppler |             | [`70`/`72`](../live-edit/effects.md#delay-tape-time-cmd0x70-param-0x72) — [Time](../parameter-options.md#delay-tape-time)                         |
| Delay Tape Delay Feedback               | Delay Tape Doppler |             | [`70`/`73`](../live-edit/effects.md#delay-feedback) — **0..200 %**                                                                                |
| Delay Tape Delay Center Frequency       | Delay Tape Doppler |             | [`70`/`77`](../live-edit/effects.md#delay-tape-frequency-cmd0x70-param-0x77) — [Frequency](../parameter-options.md#delay-tape-frequency)         |
| Delay Tape Delay Bandwidth              | Delay Tape Doppler |             | [`6E`/`11`](../live-edit/effects.md#delay-tape-bandwidth-cmd0x6e-param-0x11) — [Bandwidth](../parameter-options.md#delay-tape-bandwidth)         |
| Delay Tape Delay Modulation             | Delay Tape Doppler |             | [`70`/`75`](../live-edit/effects.md#delay-tape-modulation-cmd0x70-param-0x75) — [Modulation](../parameter-options.md#delay-tape-modulation)        |
| FX Reverb Switch                        | Reverb             |             | No TI mk2 **EDIT FX** control                                                                                                                        |
| Reverb Send                             | Reverb             |             | [`6E`/`02`](../live-edit/effects.md#reverb-send-cmd0x6e) — [LCD](../parameter-options.md#reverb-send-lcd)                                          |
| Reverb Mode                             | Reverb             |             | [`6E`/`01`](../live-edit/effects.md#reverb-mode-cmd0x6e) — **`00`–`03`**                                                                          |
| Reverb Type                             | Reverb             |             | [`6E`/`03`](../live-edit/effects.md#reverb-type-cmd0x6e)                                                                                          |
| Reverb Time                             | Reverb             |             | [`6E`/`04`](../live-edit/effects.md#reverb-time-cmd0x6e) — **0..127**                                                                             |
| Reverb Damping                          | Reverb             |             | [`6E`/`05`](../live-edit/effects.md#reverb-damping-cmd0x6e) — **0..100.0 %**                                                                      |
| Reverb Coloration                       | Reverb             |             | [`6E`/`06`](../live-edit/effects.md#reverb-coloration-cmd0x6e) — **−64..+63**                                                                      |
| Reverb Predelay                         | Reverb             |             | [`6E`/`07`](../live-edit/effects.md#reverb-predelay-cmd0x6e) — **0.0..500.0 ms**; **Clock** Off                                                  |
| Reverb Feedback                         | Reverb             |             | [`6E`/`09`](../live-edit/effects.md#reverb-feedback-cmd0x6e) — **Feedback 1/2** only                                                              |
| Reverb Clock                            | Reverb             |             | [`6E`/`08`](../live-edit/effects.md#reverb-clock-cmd0x6e) — same map as [Delay Clock](../parameter-options.md#delay-clock)                        |
| Vocoder Mode                            | Vocoder            |             | [`71`/`27`](../live-edit/effects.md#vocoder-mode-cmd0x71-param-0x27) — [enum](../parameter-options.md#vocoder-mode)                               |
| Vocoder Amount of Synthesis Bands       | Vocoder            |             | [`6E`/`3A`](../live-edit/effects.md#vocoder-bands-cmd0x6e-param-0x3a) — [Bands](../parameter-options.md#vocoder-bands)                             |
| Vocoder Balance (Dry-Wet)               | Vocoder            |             | [`6E`/`30`](../live-edit/effects.md#vocoder-balance-cmd0x6e-param-0x30) — modes **`01`–`06`                                                         |
| Vocoder Spectral Balance                | Vocoder            |             | [`6E`/`39`](../live-edit/effects.md#vocoder-spectral-balance-cmd0x6e-param-0x39)                                                                    |
| Vocoder Envelope Attack                 | Vocoder            |             | [`6E`/`36`](../live-edit/effects.md#vocoder-carrier-attack-cmd0x6e-param-0x36) — **Carrier Attack**                                                 |
| Vocoder Envelope Release                | Vocoder            |             | [`6E`/`37`](../live-edit/effects.md#vocoder-carrier-release-cmd0x6e-param-0x37) — **Carrier Release**                                             |
| Vocoder Carrier Center Frequency        | Vocoder            |             | [`6E`/`28`](../live-edit/effects.md#vocoder-center-freq-cmd0x6e-param-0x28) — **Center Freq**                                                     |
| Vocoder Carrier Frequency Spread        | Vocoder            |             | [`6E`/`2E`](../live-edit/effects.md#vocoder-spread-cmd0x6e-param-0x2e) — **Spread**                                                                 |
| Vocoder Carrier Q-Factor                | Vocoder            |             | [`6E`/`2A`](../live-edit/effects.md#vocoder-q-factor-cmd0x6e-param-0x2a) — **Q-Factor**                                                             |
| Vocoder Modulator Frequency Offset      | Vocoder            |             | [`6E`/`29`](../live-edit/effects.md#vocoder-mod-offset-cmd0x6e-param-0x29) — **Mod Offset**                                                           |
| Vocoder Modulator Input                 | Vocoder            |             | [Mode](../parameter-options.md#vocoder-mode) **`04`** In L / **`05`** In L+R / **`06`** In R — same rows as **`01`–`03`                              |

### Common

| Control                            | SubCategory       | Dump offset            | Live edit                                                                                                                                   |
| ---------------------------------- | ----------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Transpose / Patch Transpose        | Common Parameters |                        | `70` / `0x5D` (CC 93) — **−64..+63** → `ui+64` — [Transpose](edit-single.md#transpose--patch-transpose-0x5d-cmd0x70--cc-93                  |
| ~~Part Detune~~                    | —                 | —                      | **Multi** detune (`0x72`/`0x26`) — not Edit Single; CSV lists VC Common access only                                                         |
| Multi Tempo / Master Clock         | Common Parameters | `0x17` in `DUMP_MULTI` | `72` / `0x0F` — **63..190** bpm → `stored = bpm - 63` — [Multi Tempo](edit-single.md#multi-tempo--master-clock-0x0f-cmd0x72                 |
| Parameter Smooth Mode              | Common Parameters | **Not in dump**        | `71` / `0x19` — [Control Smooth Mode / clock quantize](../parameter-options.md#control-smooth-mode--clock-quantize)                         |
| Oscillator Section Keyboard Mode   | Common Parameters |                        | `70`/`0x5E` or CC 94                                                                                                                        |
| Patch Volume                       | Common Parameters |                        | `70` / `0x5B` (CC 91) — **0..127** direct — [Patch Volume](edit-single.md#patch-volume-0x5b-cmd0x70--cc-91                                  |
| Panorama                           | Common Parameters |                        | `70` / `0x0A` (CC 10) — **−64..+63** → `ui+64` — [Panorama](edit-single.md#panorama-0x0a-cmd0x70--cc-10                                     |
| Bend Down                          | Pitch Bender      | **Not in dump**        | `71` / `0x1B` — **−64..+63** → `ui+64` — [Bend Down](edit-single.md#bend-down-0x1b-cmd0x71                                                  |
| Bend Up                            | Pitch Bender      | **Not in dump**        | `71` / `0x1A` — same encoding — [Bend Up](edit-single.md#bend-up-0x1a-cmd0x71                                                               |
| Bender Scale                       | Pitch Bender      | **Not in dump**        | `71` / `0x1C` — [Bender Scale](../parameter-options.md#bender-scale) — [live](edit-single.md#bender-scale-0x1c-cmd0x71                      |
| Patch Category 1                   | Category          |                        | `71` / `0x7B` — [Patch name categories](../parameter-options.md#patch-name-categories) (**Name Cat 1**)                                     |
| Patch Category 2                   | Category          |                        | `71` / `0x7C` — same list (**Name Cat 2**) — [Categories](edit-single.md#categories-edit-single                                             |
| Surround Channel Balance           | Output            |                        | `71` / `0x3A` (−64..+63, `ui+64`) — [Surround Balance](edit-single.md#balance-0x3a-cmd0x71; also mod dest **116**                           |
| Multi Part Parameter Output Select | Output            | **Not in dump**        | **`73` / `0x2D`** — **Edit Single → Surround → Output** — [Secondary output routing](../parameter-options.md#secondary-output-routing)      |
| Soft Knob 1 Function As…           | Soft Knobs        |                        | `71` / `0x3E` — [Soft Knob Destinations](../parameter-options.md#soft-knob-destinations) (wire `<value>` ≠ index)                           |
| Soft Knob 1 Name                   | Soft Knobs        |                        | `71` / `0x33` — [Soft Knob Names](../parameter-options.md#soft-knob-names); LCD label above knob 1                                          |
| Soft Knob 2 Function As…           | Soft Knobs        |                        | `71` / `0x3F` — same destination list — [Soft Knobs](edit-single.md#soft-knobs-edit-single                                                  |
| Soft Knob 2 Name                   | Soft Knobs        |                        | `71` / `0x34` — [Soft Knob Names](../parameter-options.md#soft-knob-names)                                                                  |
| Soft Knob 3 Function As…           | Soft Knobs        |                        | `71` / `0x40` — same destination list                                                                                                       |
| Soft Knob 3 Name                   | Soft Knobs        |                        | `71` / `0x35` — [Soft Knob Names](../parameter-options.md#soft-knob-names)                                                                  |

### Patch Utility - Config

Patch utility / I/O config; likely not in `DUMP_SINGLE`.

| Control         | SubCategory                  | Dump offset | Live edit |
| --------------- | ---------------------------- | ----------- | --------- |
| USB Audio Mode  | Input / Output Configuration |             |           |
| Surround Output | Input / Output Configuration |             |           |
| Master Volume   | Input / Output Configuration |             |           |

### Patch Utility - Remote

Remote template UI; not a synth parameter.

| Control                               | SubCategory      | Dump offset | Live edit |
| ------------------------------------- | ---------------- | ----------- | --------- |
| Remote Template Configuration Ability | Remote Templates |             |           |

### Global

Global settings — see [edit-config.md](../live-edit/edit-config.md). Not stored
in `DUMP_SINGLE`.

| Control                                    | SubCategory    | Dump offset | Live edit |
| ------------------------------------------ | -------------- | ----------- | --------- |
| LED Mode                                   | Hardware Panel |             |           |
| LED Brightness (Lux) - TI Series Only      | Hardware Panel |             |           |
| BPM Brightness (Lux) - TI Series Only      | Hardware Panel |             |           |
| LCD Contrast                               | Hardware Panel |             |           |
| Memory Protect                             | Memory / RAM   |             |           |
| Sync Clock to External Host toggle         | MIDI           |             |           |
| Master Clock / Global Tempo                | MIDI           |             |           |
| MIDI Clock Source                          | MIDI           |             |           |
| MIDI Destination                           | MIDI           |             |           |
| MIDI Device ID                             | MIDI           |             |           |
| Global MIDI Channel                        | MIDI           |             |           |
| MIDI Volume Receive (RX) toggle            | MIDI           |             |           |
| Program Change Receive (RX) toggle         | MIDI           |             |           |
| MIDI Control Page A toggle                 | MIDI           |             |           |
| MIDI Control Page B toggle                 | MIDI           |             |           |
| Arpeggiator to MIDI Out / Note Send toggle | MIDI           |             |           |
| All Argpeggiators toggle                   | FX             |             |           |
| All Delays                                 | FX             |             |           |
| All Reverbs                                | FX             |             |           |
| All EQs                                    | FX             |             |           |
| Knob Response                              | Knobs          |             |           |
| Soft Knob 1 Mode                           | Knobs          |             |           |
| Soft Knob 2 Mode                           | Knobs          |             |           |
| Soft Knob 3 Mode                           | Knobs          |             |           |
| Knob Display Time                          | Knobs          |             |           |
| Keyboard Local Mode / Control              | Global         |             |           |
| Keyboard Channel Mode                      | Global         |             |           |
| Keyboard Transpose                         | Global         |             |           |
| Keyboard Aftertouch Sensitivity            | Global         |             |           |
| Modwheel Assign                            | Global         |             |           |
| Pedal 1 Assign                             | Global         |             |           |
| Pedal 2 Assign                             | Global         |             |           |
| Master Tuning                              | Global         |             |           |
| Pure Tuning                                | Global         |             |           |
| Input Source                               | In / Out       |             |           |
| Characteristic                             | In / Out       |             |           |
| Input Direct Thru                          | In / Out       |             |           |
| Input Boost                                | In / Out       |             |           |
| Sensitivity                                | In / Out       |             |           |

## Known / unknowns at this stage

- **Known**
  - Single dumps are **fixed‑size 524‑byte** SysEx messages.
  - **Arrangement** exports: **16** singles after the multi; **slot `0x08`**
    = zero-based part index **`0x00`–`0x0F`** (confirmed on
    `init-multi-arrangement.syx`).
  - Checksum at **`0x209`**; formula matches waf80 when summing from **`0x09`**.
  - The **patch name** appears as an ASCII sequence near offset 0xFA, padded to
    a fixed length with spaces.
  - The final byte before `F7` behaves like a **checksum byte**.
  - **415** UI controls are listed in [Single parameter
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
