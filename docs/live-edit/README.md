# Live Edit

Real-time SysEx parameter changes on the Virus TI mk2 (**`0x70`**, **`0x71`**,
**`0x6E`**, **`0x72`**, **`0x73`**, …).

| Document                                     | Panel / menu                                                                  |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| [edit-config.md](edit-config.md)             | CONFIG — System, MIDI, Inputs, Audio Clock, global Soft Knob behavior, tuning |
| [edit-single.md](edit-single.md)             | Edit Single — Common, Unison, Envelope 3/4, Velocity Map, Soft Knobs          |
| [oscillators.md](oscillators.md)             | Oscillators — Osc 1–3, Noise, Ring Mod, Sub Osc                               |
| [filters.md](filters.md)                     | Filters — Common, Filter 1/2, Filter/Amp envelopes, Saturation                |
| [effects.md](effects.md)                     | Edit FX — SELECT focus (`6E`/`75`, `6E`/`76`) + Delay, Reverb, EQ, …          |
| [arpeggiator.md](arpeggiator.md)             | Arpeggiator — EDIT ARP settings, pattern editor                               |
| [modulators.md](modulators.md)               | Modulators — EDIT LFO (LFO 1–3 settings, modulation amounts)                  |
| [modulation-matrix.md](modulation-matrix.md) | Modulation Matrix — slots 1–6 (Source / Destination / Amount)                 |
| [edit-multi.md](edit-multi.md)               | Edit Multi — parts, keyboard range, routing                                   |

**Enums & panel tables:**
[parameter-options.md](../parameter-options.md)
**Dump offsets (worksheet):**
[dumps/single.md](../dumps/single.md#single-parameter-map)
**Unmapped / outstanding gaps:**
[unmapped.md](../unmapped.md)
**MIDI CC (when Page A = Controller Data):**
[control-change.md](../control-change.md)

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7 # Edit Multi / common
F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B
F0 00 20 33 01 00 70 <part> <param> <value> F7 # Page A (when Page A = SysEx)
F0 00 20 33 01 00 6E <part> <param> <value> F7 # Part single buffer (FX, …)
F0 00 20 33 01 00 73 00 <param> <value> F7 # Global / CONFIG
```

Param IDs are **not global** across `cmd` bytes.

**`<part>` scope:** Multi Part 1–16 → **`0x00`–`0x0F`** for **`0x72`**
(including **Bank** / **Program**), **`0x70`**, **`0x71`**, **`0x6E`**, …
Single-mode sound edits use **`0x40`** on those same **`cmd`** bytes — see
[Single vs Multi addressing](../dumps/single.md#single-vs-multi-addressing).
**Do not** use **`0x40`** as the part byte on **`0x72`/`0x20`** or **`0x21`**
(Hardware uses **`0x00`–`0x0F`** for per-part bank/program.)
