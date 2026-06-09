# Live-edit address index

Lookup table for **live-edit** SysEx: after the fixed header, **`cmd`** selects
the **page** (address space) and **`param`** selects the parameter within that
page. Message layout: [Getting started — Message structure](../getting-started.md#message-structure).
Paging overview: [virus.md — Paging](../misc/virus.md#paging).

```text
F0 00 20 33 01 00  <cmd>  <part>  <param>  <value>  F7
```

**`<part>`** is the edit buffer (Multi Part **`00`–`0F`**, Single edit buffer
**`40`**) — not a parameter ID. **`param`** only makes sense with **`cmd`**.
Value encodings: [parameter-options.md](parameter-options.md).

## Contents

- [Page `0x70` — Page A](#page-0x70--page-a)
- [Page `0x71` — Page B](#page-0x71--page-b)
- [Page `0x6E` — Part buffer](#page-0x6e--part-buffer)
- [Page `0x6F` — Extended](#page-0x6f--extended)
- [Page `0x72` — Multi / common](#page-0x72--multi--common)
- [Page `0x73` — Global / CONFIG](#page-0x73--global--config)
- [Related](#related)

---

## Page `0x70` — Page A

| Panel group                                                 | `param`                                                                            | Detail                                                                                                                                                                                                                                         |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Oscillators](../live-edit/single/oscillators.md) — Osc 1–3 | `0x11`–`0x1B` (mode-dependent)                                                     | [Osc 1 Classic](../live-edit/single/oscillators.md#oscillator-1--classic) · [Osc 2](../live-edit/single/oscillators.md#oscillator-2)                                                                                                           |
| [Oscillators](../live-edit/single/oscillators.md) — Mixer   | `0x22`–`0x25`, `0x27`, `0x32`                                                      | [Noise](../live-edit/single/oscillators.md#noise) · [Ring mod](../live-edit/single/oscillators.md#ring-modulator) · [Sub osc](../live-edit/single/oscillators.md#sub-oscillator) · [Osc Volume](../live-edit/single/oscillators.md#osc-volume) |
| [Filters](../live-edit/single/filters.md)                   | `0x24`, `0x28`–`0x30`, `0x33`–`0x35`, `0x38`–`0x39`, `0x3D`–`0x3E`                 | [Filters](../live-edit/single/filters.md)                                                                                                                                                                                                      |
| [LFO 2](../live-edit/single/modulators.md)                  | `0x4F`–`0x5A`, `0x56`–`0x59`                                                       | [LFO 2](../live-edit/single/modulators.md#lfo-2) · destinations [`0x56`–`0x5A`](../live-edit/single/modulators.md#lfo-2-destination)                                                                                                           |
| [Effects](../live-edit/single/effects.md) — Page A          | `0x15`, `0x21`, `0x28`–`0x29`, `0x2B`, `0x2F`–`0x30`, `0x36`–`0x3A`, `0x67`–`0x77` | [Edit FX](../live-edit/single/effects.md#edit-fx-effects)                                                                                                                                                                                      |
| [Effects](../live-edit/single/effects.md) — SELECT          | `0x75`, `0x76`                                                                     | [Effects SELECT](parameter-options.md#effects-select-group-1)                                                                                                                                                                                  |
| [Common](../live-edit/single/single.md)                     | `0x05`, `0x0A`, `0x5B`, `0x5D`–`0x5E`                                              | [single.md](../live-edit/single/single.md) (Panorama `0x0A`, soft knobs, …)                                                                                                                                                                    |

---

## Page `0x71` — Page B

| Panel group                                                          | `param`                                                                   | Detail                                                                                                                           |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [Oscillators](../live-edit/single/oscillators.md) — SELECT / section | `0x7F`, `0x24`                                                            | [SELECT `71`/`7F`](../live-edit/single/oscillators.md#select-717f) · [Punch](../live-edit/single/oscillators.md#punch-intensity) |
| [Common](../live-edit/single/single.md)                              | `0x19`–`0x1C`, `0x23`, `0x3A`                                             | [Smooth mode](../live-edit/single/single.md) · pitch bend · velocity map                                                         |
| [LFO 1](../live-edit/single/modulators.md)                           | `0x12`, `0x43`–`0x49`                                                     | [LFO 1](../live-edit/single/modulators.md#lfo-1)                                                                                 |
| [LFO 3](../live-edit/single/modulators.md)                           | `0x07`–`0x09`, `0x0A`, `0x15`                                             | [LFO 3](../live-edit/single/modulators.md#lfo-3)                                                                                 |
| [Arpeggiator](../live-edit/single/arpeggiator.md)                    | `0x02`–`0x06`, `0x0F`, `0x11`                                             | [arpeggiator.md](../live-edit/single/arpeggiator.md)                                                                             |
| [Filters](../live-edit/single/filters.md)                            | `0x1E`–`0x21`                                                             | [Filter polarity](../live-edit/single/filters.md) · keyfollow · cutoff link                                                      |
| [Effects](../live-edit/single/effects.md) — Page B                   | `0x26`–`0x27`, `0x2D`–`0x2E`, `0x54`–`0x5A`, `0x5C`–`0x62`, `0x64`–`0x65` | [Edit FX](../live-edit/single/effects.md#edit-fx-effects)                                                                        |
| [Mod Matrix](../live-edit/single/mod-matrix.md)                      | `0x40`–`0x4E`, `0x67`–`0x6F` (slot-dependent)                             | [Per-slot map](../live-edit/single/mod-matrix.md#per-slot-cmd--param-map)                                                        |
| [Edit Multi](../live-edit/multis.md) — bend limits                   | `0x1A`–`0x1B`                                                             | [Bend Up / Down](../live-edit/multis.md#bend-up) (not on `0x72`)                                                                 |

---

## Page `0x6E` — Part buffer

| Panel group                                                      | `param`                                                                    | Detail                                                                                     |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [Mod Matrix](../live-edit/single/mod-matrix.md)                  | `0x5A`–`0x5F`, `0x60`–`0x6B` (slot-dependent)                              | [Per-slot map](../live-edit/single/mod-matrix.md#per-slot-cmd--param-map)                  |
| [Effects](../live-edit/single/effects.md) — part buffer          | `0x01`, `0x03`–`0x0A`, `0x0C`–`0x0E`, `0x11`, `0x13`–`0x1A`, `0x46`–`0x4A` | [Edit FX](../live-edit/single/effects.md#edit-fx-effects) · SELECT `0x75`/`0x76` on `0x6E` |
| [Oscillators](../live-edit/single/oscillators.md) — mode extras  | `0x1E`, `0x23`–`0x2C`, … (mode-dependent)                                  | [Osc 1 modes](../live-edit/single/oscillators.md#oscillator-1--mode)                       |
| [Filters](../live-edit/single/filters.md)                        | `0x7A`                                                                     | [Saturation](../live-edit/single/filters.md)                                               |
| [Common](../live-edit/single/single.md)                          | `0x52`–`0x53`, `0x57`–`0x58`                                               | Envelope 3/4                                                                               |
| [Arpeggiator](../live-edit/single/arpeggiator.md) — user pattern | `0x7F`                                                                     | [Loop length](../live-edit/single/arpeggiator.md#loop-length)                              |

---

## Page `0x6F` — Extended

| Panel group                                    | `param`       | Detail                                              |
| ---------------------------------------------- | ------------- | --------------------------------------------------- |
| [Unison](../live-edit/single/oscillators.md)   | `0x78`–`0x7B` | [Unison](../live-edit/single/oscillators.md#unison) |
| [Inputs](../live-edit/global.md) — Edit Single | `0x7C`–`0x7E` | [Inputs](../live-edit/global.md#inputs-edit-single) |

---

## Page `0x72` — Multi / common

| Panel group                                            | `param`                      | Detail                                                                                                                                                                                      |
| ------------------------------------------------------ | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Edit Multi](../live-edit/multis.md) — Master Clock    | `0x0F`                       | [Master Clock](../live-edit/multis.md#master-clock-tempo)                                                                                                                                   |
| [Edit Multi](../live-edit/multis.md) — program         | `0x20`–`0x22`                | [Bank](../live-edit/multis.md#bank) · [Program](../live-edit/multis.md#program) · [MIDI Channel](../live-edit/multis.md#midi-channel)                                                       |
| [Edit Multi](../live-edit/multis.md) — keys / tuning   | `0x23`–`0x26`                | [Low / High Key](../live-edit/multis.md#low-key) · [Transpose](../live-edit/multis.md#transpose) · [Detune](../live-edit/multis.md#detune)                                                  |
| [Edit Multi](../live-edit/multis.md) — level / routing | `0x27`–`0x29`, `0x2B`        | [Volume](../live-edit/multis.md#volume) · [Init Volume](../live-edit/multis.md#init-volume) · [Output](../live-edit/multis.md#output-routing) · [Panorama](../live-edit/multis.md#panorama) |
| [Edit Multi](../live-edit/multis.md) — part flags      | `0x48`–`0x4A`, `0x4D`–`0x4E` | [Enable](../live-edit/multis.md#enable) · [Hold](../live-edit/multis.md#hold-pedal) · [Summary](../live-edit/multis.md#summary)                                                             |
| [Edit Multi](../live-edit/multis.md) — keyboard        | `0x40`                       | [Keyboard-related](../live-edit/multis.md#keyboard-related)                                                                                                                                 |
| [Common](../live-edit/single/single.md) — Multi Tempo  | `0x0F`                       | [Multi Tempo](../live-edit/single/single.md#multi-tempo--master-clock)                                                                                                                      |

---

## Page `0x73` — Global / CONFIG

Global live edits omit **`<part>`** — the frame is `73 00 <param> <value>`.

| Panel group                                             | `param`                                                                                                                                                                                 | Detail                                                                                      |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [Global](../live-edit/global.md)                        | `0x09`, `0x10`, `0x19`–`0x1D`, `0x1F`, `0x28`–`0x29`, `0x2B`, `0x32`–`0x33`, `0x35`–`0x36`, `0x55`, `0x57`, `0x5A`–`0x5B`, `0x5D`, `0x60`, `0x6A`, `0x75`–`0x76`, `0x7A`, `0x7C`–`0x7E` | [Summary](../live-edit/global.md#summary) · [Parameters](../live-edit/global.md#parameters) |
| [Edit Multi](../live-edit/multis.md) — Secondary Output | `0x2D`                                                                                                                                                                                  | [Secondary Output](../live-edit/multis.md#secondary-output) (uses `0x73`, not `0x72`)       |

---

## Related

| Resource                                                                               | Use when                                            |
| -------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [dumps/single.md](../dumps/single.md)                                                  | Full Single field map (`cmd`/`param` + dump offset) |
| [multis.md — Summary](../live-edit/multis.md#summary)                                  | Complete `0x72` param list                          |
| [parameter-options.md — Notation](parameter-options.md#notation-cmd-param-dump-offset) | `cmd` vs `param` vs dump offset                     |
| [bank.md](../dumps/bank.md)                                                            | Requests and dumps (not live-edit pages)            |
