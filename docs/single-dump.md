# Single Dump

Single-related SysEx dump notes for Virus TI mk2.

Live-edit notes (`cmd=0x6E`, `cmd=0x10`) are in
[single-live-edit.md](single-live-edit.md). Control inventory for mapping:
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
(same as [waf80.md](waf80.md) classic formula with payload starting at `0x09`).

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

See [multis-dump.md — Embedded vs Reference](multis-dump.md#embedded-vs-reference-multis).

## High‑level regions (from `-INIT-` baseline)

Using offsets in hexadecimal (0x00 is the `F0` byte):

- **0x00–0x0B – Fixed header**
  - Arrangement / per-part: `… 10 00 <slot> 0C 10 00` (`<slot>` = `00`–`0F`).
  - Standalone edit buffer: `… 10 00 7F 0C 00 00` (see [message header](#message-header-offsets-in-full-524-byte-message)).
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

Parameter inventory (control names and categories). Host availability
matrices: [aura-notes.md](aura-notes.md#control-inventory-source).
**Excluded:** Flash ROM banks,
Assignable X/Y Pad, and Browser (Patch Saving / Patch Browsing).

Most rows are **Single-program** parameters to correlate with
`DUMP_SINGLE` bytes and live-edit SysEx. Fill **Dump offset** and
**Live edit** as mappings are confirmed. Enum option lists:
[parameter-option-lists.md](parameter-option-lists.md).

Multi edit parameters are in
[multis-dump.md — Multi parameter map](multis-dump.md#multi-parameter-map).

**415** controls in **11** categories.

### Oscillators

| Control                                | SubCategory                  | Dump offset | Live edit             |
| -------------------------------------- | ---------------------------- | ----------- | --------------------- |
| Sub Oscillator Waveform Shape          | Sub-Osc                      |             |                       |
| Oscillator 1 Model / Mode              | Oscillator 1                 |             | `6E` / `0x1E` (see live-edit by mode) |
| Oscillator 1 Detune in Semitone        | Oscillator 1                 |             | `70` / `0x14` (−48..+48, `ui+64`) |
| Oscillator 1 Keyfollow                 | Oscillator 1                 |             | `70` / `0x15` (Classic; Norm @ +32) |
| Velocity --> Osc1 Waveform Shape       | Oscillator 1                 |             |                       |
| Oscillator 1 Waveform Shape            | Oscillator 1 Classic         |             | `70` / `0x11` (`00`–`7F`; see live-edit) |
| Oscillator 1 Wave Select               | Oscillator 1 Classic         |             | `70` / `0x13` (64 waves `00`–`3F`) |
| Oscillator 1 Pulsewidth                | Oscillator 1 Classic         |             |                       |
| Oscillator 1 Density                   | Oscillator 1 Hypersaw        |             |                       |
| Oscillator 1 Local Detune              | Oscillator 1 Hypersaw        | `70` / `0x12` | **0..127** `stored = lcd` (Hypersaw; Classic `12` = Pulse Width) |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 1 Hypersaw        | `70` / `0x1B` | **0..127** when Sync On; `stored = lcd` |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable       | `70` / `0x13` | Index **0–99** → `00`–`63`; names in [parameter-option-lists.md](parameter-option-lists.md#wavetable-names) |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable       | `70` / `0x11` | **0..127** `stored = lcd` (mode `02`; not Shape/Density) |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable       |             |                       |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Wavetable PWM   |             |                       |
| Oscillator 1 Wavetable Index           | Oscillator 1 Wavetable PWM   |             |                       |
| Oscillator 1 Pulsewidth                | Oscillator 1 Wavetable PWM   |             |                       |
| Oscillator 1 Local Detune              | Oscillator 1 Wavetable PWM   |             |                       |
| Oscillator 1 Interpolation             | Oscillator 1 Wavetable PWM   |             |                       |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Simple    |             |                       |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Simple    |             |                       |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Simple    |             |                       |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Simple    |             |                       |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Wavetable Index           | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Formant Shift             | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Formant Spread            | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Local Detune              | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Interpolation             | Oscillator 1 Grain Complex   |             |                       |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Simple  |             |                       |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Simple  |             |                       |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Simple  |             |                       |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Simple  |             |                       |
| Oscillator 1 Wavetable / Waveform      | Oscillator 1 Formant Complex |             |                       |
| Oscillator 1 Wavetable Index           | Oscillator 1 Formant Complex |             |                       |
| Oscillator 1 Formant Shift             | Oscillator 1 Formant Complex |             |                       |
| Oscillator 1 Formant Spread            | Oscillator 1 Formant Complex |             |                       |
| Oscillator 1 Local Detune              | Oscillator 1 Formant Complex |             |                       |
| Oscillator 1 Interpolation             | Oscillator 1 Formant Complex |             |                       |
| Oscillator 2 Model / Mode              | Oscillator 2                 |             |                       |
| Oscillator 2 Detune in Semitone        | Oscillator 2                 |             |                       |
| Oscillator 2 Fine Detune               | Oscillator 2                 |             |                       |
| Oscillator 2 Keyfollow                 | Oscillator 2                 |             |                       |
| Velocity --> Osc2 Waveform Shape       | Oscillator 2                 |             |                       |
| Oscillator 2 Waveform Shape            | Oscillator 2 Classic         |             |                       |
| Oscillator 2 Wave Select               | Oscillator 2 Classic         |             |                       |
| Oscillator 2 Pulsewidth                | Oscillator 2 Classic         |             |                       |
| Oscillator 2 Density                   | Oscillator 2 Hypersaw        |             |                       |
| Oscillator 2 Local Detune              | Oscillator 2 Hypersaw        |             |                       |
| Oscillator 1+2 X-Sync Frequency        | Oscillator 2 Hypersaw        |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable       |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable       |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable       |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Wavetable PWM   |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Wavetable PWM   |             |                       |
| Oscillator 2 Pulsewidth                | Oscillator 2 Wavetable PWM   |             |                       |
| Oscillator 2 Local Detune              | Oscillator 2 Wavetable PWM   |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Wavetable PWM   |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Simple    |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Simple    |             |                       |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Simple    |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Simple    |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Formant Shift             | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Formant Spread            | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Local Detune              | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Grain Complex   |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Simple  |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Simple  |             |                       |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Simple  |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Simple  |             |                       |
| Oscillator 2 Wavetable / Waveform      | Oscillator 2 Formant Complex |             |                       |
| Oscillator 2 Wavetable Index           | Oscillator 2 Formant Complex |             |                       |
| Oscillator 2 Formant Shift             | Oscillator 2 Formant Complex |             |                       |
| Oscillator 2 Formant Spread            | Oscillator 2 Formant Complex |             |                       |
| Oscillator 2 Local Detune              | Oscillator 2 Formant Complex |             |                       |
| Oscillator 2 Interpolation             | Oscillator 2 Formant Complex |             |                       |
| Oscillator 3 Model                     | Oscillator 3                 |             |                       |
| Oscillator 3 Detune in Semitone        | Oscillator 3                 |             |                       |
| Oscillator 3 Fine Detune               | Oscillator 3                 |             |                       |
| Oscillator 1 Sync (2>1)                | Oscillator Common            |             |                       |
| Filter Envelope --> Oscillator 2 Pitch | Oscillator Common            |             |                       |
| Oscillator Section Initial Phase       | Oscillator Common            |             |                       |
| Velocity --> Pulsewidth                | Oscillator Common            |             |                       |
| Patch Common Portamento                | Oscillator Common            |             |                       |
| Oscillator 2 FM Amount                 | Oscillator Common FM         |             |                       |
| Filter Envelope --> FM                 | Oscillator Common FM         |             |                       |
| Velocity --> FM Amount                 | Oscillator Common FM         |             |                       |
| Oscillator 2 FM Mode                   | Oscillator Common FM         |             |                       |
| Sync Amount / X-Sync Frequency         | Oscillator Common Sync       |             |                       |
| Velocity --> FM / Sync                 | Oscillator Common Sync       |             |                       |
| Filter Envelope --> X-Sync             | Oscillator Common Sync       |             |                       |
| Unison Mode                            | Unison                       |             |                       |
| Unison Detune                          | Unison                       |             |                       |
| Unison Panorama Spread                 | Unison                       |             |                       |
| Unison LFO Phase Offset                | Unison                       |             |                       |
| Noise Oscillator Volume                | Noise                        |             |                       |
| Noise Color                            | Noise                        |             |                       |
| Oscillator Punch Intensity             | Punch                        |             |                       |
| Oscillator 1/2 Balance                 | Mixer                        |             | `70` / `0x21` (−100..+100 %) |
| Oscillator 3 Volume                    | Mixer                        |             |                       |
| Sub Oscillator Volume                  | Mixer                        | TBD         | CC 34 (no live SysEx) |
| Oscillator Section Volume / Saturation | Mixer                        |             | `71` / `0x7F`         |
| Ring Modulator Volume                  | Mixer                        |             |                       |

### Filters

| Control                               | SubCategory                | Dump offset | Live edit                   |
| ------------------------------------- | -------------------------- | ----------- | --------------------------- |
| Filter 1 Mode                         | Filter 1                   |             | `70` / `0x33`               |
| Filter 1 Envelope Amount              | Filter 1                   |             | `70` / `0x2C`               |
| Filter 1 Envelope Polarity            | Filter 1                   |             | `71` / `0x1E`               |
| Filter 1 Cutoff                       | Filter 1                   |             | `70` / `0x28` |
| Filter 1 Resonance                    | Filter 1                   |             | `70` / `0x2A`               |
| Filter 1 Keyfollow                    | Filter 1                   |             | `70` / `0x2E`               |
| ~~Analog Mode On/Off Toggle~~         | —                          | —           | **N/A** — analog types are **Filter 1 Mode** values (`04`–`07` Analog * Pole) |
| Filter 2 Mode                         | Filter 2                   |             | `70` / `0x34` (4 modes `00`–`03` only) |
| Filter 2 Envelope Amount              | Filter 2                   |             | `70` / `0x2D` (linear %) |
| Filter 2 Envelope Polarity            | Filter 2                   |             | `71` / `0x1F` |
| ~~Filter 2 Cutoff~~                   | —                          | —           | **N/A** on TI — no separate F2 cutoff; use **Offset** vs F1 |
| Filter 2 Offset                       | Filter 2                   |             | `70` / `0x29` (bipolar `ui+64`) |
| Filter 2 Resonance                    | Filter 2                   |             | `70` / `0x2B` (direct 0–127) |
| Filter 2 Keyfollow                    | Filter 2                   |             | `70` / `0x2F` (bipolar `ui+64`) |
| Oscillator Section Volume             | Filter Common              |             | `70` / `0x24` (Saturation menu; bipolar `ui+64`) |
| Filter Routing                        | Filter Common              |             | `70` / `0x35` (4 routing modes) |
| Voice Saturation Type / Curve         | Filter Common              |             | **N/A** on TI Saturation menu (only Osc Volume) |
| Filter knob target (Res / Env Amt)    | Filter Common              |             | `71` / `0x7A` (F1=`00`, F2=`01`) |
| Filter Keyfollow Base                 | Filter Common              |             | `71` / `0x21` (C-1..G9) |
| Filter Cutoff Link toggle             | Filter Common              |             | `71` / `0x20` |
| ~~Filter Link toggle~~                | Filter Common              | —           | Unconfirmed — may differ from **knob target** `7A` |
| Filter Balance                        | Filter Common              |             | `70` / `0x30` (bipolar `ui+64`) |
| Pan Spread                            | Filter Common              |             | `6E` / `0x7A` (Split routing only) |
| Filter Envelope Select                | Filter / Aux Envelopes     |             |                             |
| Filter Envelope Attack                | Filter / Aux Envelopes     |             | `70` / `0x36` (Filter 1 ADSR menu) |
| Filter Envelope Decay                 | Filter / Aux Envelopes     |             | `70` / `0x37` |
| Filter Envelope Sustain               | Filter / Aux Envelopes     |             | `70` / `0x38` (linear %) |
| Filter Envelope Sustain Slope         | Filter / Aux Envelopes     |             | `70` / `0x39` (bipolar `ui+64`) |
| Filter Envelope Release               | Filter / Aux Envelopes     |             | `70` / `0x3A` |
| Envelope 3 Attack                     | Filter / Aux Envelopes     |             |                             |
| Envelope 3 Decay                      | Filter / Aux Envelopes     |             |                             |
| Envelope 3 Sustain                    | Filter / Aux Envelopes     |             |                             |
| Envelope 3 Sustain Slope              | Filter / Aux Envelopes     |             |                             |
| Envelope 3 Release                    | Filter / Aux Envelopes     |             |                             |
| Envelope 4 Attack                     | Filter / Aux Envelopes     |             |                             |
| Envelope 4 Decay                      | Filter / Aux Envelopes     |             |                             |
| Envelope 4 Sustain                    | Filter / Aux Envelopes     |             |                             |
| Envelope 4 Sustain Slope              | Filter / Aux Envelopes     |             |                             |
| Envelope 4 Release                    | Filter / Aux Envelopes     |             |                             |
| Amplifier Envelope Attack             | Amplifier Envelope         |             | `70` / `0x3B` |
| Amplifier Envelope Decay              | Amplifier Envelope         |             | `70` / `0x3C` |
| Amplifier Envelope Sustain            | Amplifier Envelope         |             | `70` / `0x3D` (linear %) |
| Amplifier Envelope Sustain Slope      | Amplifier Envelope         |             | `70` / `0x3E` (bipolar `ui+64`) |
| Amplifier Envelope Release            | Amplifier Envelope         |             | `70` / `0x3F` |
| Velocity --> Filter 1 Envelope Amount | Velocity / Filter Envelope |             |                             |
| Velocity --> Filter 1 Resonance       | Velocity / Filter Envelope |             |                             |
| Velocity --> Filter 2 Envelope Amount | Velocity / Filter Envelope |             |                             |
| Velocity --> Filter 2 Resonance       | Velocity / Filter Envelope |             |                             |
| Velocity --> Volume                   | Velocity / Amplifier       |             |                             |
| Velocity --> Panorama                 | Velocity / Amplifier       |             |                             |
| Patch Volume                          | Amplifier                  |             | CC 91                       |
| Patch Panorama                        | Amplifier                  |             |                             |
| Reverb Send                           | Amplifier                  |             | `6E` / `0x02`               |
| Delay Send                            | Amplifier                  |             |                             |

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

### Arpeggiator

| Control                              | SubCategory    | Dump offset | Live edit |
| ------------------------------------ | -------------- | ----------- | --------- |
| Arpeggiator Mode                     | Settings       |             |           |
| Arpeggiator Pattern                  | Settings       |             |           |
| Argpeggiator Range In Octaves        | Settings       |             |           |
| Arpeggiator Clock / Resolution       | Settings       |             |           |
| Arpeggiator Note Length              | Settings       |             |           |
| Arpeggiator Swing Factor             | Settings       |             |           |
| Arpeggiator Hold Mode                | Settings       |             |           |
| Arpeggiator User Pattern Step        | Pattern Editor |             |           |
| Arpeggiator Offset Direction Buttons | Pattern Editor |             |           |
| Arpeggiator Step Random Button       | Pattern Editor |             |           |
| Arpeggiator Velocity Random Button   | Pattern Editor |             |           |
| Arpeggiator Length Random Button     | Pattern Editor |             |           |
| Arpeggiator Loop Length              | Pattern Editor |             |           |

### FX 1

| Control                         | SubCategory                   | Dump offset | Live edit |
| ------------------------------- | ----------------------------- | ----------- | --------- |
| Character Type                  | Characters                    |             |           |
| Character Intensity             | Characters                    |             |           |
| Character Tune / Frequency      | Characters                    |             |           |
| Chorus Type                     | Chorus                        |             |           |
| Chorus Mix                      | Chorus Classic                |             |           |
| Chorus Delay                    | Chorus Classic                |             |           |
| Chorus Feedback                 | Chorus Classic                |             |           |
| Chorus LFO Rate                 | Chorus Classic                |             |           |
| Chorus LFO Depth                | Chorus Classic                |             |           |
| Chorus LFO Shape                | Chorus Classic                |             |           |
| Chorus Mix                      | Chorus Vintage                |             |           |
| Chorus X Over                   | Chorus Vintage                |             |           |
| Chorus LFO Rate                 | Chorus Vintage                |             |           |
| Chorus LFO Depth                | Chorus Vintage                |             |           |
| Chorus Mix                      | Chorus Hyper                  |             |           |
| Chorus X Over                   | Chorus Hyper                  |             |           |
| Chorus Amount                   | Chorus Hyper                  |             |           |
| Chorus LFO Depth                | Chorus Hyper                  |             |           |
| Chorus X Over                   | Chorus Air                    |             |           |
| Chorus LFO Depth                | Chorus Air                    |             |           |
| Chorus X Over                   | Chorus Vibrato                |             |           |
| Chorus LFO Rate                 | Chorus Vibrato                |             |           |
| Chorus LFO Depth                | Chorus Vibrato                |             |           |
| Chorus Mix                      | Chorus Rotary Speaker         |             |           |
| Chorus Speed                    | Chorus Rotary Speaker         |             |           |
| Chorus Low/High Balance         | Chorus Rotary Speaker         |             |           |
| Chorus Mic Angle                | Chorus Rotary Speaker         |             |           |
| Chorus Distance                 | Chorus Rotary Speaker         |             |           |
| Distortion Type                 | Distortion                    |             |           |
| Distortion Mix                  | Distortion                    |             |           |
| Distortion Intensity / Drive    | Distortion                    |             |           |
| Distortion Treble Booster       | Distortion                    |             |           |
| Distortion High Cut             | Distortion                    |             |           |
| Distortion Quality              | Distortion                    |             |           |
| Distortion Intensity / Cutoff   | Distortion                    |             |           |
| Distortion Intensity / Drive    | Distortion Overdrives         |             |           |
| Distortion Tone N               | Distortion Overdrives         |             |           |
| Distortion High Cut             | Distortion Overdrives         |             |           |
| Phaser Mix                      | Phaser                        |             |           |
| Phaser Stages                   | Phaser                        |             |           |
| Phaser Frequency                | Phaser                        |             |           |
| Phaser Feedback (FB)            | Phaser                        |             |           |
| Phaser Spread                   | Phaser                        |             |           |
| Phaser LFO Rate                 | Phaser                        |             |           |
| Phaser LFO Depth                | Phaser                        |             |           |
| Filter Bank Type                | Filter Bank                   |             |           |
| Filter Bank Mix / Amount        | Filter Bank                   |             |           |
| Filter Bank Frequency           | Filter Bank                   |             |           |
| Filter Bank Stereo Phase        | Filter Bank                   |             |           |
| Frequency Shifter Left Shape    | Filter Bank Frequency Shifter |             |           |
| Frequency Shifter Right Shape   | Filter Bank Frequency Shifter |             |           |
| Filter Bank Frequency / Vowel   | Filter Bank Vowel Filter      |             |           |
| Filter Bank Resonance           | Filter Bank Vowel Filter      |             |           |
| Filter Bank Stereo Phase        | Filter Bank Vowel Filter      |             |           |
| Filter Bank Frequency           | Filter Bank Comb Filter       |             |           |
| Filter Bank Resonance           | Filter Bank Comb Filter       |             |           |
| Filter Bank Stereo Phase        | Filter Bank Comb Filter       |             |           |
| Filter Bank Frequency           | Filter Bank 1-6 Pole XFade    |             |           |
| Filter Bank Resonance           | Filter Bank 1-6 Pole XFade    |             |           |
| Filter Type                     | Filter Bank 1-6 Pole XFade    |             |           |
| Filter Bank Frequency           | Filter Bank VariSlopes        |             |           |
| Filter Bank Resonance           | Filter Bank VariSlopes        |             |           |
| Filter Bank Filter Poles        | Filter Bank VariSlopes        |             |           |
| Filter Bank Filter Slope        | Filter Bank VariSlopes        |             |           |
| EQ Low Gain (db)                | Equalizer                     |             |           |
| EQ Low Frequency (Hz)           | Equalizer                     |             |           |
| EQ Mid Gain (db)                | Equalizer                     |             |           |
| EQ Mid Frequency (Hz)           | Equalizer                     |             |           |
| EQ Mid Q-Factor                 | Equalizer                     |             |           |
| EQ High Gain (db)               | Equalizer                     |             |           |
| EQ High Frequency (Hz)          | Equalizer                     |             |           |
| Input Follower Select           | Envelope Follower             |             |           |
| Input Follower Level            | Envelope Follower             |             |           |
| Input Follower Envelope Attack  | Envelope Follower             |             |           |
| Input Follower Envelope Release | Envelope Follower             |             |           |
| Input Mode                      | Input                         |             |           |
| Input Select                    | Input                         |             |           |
| Input Atomizer                  | Input                         |             |           |

### FX 2

| Control                                 | SubCategory        | Dump offset | Live edit     |
| --------------------------------------- | ------------------ | ----------- | ------------- |
| FX Delay Switch                         | Delay              |             |               |
| Delay Send / Mix                        | Delay              |             |               |
| Delay Type                              | Delay              |             |               |
| Delay Mode                              | Delay              |             |               |
| Delay Clock                             | Delay              |             |               |
| Delay Time (ms)                         | Delay              |             |               |
| Delay Feedback                          | Delay              |             |               |
| Delay Color                             | Delay              |             |               |
| Delay LFO Rate                          | Delay              |             |               |
| Delay LFO Depth                         | Delay              |             |               |
| Delay LFO Shape                         | Delay              |             |               |
| Delay Tape Delay Clock Left             | Delay Tape Clocked |             |               |
| Delay Tape Delay Clock Right            | Delay Tape Clocked |             |               |
| Delay Tape Delay Feedback               | Delay Tape Clocked |             |               |
| Delay Tape Delay Center Frequency       | Delay Tape Clocked |             |               |
| Delay Tape Delay Bandwidth              | Delay Tape Clocked |             |               |
| Delay Tape Delay Modulation             | Delay Tape Clocked |             |               |
| Delay Tape Delay Ratio                  | Delay Tape Free    |             |               |
| Delay Tape Delay Time (ms)              | Delay Tape Free    |             |               |
| Delay Tape Delay Feedback               | Delay Tape Free    |             |               |
| Delay Tape Delay Center Frequency       | Delay Tape Free    |             |               |
| Delay Tape Delay Bandwidth              | Delay Tape Free    |             |               |
| Delay Tape Delay Modulation             | Delay Tape Free    |             |               |
| Delay Tape Delay Ratio                  | Delay Tape Doppler |             |               |
| Delay Tape Delay Time (ms)              | Delay Tape Doppler |             |               |
| Delay Tape Delay Feedback               | Delay Tape Doppler |             |               |
| Delay Tape Delay Center Frequency       | Delay Tape Doppler |             |               |
| Delay Tape Delay Bandwidth              | Delay Tape Doppler |             |               |
| Delay Tape Delay Modulation             | Delay Tape Doppler |             |               |
| FX Reverb Switch                        | Reverb             |             |               |
| Reverb Send                             | Reverb             |             | `6E` / `0x02` |
| Reverb Mode                             | Reverb             |             |               |
| Reverb Type                             | Reverb             |             |               |
| Reverb Time / Decay                     | Reverb             |             |               |
| Reverb Damping                          | Reverb             |             |               |
| Reverb Color                            | Reverb             |             |               |
| Reverb Predelay / Time                  | Reverb             |             |               |
| Reverb Feedback                         | Reverb             |             |               |
| Reverb Clock                            | Reverb             |             |               |
| Vocoder Mode                            | Vocoder            |             |               |
| Vocoder Amount of Synthesis Bands       | Vocoder            |             |               |
| Vocoder Balance (Dry-Wet)               | Vocoder            |             |               |
| Vocoder Spectral Balance                | Vocoder            |             |               |
| Vocoder Envelope Attack                 | Vocoder            |             |               |
| Vocoder Envelope Release                | Vocoder            |             |               |
| Vocoder Carrier Center Frequency        | Vocoder            |             |               |
| Vocoder Carrier Frequency Spread        | Vocoder            |             |               |
| Vocoder Carrier Q-Factor                | Vocoder            |             |               |
| Vocoder Carrier + Modulator Link Button | Vocoder            |             |               |
| Vocoder Modulator Q-Factor              | Vocoder            |             |               |
| Vocoder Modulator Frequency Spread      | Vocoder            |             |               |
| Vocoder Modulator Frequency Offset      | Vocoder            |             |               |
| Vocoder Modulator Input                 | Vocoder            |             |               |

### Common

| Control                            | SubCategory       | Dump offset     | Live edit                                                                           |
| ---------------------------------- | ----------------- | --------------- | ----------------------------------------------------------------------------------- |
| Patch Transpose                    | Common Parameters |                 | CC 93                                                                               |
| ~~Part Detune~~                    | —                 | —               | **Multi** detune (`0x72`/`0x26`) — not Edit Single; CSV lists VC Common access only |
| Parameter Smooth Mode              | Common Parameters | **Not in dump** | `71` / `0x19`                                                                       |
| Oscillator Section Keyboard Mode   | Common Parameters |                 | `70`/`0x5E` or CC 94                                                                |
| Patch Volume                       | Common Parameters |                 | CC 91                                                                               |
| Bender Down Range                  | Pitch Bender      | **Not in dump** | `71` / `0x1A`                                                                       |
| Bender Up Range                    | Pitch Bender      | **Not in dump** | `71` / `0x1B`                                                                       |
| Patch Common Bender Scale          | Pitch Bender      | **Not in dump** | `72`/`0x1D` Linear; `71`/`0x1C` Exp                                                 |
| Patch Category 1                   | Category          |                 |                                                                                     |
| Patch Category 2                   | Category          |                 |                                                                                     |
| Surround Channel Balance           | Output            |                 |                                                                                     |
| Multi Part Parameter Output Select | Output            |                 |                                                                                     |
| Soft Knob 1 Destination            | Soft Knobs        |                 |                                                                                     |
| Soft Knob 1 Name                   | Soft Knobs        |                 |                                                                                     |
| Soft Knob 1 Amount                 | Soft Knobs        |                 |                                                                                     |
| Soft Knob 2 Destination            | Soft Knobs        |                 |                                                                                     |
| Soft Knob 2 Name                   | Soft Knobs        |                 |                                                                                     |
| Soft Knob 2 Amount                 | Soft Knobs        |                 |                                                                                     |
| Soft Knob 3 Destination            | Soft Knobs        |                 |                                                                                     |
| Soft Knob 3 Name                   | Soft Knobs        |                 |                                                                                     |
| Soft Knob 3 Amount                 | Soft Knobs        |                 |                                                                                     |

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

Global settings — see [global-live-edit.md](global-live-edit.md). Not stored
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
  - **415** UI controls are listed in [Single parameter map](#single-parameter-map)
    for byte /
    live-edit correlation (Multi parameters →
    [multis-dump.md](multis-dump.md#multi-parameter-map); excluding Flash ROM,
    X/Y Pad, and Browser).
- **Unknown (to be refined with more examples)**
  - Exact mapping from payload offsets to GUI parameters.
  - Meaning of **`0x09`–`0x0B`** (`0C 10 00` vs `0C 00 00`) beyond “TI header”.
  - Trailer bytes at **`0x204`–`0x208`** (`7F 40 00 01 00 00`).

Future work: compare additional Single dumps (small, targeted parameter
changes) and record byte deltas in the parameter map.
