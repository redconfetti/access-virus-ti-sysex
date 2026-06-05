# Parameter options

Enumerated UI options for Virus TI parameters. **Index** is the zero-based
list position; for most panel enums **`stored = index`** (exceptions: [Soft Knob
Destinations](#soft-knob-destinations), [Soft Knob Names](#soft-knob-names) use
per-row **`<value>`**) (hex in tables as
**`<value>`**).

Live-edit docs ([live-edit/README.md](live-edit/README.md),
[edit-multi.md](live-edit/edit-multi.md)) record **`cmd` / `param` / encoding**
only — **option names live here**. Link with:

```markdown
See [Option name](parameter-options.md#anchor) from live-edit or dump rows.
```

See [waf80.md](waf80.md) for classic Page A/B parameter indices.

## Index

| Section                                                                      | Used by                                                                                    |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [Secondary output routing](#secondary-output-routing)                        | Edit Single → Surround → **Output**; Edit Multi → **Secondary Output** (`73`/`2D`)         |
| [Input Mode](#input-mode)                                                    | Edit Single → Inputs (`6F`/`7C`)                                                           |
| [Input Select](#input-select)                                                | Edit Single → Inputs (`6F`/`7D`)                                                           |
| [Atomizer preset](#atomizer-preset)                                          | Edit Single → Inputs → **Atomizer** (`6F`/`7E`)                                            |
| [Patch name categories](#patch-name-categories)                              | Edit Single → Categories → **Name Cat 1** / **Name Cat 2** (`71`/`7B`, `71`/`7C`)          |
| [Soft Knob Destinations](#soft-knob-destinations)                            | Soft Knob **Function As…** — `71`/`3E`, `3F`, `40` (wire `<value>` per row)                |
| [Soft Knob Names](#soft-knob-names)                                          | Soft Knob **Name** — `71`/`33`, `34`, `35` (wire `<value>` per row)                        |
| [Control Smooth Mode / clock quantize](#control-smooth-mode--clock-quantize) | Common **Smooth Mode** (`71`/`19`); same grid as LFO/Delay **Clock** (WAF80)               |
| [Bender Scale](#bender-scale)                                                | Common **Bender Scale** (`71`/`1C`)                                                        |
| [Delay Type](#delay-type)                                                    | Edit FX → Delay **Type**                                                                   |
| [Delay panel visibility](#delay-panel-visibility)                            | **Send** Off vs on; controls per **Type**                                                  |
| [Delay Mode](#delay-mode)                                                    | Edit FX → Delay **Mode** (Classic; **`01`–`16`**)                                          |
| [Delay Clock](#delay-clock)                                                  | Edit FX → Delay **Clock** (Simple Delay / Ping Pong modes)                                 |
| [Delay Coloration](#delay-coloration)                                        | Edit FX → Delay **Coloration** (Classic; **−64..+63**)                                     |
| [Delay LFO](#delay-lfo)                                                      | **Rate** / **Depth** / **LFO Wave** (Classic modulation row)                               |
| [Delay LFO Rate](#delay-lfo-rate)                                            | **Rate** (`70`/`74`; `0`–`127`)                                                            |
| [Delay LFO Depth](#delay-lfo-depth)                                          | **Depth** (`0.0`–`100.0 %`; `70`/`75`)                                                     |
| [Delay LFO Wave](#delay-lfo-wave)                                            | **LFO Wave** (`70`/`76`; `00`–`05`)                                                        |
| [Delay Tape Left Clock](#delay-tape-left-clock)                              | Tape Clocked **Left Clock** (`6E`/`0D`; `00`–`05`)                                         |
| [Delay Tape Right Clock](#delay-tape-right-clock)                            | Tape Clocked **Right Clock** (`6E`/`0E`; `00`–`05`)                                        |
| [Delay Tape Frequency](#delay-tape-frequency)                                | Tape **Frequency** (`70`/`77`; `0`–`127`)                                                  |
| [Delay Tape Bandwidth](#delay-tape-bandwidth)                                | Tape **Bandwidth** (`6E`/`11`; `0`–`127`)                                                  |
| [Delay Tape Modulation](#delay-tape-modulation)                              | Tape **Modulation** (`70`/`75`; `0`–`100 %`)                                               |
| [Delay Time (ms)](#delay-tape-time)                                          | **Delay Time** (Classic) / **Time** (Tape Free, Doppler) — same `70`/`72`, `0.0`–`693.6 ms |
| [Delay Tape Ratio](#delay-tape-ratio)                                        | **Tape Free** / **Doppler** **Ratio** (`6E`/`0C`; `00`–`06`)                               |
| [Delay Feedback](#delay-feedback)                                            | **Feedback** — Classic **0..100 %** / Tape **0..200 %** (`70`/`73`)                        |
| [Delay Send (LCD)](#delay-send-lcd)                                          | Edit FX → Delay **Send** (`stored` = index `00`–`7F`; `70`/`71`)                           |
| [Reverb Mode](#reverb-mode)                                                  | **Mode** — `6E`/`01`; **Off** / **Reverb** / **Feedback 1/2**                              |
| [Reverb Type](#reverb-type)                                                  | **Type** — `6E`/`03`; Ambience … Hall (**Mode** = Reverb)                                  |
| [Reverb panel visibility](#reverb-panel-visibility)                          | Controls per **Mode**; **Send** / **Clock** / **Predelay** rules                           |
| [Reverb Clock](#reverb-clock)                                                | **Clock** — `6E`/`08`; same wire map as [Delay Clock](#delay-clock)                        |
| [Reverb Time](#reverb-time)                                                  | **Time** — `6E`/`04`; tail **0..127** (`stored = lcd`)                                     |
| [Reverb Damping](#reverb-damping)                                            | **Damping** — `6E`/`05`; **0..100.0 %**                                                    |
| [Reverb Coloration](#reverb-coloration)                                      | **Coloration** — `6E`/`06`; **−64..+63**                                                   |
| [Reverb Predelay](#reverb-predelay)                                          | **Predelay** — `6E`/`07`; **0.0..500.0 ms** (**Clock** Off)                                |
| [Reverb Feedback](#reverb-feedback)                                          | **Feedback** — `6E`/`09`; **0..127** (**Feedback 1/2**)                                    |
| [Reverb Send (LCD)](#reverb-send-lcd)                                        | **Send** — `6E`/`02`; **`00`** Off … **`7F`** Effect (TX confirmed)                        |
| [EQ Low Frequency](#eq-low-frequency)                                        | **Low EQ → Frequency (Hz)** — `71`/`2D`; **32..458 Hz**                                    |
| [EQ Low Gain](#eq-low-gain)                                                  | **Low EQ → Gain** — `71`/`5F`; **−16..+16 dB**, **Off** @ **`40`**                         |
| [EQ Mid Frequency](#eq-mid-frequency)                                        | **Mid EQ → Frequency (Hz)** — `71`/`5D`; **19 Hz..24.0 kHz**                               |
| [EQ Mid Gain](#eq-mid-gain)                                                  | **Mid EQ → Gain** — `71`/`5C`; same dB map as [Low Gain](#eq-low-gain)                     |
| [EQ Mid Q-Factor](#eq-mid-q-factor)                                          | **Mid EQ → Q** — `71`/`5E`; **0.28..15.4**                                                 |
| [EQ High Frequency](#eq-high-frequency)                                      | **High EQ → Frequency (Hz)** — `71`/`2E`; **1831 Hz..24.0 kHz**                            |
| [EQ High Gain](#eq-high-gain)                                                | **High EQ → Gain** — `71`/`60`; same dB map as [Low Gain](#eq-low-gain)                    |
| [EFFECTS focus group 1](#effects-focus-group-1)                              | Front-panel **EFFECTS** SELECT (1st group) — `6E`/`75`                                     |
| [EFFECTS focus group 2](#effects-focus-group-2)                              | **EFFECTS** SELECT group 2 — `6E`/`76` (Distortion … Others)                               |
| [Distortion Type](#distortion-type)                                          | **EDIT FX → Distortion → Type** — `71`/`64`; sparse wire map                               |
| [Distortion panel visibility](#distortion-panel-visibility)                  | **Type** Off vs standard / minimal / reducer panel rows                                    |
| [Mod Matrix Sources](#mod-matrix-sources)                                    | Mod matrix **Source**                                                                      |
| [Mod Matrix Destinations](#mod-matrix-destinations)                          | Mod matrix **Destination**                                                                 |
| [Wavetable Names](#wavetable-names)                                          | Osc wavetable wave select                                                                  |

LCD↔wire curves (not simple enums): [Edit Single
Panorama](#edit-single--panorama-lcd),
[Osc 1 Classic Pulse Width](#osc-1-classic--pulse-width-lcd),
[Osc 1 Hypersaw Density](#osc-1-hypersaw--density-lcd).

---

## Secondary output routing

**Off** plus **Out 1 L** … **USB 3 R**. **`00`** = Off; otherwise
**primary routing index + 1** (see [Output routing
(primary)](live-edit/edit-multi.md#output-routing-enum-0x29)).

Analog **Out 1**–**Out 3**: **`00`–`09`**; USB outs through **`12`**.

| Index | `<value>` | Option    |
| ----- | --------- | --------- |
| 0     | `00`      | Off       |
| 1     | `01`      | Out 1 L   |
| 2     | `02`      | Out 1 L+R |
| 3     | `03`      | Out 1 R   |
| 4     | `04`      | Out 2 L   |
| 5     | `05`      | Out 2 L+R |
| 6     | `06`      | Out 2 R   |
| 7     | `07`      | Out 3 L   |
| 8     | `08`      | Out 3 L+R |
| 9     | `09`      | Out 3 R   |
| 10    | `0A`      | USB 1 L   |
| 11    | `0B`      | USB 1 L+R |
| 12    | `0C`      | USB 1 R   |
| 13    | `0D`      | USB 2 L   |
| 14    | `0E`      | USB 2 L+R |
| 15    | `0F`      | USB 2 R   |
| 16    | `10`      | USB 3 L   |
| 17    | `11`      | USB 3 L+R |
| 18    | `12`      | USB 3 R   |

---

## Input Mode

3 options (`00`–`02`).

| Index | `<value>` | Option  |
| ----- | --------- | ------- |
| 0     | `00`      | Off     |
| 1     | `01`      | Dynamic |
| 2     | `02`      | Static  |

---

## Input Select

3 options (`00`–`02`). Panel visible when [Input Mode](#input-mode) is
**Dynamic** or **Static**.

| Index | `<value>` | Option  |
| ----- | --------- | ------- |
| 0     | `00`      | Left    |
| 1     | `01`      | L + R   |
| 2     | `02`      | Right   |

---

## Atomizer preset

**Inputs → Atomizer** menu index (not loop trigger keys). **Off** / **On** /
panel **2**–**16** → **`02`–`10`**.

| Index | `<value>` | Option |
| ----- | --------- | ------ |
| 0     | `00`      | Off    |
| 1     | `01`      | On     |
| 2     | `02`      | 2      |
| 3     | `03`      | 3      |
| 4     | `04`      | 4      |
| 5     | `05`      | 5      |
| 6     | `06`      | 6      |
| 7     | `07`      | 7      |
| 8     | `08`      | 8      |
| 9     | `09`      | 9      |
| 10    | `0A`      | 10     |
| 11    | `0B`      | 11     |
| 12    | `0C`      | 12     |
| 13    | `0D`      | 13     |
| 14    | `0E`      | 14     |
| 15    | `0F`      | 15     |
| 16    | `10`      | 16     |

---

## Bender Scale

**Edit Single → Common → Bender Scale** (`71` / `0x1C`). **`stored = index`**.

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | Linear        |
| 1     | `01`      | Exponential   |

---

## Delay Type

**Edit FX → Delay → Type**. **`stored = index`**.

| Index | `<value>` | Option         |
| ----- | --------- | -------------- |
| 0     | `00`      | Classic        |
| 1     | `01`      | Tape Clocked   |
| 2     | `02`      | Tape Free      |
| 3     | `03`      | Tape Doppler   |

---

## Delay panel visibility {#delay-panel-visibility}

**Edit FX → Delay**. Panel-confirmed (TI mk2). **Type** is always available.

### Send = Off (`00`)

For every **Type**, when **Send** = **Off** (`00` in [Delay
Send](#delay-send-lcd)),
the panel shows only **Type**, **Send**, and **Feedback** (panel-confirmed). No
**Delay Time** / **Time**, **Mode**, **Clock**, **Coloration**, LFO rows, or
other
tape/classic rows.

| Control      | Visible | Notes                                                                                       |
| ------------ | ------- | ------------------------------------------------------------------------------------------- |
| **Type**     | Yes     | [Delay Type](#delay-type) — always available                                                |
| **Send**     | Yes     | [Delay Send (LCD)](#delay-send-lcd)                                                         |
| **Feedback** | Yes     | [Delay Feedback](#delay-feedback) — **Classic** **0.0..100.0 %**; **Tape** **0.0..200.0 %** |

Set **Send** to any value **other than Off** to reveal the type-specific
controls
below (**Type**, **Send**, and **Feedback** stay available).

### Type = Classic (`00`) — Send not Off

| Control                   | Visible                                     | Panel range / notes                                                                                       |
| ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Send                      | Yes                                         | [Delay Send (LCD)](#delay-send-lcd)                                                                       |
| Feedback                  | Yes                                         | [Delay Feedback](#delay-feedback) — **Classic** **0..100 %** / **Tape** **0..200 %** on **`73`**          |
| Mode                      | Yes                                         | [Delay Mode](#delay-mode) — **`01`–`16`**                                                                 |
| Coloration                | Yes                                         | [Delay Coloration](#delay-coloration) — **−64..+63** (panel-confirmed)                                    |
| LFO (Rate / Depth / Wave) | Yes                                         | [Delay LFO](#delay-lfo) — same panel page                                                                 |
| Clock                     | Simple Delay / Ping Pong … only             | [Delay Clock](#delay-clock) — **`00`–`10`**; **`00`** = **Off**                                           |
| Delay Time                | Simple/Ping Pong + **Clock** = **Off** only | [Delay Time (ms)](#delay-tape-time) — **not** on **Pattern** (`06`–`16`; panel-confirmed **Pattern 5+5**) |

When **Clock** is a tempo division (**not** **Off**), **Delay Time** is
**hidden**
(synced delay). When **Clock** = **Off** (`00`), **Delay Time** replaces it on
the
panel.

**Pattern …** modes (`06`–`16`): no **Clock**, no **Delay Time** / **Time** on
the
panel (confirmed on **Pattern 5+5**). **Coloration** and LFO rows stay visible —
see
[Delay Mode](#delay-mode).

### Type = Tape Clocked (`01`) — Send not Off

| Control     | Visible | Notes                                                          |
| ----------- | ------- | -------------------------------------------------------------- |
| Send        | Yes     | [Delay Send (LCD)](#delay-send-lcd) — same curve all **Types** |
| Feedback    | Yes     | [Delay Feedback](#delay-feedback) — **0.0..200.0 %**           |
| Left Clock  | Yes     | [Delay Tape Left Clock](#delay-tape-left-clock)                |
| Right Clock | Yes     | [Delay Tape Right Clock](#delay-tape-right-clock)              |
| Frequency   | Yes     | [Tape Frequency](#delay-tape-frequency)                        |
| Bandwidth   | Yes     | [Tape Bandwidth](#delay-tape-bandwidth)                        |
| Modulation  | Yes     | [Tape Modulation](#delay-tape-modulation)                      |

No **Mode**, **Clock**, **Coloration**, **Rate**, **Depth**, **LFO Wave**,
**Time**,
or **Ratio**.

### Type = Tape Free (`02`) or Tape Doppler (`03`) — Send not Off

| Control    | Visible | Panel range (Free = Doppler)                                                                     |
| ---------- | ------- | ------------------------------------------------------------------------------------------------ |
| Send       | Yes     | [Delay Send (LCD)](#delay-send-lcd) — **Off**, −46.2 dB … **0/−24.0 dB**, **Effect** (`00`–`7F`) |
| Feedback   | Yes     | [Delay Feedback](#delay-feedback) — **0.0..200.0 %**                                             |
| Time       | Yes     | [Delay Time (ms)](#delay-tape-time) — panel **Time** = Classic **Delay Time**; **0.0..693.6 ms** |
| Ratio      | Yes     | [Delay Tape Ratio](#delay-tape-ratio) — **1/4** … **4/1** (`00`–`06`)                            |
| Frequency  | Yes     | [Tape Frequency](#delay-tape-frequency) — **`0`–`127`**                                          |
| Bandwidth  | Yes     | [Tape Bandwidth](#delay-tape-bandwidth) — **`0`–`127`**                                          |
| Modulation | Yes     | [Tape Modulation](#delay-tape-modulation) — **0.0..100.0 %**                                     |

Same panel set and ranges for **Tape Free** (`02`) and **Tape Doppler** (`03`).
All seven type-specific rows above panel-confirmed on **Tape Doppler**
(`6E`/`0A`/`03`).
No **Left Clock** / **Right Clock** (Tape Clocked only). No Classic rows.

---

## Delay Tape Left Clock {#delay-tape-left-clock}

**Edit FX → Delay → Left Clock** (**Type** = Tape Clocked, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0D`**. **`stored = <value>`** (wire byte).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/32   |
| `01`      | 1/16   |
| `02`      | 2/16   |
| `03`      | 3/16   |
| `04`      | 4/16   |
| `05`      | 5/16   |

---

## Delay Tape Right Clock {#delay-tape-right-clock}

**Edit FX → Delay → Right Clock** (**Type** = Tape Clocked, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0E`**. Same options as
[Left Clock](#delay-tape-left-clock).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/32   |
| `01`      | 1/16   |
| `02`      | 2/16   |
| `03`      | 3/16   |
| `04`      | 4/16   |
| `05`      | 5/16   |

---

## Delay Tape Frequency {#delay-tape-frequency}

**Edit FX → Delay → Frequency** (**Tape Clocked**, **Tape Free**, **Tape
Doppler**
— not Classic). **No** **Time** / **Ratio** on Tape Clocked.
Live edit: **`cmd=0x70`**, param **`0x77`** (Page **A#119**). **`stored = lcd`**
(**`0`–`127`**). Panel **0..127** on **Tape Doppler** (`03`). Same param byte as
[Delay Coloration](#delay-coloration) on **Classic** (**`stored = ui + 64`**).

---

## Delay Tape Bandwidth {#delay-tape-bandwidth}

**Edit FX → Delay → Bandwidth** (all three **Tape** types when **Send** ≠ Off).
Live edit:
**`cmd=0x6E`**, param **`0x11`**. **`stored = lcd`** (**`0`–`127`**). Panel
**0..127**
on **Tape Doppler** (`03`).

---

## Delay Tape Modulation {#delay-tape-modulation}

**Edit FX → Delay → Modulation** (all three **Tape** types when **Send** ≠ Off).
Live edit:
**`cmd=0x70`**, param **`0x75`** (same param byte as Classic delay
[Delay Feedback](docs/live-edit/effects.md#delay-feedback); tape
**Feedback** uses **`73`** instead).

**0.0..100.0 %**:

```text
stored = round(pct × 127 / 100)
```

**`00`** = 0 %, **`7F`** = 100.0 %. Panel **0.0..100.0 %** on **Tape Doppler**
(`03`).

---

## Delay Time (ms) {#delay-tape-time}

One control, two panel labels: **Delay Time** (**Classic**) and **Time** (**Tape
Free** / **Tape Doppler**). Same live edit, scale, and wire map.

Live edit: **`cmd=0x70`**, param **`0x72`** (Page **A#114**). Panel **0.0..693.6
ms**
(one decimal on LCD). **`stored = lcd`** (direct byte **`00`–`7F`**). Hardware
TX
confirmed (**Tape Free** `6E`/`0A`/`02`, **Time** sweep `70`/`72`
**`00`–`7F`**).

| Context                          | Panel label    | When visible                                                                                                                                      |
| -------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Classic**                      | **Delay Time** | **Send** ≠ Off, **Mode** = Simple Delay or Ping Pong … (`01`–`05`), **[Clock](#delay-clock) = Off** (`00`); **hidden** on **Pattern** (`06`–`16`) |
| **Tape Free** / **Tape Doppler** | **Time**       | **Send** ≠ Off (no **Clock** row)                                                                                                                 |

Approximate scale (intermediate rows not all spot-checked):

```text
lcd_ms ≈ stored × 693.6 / 127    # round display to 0.1 ms
```

| `<value>` | dec | LCD (ms) | Confirmed |
| --------- | --- | -------- | --------- |
| `00`      | 0   | 0.0      | ✓         |
| `20`      | 32  | 174.8    | ✓         |
| `28`      | 40  | 218.5    | ✓         |
| `40`      | 64  | 349.5    | ✓         |
| `50`      | 80  | 436.9    | ✓         |
| `60`      | 96  | 524.3    | ✓         |
| `64`      | 100 | 546.1    | ✓         |
| `70`      | 112 | 611.7    | ✓         |
| `7F`      | 127 | 693.6    | ✓         |

Wire **`40`** is hex (**decimal 64**), not decimal 40.

---

## Delay Tape Ratio {#delay-tape-ratio}

**Edit FX → Delay → Ratio** (**Tape Free** or **Tape Doppler**, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0C`**. **`stored = <value>`** (wire byte).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/4    |
| `01`      | 2/4    |
| `02`      | 3/4    |
| `03`      | 4/4    |
| `04`      | 4/3    |
| `05`      | 4/2    |
| `06`      | 4/1    |

Same seven options on **Tape Doppler** (`03`). Panel-confirmed (`6E`/`0C`
stepped).

---

## Delay Feedback {#delay-feedback}

**Edit FX → Delay → Feedback** (visible when **Send** = Off with **Type** and
**Send**;
also when **Send** ≠ Off with type-specific rows). **EFFECTS → Delay** knob 3 —
see
[Delay EFFECTS knobs](docs/live-edit/effects.md#delay-effects-knobs). Live edit:
**`cmd=0x70`**, param **`0x73`** (Page **A#115**).
Same wire byte; **encoding depends on Type**:

| **Type**             | Panel range      | Encoding                          |
| -------------------- | ---------------- | --------------------------------- |
| **Classic** (`00`)   | **0.0..100.0 %** | `stored = round(pct × 127 / 100)` |
| **Tape** (`01`–`03`) | **0.0..200.0 %** | `stored = round(pct × 127 / 200)` |

### Classic (`00`)

| LCD     | `<value>` | Confirmed                                          |
| ------- | --------- | -------------------------------------------------- |
| 0.0 %   | `00`      | ✓ (capture sweep; **Mode** = **Pattern 5+5** `16`) |
| 100.0 % | `7F`      | ✓ (capture sweep; **Mode** = **Pattern 5+5** `16`) |

### Tape (`01`–`03`)

| LCD     | `<value>` | Confirmed                        |
| ------- | --------- | -------------------------------- |
| 0 %     | `00`      | ✓ (capture)                      |
| 100.0 % | `40`      | ✓ (panel + Tape Clocked capture) |
| 200.0 % | `7F`      | ✓ (capture sweep)                |

See [single-live-edit — Delay
Feedback](docs/live-edit/effects.md#delay-feedback).

---

## Delay Mode {#delay-mode}

**Edit FX → Delay → Mode** (**Type** = Classic, **Send** ≠ Off). Live edit:
**`cmd=0x70`**, param **`0x70`** (Page **A#112**). **`stored = <value>`** (wire
byte;
first option is **`01`**, not **`00`**). Hardware TX confirmed (**`05`–`16`**
stepped; full enum **`01`–`16`**). Not **Type** (`6E`/`0A`).

**Do not confuse** with [Delay LFO Rate](#delay-lfo-rate) (**`70`/`74`**, not
**`0x70`**).

### Simple Delay and Ping Pong (`01`–`05`)

Show **Clock** (and **Delay Time** when **Clock** = Off), **Coloration**,
**Rate**,
**Depth**, **LFO Wave**.

| `<value>` | Option           | Confirmed |
| --------- | ---------------- | --------- |
| `01`      | Simple Delay     | ✓ (panel) |
| `02`      | Ping Pong 2:1    | ✓ (panel) |
| `03`      | Ping Pong 4:3    | ✓ (panel) |
| `04`      | Ping Pong 4:1    | ✓ (panel) |
| `05`      | Ping Pong 8:7    | ✓ (panel) |

### Pattern (`06`–`16`)

No **Clock** row; no **Delay Time** / **Time** control on the panel (confirmed
**Pattern 5+5**). **Coloration** + LFO rows remain. Live-edit TX confirmed for
**Feedback** (`73`) and **Coloration** (`77`) on **Pattern 5+5** (`16`).

| `<value>` | Option           | Confirmed |
| --------- | ---------------- | --------- |
| `06`      | Pattern 1+1      | ✓ (panel) |
| `07`      | Pattern 2+1      | ✓ (panel) |
| `08`      | Pattern 3+1      | ✓ (panel) |
| `09`      | Pattern 4+1      | ✓ (panel) |
| `0A`      | Pattern 5+1      | ✓ (panel) |
| `0B`      | Pattern 2+3      | ✓ (panel) |
| `0C`      | Pattern 2+5      | ✓ (panel) |
| `0D`      | Pattern 3+2      | ✓ (panel) |
| `0E`      | Pattern 3+3      | ✓ (panel) |
| `0F`      | Pattern 3+4      | ✓ (panel) |
| `10`      | Pattern 3+5      | ✓ (panel) |
| `11`      | Pattern 4+3      | ✓ (panel) |
| `12`      | Pattern 4+5      | ✓ (panel) |
| `13`      | Pattern 5+2      | ✓ (panel) |
| `14`      | Pattern 5+3      | ✓ (panel) |
| `15`      | Pattern 5+4      | ✓ (panel) |
| `16`      | Pattern 5+5      | ✓ (panel) |

**Simple Delay** / **Ping Pong …**: **Clock** + **Delay Time** when **Clock** =
**Off** — [Delay Clock](#delay-clock), [Delay Time (ms)](#delay-tape-time).

---

## Delay Coloration {#delay-coloration}

**Edit FX → Delay → Coloration** (**Type** = Classic, **Send** ≠ Off). **EFFECTS
→
Delay** knob 2 (**Delay Color**) — same byte when Classic routing applies — see
[Delay EFFECTS knobs](docs/live-edit/effects.md#delay-effects-knobs). Panel
**−64..+63**
(signed UI). **`stored = ui + 64`** (direct wire byte **`00`–`7F`**).

```text
stored = ui + 64
ui     = stored − 64
```

| UI  | `<value>` | Confirmed                                                  |
| --- | --------- | ---------------------------------------------------------- |
| −64 | `00`      | ✓ (EDIT FX + EFFECTS knob; full sweep to **+63** and back) |
| +0  | `40`      | ✓ (panel + capture)                                        |
| +63 | `7F`      | ✓ (EDIT FX + EFFECTS knob sweep)                           |

Live edit: **`cmd=0x70`**, param **`0x77`** (Page **A#119**). Hardware TX
confirmed
(**`00`–`7F`–`00`**). Mod-matrix **Delay Coloration** id **`0x54`** ≠
live-edit param byte (same pattern as **Delay Rate** `0x1E` vs **`0x74`**).

On **Tape** types, **`77`** is [Tape Frequency](#delay-tape-frequency)
(**`0`–`127`**,
`stored = lcd`) — same wire byte, different **Type** context.

---

## Delay Clock

**Edit FX → Delay → Clock** ( **Type** = Classic, **Send** ≠ Off, **Mode** =
Simple Delay or Ping Pong …).
Live edit: **`F0 … 71 00 14 <value> F7`** (WAF80 Page **B#20**). **`stored =
<value>`**
(wire byte). Table order = **panel menu** (slow → fast). Distinct from Common
**Smooth Mode** (`71`/`19`); same division labels as
[Control Smooth Mode / clock quantize](#control-smooth-mode--clock-quantize)
quantize rows but **different** wire map.

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | 1/64   |
| `02`      | 1/32   |
| `0B`      | 1/24   |
| `07`      | 3/64   |
| `03`      | 1/16   |
| `0C`      | 1/12   |
| `08`      | 3/32   |
| `04`      | 1/8    |
| `0D`      | 1/6    |
| `09`      | 3/16   |
| `05`      | 1/4    |
| `0E`      | 1/3    |
| `0A`      | 3/8    |
| `06`      | 1/2    |
| `0F`      | 2/3    |
| `10`      | 3/4    |

Valid wire values **`00`–`10`** only (every byte in that range is used; no
gaps).
**`11`**, **`12`** probed via SysEx → **ignored**. **`13`–`7F`** not in menu.

**Panel visibility:** **`00` Off** shows [Delay Time (ms)](#delay-tape-time)
(**0.0..693.6 ms**). Any synced division **hides** **Delay Time** (tempo-locked
delay length).

---

## Delay LFO {#delay-lfo}

**Edit FX → Delay** — **Rate**, **Depth**, and **LFO Wave** share one panel page
(delay **LFO modulation** of the effect). Visible on **Classic** when **Send** ≠
Off
(and on **Pattern …** modes with **Coloration**; no **Clock** / **Delay Time**).
Not on **Tape** types (those use **Frequency** / **Bandwidth** / **Modulation**
instead).

| Control      | Live edit                     | Range                          |
| ------------ | ----------------------------- | ------------------------------ |
| **Rate**     | [`70`/`74`](#delay-lfo-rate)  | **`0`–`127`** (`stored = lcd`) |
| **Depth**    | [`70`/`75`](#delay-lfo-depth) | **0.0..100.0 %**               |
| **LFO Wave** | [`70`/`76`](#delay-lfo-wave)  | enum **`00`–`05`**             |

---

## Delay LFO Rate {#delay-lfo-rate}

**Edit FX → Delay → Rate** (part of [Delay LFO](#delay-lfo)). Live edit:
**`cmd=0x70`**, param
**`0x74`** (Page **A#116**). **`stored = lcd`** (**`0`–`127`**). Hardware TX
confirmed
(sweep **`00`–`7F`**; **Rate** `0` → **`00`**). Not **`0x70`** ([Delay
Mode](#delay-mode)).
Mod-matrix **Delay Rate** id **`0x1E`** ≠ live-edit param byte.

| LCD | `<value>` | Confirmed           |
| --- | --------- | ------------------- |
| 0   | `00`      | ✓ (panel + capture) |
| 127 | `7F`      | ✓ (capture sweep)   |

---

## Delay LFO Depth {#delay-lfo-depth}

**Edit FX → Delay → Depth** (part of [Delay LFO](#delay-lfo); **Classic** only
on this
LFO page). Live edit: **`cmd=0x70`**, param **`0x75`** (Page **A#117**). Panel
**0.0..100.0 %**. Hardware TX confirmed (full sweep **`00`–`7F`**).

```text
stored = round(pct × 127 / 100)
```

| LCD     | `<value>` | Confirmed   |
| ------- | --------- | ----------- |
| 0.0 %   | `00`      | ✓ (capture) |
| 100.0 % | `7F`      | ✓ (capture) |

On **Tape** types, **`75`** is [Tape Modulation](#delay-tape-modulation) (same
wire
byte, different **Type** context). **`73`** is [Delay
Feedback](#delay-feedback).

---

## Delay LFO Wave {#delay-lfo-wave}

**Edit FX → Delay → LFO Wave** (part of [Delay LFO](#delay-lfo)). Live edit:
**`cmd=0x70`**, param **`0x76`**
(Page **A#118**). **`stored = <value>`** (wire byte).

| `<value>` | Option    | Notes                                             |
| --------- | --------- | ------------------------------------------------- |
| `00`      | Sine      |                                                   |
| `01`      | Triangle  |                                                   |
| `02`      | Sawtooth  |                                                   |
| `03`      | Square    |                                                   |
| `04`      | S&H       | **Sample and Hold**                               |
| `05`      | S&G       | **Sample and Glide** — S&H through a slew limiter |

---

## Delay Send (LCD) {#delay-send-lcd}

**Edit FX → Delay → Send** (all **Types**). Also **EFFECTS → Delay** knob 1 —
[single-live-edit — Delay EFFECTS
knobs](docs/live-edit/effects.md#delay-effects-knobs).
**`stored = index`** (`00`–`7F`). Live edit: **`cmd=0x70`**, param **`0x71`**
(Page **A#113**). Panel-confirmed on TI mk2 (see table). Rows **`19`–`1D`**,
**`1F`–`27`**, **`29`–`3F`** are
**amplitude-interpolated** (not yet spot-checked).

| Region                  | Rule                                                                |
| ----------------------- | ------------------------------------------------------------------- |
| `00`                    | **Off**                                                             |
| `01`–`40`               | Piecewise attenuation — see table                                   |
| `41`–`95` (`29`–`5F`)   | **`−0.25 × (96 − index)`** dB; wholes show **`.0`** (**`−9.0 dB`**) |
| `96`–`103` (`60`–`67`)  | **`0/−0.3 × (index − 96)`** dB                                      |
| `104`–`107` (`68`–`6B`) | Increasing steps — see table                                        |
| `108`–`126` (`6C`–`7E`) | **`0/−X dB`** headroom                                              |
| `127` (`7F`)            | **Effect** (max send)                                               |

| Index | `<value>` | LCD        |     |
| ----- | --------- | ---------- | --- |
| 0     | `00`      | Off        |     |
| 1     | `01`      | −46.2 dB   | ✓   |
| 2     | `02`      | −40.2 dB   | ✓   |
| 3     | `03`      | −36.6 dB   | ✓   |
| 4     | `04`      | −34.1 dB   | ✓   |
| 5     | `05`      | −32.2 dB   | ✓   |
| 6     | `06`      | −30.6 dB   | ✓   |
| 7     | `07`      | −29.3 dB   | ✓   |
| 8     | `08`      | −28.1 dB   | ✓   |
| 9     | `09`      | −27.1 dB   | ✓   |
| 10    | `0A`      | −26.2 dB   | ✓   |
| 11    | `0B`      | −25.4 dB   | ✓   |
| 12    | `0C`      | −24.6 dB   | ✓   |
| 13    | `0D`      | −23.9 dB   | ✓   |
| 14    | `0E`      | −23.3 dB   | ✓   |
| 15    | `0F`      | −22.7 dB   | ✓   |
| 16    | `10`      | −22.1 dB   | ✓   |
| 17    | `11`      | −21.6 dB   | ✓   |
| 18    | `12`      | −21.1 dB   | ✓   |
| 19    | `13`      | −20.6 dB   | ✓   |
| 20    | `14`      | −20.6 dB   | ✓   |
| 21    | `15`      | −19.7 dB   | ✓   |
| 22    | `16`      | −19.3 dB   | ✓   |
| 23    | `17`      | −18.9 dB   | ✓   |
| 24    | `18`      | −18.6 dB   | ✓   |
| 25    | `19`      | −18.2 dB   | ≈   |
| 26    | `1A`      | −17.8 dB   | ≈   |
| 27    | `1B`      | −17.5 dB   | ≈   |
| 28    | `1C`      | −17.2 dB   | ≈   |
| 29    | `1D`      | −16.9 dB   | ≈   |
| 30    | `1E`      | −16.6 dB   | ✓   |
| 31    | `1F`      | −16.3 dB   | ≈   |
| 32    | `20`      | −16.0 dB   | ≈   |
| 33    | `21`      | −15.7 dB   | ≈   |
| 34    | `22`      | −15.5 dB   | ≈   |
| 35    | `23`      | −15.2 dB   | ≈   |
| 36    | `24`      | −14.9 dB   | ≈   |
| 37    | `25`      | −14.7 dB   | ≈   |
| 38    | `26`      | −14.5 dB   | ≈   |
| 39    | `27`      | −14.2 dB   | ≈   |
| 40    | `28`      | −14.0 dB   | ✓   |
| 41    | `29`      | −13.75 dB  | ✓   |
| 42    | `2A`      | −13.5 dB   | ✓   |
| 43    | `2B`      | −13.25 dB  | ✓   |
| 44    | `2C`      | −13.0 dB   | ✓   |
| 45    | `2D`      | −12.75 dB  | ✓   |
| 46    | `2E`      | −12.5 dB   | ✓   |
| 47    | `2F`      | −12.25 dB  | ✓   |
| 48    | `30`      | −12.0 dB   | ✓   |
| 49    | `31`      | −11.75 dB  | ✓   |
| 50    | `32`      | −11.5 dB   | ✓   |
| 51    | `33`      | −11.25 dB  | ✓   |
| 52    | `34`      | −11.0 dB   | ✓   |
| 53    | `35`      | −10.75 dB  | ✓   |
| 54    | `36`      | −10.5 dB   | ✓   |
| 55    | `37`      | −10.25 dB  | ✓   |
| 56    | `38`      | −10.0 dB   | ✓   |
| 57    | `39`      | −9.75 dB   | ✓   |
| 58    | `3A`      | −9.5 dB    | ✓   |
| 59    | `3B`      | −9.25 dB   | ✓   |
| 60    | `3C`      | −9.0 dB    | ✓   |
| 61    | `3D`      | −8.75 dB   | ✓   |
| 62    | `3E`      | −8.5 dB    | ✓   |
| 63    | `3F`      | −8.25 dB   | ✓   |
| 64    | `40`      | −8.0 dB    | ✓   |
| 65    | `41`      | −7.75 dB   | ✓   |
| 66    | `42`      | −7.5 dB    | ✓   |
| 67    | `43`      | −7.25 dB   | ✓   |
| 68    | `44`      | −7.0 dB    | ✓   |
| 69    | `45`      | −6.75 dB   | ✓   |
| 70    | `46`      | −6.5 dB    | ✓   |
| 71    | `47`      | −6.25 dB   | ✓   |
| 72    | `48`      | −6.0 dB    | ✓   |
| 73    | `49`      | −5.75 dB   | ✓   |
| 74    | `4A`      | −5.5 dB    | ✓   |
| 75    | `4B`      | −5.25 dB   | ✓   |
| 76    | `4C`      | −5.0 dB    | ✓   |
| 77    | `4D`      | −4.75 dB   | ✓   |
| 78    | `4E`      | −4.5 dB    | ✓   |
| 79    | `4F`      | −4.25 dB   | ✓   |
| 80    | `50`      | −4.0 dB    | ✓   |
| 81    | `51`      | −3.75 dB   | ✓   |
| 82    | `52`      | −3.5 dB    | ✓   |
| 83    | `53`      | −3.25 dB   | ✓   |
| 84    | `54`      | −3.0 dB    | ✓   |
| 85    | `55`      | −2.75 dB   | ✓   |
| 86    | `56`      | −2.5 dB    | ✓   |
| 87    | `57`      | −2.25 dB   | ✓   |
| 88    | `58`      | −2.0 dB    | ✓   |
| 89    | `59`      | −1.75 dB   | ✓   |
| 90    | `5A`      | −1.5 dB    | ✓   |
| 91    | `5B`      | −1.25 dB   | ✓   |
| 92    | `5C`      | −1.0 dB    | ✓   |
| 93    | `5D`      | −0.75 dB   | ✓   |
| 94    | `5E`      | −0.5 dB    | ✓   |
| 95    | `5F`      | −0.25 dB   | ✓   |
| 96    | `60`      | 0/0 dB     | ✓   |
| 97    | `61`      | 0/−0.3 dB  | ✓   |
| 98    | `62`      | 0/−0.6 dB  | ✓   |
| 99    | `63`      | 0/−0.9 dB  | ✓   |
| 100   | `64`      | 0/−1.2 dB  | ✓   |
| 101   | `65`      | 0/−1.5 dB  | ✓   |
| 102   | `66`      | 0/−1.8 dB  | ✓   |
| 103   | `67`      | 0/−2.1 dB  | ✓   |
| 104   | `68`      | 0/−2.5 dB  | ✓   |
| 105   | `69`      | 0/−2.9 dB  | ✓   |
| 106   | `6A`      | 0/−3.3 dB  | ✓   |
| 107   | `6B`      | 0/−3.7 dB  | ✓   |
| 108   | `6C`      | 0/−4.1 dB  | ✓   |
| 109   | `6D`      | 0/−4.5 dB  | ✓   |
| 110   | `6E`      | 0/−5.0 dB  | ✓   |
| 111   | `6F`      | 0/−5.5 dB  | ✓   |
| 112   | `70`      | 0/−6.0 dB  | ✓   |
| 113   | `71`      | 0/−6.6 dB  | ✓   |
| 114   | `72`      | 0/−7.2 dB  | ✓   |
| 115   | `73`      | 0/−7.8 dB  | ✓   |
| 116   | `74`      | 0/−8.5 dB  | ✓   |
| 117   | `75`      | 0/−9.3 dB  | ✓   |
| 118   | `76`      | 0/−10.1 dB | ✓   |
| 119   | `77`      | 0/−11.0 dB | ✓   |
| 120   | `78`      | 0/−12.0 dB | ✓   |
| 121   | `79`      | 0/−13.2 dB | ✓   |
| 122   | `7A`      | 0/−14.5 dB | ✓   |
| 123   | `7B`      | 0/−16.1 dB | ✓   |
| 124   | `7C`      | 0/−18.1 dB | ✓   |
| 125   | `7D`      | 0/−20.6 dB | ✓   |
| 126   | `7E`      | 0/−24.0 dB | ✓   |
| 127   | `7F`      | Effect     | ✓   |

**`60`–`67`:** **`0/−0.3 × (index − 96)`** dB. **`68`–`6B`:** larger steps
(**`68`** **`−2.5`**, then **`−0.4`** through **`6A`**, **`6B`** **`−3.7`**).
**`6C`–`7E`:** headroom ladder. **`7F`** = **Effect**.

Legend: **✓** = panel-confirmed; **≈** = **`01`–`40`** gaps only (amp interp).

---

## Reverb Mode {#reverb-mode}

**Edit FX → Reverb → Mode**. Part-sound buffer (**`6E`**, not Page A). Live
edit:
**`cmd=0x6E`**, param **`0x01`**. **`stored = <value>`** (wire byte). Hardware
TX
confirmed (**`01`–`03`** stepped; **`00`** Off). First active algorithm is
**`01`**
(not **`00`**), same pattern as [Delay Mode](#delay-mode).

| `<value>` | Option      | Confirmed           | Meaning (TI reference)                         |
| --------- | ----------- | ------------------- | ---------------------------------------------- |
| `00`      | Off         | ✓ (panel)           | No reverb; other rows **hidden**               |
| `01`      | Reverb      | ✓ (capture + panel) | Standard reverb + [Predelay](#reverb-predelay) |
| `02`      | Feedback 1  | ✓ (capture + panel) | Feedback in predelay line → multiple tails     |
| `03`      | Feedback 2  | ✓ (capture + panel) | Like Feedback 1; first tail **immediate**      |

---

## Reverb Type {#reverb-type}

**Edit FX → Reverb → Type** — room / early-reflection character (**Ambience** …
**Hall**). Visible when **Mode** is **Reverb** or **Feedback 1/2** (not **Mode**
**Off**). Changing **Type** does not hide other rows. Live edit: **`cmd=0x6E`**,
param **`0x03`**. **`stored = <value>`**
(wire byte). Hardware TX confirmed (**`00`–`03`**).

```text
F0 00 20 33 01 00 6E 00 03 00 F7   # Ambience (Part 1)
```

| `<value>` | Option     | Confirmed           |
| --------- | ---------- | ------------------- |
| `00`      | Ambience   | ✓ (capture + panel) |
| `01`      | Small Room | ✓ (capture + panel) |
| `02`      | Large Room | ✓ (capture + panel) |
| `03`      | Hall       | ✓ (capture + panel) |

---

## Reverb panel visibility {#reverb-panel-visibility}

**Edit FX → Reverb**. Panel-confirmed on TI mk2 (differs from TI reference
manual
in places and from [Delay panel visibility](#delay-panel-visibility)).

### Mode = Off (`00`)

**Mode** and **[Send](#reverb-send-lcd)** only — algorithm rows **hidden** (TI
reference; not re-checked this session).

### Send = Off (`00` on Send control)

When **Mode** is **Reverb** or **Feedback 1/2**, **Send** = **Off** does **not**
hide **Type**, **Clock**, **Time**, **Damping**, **Coloration**, or **Predelay**
(mk2 panel-confirmed). Unlike **Delay**, where **Send** = **Off** leaves only
**Type**, **Send**, and **Feedback**.

### Mode = Reverb (`01`), Feedback 1 (`02`), or Feedback 2 (`03`)

Shared rows for all three **Modes** (mk2 panel-confirmed). **Feedback 2** shows
the
**same** controls as **Feedback 1** (only the algorithm differs — first tail
**immediate** on **Feedback 2** per TI reference).

| Control        | Visible                  | Notes                                                                          |
| -------------- | ------------------------ | ------------------------------------------------------------------------------ |
| **Mode**       | Yes                      | [Reverb Mode](#reverb-mode)                                                    |
| **Send**       | Yes                      | [Reverb Send (LCD)](#reverb-send-lcd)                                          |
| **Type**       | Yes                      | [Reverb Type](#reverb-type) — room **Type** does not hide other rows           |
| **Clock**      | Yes                      | [Reverb Clock](#reverb-clock)                                                  |
| **Time**       | Yes                      | [Reverb Time](#reverb-time) — **0..127**                                       |
| **Damping**    | Yes                      | [Reverb Damping](#reverb-damping) — **0.0..100.0 %**                           |
| **Coloration** | Yes                      | [Reverb Coloration](#reverb-coloration) — **−64..+63**                         |
| **Predelay**   | **Clock** = **Off** only | [Reverb Predelay](#reverb-predelay) — **0.0..500.0 ms**                        |
| **Feedback**   | **Feedback 1/2 only**    | [Reverb Feedback](#reverb-feedback) — **0..127**; **not** on **Reverb** (`01`) |

When **Clock** is a tempo division (**not** **Off**), **Predelay** is
**hidden**.
When **Clock** = **Off**, **Predelay** is on the panel.

**Signal path:** delay → reverb in series (dry + delay → reverb input) — TI
reference.

---

## Reverb Clock {#reverb-clock}

**Edit FX → Reverb → Clock**. Synchronizes **[Predelay](#reverb-predelay)** to
the
tempo grid. Live edit: **`cmd=0x6E`**, param **`0x08`**. **`stored = <value>`**
(wire byte). Hardware TX confirmed (sweep **Off** → **3/4** (`10`) → **Off**).

**Same wire map** as [Delay Clock](#delay-clock) (`71`/`14` on Page **B**);
Reverb
uses the **part buffer** (`6E`) instead.

| `<value>` | Option           |
| --------- | ---------------- |
| `00`      | Off ✓ (capture)  |
| `01`      | 1/64 ✓ (capture) |
| `02`      | 1/32             |
| `0B`      | 1/24             |
| `07`      | 3/64             |
| `03`      | 1/16             |
| `0C`      | 1/12             |
| `08`      | 3/32             |
| `04`      | 1/8              |
| `0D`      | 1/6              |
| `09`      | 3/16             |
| `05`      | 1/4              |
| `0E`      | 1/3              |
| `0A`      | 3/8              |
| `06`      | 1/2              |
| `0F`      | 2/3              |
| `10`      | 3/4 ✓ (capture)  |

Valid wire values **`00`–`10`** (same as Delay Clock). **`11`–`7F`** not in
menu.

```text
F0 00 20 33 01 00 6E 00 08 00 F7   # Off
F0 00 20 33 01 00 6E 00 08 10 F7   # 3/4
```

---

## Reverb Time {#reverb-time}

**Edit FX → Reverb → Time**. Tail
length **0..127** on the panel. Live edit: **`cmd=0x6E`**, param **`0x04`**.
**`stored = lcd`** (direct wire byte). Hardware TX confirmed (sweep
**`00`–`7F`**).
Mod-matrix **Reverb Time** id **`0x1C`** ≠ live-edit param byte.

| LCD | `<value>` | Confirmed   |
| --- | --------- | ----------- |
| 0   | `00`      | ✓ (capture) |
| 127 | `7F`      | ✓ (capture) |

```text
F0 00 20 33 01 00 6E 00 04 00 F7   # 0
F0 00 20 33 01 00 6E 00 04 44 F7   # 68 (panel anchor)
F0 00 20 33 01 00 6E 00 04 7F F7   # 127
```

---

## Reverb Damping {#reverb-damping}

**Edit FX → Reverb → Damping**. Panel **0.0..100.0 %**.
Live edit: **`cmd=0x6E`**, param **`0x05`**.

```text
stored = round(pct × 127 / 100)
```

Hardware TX confirmed (sweep **`00`–`7F`**). Mod-matrix **Reverb Dampening** id
**`0x65`** ≠ live-edit param byte.

| LCD     | `<value>` | Confirmed                                 |
| ------- | --------- | ----------------------------------------- |
| 0.0 %   | `00`      | ✓ (capture)                               |
| 15.6 %  | `14`      | ✓ (panel; `round(15.6 × 127 / 100)` = 20) |
| 100.0 % | `7F`      | ✓ (capture)                               |

```text
F0 00 20 33 01 00 6E 00 05 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 05 7F F7   # 100.0 %
```

---

## Reverb Coloration {#reverb-coloration}

**Edit FX → Reverb → Coloration**. Post-EQ **−64..+63**.
Live edit: **`cmd=0x6E`**, param **`0x06`**.

```text
stored = ui + 64
ui     = stored − 64
```

Hardware TX confirmed (sweep **+63** → **−64**, **`7F`–`00`**). Mod-matrix
**Reverb
Coloration** id **`0x66`** ≠ live-edit param byte (Delay
[Coloration](#delay-coloration) uses **`70`/`77`** on Classic).

| UI  | `<value>` | Confirmed           |
| --- | --------- | ------------------- |
| −64 | `00`      | ✓ (capture)         |
| +0  | `40`      | ✓ (panel + capture) |
| +63 | `7F`      | ✓ (capture)         |

```text
F0 00 20 33 01 00 6E 00 06 00 F7   # −64
F0 00 20 33 01 00 6E 00 06 40 F7   # +0
F0 00 20 33 01 00 6E 00 06 7F F7   # +63
```

---

## Reverb Predelay {#reverb-predelay}

**Edit FX → Reverb → Predelay**. **0.0..500.0 ms** on the TI mk2 panel when
**[Clock](#reverb-clock)** = **Off** (TI reference manual cites **300.4 ms** max
—
mk2 panel reaches **500.0 ms**). Also used as the repeat period for **Feedback
1/2**. Live edit: **`cmd=0x6E`**, param **`0x07`**. **`stored = lcd`** (wire
byte
**`00`–`5C`** only — **`5D`–`7F`** not used).

```text
lcd_ms ≈ stored × 500.0 / 92    # 92 = 0x5C (panel max wire)
```

Hardware TX confirmed (sweep **0.0** → **500.0** ms; max wire **`5C`**).

| LCD (ms) | `<value>` | Confirmed               |
| -------- | --------- | ----------------------- |
| 0.0      | `00`      | ✓ (capture + panel)     |
| 174.8    | `20`      | ✓ (panel)               |
| 349.5    | `40`      | ✓ (panel)               |
| 500.0    | `5C`      | ✓ (capture + panel max) |

```text
F0 00 20 33 01 00 6E 00 07 00 F7   # 0.0 ms
F0 00 20 33 01 00 6E 00 07 20 F7   # 174.8 ms
F0 00 20 33 01 00 6E 00 07 40 F7   # 349.5 ms
F0 00 20 33 01 00 6E 00 07 5C F7   # 500.0 ms
```

---

## Reverb Feedback {#reverb-feedback}

**Edit FX → Reverb → Feedback**. **0..127** on the panel. Visible only when
**Mode** = **Feedback 1** (`02`) or **Feedback 2** (`03`) — same panel on both.
Live edit: **`cmd=0x6E`**, param **`0x09`**. **`stored = lcd`** (direct wire
byte
**`00`–`7F`**). Hardware TX confirmed (**Feedback 2** mode, sweep to **`7F`**).
Mod-matrix **Reverb Feedback** id **`0x67`** ≠ live-edit param byte.

| LCD | `<value>` | Confirmed   |
| --- | --------- | ----------- |
| 0   | `00`      | ✓ (capture) |
| 127 | `7F`      | ✓ (capture) |

```text
F0 00 20 33 01 00 6E 00 09 00 F7   # 0
F0 00 20 33 01 00 6E 00 09 7F F7   # 127
```

---

## Reverb Send (LCD) {#reverb-send-lcd}

**Edit FX → Reverb → Send** (live edit **`6E`/`02`** — see
[single-live-edit.md](docs/live-edit/effects.md#reverb-send-cmd0x6e)). **`stored
= index`**
(`00`–`7F`). **`stored = lcd`** (direct wire byte). **Not the same LCD curve as
[Delay Send](#delay-send-lcd)** (`70`/`71`).

Hardware TX confirmed (**Off** `00` → **Effect** `7F` sweep; sparse LCD rows
below).
Unlisted indices still **TBD** on panel labels:

| Index | `<value>` | LCD                          |
| ----- | --------- | ---------------------------- |
| 0     | `00`      | Off ✓ (capture)              |
| 1     | `01`      | −46.2 dB                     |
| 2     | `02`      | −40.2 dB                     |
| 10    | `0A`      | −26.2 dB                     |
| 20    | `14`      | −20.6 dB                     |
| 30    | `1E`      | −16.6 dB                     |
| 40    | `28`      | −14.0 dB                     |
| 41    | `29`      | −13.75 dB                    |
| 45    | `2D`      | −12.75 dB                    |
| 54    | `36`      | −10.5 dB                     |
| 57    | `39`      | −9.75 dB                     |
| 90    | `5A`      | −1.5 dB                      |
| 91    | `5B`      | −1.25 dB                     |
| 92    | `5C`      | −1.0 dB                      |
| 93    | `5D`      | −0.75 dB                     |
| 94    | `5E`      | −0.5 dB                      |
| 95    | `5F`      | −0.25 dB                     |
| 96    | `60`      | 0/0 dB ✓ (capture)           |
| 97    | `61`      | 0/−0.3 dB                    |
| 98    | `62`      | 0/−0.6 dB                    |
| 99    | `63`      | 0/−0.9 dB                    |
| 100   | `64`      | 0/−1.2 dB                    |
| 108   | `6C`      | 0/−4.1 dB                    |
| 109   | `6D`      | 0/−4.5 dB                    |
| 110   | `6E`      | 0/−5.0 dB                    |
| 111   | `6F`      | 0/−5.5 dB                    |
| 112   | `70`      | 0/−6.0 dB                    |
| 114   | `72`      | 0/−7.2 dB                    |
| 115   | `73`      | 0/−7.8 dB                    |
| 116   | `74`      | 0/−8.5 dB                    |
| 117   | `75`      | 0/−9.3 dB                    |
| 118   | `76`      | 0/−10.1 dB                   |
| 119   | `77`      | 0/−11.0 dB ✓ (wire in sweep) |
| 120   | `78`      | 0/−12.0 dB                   |
| 121   | `79`      | 0/−13.2 dB                   |
| 122   | `7A`      | 0/−14.5 dB                   |
| 123   | `7B`      | 0/−16.1 dB                   |
| 124   | `7C`      | 0/−18.1 dB                   |
| 125   | `7D`      | 0/−20.6 dB                   |
| 126   | `7E`      | 0/−24.0 dB                   |
| 127   | `7F`      | Effect (max) ✓ (capture)     |

Intermediate wire bytes from the same sweep (LCD labels **TBD**): **`0D`**,
**`19`**,
**`24`**, **`33`**, **`3F`**, **`43`**, **`52`**, **`61`**, **`62`**, **`77`**.

All other indices: label on panel sweep if needed.

---

## EQ Low Frequency {#eq-low-frequency}

**Edit FX → Low EQ → Frequency (Hz)**. Page **B#45** = **`0x2D`**. Live edit
**`cmd=0x71`**, param **`0x2D`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-low-frequency-cmd0x71-param-0x2d).

Log-spaced Hz display (not `stored = lcd` Hz). Hardware TX confirmed (sweep
**`00`–`7F`** then down to **`00`**).

| `<value>` | LCD (Hz) | Notes |
| --------- | -------- | ----- |
| `00`      | 32       | min ✓ |
| `7F`      | 458      | max ✓ |

INIT-style panel reading **78 Hz** is mid-band (exact wire byte not logged at
session start; approximate fit on log curve: **`~0x42`**).

---

## EQ Low Gain {#eq-low-gain}

**Edit FX → Low EQ → Gain**. Page **B#95** = **`0x5F`**. Live edit
**`cmd=0x71`**, param **`0x5F`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-low-gain-cmd0x71-param-0x5f).

Symmetric dB range with **Off** (0 dB) at wire center **`40`**:

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

Approximate mapping: **`gain_db ≈ (stored − 64) × 16 / 63`** (64 = **`0x40`**).

**Not** [Reverb Send](reverb-send-lcd) index **`0x5F`** (−0.25 dB row). **Not**
Page A **Filter 2 Envelope Amount** (`70`/`2D`).

---

## EQ Mid Frequency {#eq-mid-frequency}

**Edit FX → Mid EQ → Frequency (Hz)**. Page **B#93** = **`0x5D`**. Live edit
**`cmd=0x71`**, param **`0x5D`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-mid-frequency-cmd0x71-param-0x5d).

Log-spaced Hz / kHz display (**`stored` ≠ Hz**). Hardware TX confirmed (sweep
**`7F`** → **`00`** → **`3E`**).

| `<value>` | LCD  | Notes                       |
| --------- | ---- | --------------------------- |
| `00`      | 19   | min (Hz) ✓                  |
| `3E`      | 632  | Hz ✓ (capture)              |
| `7F`      | 24.0 | max (panel shows **kHz**) ✓ |

INIT-style panel **1046 Hz** is mid-band (exact wire byte not logged at session
start).

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid
Frequency**
(wire **`71`** in **`71`/`3E`**, not param **`5D`**).

---

## EQ Mid Gain {#eq-mid-gain}

**Edit FX → Mid EQ → Gain**. Page **B#92** = **`0x5C`**. Live edit
**`cmd=0x71`**, param **`0x5C`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-mid-gain-cmd0x71-param-0x5c).

Same symmetric dB encoding as [EQ Low Gain](#eq-low-gain) (**`40`** = Off):

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid Gain**
(wire **`70`** in **`71`/`3E`**, not param **`5C`**).

---

## EQ Mid Q-Factor {#eq-mid-q-factor}

**Edit FX → Mid EQ → Q-Factor**. Page **B#94** = **`0x5E`**. Live edit
**`cmd=0x71`**, param **`0x5E`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-mid-q-factor-cmd0x71-param-0x5e).

| `<value>` | LCD (Q) | Notes                                        |
| --------- | ------- | -------------------------------------------- |
| `00`      | 0.28    | min ✓                                        |
| `40`      | 1.58    | ✓ (capture; panel had started near **1.02**) |
| `7F`      | 15.4    | max ✓                                        |

Non-linear LCD curve between endpoints (full table **TBD**).

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid
Q-Factor**
(wire **`72`** in **`71`/`3E`**, not param **`5E`**).

---

## EQ High Frequency {#eq-high-frequency}

**Edit FX → High EQ → Frequency (Hz)**. Page **B#46** = **`0x2E`**. Live edit
**`cmd=0x71`**, param **`0x2E`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-high-frequency-cmd0x71-param-0x2e).

Log-spaced Hz / kHz display (**`stored` ≠ Hz**). Hardware TX confirmed (sweep
**`7F`** → **`00`** → **`40`**).

| `<value>` | LCD  | Notes                       |
| --------- | ---- | --------------------------- |
| `00`      | 1831 | Hz ✓                        |
| `40`      | 7012 | Hz ✓ (capture)              |
| `7F`      | 24.0 | max (panel shows **kHz**) ✓ |

INIT-style panel **10.6** is mid/high band (likely **kHz**; exact wire byte not
logged at session start).

**Not** Page A **Filter 1 Keyfollow** (`70`/`2E`).

---

## EQ High Gain {#eq-high-gain}

**Edit FX → High EQ → Gain**. Page **B#96** = **`0x60`**. Live edit
**`cmd=0x71`**, param **`0x60`** — see
[single-live-edit.md](docs/live-edit/effects.md#eq-high-gain-cmd0x71-param-0x60).

Same symmetric dB encoding as [EQ Low Gain](#eq-low-gain) (**`40`** = Off):

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

---

## EFFECTS focus group 1 {#effects-focus-group-1}

**EFFECTS** section — first **SELECT** group (Delay / Reverb / EQ band). Live
edit
**`cmd=0x6E`**, param **`0x75`** — see
[single-live-edit — EFFECTS section
focus](docs/live-edit/effects.md#effects-section-focus).
**`stored = index`** (`00`–`04` confirmed; higher values **TBD**).

| Index | `<value>` | Panel focus | Confirmed              |
| ----- | --------- | ----------- | ---------------------- |
| 0     | `00`      | Delay       | ✓ (panel + `sendmidi`) |
| 1     | `01`      | Reverb      | ✓                      |
| 2     | `02`      | Low EQ      | ✓                      |
| 3     | `03`      | Mid EQ      | ✓                      |
| 4     | `04`      | High EQ     | ✓                      |

Does **not** arm effect parameters; only changes which effect the three
**EFFECTS**
knobs edit (e.g. [Delay EFFECTS
knobs](docs/live-edit/effects.md#delay-effects-knobs) when
**Delay**). Panel **LED** can lag the SysEx by **> 0.5 s** — when testing with
`sendmidi`, pause **≥ 1 s** between values so each focus change is visible.

---

## EFFECTS focus group 2 {#effects-focus-group-2}

**EFFECTS** section — second **SELECT** group. Live edit **`cmd=0x6E`**, param
**`0x76`** — see
[single-live-edit — EFFECTS section
focus](docs/live-edit/effects.md#effects-section-focus).
**`stored = index`** (`00`–`04` confirmed; higher values **TBD**). Same **LED
lag** as [group 1](#effects-focus-group-1) (**≥ 1 s** between `sendmidi`
probes).

| Index | `<value>` | Panel focus | Confirmed           |
| ----- | --------- | ----------- | ------------------- |
| 0     | `00`      | Distortion  | ✓ (panel + capture) |
| 1     | `01`      | Character   | ✓                   |
| 2     | `02`      | Chorus      | ✓                   |
| 3     | `03`      | Phaser      | ✓                   |
| 4     | `04`      | **Others**  | ✓                   |

**Others (`04`)** — **EDIT FX** (or equivalent LCD path) then offers
**Vocoder**,
**Input Follower**, **Filter Bank** (sub-focus **TBD** — may be another SysEx
byte
or menu-only).

**Not** [Delay LFO Wave](#delay-lfo-wave) (`70`/`76`). **Not** global Memory
Protect
(`73`/`76`).

---

## Distortion Type {#distortion-type}

**Edit FX → Distortion → Type**. Live edit **`cmd=0x71`**, param **`0x64`**
(Page **B#100**) — see
[single-live-edit.md](docs/live-edit/effects.md#distortion-type-cmd0x71-param-0x64).
**`stored = <value>`** (wire byte; **not** a dense `00`–`19` index). Hardware TX
confirmed (full type step-through after **`6E`/`76`/`00`** focus).

Panel menu order (TI mk2); gaps **`0A`–`19`** only — no unused bytes confirmed
in
this pass:

| `<value>` | Option            |
| --------- | ----------------- |
| `00`      | Off               |
| `0C`      | Wide              |
| `01`      | Light             |
| `02`      | Soft              |
| `03`      | Medium            |
| `04`      | Hard              |
| `05`      | Digital           |
| `06`      | Wave Shaper       |
| `07`      | Rectifier         |
| `13`      | Bit Reducer       |
| `12`      | Rate Reducer      |
| `0D`      | Soft Bounce       |
| `0E`      | Hard Bounce       |
| `0F`      | Sine Fold         |
| `10`      | Triangle Fold     |
| `11`      | Sawtooth Fold     |
| `0A`      | Low Pass          |
| `0B`      | High Pass         |
| `08`      | Bit Reducer Old   |
| `09`      | Rate Reducer Old  |
| `14`      | Mint Overdrive    |
| `15`      | Curry Overdrive   |
| `16`      | Saffron Overdrive |
| `17`      | Onion Overdrive   |
| `18`      | Pepper Overdrive  |
| `19`      | Chili Overdrive   |

Panel rows per **Type**: [Distortion panel
visibility](#distortion-panel-visibility).

**Not** global multi **Part Enable** (`72`/`48`).

---

## Distortion panel visibility {#distortion-panel-visibility}

**Edit FX → Distortion**. **Type** is always on the panel.

### Type = Off (`00`)

| Control    | Visible |
| ---------- | ------- |
| **Type**   | Yes     |
| All others | No      |

### Standard types — same four percent rows

**Type** wire values sharing **Mix**, **Intensity**, **Treble Boost**, **High
Cut**
(all **0.0..100.0 %**). Panel-confirmed on TI mk2:

| `<value>` | Type          |
| --------- | ------------- |
| `0C`      | Wide          |
| `01`      | Light         |
| `02`      | Soft          |
| `03`      | Medium        |
| `04`      | Hard          |
| `05`      | Digital       |
| `06`      | Wave Shaper   |
| `07`      | Rectifier     |
| `0D`      | Soft Bounce   |
| `0E`      | Hard Bounce   |
| `0F`      | Sine Fold     |
| `10`      | Triangle Fold |
| `11`      | Sawtooth Fold |

Live edit bytes confirmed on capture (standard sweeps through **Sawtooth
Fold**):

| Control          | Visible | Live edit | Range                               |
| ---------------- | ------- | --------- | ----------------------------------- |
| **Type**         | Yes     | `71`/`64` | [Distortion Type](#distortion-type) |
| **Mix**          | Yes     | `6E`/`48` | **0.0..100.0 %**                    |
| **Intensity**    | Yes     | `71`/`65` | **0.0..100.0 %**                    |
| **Treble Boost** | Yes     | `6E`/`46` | **0.0..100.0 %**                    |
| **High Cut**     | Yes     | `6E`/`47` | **0.0..100.0 %**                    |

Percent params: `stored = round(pct × 127 / 100)` — endpoints **`00`** = 0 %,
**`7F`** = 100.0 %.

| UI      | `<value>` | Param                                                                           | Notes                                                     |
| ------- | --------- | ------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 0.0 %   | `00`      | Mix / Intensity / Treble / High Cut                                             | ✓ (sweeps)                                                |
| 56.3 %  | `48`      | **Mix** (`6E`/`48`)                                                             | ✓ (**Wide**; matches `round(pct × 127 / 100)`)            |
| 78.9 %  | `65`      | **Intensity** (`71`/`65`)                                                       | ✓ (**Wide**; naive round → **`64`**, panel uses **`65`**) |
| 50.0 %  | `40`      | **Treble Boost** (`6E`/`46`), **High Cut** (`6E`/`47`), **Quality** (`6E`/`49`) | ✓ (`round(50 × 127 / 100)` = **`0x40`**)                  |
| 100.0 % | `7F`      | standard % rows + **Quality**                                                   | ✓ (sweeps)                                                |

### Reducer types — Mix, Intensity, Quality

**Type** = **Rate Reducer** (`12`) or **Bit Reducer** (`13`). Same three rows;
panel-confirmed on both. Live edit **`6E`/`49`** for **Quality** (capture on
**`12`**
and **`13`**; **50.0 %** → **`40`**).

| Control       | Visible | Live edit | Range                               |
| ------------- | ------- | --------- | ----------------------------------- |
| **Type**      | Yes     | `71`/`64` | [Distortion Type](#distortion-type) |
| **Mix**       | Yes     | `6E`/`48` | **0.0..100.0 %**                    |
| **Intensity** | Yes     | `71`/`65` | **0.0..100.0 %**                    |
| **Quality**   | Yes     | `6E`/`49` | **0.0..100.0 %**                    |

No **Treble Boost** / **High Cut** (capture: no **`46`/`47`** after **`64 12`**
/
**`64 13`**).

### Minimal types — Mix and Intensity only

**Type** wire values with only **Mix** and **Intensity** (both **0.0..100.0
%**).
Panel-confirmed on TI mk2:

| `<value>` | Type             |
| --------- | ---------------- |
| `0A`      | Low Pass         |
| `0B`      | High Pass        |
| `08`      | Bit Reducer Old  |
| `09`      | Rate Reducer Old |

Live edit bytes confirmed on capture (**`48`/`65`** sweeps after **`64 0A`**,
**`64 0B`**,
**`64 08`**, **`64 09`**; no **`46`/`47`/`49`/`4A`**):

| Control       | Visible | Live edit | Range                               |
| ------------- | ------- | --------- | ----------------------------------- |
| **Type**      | Yes     | `71`/`64` | [Distortion Type](#distortion-type) |
| **Mix**       | Yes     | `6E`/`48` | **0.0..100.0 %**                    |
| **Intensity** | Yes     | `71`/`65` | **0.0..100.0 %**                    |

Percent encoding: same as [standard
types](#standard-types--same-four-percent-rows) (**Mix** /
**Intensity** calibration anchors apply).

### Overdrive types — Drive, Mix, High Cut {#overdrive-types--drive-mix-high-cut}

**Type** wire values with **Drive**, **Mix**, and **High Cut** (all **0.0..100.0
%**).
Panel label **Drive** uses the same live-edit byte as **Intensity** (`71`/`65`).

| `<value>` | Type              | **Tone** |
| --------- | ----------------- | -------- |
| `15`      | Curry Overdrive   | No       |
| `19`      | Chili Overdrive   | No       |
| `14`      | Mint Overdrive    | Yes      |
| `16`      | Saffron Overdrive | Yes      |
| `17`      | Onion Overdrive   | Yes      |
| `18`      | Pepper Overdrive  | Yes      |

| Control      | Visible              | Live edit | Range                                 |
| ------------ | -------------------- | --------- | ------------------------------------- |
| **Type**     | Yes                  | `71`/`64` | [Distortion Type](#distortion-type)   |
| **Drive**    | Yes                  | `71`/`65` | **0.0..100.0 %**                      |
| **Tone**     | Types with Tone only | `6E`/`4A` | **−100.0..+100.0 %**; **`40`** = +0 % |
| **Mix**      | Yes                  | `6E`/`48` | **0.0..100.0 %**                      |
| **High Cut** | Yes                  | `6E`/`47` | **0.0..100.0 %**                      |

**Drive** / **Mix** / **High Cut**: `stored = round(pct × 127 / 100)` — same as
standard
**Mix** row (**50.0 %** → **`40`** on **High Cut**).

**Tone** (when shown): capture on **`14`**/**`16`**/**`17`**/**`18`** —
**`6E`/`4A`**
sweep; **`00`** = −100.0 %, **`40`** = +0 % (panel-confirmed), **`7F`** = +100.0
%.
No **`4A`** after **`64 15`** / **`64 19`** (Curry / Chili). No
**`46`**/**`49`** on
overdrive types.

No **Intensity** / **Treble Boost** labels on the panel (byte **`65`** is
**Drive** here).

All **Distortion Type** wire values **`00`–`19`** panel-mapped on TI mk2 (this
pass).

---

## Patch name categories

**Edit Single → Categories → Name Cat 1** / **Name Cat 2** (same list on both).
Virus TI **Search by Category** / browser filter names; **`stored = index`**.

23 options (`0`–`22`).

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | Off           |
| 1     | `01`      | Acid          |
| 2     | `02`      | Arpeggiator   |
| 3     | `03`      | Atomizer      |
| 4     | `04`      | Bass          |
| 5     | `05`      | Classic       |
| 6     | `06`      | Decay         |
| 7     | `07`      | Digital       |
| 8     | `08`      | Drums         |
| 9     | `09`      | EFX           |
| 10    | `0A`      | FM            |
| 11    | `0B`      | Input         |
| 12    | `0C`      | Lead          |
| 13    | `0D`      | Organ         |
| 14    | `0E`      | Pad           |
| 15    | `0F`      | Percussion    |
| 16    | `10`      | Piano         |
| 17    | `11`      | Pluck         |
| 18    | `12`      | String        |
| 19    | `13`      | Vocoder       |
| 20    | `14`      | Favourites 1  |
| 21    | `15`      | Favourites 2  |
| 22    | `16`      | Favourites 3  |

---

## Soft Knob Destinations

Soft Knob 1/2/3 **Function As…** — panel menu order (**128** names).
**`<value>`** is the SysEx destination byte (not the table index).
TI mk2 capture: **`cmd=0x71`** — **Function As…** Knob 1 **`3E`** (WAF80
**B#62** *Definable1 Single*),
Knob 2 **`3F`** (**B#63** *Definable2 Single*), Knob 3 **`40`**.
Indices **59** / **61** use LCD names **Freq Shifter Mix** / **FreqShifter
Frequency**.

| Index | `<value>` | Option                             |
| ----- | --------- | ---------------------------------- |
| 0     | `00`      | Off                                |
| 1     | `40`      | Aftertouch                         |
| 2     | `55`      | Analog Boost Int                   |
| 3     | `56`      | Analog Boost Tune                  |
| 4     | `6F`      | Arp Hold                           |
| 5     | `69`      | Arp Mode                           |
| 6     | `6C`      | Arp Note Length                    |
| 7     | `6E`      | Arp Octaves                        |
| 8     | `6A`      | Arp Pattern                        |
| 9     | `6B`      | Arp Resolution                     |
| 10    | `6D`      | Arp Swing                          |
| 11    | `48`      | Assign 1 Amount 1                  |
| 12    | `49`      | Assign 2 Amount 1                  |
| 13    | `4A`      | Assign 2 Amount 2                  |
| 14    | `4B`      | Assign 3 Amount 1                  |
| 15    | `4C`      | Assign 3 Amount 2                  |
| 16    | `4D`      | Assign 3 Amount 3                  |
| 17    | `73`      | Assign 4 Amount 1                  |
| 18    | `74`      | Assign 5 Amount 1                  |
| 19    | `75`      | Assign 6 Amount 1                  |
| 20    | `06`      | Balance                            |
| 21    | `3E`      | Bend Up                            |
| 22    | `3F`      | Bend Down                          |
| 23    | `02`      | Breath                             |
| 24    | `0F`      | Channel Volume                     |
| 25    | `19`      | Chorus Delay                       |
| 26    | `18`      | Chorus Depth                       |
| 27    | `1A`      | Chorus Feedback                    |
| 28    | `16`      | Chorus Mix                         |
| 29    | `17`      | Chorus Rate                        |
| 30    | `4E`      | Clock Tempo                        |
| 31    | `03`      | Control 03                         |
| 32    | `07`      | Control 09                         |
| 33    | `09`      | Control 12                         |
| 34    | `0A`      | Control 13                         |
| 35    | `0B`      | Control 14                         |
| 36    | `0C`      | Control 15                         |
| 37    | `0D`      | Control 16                         |
| 38    | `05`      | Data Entry                         |
| 39    | `54`      | Delay Coloration                   |
| 40    | `1F`      | Delay Depth                        |
| 41    | `1D`      | Delay Feedback                     |
| 42    | `1E`      | Delay Rate                         |
| 43    | `1C`      | Delay Time                         |
| 44    | `57`      | Distortion Intensity               |
| 45    | `71`      | EQ Mid Frequency                   |
| 46    | `70`      | EQ Mid Gain                        |
| 47    | `72`      | EQ Mid Q-Factor                    |
| 48    | `1B`      | Effect Send (Delay)                |
| 49    | `76`      | Effect Send (Reverb)               |
| 50    | `08`      | Expression                         |
| 51    | `27`      | Filter Env > FM Amount             |
| 52    | `26`      | Filter Env > Osc 2 Pitch           |
| 53    | `2C`      | Filter 1 Env Amount                |
| 54    | `2E`      | Filter 1 Key Follow                |
| 55    | `2A`      | Filter 1 Resonance                 |
| 56    | `2D`      | Filter 2 Env Amount                |
| 57    | `2F`      | Filter 2 Key Follow                |
| 58    | `2B`      | Filter 2 Resonance                 |
| 59    | `7F`      | Freq Shifter Mix *(LCD name)*      |
| 60    | `04`      | Foot Pedal                         |
| 61    | `58`      | FreqShifter Frequency *(LCD name)* |
| 62    | `4F`      | Input Thru                         |
| 63    | `30`      | LFO 1 Contour                      |
| 64    | `5C`      | LFO 1 > Assign Amount              |
| 65    | `35`      | LFO 1 > Filter Gain                |
| 66    | `31`      | LFO 1 > Osc 1                      |
| 67    | `32`      | LFO 1 > Osc 2                      |
| 68    | `33`      | LFO 1 > Pulse Width                |
| 69    | `34`      | LFO 1 > Resonance                  |
| 70    | `36`      | LFO 2 Contour                      |
| 71    | `5D`      | LFO 2 > Assign Amount              |
| 72    | `39`      | LFO 2 > Cutoff 1                   |
| 73    | `3A`      | LFO 2 > Cutoff 2                   |
| 74    | `38`      | LFO 2 > FM Amount                  |
| 75    | `3B`      | LFO 2 > Panorama                   |
| 76    | `37`      | LFO 2 > Shape                      |
| 77    | `3C`      | LFO 3 Rate                         |
| 78    | `3D`      | LFO 3 > Assign Amount              |
| 79    | `01`      | Modulation Wheel                   |
| 80    | `53`      | Noise Color                        |
| 81    | `29`      | Noise Volume                       |
| 82    | `50`      | Osc Initial Phase                  |
| 83    | `79`      | Osc 1 F-Shift                      |
| 84    | `7B`      | Osc 1 F-Spread                     |
| 85    | `7D`      | Osc 1 Interpolation                |
| 86    | `23`      | Osc 1 Key Follow                   |
| 87    | `77`      | Osc 1 Local Detune                 |
| 88    | `22`      | Osc 1 Pitch                        |
| 89    | `21`      | Osc 1 Pulse Width                  |
| 90    | `20`      | Osc 1 Wave Select                  |
| 91    | `7A`      | Osc 2 F-Shift                      |
| 92    | `7C`      | Osc 2 F-Spread                     |
| 93    | `7E`      | Osc 2 Interpolation                |
| 94    | `28`      | Osc 2 Key Follow                   |
| 95    | `78`      | Osc 2 Local Detune                 |
| 96    | `25`      | Osc 2 Pulse Width                  |
| 97    | `24`      | Osc 2 Wave Select                  |
| 98    | `5B`      | Osc 3 Detune                       |
| 99    | `5A`      | Osc 3 Pitch                        |
| 100   | `59`      | Osc 3 Volume                       |
| 101   | `10`      | Panorama                           |
| 102   | `0E`      | Patch Volume                       |
| 103   | `60`      | Phaser Depth                       |
| 104   | `62`      | Phaser Feedback                    |
| 105   | `61`      | Phaser Frequency                   |
| 106   | `5E`      | Phaser Mix                         |
| 107   | `5F`      | Phaser Rate                        |
| 108   | `63`      | Phaser Spread                      |
| 109   | `12`      | Portamento                         |
| 110   | `51`      | Punch Intensity                    |
| 111   | `66`      | Reverb Coloration                  |
| 112   | `65`      | Reverb Dampening                   |
| 113   | `64`      | Reverb Decay                       |
| 114   | `67`      | Reverb Feedback                    |
| 115   | `52`      | Ring Modulator                     |
| 116   | `68`      | Surround Balance                   |
| 117   | `11`      | Transpose                          |
| 118   | `13`      | Unison Detune                      |
| 119   | `15`      | Unison LFO Phase                   |
| 120   | `14`      | Unison Spread                      |
| 121   | `41`      | Velo > FM Amount                   |
| 122   | `42`      | Velo > Filt 1 Env Amount           |
| 123   | `43`      | Velo > Filt 2 Env Amount           |
| 124   | `47`      | Velo > Panorama                    |
| 125   | `44`      | Velo > Resonance 1                 |
| 126   | `45`      | Velo > Resonance 2                 |
| 127   | `46`      | Velo > Volume                      |

---

## Soft Knob Names

Soft Knob 1/2/3 **Name** LCD label — **`71`/`33`**, **`34`**, **`35`**.

88 panel options. **Index** is the **alphabetical** menu order on the Virus
(e.g.
**>Para** … **Width**); **`<value>`** is the firmware wire byte — **not**
alphabetical and **not** the index (e.g. **Soften** `39`, **Speaker** `57`,
**Speed** `3A`, **Width** `47`).

Panel **Name** appears when **Function As…** ≠ Off.

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | >Para         |
| 1     | `01`      | +3rds         |
| 2     | `02`      | +4ths         |
| 3     | `03`      | +5ths         |
| 4     | `04`      | +7ths         |
| 5     | `05`      | +Octave       |
| 6     | `06`      | Access        |
| 7     | `07`      | ArpMode       |
| 8     | `08`      | ArpOct        |
| 9     | `09`      | Attack        |
| 10    | `0A`      | Balance       |
| 11    | `0B`      | Bite          |
| 12    | `0C`      | Bush          |
| 13    | `0D`      | Chorus        |
| 14    | `0E`      | Comb          |
| 15    | `0F`      | Cutoff        |
| 16    | `10`      | Decay         |
| 17    | `11`      | Delay         |
| 18    | `12`      | Depth         |
| 19    | `13`      | Destroy       |
| 20    | `14`      | Detune        |
| 21    | `15`      | Disolve       |
| 22    | `16`      | Distort       |
| 23    | `17`      | Dive          |
| 24    | `18`      | Effects       |
| 25    | `19`      | Elevate       |
| 26    | `1A`      | Energy        |
| 27    | `1B`      | EqHigh        |
| 28    | `1C`      | EqLow         |
| 29    | `1D`      | EqMid         |
| 30    | `1E`      | FM            |
| 31    | `1F`      | Fast          |
| 32    | `20`      | Fear          |
| 33    | `21`      | Filter        |
| 34    | `22`      | Flanger       |
| 35    | `23`      | Fuzz          |
| 36    | `24`      | F-Shift       |
| 37    | `25`      | F-Spread      |
| 38    | `26`      | Glide         |
| 39    | `27`      | Hold          |
| 40    | `28`      | Hype          |
| 41    | `29`      | Infect        |
| 42    | `2A`      | Interpolation |
| 43    | `2B`      | Length        |
| 44    | `2C`      | Mix           |
| 45    | `2D`      | Modulate      |
| 46    | `2E`      | Morph         |
| 47    | `2F`      | Muscle        |
| 48    | `30`      | Mutate        |
| 49    | `31`      | Noise         |
| 50    | `32`      | Open          |
| 51    | `33`      | Orbit         |
| 52    | `34`      | PWM           |
| 53    | `35`      | Pan           |
| 54    | `36`      | Party!        |
| 55    | `37`      | Phaser        |
| 56    | `38`      | Phatter       |
| 57    | `39`      | Pitch         |
| 58    | `3A`      | Pulsate       |
| 59    | `3B`      | Punch         |
| 60    | `3C`      | Push          |
| 61    | `3D`      | Rate          |
| 62    | `3E`      | Release       |
| 63    | `3F`      | Reso          |
| 64    | `40`      | Reverb        |
| 65    | `41`      | RingMod       |
| 66    | `42`      | Sack          |
| 67    | `43`      | Scream        |
| 68    | `44`      | Shape         |
| 69    | `45`      | Sharpen       |
| 70    | `46`      | Slow          |
| 71    | `39`      | Soften        |
| 72    | `57`      | Speaker       |
| 73    | `3A`      | Speed         |
| 74    | `4A`      | SubOsc        |
| 75    | `4B`      | Sustain       |
| 76    | `4C`      | Sweep         |
| 77    | `4D`      | Swing         |
| 78    | `4E`      | Tempo         |
| 79    | `4F`      | Thinner       |
| 80    | `50`      | Tone          |
| 81    | `51`      | Tremolo       |
| 82    | `52`      | Vibrato       |
| 83    | `53`      | Vowel         |
| 84    | `54`      | WahWah        |
| 85    | `55`      | Warmth        |
| 86    | `56`      | Warp          |
| 87    | `47`      | Width         |

## Mod Matrix Sources

Mod Matrix slot **Source**.

40 options (`0`–`39`).

| Index | Option           |
| ----- | ---------------- |
| 0     | Off              |
| 1     | Pitch Bend       |
| 2     | Channel Pressure |
| 3     | Mod Wheel        |
| 4     | Breath           |
| 5     | Controller 3     |
| 6     | Foot Pedal       |
| 7     | Data Entry       |
| 8     | Balance          |
| 9     | Controller 9     |
| 10    | Expression       |
| 11    | Controller 12    |
| 12    | Controller 13    |
| 13    | Controller 14    |
| 14    | Controller 15    |
| 15    | Controller 16    |
| 16    | Hold Pedal       |
| 17    | Portamento Sw    |
| 18    | Sost Pedal       |
| 19    | Amp Envelope     |
| 20    | Filter Envelope  |
| 21    | Envelope 3       |
| 22    | Envelope 4       |
| 23    | LFO 1 bipolar    |
| 24    | LFO 1 unipolar   |
| 25    | LFO 2 bipolar    |
| 26    | LFO 2 unipolar   |
| 27    | LFO 3 bipolar    |
| 28    | LFO 3 unipolar   |
| 29    | Velocity On      |
| 30    | Velocity Off     |
| 31    | Key Follow       |
| 32    | Random           |
| 33    | Arp Input        |
| 34    | AnaKey1 Fine     |
| 35    | AnaKey 2 Fine    |
| 36    | AnaKey1 Coarse   |
| 37    | AnaKey2 Coarse   |
| 38    | 1% Constant      |
| 39    | 10% Constant     |

## Mod Matrix Destinations

Mod Matrix slot **Destination**.

122 options (`0`–`121`).

| Index | Option                   |
| ----- | ------------------------ |
| 0     | Off                      |
| 1     | Amp Env Attack           |
| 2     | Amp Env Decay            |
| 3     | Amp Env Slope            |
| 4     | Amp Env Sustain          |
| 5     | Amp Env Release          |
| 6     | Arp Note Length          |
| 7     | Arp Pattern              |
| 8     | Arp Swing Factor         |
| 9     | Chorus Delay             |
| 10    | Chorus Feedback          |
| 11    | Chorus Mix               |
| 12    | Chorus Mod Depth         |
| 13    | Chorus Mod Rate          |
| 14    | Delay Coloration         |
| 15    | Delay Feedback           |
| 16    | Delay Mod Depth          |
| 17    | Delay Mod Rate           |
| 18    | Delay Send               |
| 19    | Delay Time               |
| 20    | Distortion Intensity     |
| 21    | Distortion Mix           |
| 22    | EQ Mid Frequency         |
| 23    | EQ Mid Gain              |
| 24    | Filter Env > FM/Sync     |
| 25    | Filter Env > Osc 2 Pitch |
| 26    | Filter Balance           |
| 27    | Filter Env Attack        |
| 28    | Filter Env Decay         |
| 29    | Filter Env Slope         |
| 30    | Filter Env Sustain       |
| 31    | Filter Env Release       |
| 32    | Filter 1 Cutoff          |
| 33    | Filter 1 Env Amount      |
| 34    | Filter 1 Resonance       |
| 35    | Filter 2 Cutoff          |
| 36    | Filter 2 Env Amount      |
| 37    | Filter 2 Resonance       |
| 38    | Filterbank Poles         |
| 39    | Filterbank Resonance     |
| 40    | Filterbank Slope         |
| 41    | Filterbank Frequency     |
| 42    | LFO 1 > Assign Amount    |
| 43    | LFO 1 Contour            |
| 44    | LFO 1 Rate               |
| 45    | LFO 1 > Filter Gain      |
| 46    | LFO 1 > Osc 1 Pitch      |
| 47    | LFO 1 > Osc 2 Pitch      |
| 48    | LFO 1 > Pulse Width      |
| 49    | LFO 1 > Resonance        |
| 50    | LFO 2 > Assign Amount    |
| 51    | LFO 2 Contour            |
| 52    | LFO 2 Rate               |
| 53    | LFO 2 > Cutoff 1         |
| 54    | LFO 2 > Cutoff 2         |
| 55    | LFO 2 > FM Amount        |
| 56    | LFO 2 > Panorama         |
| 57    | LFO 2 > Shape            |
| 58    | LFO 3 > Assign Amount    |
| 59    | LFO 3 Rate               |
| 60    | Noise Color              |
| 61    | Noise Volume             |
| 62    | Oscillator Balance       |
| 63    | Oscillator Volume        |
| 64    | Osc 1 F-Shift            |
| 65    | Osc 1 F-Spread           |
| 66    | Osc 1 Interpolation      |
| 67    | Osc 1 Pitch              |
| 68    | Osc 1 Pulse Width        |
| 69    | Osc 1 Shape/Index        |
| 70    | Osc 1 Wave Select        |
| 71    | Osc 2 Detune             |
| 72    | Osc 2 FM Amount          |
| 73    | Osc 2 F-Shift            |
| 74    | Osc 2 F-Spread           |
| 75    | Osc 2 Interpolation      |
| 76    | Osc 2 Pitch              |
| 77    | Osc 2 Pulse Width        |
| 78    | Osc 2 Shape/Index        |
| 79    | Osc 2 Wave Select        |
| 80    | Osc 3 Detune             |
| 81    | Osc 3 Pitch              |
| 82    | Osc 3 Volume             |
| 83    | Sub Osc Volume           |
| 84    | Pan Spread               |
| 85    | Panorama                 |
| 86    | Patch Volume             |
| 87    | Phaser Feedback          |
| 88    | Phaser Frequency         |
| 89    | Phaser Mix               |
| 90    | Phaser Mod Depth         |
| 91    | Phaser Mod Rate          |
| 92    | Portamento               |
| 93    | Punch Intensity          |
| 94    | Reverb Send              |
| 95    | Reverb Coloration        |
| 96    | Reverb Dampening         |
| 97    | Reverb Time              |
| 98    | Reverb PreDelay          |
| 99    | Ring Modulator           |
| 100   | Slot 1 Amount 1          |
| 101   | Slot 1 Amount 2          |
| 102   | Slot 1 Amount 3          |
| 103   | Slot 2 Amount 1          |
| 104   | Slot 2 Amount 2          |
| 105   | Slot 2 Amount 3          |
| 106   | Slot 3 Amount 1          |
| 107   | Slot 3 Amount 2          |
| 108   | Slot 3 Amount 3          |
| 109   | Slot 4 Amount 1          |
| 110   | Slot 4 Amount 2          |
| 111   | Slot 4 Amount 3          |
| 112   | Slot 5 Amount 1          |
| 113   | Slot 5 Amount 2          |
| 114   | Slot 5 Amount 3          |
| 115   | Slot 6 Amount 1          |
| 116   | Slot 6 Amount 2          |
| 117   | Slot 6 Amount 3          |
| 118   | Surround Balance         |
| 119   | Transpose                |
| 120   | Unison Detune            |
| 121   | Unison LFO Phase         |

## Wavetable Names

Oscillator **Wavetable** wave select names (`cmd=0x70`, `param=0x13`,
**Mode `02`**).
**Wire** = index **`00`–`63`** for panel indices **0–99**. Order confirmed
on TI mk2 hardware (full **+** sweep).

100 options (`0`–`99`).

| Index | Option       |
| ----- | ------------ |
| 0     | Sine         |
| 1     | HarmncSweep  |
| 2     | Glass Sweep  |
| 3     | Draw Bars    |
| 4     | Clusters     |
| 5     | Insine Out   |
| 6     | Landing      |
| 7     | Liquid Metal |
| 8     | Opposition   |
| 9     | Overtunes 1  |
| 10    | Overtunes 2  |
| 11    | Scale Trix   |
| 12    | Sine Rider   |
| 13    | Sqr Series   |
| 14    | Upsine Down  |
| 15    | Thumbs Up    |
| 16    | Waterphone   |
| 17    | E-Chime      |
| 18    | Tinkabell    |
| 19    | Bellfizz     |
| 20    | Bellentine   |
| 21    | Robot Wars   |
| 22    | Alternator   |
| 23    | Finger Bass  |
| 24    | Fizzybar     |
| 25    | Flutes       |
| 26    | HP Love      |
| 27    | Majestix     |
| 28    | Hotch Potch  |
| 29    | Resynater    |
| 30    | Smooth Rough |
| 31    | Sawsalito    |
| 32    | Bells 1      |
| 33    | Bells 2      |
| 34    | SportReport  |
| 35    | Metal Guru   |
| 36    | Bat Cave     |
| 37    | Acetate      |
| 38    | Buzzbizz     |
| 39    | Buzzpartout  |
| 40    | Vanish       |
| 41    | Overbones    |
| 42    | Pulsechecker |
| 43    | Stratosfear  |
| 44    | Sooty Sweep  |
| 45    | Throaty      |
| 46    | Didgitalis   |
| 47    | Evil         |
| 48    | Chords       |
| 49    | FM Grit      |
| 50    | Bellsarnie   |
| 51    | Octavius     |
| 52    | Eat Pulse    |
| 53    | Sinzin       |
| 54    | Sine System  |
| 55    | Clip Sweep   |
| 56    | Roughage     |
| 57    | Waving       |
| 58    | Pling Saw    |
| 59    | E-Peas       |
| 60    | Bump Sweep   |
| 61    | Filter Sqr   |
| 62    | Fourmant     |
| 63    | Formantera   |
| 64    | Sundial 1    |
| 65    | Sundial 2    |
| 66    | Sundial 3    |
| 67    | Clipdial 1   |
| 68    | Clipdial 2   |
| 69    | Voxonix      |
| 70    | Solenoid     |
| 71    | KlingKlang   |
| 72    | Violator     |
| 73    | Potassium    |
| 74    | Pile Up      |
| 75    | Tincanali    |
| 76    | Sniper       |
| 77    | Squeezy      |
| 78    | Decomposer   |
| 79    | Morfants     |
| 80    | Pingvox      |
| 81    | Adenoids     |
| 82    | Nasal        |
| 83    | Partialism   |
| 84    | TableDance   |
| 85    | Cascade      |
| 86    | Prismism     |
| 87    | Friction     |
| 88    | Robotix      |
| 89    | Whizzfizz    |
| 90    | Spangly      |
| 91    | Fluxbin      |
| 92    | Fiboglide    |
| 93    | Fibonice     |
| 94    | Fibonasty    |
| 95    | Penetrator   |
| 96    | Blinder      |
| 97    | Element 5    |
| 98    | Bad Signs    |
| 99    | Domina7rix   |

## Control Smooth Mode / clock quantize

**Edit Single → Common → Smooth Mode** (`cmd=0x71`, `param=0x19`). **`stored =
index`**
(`00`–`14`). The **Quantise …** rows (`04`–`14`, hardware-confirmed) use the
same **clock division
labels** Access documents for **LFO 1/2/3 / Delay Clock** (WAF80 Page B: *Off,
1/64 …*) and the same naming as **Arpeggiator Clock / Resolution** on the panel
— those parameters are **not yet wire-mapped** in this repo, so they do **not**
share a second table here; expect the **quantize names and order** to match when
captured.

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | Off           |
| 1     | `01`      | On            |
| 2     | `02`      | Auto          |
| 3     | `03`      | Note          |
| 4     | `04`      | Quantise 1/64 |
| 5     | `05`      | Quantise 1/32 |
| 6     | `06`      | Quantise 1/16 |
| 7     | `07`      | Quantise 1/8  |
| 8     | `08`      | Quantise 1/4  |
| 9     | `09`      | Quantise 1/2  |
| 10    | `0A`      | Quantise 3/64 |
| 11    | `0B`      | Quantise 3/32 |
| 12    | `0C`      | Quantise 3/16 |
| 13    | `0D`      | Quantise 3/8  |
| 14    | `0E`      | Quantise 1/24 |
| 15    | `0F`      | Quantise 1/12 |
| 16    | `10`      | Quantise 1/6  |
| 17    | `11`      | Quantise 1/3  |
| 18    | `12`      | Quantise 2/3  |
| 19    | `13`      | Quantise 3/4  |
| 20    | `14`      | Quantise 1/1  |

WAF80 *Control Smooth Mode* lists only **Off / On / Auto / Note** (vintage
four-mode summary); the Virus TI panel exposes the full quantize grid above.

---

## Edit Single — Panorama (LCD)

**Edit Single → Common → Panorama** (`cmd=0x70`, `param=0x0A`).
Bipolar **`stored = ui + 64`** (`00` = full left, `40` = center, `7F` = full
right).
Panel readout is **not** linear in the wire byte; VALUE ± steps are mostly **1.5
%**
or **1.6 %** in the displayed value.

**Mirror rule** (hardware-confirmed **`41`–`7E`**): for right wire **`R`**, the
label
matches left wire **`0x80 − R`** with **`L<`** → **`% >R`**. Endpoints **`00`**
/
**`7F`** are both **100.0 %** (not mirrored).

| `<value>` | LCD        | `<value>` | LCD       |
| --------- | ---------- | --------- | --------- |
| `00`      | L< 100.0 % | `01`      | L< 98.4 % |
| `02`      | L< 96.9 %  | `03`      | L< 95.3 % |
| `04`      | L< 93.8 %  | `05`      | L< 92.2 % |
| `06`      | L< 90.6 %  | `07`      | L< 89.1 % |
| `08`      | L< 87.5 %  | `09`      | L< 85.9 % |
| `0A`      | L< 84.4 %  | `0B`      | L< 82.8 % |
| `0C`      | L< 81.3 %  | `0D`      | L< 79.7 % |
| `0E`      | L< 78.1 %  | `0F`      | L< 76.6 % |
| `10`      | L< 75.0 %  | `11`      | L< 73.4 % |
| `12`      | L< 71.9 %  | `13`      | L< 70.3 % |
| `14`      | L< 68.8 %  | `15`      | L< 67.2 % |
| `16`      | L< 65.6 %  | `17`      | L< 64.1 % |
| `18`      | L< 62.5 %  | `19`      | L< 60.9 % |
| `1A`      | L< 59.4 %  | `1B`      | L< 57.8 % |
| `1C`      | L< 56.3 %  | `1D`      | L< 54.7 % |
| `1E`      | L< 53.1 %  | `1F`      | L< 51.6 % |
| `20`      | L< 50.0 %  | `21`      | L< 48.4 % |
| `22`      | L< 46.9 %  | `23`      | L< 45.3 % |
| `24`      | L< 43.8 %  | `25`      | L< 42.2 % |
| `26`      | L< 40.6 %  | `27`      | L< 39.0 % |
| `28`      | L< 37.5 %  | `29`      | L< 35.9 % |
| `2A`      | L< 34.4 %  | `2B`      | L< 32.8 % |
| `2C`      | L< 31.3 %  | `2D`      | L< 29.7 % |
| `2E`      | L< 28.1 %  | `2F`      | L< 26.6 % |
| `30`      | L< 25.0 %  | `31`      | L< 23.4 % |
| `32`      | L< 21.9 %  | `33`      | L< 20.3 % |
| `34`      | L< 18.8 %  | `35`      | L< 17.2 % |
| `36`      | L< 15.6 %  | `37`      | L< 14.1 % |
| `38`      | L< 12.5 %  | `39`      | L< 10.9 % |
| `3A`      | L< 9.4 %   | `3B`      | L< 7.8 %  |
| `3C`      | L< 6.3 %   | `3D`      | L< 4.7 %  |
| `3E`      | L< 3.1 %   | `3F`      | L< 1.6 %  |
| `40`      | <0>        |           |           |

Right of center (`41`–`7F`):

| `<value>` | LCD        | `<value>` | LCD       |
| --------- | ---------- | --------- | --------- |
| `41`      | 1.6 % >R   | `42`      | 3.1 % >R  |
| `43`      | 4.7 % >R   | `44`      | 6.3 % >R  |
| `45`      | 7.8 % >R   | `46`      | 9.4 % >R  |
| `47`      | 10.9 % >R  | `48`      | 12.5 % >R |
| `49`      | 14.1 % >R  | `4A`      | 15.6 % >R |
| `4B`      | 17.2 % >R  | `4C`      | 18.8 % >R |
| `4D`      | 20.3 % >R  | `4E`      | 21.9 % >R |
| `4F`      | 23.4 % >R  | `50`      | 25.0 % >R |
| `51`      | 26.6 % >R  | `52`      | 28.1 % >R |
| `53`      | 29.7 % >R  | `54`      | 31.3 % >R |
| `55`      | 32.8 % >R  | `56`      | 34.4 % >R |
| `57`      | 35.9 % >R  | `58`      | 37.5 % >R |
| `59`      | 39.0 % >R  | `5A`      | 40.6 % >R |
| `5B`      | 42.2 % >R  | `5C`      | 43.8 % >R |
| `5D`      | 45.3 % >R  | `5E`      | 46.9 % >R |
| `5F`      | 48.4 % >R  | `60`      | 50.0 % >R |
| `61`      | 51.6 % >R  | `62`      | 53.1 % >R |
| `63`      | 54.7 % >R  | `64`      | 56.3 % >R |
| `65`      | 57.8 % >R  | `66`      | 59.4 % >R |
| `67`      | 60.9 % >R  | `68`      | 62.5 % >R |
| `69`      | 64.1 % >R  | `6A`      | 65.6 % >R |
| `6B`      | 67.2 % >R  | `6C`      | 68.8 % >R |
| `6D`      | 70.3 % >R  | `6E`      | 71.9 % >R |
| `6F`      | 73.4 % >R  | `70`      | 75.0 % >R |
| `71`      | 76.6 % >R  | `72`      | 78.1 % >R |
| `73`      | 79.7 % >R  | `74`      | 81.3 % >R |
| `75`      | 82.8 % >R  | `76`      | 84.4 % >R |
| `77`      | 85.9 % >R  | `78`      | 87.5 % >R |
| `79`      | 89.1 % >R  | `7A`      | 90.6 % >R |
| `7B`      | 92.2 % >R  | `7C`      | 93.8 % >R |
| `7D`      | 95.3 % >R  | `7E`      | 96.9 % >R |
| `7F`      | 100.0 % >R |           |           |

## Osc 1 Classic — Pulse Width (LCD)

Hardware sweep for **Osc 1 Pulse Width** (`cmd=0x70`, `param=0x12`, **Shape ≥
`40`**).
**Wire:** `pct = 50 + stored × 50 / 127` — see
[single-live-edit.md — Pulse
Width](docs/live-edit/edit-single.md#pulse-width-shape--sawtooth).
**LCD:** `round(pct + 0.4, 0.1)` in most of the range (partial map below; not
every
detent listed).

| `<value>` | LCD % | `<value>` | LCD % | `<value>` | LCD % |
| --------- | ----- | --------- | ----- | --------- | ----- |
| `00`      | 50.0  | `01`      | 50.4  | `02`      | 50.8  |
| `03`      | 51.2  | `04`      | 51.6  | `05`      | 52.0  |
| `06`      | 52.4  | `07`      | 52.7  | `08`      | 53.1  |
| `09`      | 53.5  | `0A`      | 53.9  | `0B`      | 54.3  |
| `0C`      | 54.7  | `0D`      | 55.1  | `0E`      | 55.5  |
| `0F`      | 55.9  | `10`      | 56.2  | `11`      | 56.7  |
| `12`      | 57.0  | `13`      | 57.5  | `14`      | 57.9  |
| `15`      | 58.7  | `16`      | 59.1  | `17`      | 59.4  |
| `18`      | 59.8  | `19`      | 60.2  | `1A`      | 60.6  |
| `1B`      | 61.0  | `1C`      | 61.4  | `1D`      | 61.8  |
| `1E`      | 62.2  | `1F`      | 63.0  | `20`      | 63.4  |
| `21`      | 63.8  | `22`      | 64.2  | `23`      | 64.2  |
| `24`      | 64.6  | `25`      | 65.0  | `26`      | 65.4  |
| `27`      | 65.7  | `28`      | 66.1  | `29`      | 66.5  |
| `2A`      | 66.9  | `2B`      | 67.3  | `2C`      | 67.7  |
| `2D`      | 68.1  | `2E`      | 68.5  | `2F`      | 68.9  |
| `30`      | 69.3  | `31`      | 69.7  | `32`      | 70.1  |
| `33`      | 70.5  | `34`      | 70.9  | `35`      | 71.3  |
| `36`      | 71.7  | `37`      | 72.0  | `38`      | 72.4  |
| `39`      | 72.8  | `3A`      | 73.2  | `3B`      | 73.6  |
| `3C`      | 74.0  | `3D`      | 74.4  | `3E`      | 74.8  |
| `3F`      | 75.2  | `40`      | 75.6  | `41`      | 76.0  |
| `42`      | 76.4  | `43`      | 76.8  | `44`      | 77.2  |
| `45`      | 77.6  | `46`      | 78.0  | `47`      | 78.3  |
| `48`      | 78.7  | `49`      | 79.1  | `4A`      | 79.5  |
| `4B`      | 79.9  | `4C`      | 80.3  | `4D`      | 80.7  |
| `4E`      | 81.1  | `4F`      | 81.5  | `50`      | 81.9  |
| `51`      | 82.3  | `52`      | 82.7  | `5A`      | 85.8  |
| `65`      | 90.2  | `6C`      | 92.9  | `6E`      | 93.7  |
| `79`      | 98.0  | `7A`      | 98.4  | `7D`      | 99.6  |
| `7F`      | 100   |           |       |           |       |

## Osc 1 Hypersaw — Density (LCD)

**Mode `01`**, `cmd=0x70`, `param=0x11`.
**Wire:** `internal = 1 + stored × 8 / 127`.
**LCD candidate:** `round(1 + (internal − 1) × (stored / 127), 0.1)` — see
[single-live-edit.md —
Density](docs/live-edit/oscillators.md#oscillator-1--hypersaw).
**128/128** wire → LCD entries (`00`–`7F`); duplicate labels on some detents.

| `<value>` | LCD | `<value>` | LCD | `<value>` | LCD |
| --------- | --- | --------- | --- | --------- | --- |
| `00`      | 1.0 | `01`      | 1.1 | `02`      | 1.1 |
| `03`      | 1.1 | `04`      | 1.2 | `05`      | 1.2 |
| `06`      | 1.2 | `07`      | 1.3 | `08`      | 1.3 |
| `09`      | 1.3 | `0A`      | 1.4 | `0B`      | 1.4 |
| `0C`      | 1.4 | `0D`      | 1.5 | `0E`      | 1.5 |
| `0F`      | 1.5 | `10`      | 1.6 | `11`      | 1.6 |
| `12`      | 1.6 | `13`      | 1.7 | `14`      | 1.7 |
| `15`      | 1.7 | `16`      | 1.7 | `17`      | 1.8 |
| `18`      | 1.8 | `19`      | 1.8 | `1A`      | 1.8 |
| `1B`      | 1.9 | `1C`      | 1.9 | `1D`      | 1.9 |
| `1E`      | 1.9 | `1F`      | 2.0 | `20`      | 2.0 |
| `21`      | 2.1 | `22`      | 2.1 | `23`      | 2.1 |
| `24`      | 2.2 | `25`      | 2.2 | `26`      | 2.2 |
| `27`      | 2.3 | `28`      | 2.3 | `29`      | 2.3 |
| `2A`      | 2.4 | `2B`      | 2.4 | `2C`      | 2.4 |
| `2D`      | 2.5 | `2E`      | 2.5 | `2F`      | 2.5 |
| `30`      | 2.6 | `31`      | 2.6 | `32`      | 2.6 |
| `33`      | 2.7 |           |     |           |     |
| `34`      | 2.7 | `35`      | 2.7 | `36`      | 2.7 |
| `37`      | 2.8 | `38`      | 2.8 | `39`      | 2.8 |
| `3A`      | 2.8 | `3B`      | 2.9 | `3C`      | 2.9 |
| `3D`      | 2.9 | `3E`      | 2.9 | `3F`      | 3.0 |
| `40`      | 3.0 | `41`      | 3.1 | `42`      | 3.2 |
| `43`      | 3.3 | `44`      | 3.4 | `45`      | 3.5 |
| `46`      | 3.5 | `47`      | 3.6 | `48`      | 3.6 |
| `49`      | 3.7 | `4A`      | 3.7 | `4B`      | 3.8 |
| `4C`      | 3.8 | `4D`      | 3.9 | `4E`      | 3.9 |
| `4F`      | 4.0 | `50`      | 4.0 | `51`      | 4.1 |
| `52`      | 4.2 | `53`      | 4.3 | `54`      | 4.4 |
| `55`      | 4.5 | `56`      | 4.5 | `57`      | 4.6 |
| `58`      | 4.6 | `59`      | 4.7 | `5A`      | 4.7 |
| `5B`      | 4.8 | `5C`      | 4.8 | `5D`      | 4.9 |
| `5E`      | 4.9 | `5F`      | 5.0 | `60`      | 5.0 |
| `61`      | 5.1 | `62`      | 5.3 | `63`      | 5.5 |
| `64`      | 5.7 |           |     |           |     |
| `65`      | 5.8 | `66`      | 5.9 | `67`      | 6.0 |
| `68`      | 6.0 | `69`      | 6.1 | `6A`      | 6.3 |
| `6B`      | 6.5 | `6C`      | 6.7 | `6D`      | 6.8 |
| `6E`      | 6.9 | `6F`      | 7.0 |           |     |
| `70`      | 7.0 | `71`      | 7.1 | `72`      | 7.3 |
| `73`      | 7.5 | `74`      | 7.7 | `75`      | 7.8 |
| `76`      | 7.9 | `77`      | 8.0 | `78`      | 8.0 |
| `79`      | 8.1 | `7A`      | 8.3 | `7B`      | 8.5 |
| `7C`      | 8.7 | `7D`      | 8.8 | `7E`      | 8.9 |
| `7F`      | 9.0 |           |     |           |     |
