# Effects (Edit FX)

Edit FX — **Delay**, **Reverb**, **EQ**, **Distortion**, **Character**,
**Chorus**, **Phaser**, **Others** (focus + documented blocks).

Part of [Live Edit](README.md). Enumerated options:
[parameter-options.md](../parameter-options.md).
Dump worksheet: [Single parameter map](../dumps/single.md#single-parameter-map)
· Multi: [Edit Multi](edit-multi.md).

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7 # multi / common (some params)
F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B single (some params)
F0 00 20 33 01 00 70 <part> <param> <value> F7 # Page A single (when global Page A = SysEx)
F0 00 20 33 01 00 6E <part> <param> <value> F7 # part single edit buffer
```

Param IDs are **not global** — the same hex ID can mean different settings under
different `cmd` bytes. See [Implementer notes](../getting-started.md#implementer-notes).

**Chorus** reuses Page A bytes **`68`–`6F`** across [types](#chorus-type-cmd0x70-param-0x67)
— always decode with **`70`/`67`** (and **`6E`/`76`/`02`** for EFFECTS focus).

## Edit FX (Effects)

Panel **EDIT FX** (after **Common**). SysEx **`cmd` / `param`** per control —
capture as you step through sub-menus.

### SELECT (`6E`/`75`, `6E`/`76`) {#effects-select}

Front-panel **EFFECTS** area — two **SELECT** button groups. Live edit on the
part single buffer. **`6E`/`75`** = group **1**; **`6E`/`76`** = group **2**.
**`stored = index`**. Does **not** write effect parameter values — only which
effect block the shared **EFFECTS** section of the physical panel targets.

Physical knob-to-parameter routing is panel UX (out of scope here). Hosts set
focus with **`6E`/`75`** or **`6E`/`76`**, then send parameter SysEx from the
**EDIT FX** sections below.

| `param`    | Enum                                                                    |
| ---------- | ----------------------------------------------------------------------- |
| **`0x75`** | [EFFECTS SELECT group 1](../parameter-options.md#effects-focus-group-1) |
| **`0x76`** | [EFFECTS SELECT group 2](../parameter-options.md#effects-focus-group-2) |

| Item           | Value                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> <param> <value> F7`                                             |
| Confirmed      | Hardware **TX** + **`sendmidi` RX** (TI mk2) — values **`00`–`04`** on **`75`** and **`76`** |

```text
F0 00 20 33 01 00 6E 00 75 00 F7 # 75/00 — Delay
F0 00 20 33 01 00 6E 00 75 01 F7 # 75/01 — Reverb
F0 00 20 33 01 00 6E 00 75 02 F7 # 75/02 — Low EQ
F0 00 20 33 01 00 6E 00 75 03 F7 # 75/03 — Mid EQ
F0 00 20 33 01 00 6E 00 75 04 F7 # 75/04 — High EQ
F0 00 20 33 01 00 6E 00 76 00 F7 # 76/00 — Distortion
F0 00 20 33 01 00 6E 00 76 01 F7 # 76/01 — Character
F0 00 20 33 01 00 6E 00 76 02 F7 # 76/02 — Chorus
F0 00 20 33 01 00 6E 00 76 03 F7 # 76/03 — Phaser
F0 00 20 33 01 00 6E 00 76 04 F7 # 76/04 — Others
```

| Group | `75` / `76` | EDIT FX block             |
| ----- | ----------- | ------------------------- |
| 1     | `00`        | [Delay](#delay)           |
| 1     | `01`        | [Reverb](#reverb)         |
| 1     | `02`        | [Low EQ](#low-eq)         |
| 1     | `03`        | [Mid EQ](#mid-eq)         |
| 1     | `04`        | [High EQ](#high-eq)       |
| 2     | `00`        | [Distortion](#distortion) |
| 2     | `01`        | [Character](#character)   |
| 2     | `02`        | [Chorus](#chorus)         |
| 2     | `03`        | [Phaser](#phaser)         |
| 2     | `04`        | [Others](#others)         |

**Not** global [Memory Protect](edit-config.md#memory-protect-0x76) (`73`/`76`).
**Not** [Delay LFO Wave](../parameter-options.md#delay-lfo-wave)
(`70`/`76`).

### Distortion

**EDIT FX → Distortion**. EFFECTS focus: [`6E`/`76`/`00`](#effects-select).

Panel layout: [Distortion panel
visibility](../parameter-options.md#distortion-panel-visibility).

| Control                   | Notes                                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Type**                  | [`71`/`64`](#distortion-type-cmd0x71-param-0x64) — **`00`** = Off                                                                                |
| **Mix**                   | [`6E`/`48`](#distortion-mix-cmd0x6e-param-0x48) — standard / minimal / reducer / overdrive                                                       |
| **Intensity** / **Drive** | [`71`/`65`](#distortion-intensity-cmd0x71-param-0x65) — **Intensity** (standard / minimal / reducer); **Drive** (overdrive `14`–`19`)            |
| **Tone**                  | [`6E`/`4A`](#distortion-tone-cmd0x6e-param-0x4a) — overdrive with Tone (`14`/`16`/`17`/`18`)                                                     |
| **Treble Boost**          | [`6E`/`46`](#distortion-treble-boost-cmd0x6e-param-0x46) — [standard types](../parameter-options.md#standard-types--same-four-percent-rows) only |
| **High Cut**              | [`6E`/`47`](#distortion-high-cut-cmd0x6e-param-0x47) — standard + [overdrive](../parameter-options.md#overdrive-types--drive-mix-high-cut)       |
| **Quality**               | [`6E`/`49`](#distortion-quality-cmd0x6e-param-0x49) — **Bit** / **Rate Reducer** (`13`/`12`) only                                                |

### Distortion Type (`cmd=0x71`, param `0x64`) {#distortion-type-cmd0x71-param-0x64}

**EDIT FX → Distortion → Type**. Page **B#100** = **`0x64`**. Enum:
[Distortion Type](../parameter-options.md#distortion-type) (**`stored =
<value>`**,
not a dense index).

| Item           | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 64 <value> F7`                          |
| Value encoding | Wire byte per option table (**`00`** Off … **`19`** Chili Overdrive) |
| Confirmed      | Hardware TX (menu step-through; matches panel labels)                |

```text
F0 00 20 33 01 00 71 00 64 00 F7 # Off
F0 00 20 33 01 00 71 00 64 0C F7 # Wide
F0 00 20 33 01 00 71 00 64 01 F7 # Light
F0 00 20 33 01 00 71 00 64 03 F7 # Medium
F0 00 20 33 01 00 71 00 64 04 F7 # Hard
F0 00 20 33 01 00 71 00 64 05 F7 # Digital
F0 00 20 33 01 00 71 00 64 06 F7 # Wave Shaper
F0 00 20 33 01 00 71 00 64 07 F7 # Rectifier
F0 00 20 33 01 00 71 00 64 12 F7 # Rate Reducer
F0 00 20 33 01 00 71 00 64 13 F7 # Bit Reducer
F0 00 20 33 01 00 71 00 64 0D F7 # Soft Bounce
F0 00 20 33 01 00 71 00 64 0E F7 # Hard Bounce
F0 00 20 33 01 00 71 00 64 0F F7 # Sine Fold
F0 00 20 33 01 00 71 00 64 10 F7 # Triangle Fold
F0 00 20 33 01 00 71 00 64 11 F7 # Sawtooth Fold
F0 00 20 33 01 00 71 00 64 0A F7 # Low Pass
F0 00 20 33 01 00 71 00 64 0B F7 # High Pass
F0 00 20 33 01 00 71 00 64 08 F7 # Bit Reducer Old
F0 00 20 33 01 00 71 00 64 09 F7 # Rate Reducer Old
F0 00 20 33 01 00 71 00 64 14 F7 # Mint Overdrive
F0 00 20 33 01 00 71 00 64 15 F7 # Curry Overdrive
F0 00 20 33 01 00 71 00 64 16 F7 # Saffron Overdrive
F0 00 20 33 01 00 71 00 64 17 F7 # Onion Overdrive
F0 00 20 33 01 00 71 00 64 18 F7 # Pepper Overdrive
F0 00 20 33 01 00 71 00 64 19 F7 # Chili Overdrive
```

### Distortion Mix (`cmd=0x6E`, param `0x48`) {#distortion-mix-cmd0x6e-param-0x48}

**EDIT FX → Distortion → Mix** ([panel
visibility](../parameter-options.md#distortion-panel-visibility) — standard
/ minimal / reducer / overdrive).
Part buffer **`6E`**.

| Item           | Value                                                                                   |
| -------------- | --------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 48 <value> F7`                                             |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`                                    |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**; standard types incl. **Wave Shaper** / **Rectifier**) |

```text
F0 00 20 33 01 00 6E 00 48 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 48 48 F7 # 56.3 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 48 7F F7 # 100.0 %
```

Param id and value both **`48`** in the last example — **`6E <part> 48
<value>`** (Page
**B** param **`0x48`**, wire value **`0x48`**).

### Distortion Intensity (`cmd=0x71`, param `0x65`) {#distortion-intensity-cmd0x71-param-0x65}

**EDIT FX → Distortion → Intensity** ([panel
visibility](../parameter-options.md#distortion-panel-visibility) — standard
/ minimal / reducer). On [overdrive
types](../parameter-options.md#overdrive-types--drive-mix-high-cut) the
panel label is **Drive** (same byte).
Page **B#101** = **`0x65`**. Same byte as [soft-knob
runtime](edit-single.md#soft-knob-runtime-distortion-intensity).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 65 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 71 00 65 00 F7 # 0.0 %
F0 00 20 33 01 00 71 00 65 65 F7 # 78.9 % (Wide; panel-confirmed)
F0 00 20 33 01 00 71 00 65 7F F7 # 100.0 %
```

Param id and value both **`65`** in the middle example — **`71 <part> 65
<value>`**.

### Distortion Treble Boost (`cmd=0x6E`, param `0x46`) {#distortion-treble-boost-cmd0x6e-param-0x46}

**EDIT FX → Distortion → Treble Boost** ([standard
types](../parameter-options.md#distortion-panel-visibility)).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 46 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 6E 00 46 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 46 40 F7 # 50.0 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 46 7F F7 # 100.0 %
```

### Distortion Tone (`cmd=0x6E`, param `0x4A`) {#distortion-tone-cmd0x6e-param-0x4a}

**EDIT FX → Distortion → Tone** ([overdrive types with
Tone](../parameter-options.md#overdrive-types--drive-mix-high-cut) —
**Mint** / **Saffron** / **Onion** / **Pepper**; not **Curry** / **Chili**).

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 4A <value> F7`                                        |
| Panel range    | **−100.0..+100.0 %**; **`40`** = +0 %                                              |
| Endpoints      | **`00`** → −100.0 %, **`7F`** → +100.0 %                                           |
| Confirmed      | Hardware TX (sweep on **`64 16`** / **`64 17`** / **`64 18`**; **`40`** at center) |

```text
F0 00 20 33 01 00 6E 00 4A 00 F7 # −100.0 %
F0 00 20 33 01 00 6E 00 4A 40 F7 # +0 % (panel-confirmed)
F0 00 20 33 01 00 6E 00 4A 7F F7 # +100.0 %
```

### Distortion High Cut (`cmd=0x6E`, param `0x47`) {#distortion-high-cut-cmd0x6e-param-0x47}

**EDIT FX → Distortion → High Cut** ([standard
types](../parameter-options.md#standard-types--same-four-percent-rows) and
[overdrive
types](../parameter-options.md#overdrive-types--drive-mix-high-cut)).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 47 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 6E 00 47 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 47 40 F7 # 50.0 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 47 7F F7 # 100.0 %
```

### Distortion Quality (`cmd=0x6E`, param `0x49`) {#distortion-quality-cmd0x6e-param-0x49}

**EDIT FX → Distortion → Quality** (**Type** = **Bit Reducer** or **Rate
Reducer**).
Replaces **Treble Boost** / **High Cut** on those types — see
[Distortion panel
visibility](../parameter-options.md#distortion-panel-visibility).

| Item           | Value                                                                                |
| -------------- | ------------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 49 <value> F7`                                          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`                                 |
| Confirmed      | Hardware TX (**Rate** / **Bit Reducer**; sweep **`00`–`7F`**; **50.0 %** → **`40`**) |

```text
F0 00 20 33 01 00 6E 00 49 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 49 40 F7 # 50.0 % (Rate / Bit Reducer; panel-confirmed)
F0 00 20 33 01 00 6E 00 49 7F F7 # 100.0 %
```

### Character {#character}

**EDIT FX → Character**. EFFECTS focus: [`6E`/`76`/`01`](#effects-select).

Panel layout: [Character panel
visibility](../parameter-options.md#character-panel-visibility).

All nine **Type** values (`00`–`08`) panel-mapped on TI mk2. Three wire families:
**Analog Boost** (`70`/`15`, `70`/`21`); **Stereo Widener** / **Speaker Cabinet**
(`71`/`61`, `71`/`62`); preset types **`01`–`06`** (**Type** only).

#### Analog Boost (`00`) {#analog-boost-00}

| Control       | Notes                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Type**      | [`6E`/`1A`](#character-type-cmd0x6e-param-0x1a)                                                                     |
| **Intensity** | [`70`/`15`](#character-intensity-cmd0x70-param-0x15) — [LCD curve](../parameter-options.md#character-intensity-lcd) |
| **Frequency** | [`70`/`21`](#character-frequency-cmd0x70-param-0x21) — **`0`–`127`**                                                |

#### Preset types (`01`–`06`)

[Vintage 1](../parameter-options.md#character-preset-types) … **Bass Enhancer**
— **Type** only (`6E`/`1A`); no further live-edit params (panel-confirmed).

#### Stereo Widener (`07`) / Speaker Cabinet (`08`) {#character-adjustable-07-08}

Same panel and wire map for both types — see [parameter-options](../parameter-options.md#character-adjustable-07-08).

| Control       | Notes                                                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Type**      | [`6E`/`1A`](#character-type-cmd0x6e-param-0x1a)                                                                                    |
| **Intensity** | [`71`/`61`](#character-intensity-stereo-widener-cmd0x71-param-0x61) — [LCD curve](../parameter-options.md#character-intensity-lcd) |
| **Frequency** | [`71`/`62`](#character-frequency-stereo-widener-cmd0x71-param-0x62) — **`0`–`127`**                                                |

### Character Type (`cmd=0x6E`, param `0x1A`) {#character-type-cmd0x6e-param-0x1a}

**EDIT FX → Character → Type**. Part-sound buffer (**`6E`**, not Page A).

| Item           | Value                                                                    |
| -------------- | ------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 1A <value> F7`                              |
| Value encoding | [Character Type](../parameter-options.md#character-type) — **`00`–`08`** |
| Confirmed      | Hardware TX (menu step-through; matches panel labels)                    |

```text
F0 00 20 33 01 00 6E 00 1A 00 F7 # Analog Boost
F0 00 20 33 01 00 6E 00 1A 01 F7 # Vintage 1
F0 00 20 33 01 00 6E 00 1A 02 F7 # Vintage 2
F0 00 20 33 01 00 6E 00 1A 03 F7 # Vintage 3
F0 00 20 33 01 00 6E 00 1A 04 F7 # Pad Opener
F0 00 20 33 01 00 6E 00 1A 05 F7 # Lead Enhancer
F0 00 20 33 01 00 6E 00 1A 06 F7 # Bass Enhancer
F0 00 20 33 01 00 6E 00 1A 07 F7 # Stereo Widener
F0 00 20 33 01 00 6E 00 1A 08 F7 # Speaker Cabinet
```

### Character Intensity — Analog Boost (`cmd=0x70`, param `0x15`) {#character-intensity-cmd0x70-param-0x15}

**EDIT FX → Character → Intensity** when [Type](../parameter-options.md#analog-boost-00) =
**Analog Boost** (`00`). Page A param **`0x15`**. LCD index = wire byte —
[Character Intensity (LCD)](../parameter-options.md#character-intensity-lcd).
Soft-knob **Analog Boost Int** (wire **`55`**).

| Item           | Value                                                     |
| -------------- | --------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 15 <value> F7`               |
| Value encoding | **`00`** Off; **`01`–`7F`** → panel **%** (see LCD table) |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**)        |

```text
F0 00 20 33 01 00 70 00 15 00 F7 # Off
F0 00 20 33 01 00 70 00 15 01 F7 # 0.8 %
F0 00 20 33 01 00 70 00 15 02 F7 # 1.6 %
F0 00 20 33 01 00 70 00 15 03 F7 # 2.3 %
F0 00 20 33 01 00 70 00 15 7F F7 # 100.0 %
```

### Character Intensity — Stereo Widener / Speaker Cabinet (`cmd=0x71`, param `0x61`) {#character-intensity-stereo-widener-cmd0x71-param-0x61}

**EDIT FX → Character → Intensity** when [Type](../parameter-options.md#character-adjustable-07-08) =
**Stereo Widener** (`07`) or **Speaker Cabinet** (`08`). Page **B** param
**`0x61`**. Same [LCD curve](../parameter-options.md#character-intensity-lcd) as
Analog Boost.

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 61 <value> F7`                                        |
| Value encoding | **`00`** Off; **`01`–`7F`** → panel **%** (see LCD table)                          |
| Dump offset    | `0x0E9`                                                                            |
| Confirmed      | Hardware TX + dump diff (TI mk2)                                                   |

```text
F0 00 20 33 01 00 71 00 61 00 F7 # Off
F0 00 20 33 01 00 71 00 61 01 F7 # 0.8 %
F0 00 20 33 01 00 71 00 61 02 F7 # 1.6 %
F0 00 20 33 01 00 71 00 61 7F F7 # 100.0 %
```

### Character Frequency — Analog Boost (`cmd=0x70`, param `0x21`) {#character-frequency-cmd0x70-param-0x21}

**EDIT FX → Character → Frequency** when [Type](../parameter-options.md#analog-boost-00) =
**Analog Boost** (`00`). Page A param **`0x21`**. Soft-knob **Analog Boost
Tune** (wire **`56`**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 21 <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 21 00 F7 # 0
F0 00 20 33 01 00 70 00 21 40 F7 # 64
F0 00 20 33 01 00 70 00 21 7F F7 # 127
```

### Character Frequency — Stereo Widener / Speaker Cabinet (`cmd=0x71`, param `0x62`) {#character-frequency-stereo-widener-cmd0x71-param-0x62}

**EDIT FX → Character → Frequency** when [Type](../parameter-options.md#character-adjustable-07-08) =
**Stereo Widener** (`07`) or **Speaker Cabinet** (`08`). Page **B** param
**`0x62`**.

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 62 <value> F7`                                        |
| Panel range    | **`0`–`127`** → `stored = value`                                                   |
| Dump offset    | `0x0EA`                                                                              |
| Confirmed      | Hardware TX + dump diff (TI mk2)                                                     |

```text
F0 00 20 33 01 00 71 40 62 00 F7 # 0
F0 00 20 33 01 00 71 40 62 40 F7 # 64
F0 00 20 33 01 00 71 40 62 7F F7 # 127
```

### Chorus {#chorus}

**EDIT FX → Chorus**. EFFECTS focus: [`6E`/`76`/`02`](#effects-select).

Panel layout: [Chorus panel
visibility](../parameter-options.md#chorus-panel-visibility).

#### Classic (`01`) {#chorus-classic-01}

| Control      | Notes                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------- |
| **Type**     | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`01`** Classic                                    |
| **Rate**     | [`70`/`6A`](#chorus-rate-cmd0x70-param-0x6a) — **`0`–`127`**                                       |
| **Depth**    | [`70`/`6B`](#chorus-depth-cmd0x70-param-0x6b) — **0.0..100.0 %**                                   |
| **Feedback** | [`70`/`6D`](#chorus-feedback-cmd0x70-param-0x6d) — **−100.0..+100.0 %**                            |
| **Delay**    | [`70`/`6C`](#chorus-delay-cmd0x70-param-0x6c) — **`0`–`127`**                                      |
| **Mix**      | [`70`/`69`](#chorus-mix-cmd0x70-param-0x69) — **`00`** Off; **`01`–`7F`**                          |
| **LFO Wave** | [`70`/`6E`](#chorus-lfo-wave-cmd0x70-param-0x6e) — [enum](../parameter-options.md#chorus-lfo-wave) |

#### Vintage (`02`) {#chorus-vintage-02}

| Control    | Notes                                                               |
| ---------- | ------------------------------------------------------------------- |
| **Type**   | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`02`** Vintage     |
| **Rate**   | [`70`/`6A`](#chorus-rate-cmd0x70-param-0x6a) — **`0`–`127`**        |
| **Depth**  | [`70`/`6B`](#chorus-depth-cmd0x70-param-0x6b) — **0.0..100.0 %**    |
| **Mix**    | [`70`/`68`](#chorus-mix-vintage-cmd0x70-param-0x68) — **`0`–`127`** |
| **X-Over** | [`70`/`6F`](#chorus-x-over-cmd0x70-param-0x6f) — **`0`–`127`**      |

#### Hyper Chorus (`03`) {#chorus-hyper-03}

| Control    | Notes                                                                                                    |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| **Type**   | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`03`** Hyper Chorus                                     |
| **Depth**  | [`70`/`6B`](#chorus-depth-cmd0x70-param-0x6b) — **0.0..100.0 %**                                         |
| **Amount** | [`70`/`6C`](#chorus-amount-cmd0x70-param-0x6c) — [1.00..3.00](../parameter-options.md#chorus-amount-lcd) |
| **Mix**    | [`70`/`68`](#chorus-mix-vintage-cmd0x70-param-0x68) — **`0`–`127`**                                      |
| **X-Over** | [`70`/`6F`](#chorus-x-over-cmd0x70-param-0x6f) — **`0`–`127`**                                           |

#### Air Chorus (`04`) {#chorus-air-04}

| Control    | Notes                                                              |
| ---------- | ------------------------------------------------------------------ |
| **Type**   | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`04`** Air Chorus |
| **Depth**  | [`70`/`6B`](#chorus-depth-cmd0x70-param-0x6b) — **0.0..100.0 %**   |
| **X-Over** | [`70`/`6F`](#chorus-x-over-cmd0x70-param-0x6f) — **`0`–`127`**     |

#### Vibrato (`05`) {#chorus-vibrato-05}

| Control    | Notes                                                                 |
| ---------- | --------------------------------------------------------------------- |
| **Type**   | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`05`** Vibrato       |
| **Rate**   | [`70`/`6A`](#chorus-rate-cmd0x70-param-0x6a) — **`0`–`127`**          |
| **Depth**  | [`70`/`6B`](#chorus-depth-vibrato-cmd0x70-param-0x6b) — **`0`–`127`** |
| **X-Over** | [`70`/`6F`](#chorus-x-over-cmd0x70-param-0x6f) — **`0`–`127`**        |

#### Rotary Speaker (`06`) {#chorus-rotary-speaker-06}

| Control              | Notes                                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**             | [`70`/`67`](#chorus-type-cmd0x70-param-0x67) — **`06`** Rotary Speaker                                                                      |
| **Speed**            | [`70`/`6A`](#chorus-speed-rotary-cmd0x70-param-0x6a) — [Slow … Fast](../parameter-options.md#chorus-rotary-speed)                           |
| **Distance**         | [`70`/`6B`](#chorus-distance-rotary-cmd0x70-param-0x6b) — [4.0..30.0 cm](../parameter-options.md#chorus-rotary-distance-lcd)                |
| **Mix**              | [`70`/`68`](#chorus-mix-vintage-cmd0x70-param-0x68) — **`0`–`127`**                                                                         |
| **Mic Angle**        | [`70`/`6C`](#chorus-mic-angle-rotary-cmd0x70-param-0x6c) — [−180..+180 °](../parameter-options.md#chorus-rotary-mic-angle-lcd)              |
| **Low/High Balance** | [`70`/`6D`](#chorus-low-high-balance-rotary-cmd0x70-param-0x6d) — [LowHigh Bal](../parameter-options.md#chorus-rotary-low-high-balance-lcd) |

### Chorus Type (`cmd=0x70`, param `0x67`) {#chorus-type-cmd0x70-param-0x67}

**EDIT FX → Chorus → Type**. Page A param **`0x67`**.

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 67 <value> F7`        |
| Value encoding | [Chorus Type](../parameter-options.md#chorus-type) |
| Confirmed      | Hardware TX — **`01`–`06`** on part **`0F`**       |

```text
F0 00 20 33 01 00 70 00 67 01 F7 # Classic
F0 00 20 33 01 00 70 00 67 02 F7 # Vintage
F0 00 20 33 01 00 70 00 67 03 F7 # Hyper Chorus
F0 00 20 33 01 00 70 00 67 04 F7 # Air Chorus
F0 00 20 33 01 00 70 00 67 05 F7 # Vibrato
F0 00 20 33 01 00 70 00 67 06 F7 # Rotary Speaker
```

### Chorus Rate (`cmd=0x70`, param `0x6A`) {#chorus-rate-cmd0x70-param-0x6a}

**EDIT FX → Chorus → Rate** ([Classic](#chorus-classic-01),
[Vintage](#chorus-vintage-02), [Vibrato](#chorus-vibrato-05)). On **Rotary
Speaker**, the same byte is [Speed](#chorus-speed-rotary-cmd0x70-param-0x6a).
Soft-knob **Chorus Rate** (wire **`17`**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6A <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6A 00 F7 # 0
F0 00 20 33 01 00 70 00 6A 40 F7 # 64
F0 00 20 33 01 00 70 00 6A 7F F7 # 127
```

### Chorus Speed — Rotary Speaker (`cmd=0x70`, param `0x6A`) {#chorus-speed-rotary-cmd0x70-param-0x6a}

**EDIT FX → Chorus → Speed** ([Rotary Speaker](#chorus-rotary-speaker-06)). Same
param byte as [Rate](#chorus-rate-cmd0x70-param-0x6a) on other types — see
[Chorus Rotary Speed](../parameter-options.md#chorus-rotary-speed).

| Item           | Value                                            |
| -------------- | ------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 6A <value> F7`      |
| Panel range    | **`00`** Slow … **`7F`** Fast (`stored = value`) |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**, part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6A 00 F7 # Slow
F0 00 20 33 01 00 70 00 6A 7F F7 # Fast
```

### Chorus Depth (`cmd=0x70`, param `0x6B`) {#chorus-depth-cmd0x70-param-0x6b}

**EDIT FX → Chorus → Depth** ([Classic](#chorus-classic-01),
[Vintage](#chorus-vintage-02), [Hyper](#chorus-hyper-03),
[Air](#chorus-air-04)). On **Vibrato**, same byte is raw **`0`–`127`**
[Depth](#chorus-depth-vibrato-cmd0x70-param-0x6b); on **Rotary Speaker**,
[Distance](#chorus-distance-rotary-cmd0x70-param-0x6b). Soft-knob **Chorus Depth** (wire **`18`**).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6B <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**)   |

```text
F0 00 20 33 01 00 70 00 6B 00 F7 # 0.0 %
F0 00 20 33 01 00 70 00 6B 40 F7 # 50.4 %
F0 00 20 33 01 00 70 00 6B 7F F7 # 100.0 %
```

### Chorus Depth — Vibrato (`cmd=0x70`, param `0x6B`) {#chorus-depth-vibrato-cmd0x70-param-0x6b}

**EDIT FX → Chorus → Depth** ([Vibrato](#chorus-vibrato-05) only). **`0`–`127`**
direct — not the **%** curve used on Classic / Vintage / Hyper / Air.

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6B <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6B 00 F7 # 0
F0 00 20 33 01 00 70 00 6B 7F F7 # 127
```

### Chorus Distance — Rotary Speaker (`cmd=0x70`, param `0x6B`) {#chorus-distance-rotary-cmd0x70-param-0x6b}

**EDIT FX → Chorus → Distance** ([Rotary Speaker](#chorus-rotary-speaker-06)).
LCD: [Chorus Rotary Distance (LCD)](../parameter-options.md#chorus-rotary-distance-lcd).

| Item           | Value                                            |
| -------------- | ------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 6B <value> F7`      |
| Panel range    | **4.0..30.0 cm** — see LCD table                 |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**, part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6B 00 F7 # 4.0 cm
F0 00 20 33 01 00 70 00 6B 10 F7 # 6.0 cm (init patch default, panel-confirmed)
F0 00 20 33 01 00 70 00 6B 29 F7 # 9.1 cm
F0 00 20 33 01 00 70 00 6B 40 F7 # 12.0 cm
F0 00 20 33 01 00 70 00 6B 5A F7 # 17.5 cm
F0 00 20 33 01 00 70 00 6B 7F F7 # 30.0 cm
```

### Chorus Feedback (`cmd=0x70`, param `0x6D`) {#chorus-feedback-cmd0x70-param-0x6d}

**EDIT FX → Chorus → Feedback** ([Classic](#chorus-classic-01)). On **Rotary
Speaker**, same byte is [Low/High Balance](#chorus-low-high-balance-rotary-cmd0x70-param-0x6d).
Soft-knob **Chorus Feedback** (wire **`1A`**). Bipolar **percent** display.

| Item           | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6D <value> F7`                          |
| Panel range    | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64`         |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**; **`40`** = 0.0 % on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6D 00 F7 # −100.0 %
F0 00 20 33 01 00 70 00 6D 40 F7 # 0.0 %
F0 00 20 33 01 00 70 00 6D 7F F7 # +100.0 % (panel; wire max 127)
```

### Chorus Delay — Classic (`cmd=0x70`, param `0x6C`) {#chorus-delay-cmd0x70-param-0x6c}

**EDIT FX → Chorus → Delay** ([Classic](#chorus-classic-01) only). On **Hyper
Chorus**, the same param byte is [Amount](#chorus-amount-cmd0x70-param-0x6c). On
**Rotary Speaker**, [Mic Angle](#chorus-mic-angle-rotary-cmd0x70-param-0x6c).
Soft-knob **Chorus Delay** (wire **`19`**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6C <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6C 00 F7 # 0
F0 00 20 33 01 00 70 00 6C 7F F7 # 127
```

### Chorus Mix — Classic (`cmd=0x70`, param `0x69`) {#chorus-mix-cmd0x70-param-0x69}

**EDIT FX → Chorus → Mix** ([Classic](#chorus-classic-01) only). Soft-knob
**Chorus Mix** (wire **`16`**).

| Item           | Value                                                      |
| -------------- | ---------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 69 <value> F7`                |
| Panel range    | **`00`** Off; **`01`–`7F`** wet level (**1..127**)         |
| Confirmed      | Hardware TX ( **`00`** Off; sweep to **`7F`** on **`0F`**) |

```text
F0 00 20 33 01 00 70 00 69 00 F7 # Off
F0 00 20 33 01 00 70 00 69 01 F7 # 1
F0 00 20 33 01 00 70 00 69 7F F7 # 127
```

### Chorus Mix — Vintage / Hyper / Rotary (`cmd=0x70`, param `0x68`) {#chorus-mix-vintage-cmd0x70-param-0x68}

**EDIT FX → Chorus → Mix** ([Vintage](#chorus-vintage-02),
[Hyper](#chorus-hyper-03), [Rotary Speaker](#chorus-rotary-speaker-06)).
**`0`–`127`** direct — **`00`** = **0**, not **Off** (Classic uses **`69`**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 68 <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 68 00 F7 # 0
F0 00 20 33 01 00 70 00 68 40 F7 # 64
F0 00 20 33 01 00 70 00 68 7F F7 # 127
```

### Chorus Mic Angle — Rotary Speaker (`cmd=0x70`, param `0x6C`) {#chorus-mic-angle-rotary-cmd0x70-param-0x6c}

**EDIT FX → Chorus → Mic Angle** ([Rotary Speaker](#chorus-rotary-speaker-06)).
Same param byte as [Delay](#chorus-delay-cmd0x70-param-0x6c) (Classic) and
[Amount](#chorus-amount-cmd0x70-param-0x6c) (Hyper) — decode with **`70`/`67`**.

| Item           | Value                                                            |
| -------------- | ---------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6C <value> F7`                      |
| Panel range    | **−180..+180 °** → `stored = round(deg × 64 / 180) + 64`         |
| Confirmed      | Hardware TX — **`00`** = −180°, **`40`** = +0°, **`7F`** = +180° |

```text
F0 00 20 33 01 00 70 00 6C 00 F7 # −180°
F0 00 20 33 01 00 70 00 6C 40 F7 # +0°
F0 00 20 33 01 00 70 00 6C 7F F7 # +180°
```

LCD: [Chorus Rotary Mic Angle (LCD)](../parameter-options.md#chorus-rotary-mic-angle-lcd).

### Chorus Low/High Balance — Rotary Speaker (`cmd=0x70`, param `0x6D`) {#chorus-low-high-balance-rotary-cmd0x70-param-0x6d}

**EDIT FX → Chorus → LowHigh Bal** ([Rotary Speaker](#chorus-rotary-speaker-06)).
Same param byte as [Feedback](#chorus-feedback-cmd0x70-param-0x6d) (Classic) —
decode with **`70`/`67`**.

| Item           | Value                                                                     |
| -------------- | ------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6D <value> F7`                               |
| Panel range    | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64`              |
| Confirmed      | Hardware TX — **`00`** = −100.0 %, **`40`** = +0.0 %, **`7F`** = +100.0 % |

```text
F0 00 20 33 01 00 70 00 6D 00 F7 # −100.0 %
F0 00 20 33 01 00 70 00 6D 40 F7 # +0.0 %
F0 00 20 33 01 00 70 00 6D 7F F7 # +100.0 %
```

LCD: [Chorus Rotary Low/High Balance (LCD)](../parameter-options.md#chorus-rotary-low-high-balance-lcd).

### Chorus X-Over (`cmd=0x70`, param `0x6F`) {#chorus-x-over-cmd0x70-param-0x6f}

**EDIT FX → Chorus → X-Over** ([Vintage](#chorus-vintage-02),
[Hyper](#chorus-hyper-03), [Air](#chorus-air-04),
[Vibrato](#chorus-vibrato-05)).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6F <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6F 00 F7 # 0
F0 00 20 33 01 00 70 00 6F 40 F7 # 64
F0 00 20 33 01 00 70 00 6F 7F F7 # 127
```

### Chorus Amount — Hyper (`cmd=0x70`, param `0x6C`) {#chorus-amount-cmd0x70-param-0x6c}

**EDIT FX → Chorus → Amount** ([Hyper](#chorus-hyper-03) only). Page A param
**`0x6C`** — same byte as [Classic Delay](#chorus-delay-cmd0x70-param-0x6c),
different **Type** context. LCD:
[Chorus Amount (LCD)](../parameter-options.md#chorus-amount-lcd).

| Item           | Value                                                                  |
| -------------- | ---------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6C <value> F7`                            |
| Panel range    | **1.00..3.00** → `amount = 1.00 + stored × (2.00 / 127)`               |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** after **`67`/`03`** on part **`0F`**) |

```text
F0 00 20 33 01 00 70 00 6C 00 F7 # 1.00
F0 00 20 33 01 00 70 00 6C 40 F7 # ≈2.00
F0 00 20 33 01 00 70 00 6C 7F F7 # 3.00
```

### Chorus LFO Wave (`cmd=0x70`, param `0x6E`) {#chorus-lfo-wave-cmd0x70-param-0x6e}

**EDIT FX → Chorus → LFO Wave** ([Classic](#chorus-classic-01)). Page A param
**`0x6E`** (not SELECT **`6E`/`76`**, not [Delay LFO Wave](#delay-lfo-wave-cmd0x70-param-0x76)).
Enum: [Chorus LFO Wave](../parameter-options.md#chorus-lfo-wave).

| Item           | Value                                                                                   |
| -------------- | --------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 6E <value> F7`                                             |
| Value encoding | **`00`–`05`** — same shapes as [Delay LFO Wave](../parameter-options.md#delay-lfo-wave) |
| Confirmed      | Hardware TX (step **`00`–`05`** on part **`0F`**)                                       |

```text
F0 00 20 33 01 00 70 00 6E 00 F7 # Sine
F0 00 20 33 01 00 70 00 6E 01 F7 # Triangle
F0 00 20 33 01 00 70 00 6E 02 F7 # Sawtooth
F0 00 20 33 01 00 70 00 6E 03 F7 # Square
F0 00 20 33 01 00 70 00 6E 04 F7 # S&H
F0 00 20 33 01 00 70 00 6E 05 F7 # S&G
```

### Phaser {#phaser}

**EDIT FX → Phaser**. EFFECTS focus: [`6E`/`76`/`03`](#effects-select).

Panel layout: [Phaser panel
visibility](../parameter-options.md#phaser-panel-visibility).

| Control       | Notes                                                                      |
| ------------- | -------------------------------------------------------------------------- |
| **Mix**       | [`71`/`55`](#phaser-mix-cmd0x71-param-0x55) — always visible               |
| **Frequency** | [`71`/`58`](#phaser-frequency-cmd0x71-param-0x58) — **Mix** ≠ **Off** only |
| **Feedback**  | [`71`/`59`](#phaser-feedback-cmd0x71-param-0x59) — **Mix** ≠ **Off** only  |
| **Mod Rate**  | [`71`/`56`](#phaser-mod-rate-cmd0x71-param-0x56) — **Mix** ≠ **Off** only  |
| **Mod Depth** | [`71`/`57`](#phaser-mod-depth-cmd0x71-param-0x57) — **Mix** ≠ **Off** only |
| **Stages**    | [`71`/`54`](#phaser-stages-cmd0x71-param-0x54) — **Mix** ≠ **Off** only    |
| **Spread**    | [`71`/`5A`](#phaser-spread-cmd0x71-param-0x5a) — **Mix** ≠ **Off** only    |

### Phaser Mix (`cmd=0x71`, param `0x55`) {#phaser-mix-cmd0x71-param-0x55}

**EDIT FX → Phaser → Mix**. Page **B** param **`0x55`**. LCD index = wire byte
— [Phaser Mix (LCD)](../parameter-options.md#phaser-mix-lcd). Soft-knob
**Phaser Mix** destination uses wire **`5E`** (not this live-edit byte).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 55 <value> F7`        |
| Panel range    | **`00`** Off; **`01`–`7F`** wet level (**1..127**) |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 55 00 F7 # Off
F0 00 20 33 01 00 71 00 55 01 F7 # 1
F0 00 20 33 01 00 71 00 55 40 F7 # 64
F0 00 20 33 01 00 71 00 55 7F F7 # 127
```

### Phaser Frequency (`cmd=0x71`, param `0x58`) {#phaser-frequency-cmd0x71-param-0x58}

**EDIT FX → Phaser → Frequency** ([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 58 <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 58 00 F7 # 0
F0 00 20 33 01 00 71 00 58 7F F7 # 127
```

### Phaser Feedback (`cmd=0x71`, param `0x59`) {#phaser-feedback-cmd0x71-param-0x59}

**EDIT FX → Phaser → Feedback**
([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**). Same bipolar **%**
encoding as [Chorus Feedback](#chorus-feedback-cmd0x70-param-0x6d).

| Item           | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 71 <part> 59 <value> F7`                  |
| Panel range    | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**)           |

```text
F0 00 20 33 01 00 71 00 59 00 F7 # −100.0 %
F0 00 20 33 01 00 71 00 59 40 F7 # 0.0 %
F0 00 20 33 01 00 71 00 59 7F F7 # +100.0 %
```

### Phaser Mod Rate (`cmd=0x71`, param `0x56`) {#phaser-mod-rate-cmd0x71-param-0x56}

**EDIT FX → Phaser → Mod Rate** ([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 56 <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 56 00 F7 # 0
F0 00 20 33 01 00 71 00 56 7F F7 # 127
```

### Phaser Mod Depth (`cmd=0x71`, param `0x57`) {#phaser-mod-depth-cmd0x71-param-0x57}

**EDIT FX → Phaser → Mod Depth** ([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 57 <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 57 00 F7 # 0
F0 00 20 33 01 00 71 00 57 7F F7 # 127
```

### Phaser Stages (`cmd=0x71`, param `0x54`) {#phaser-stages-cmd0x71-param-0x54}

**EDIT FX → Phaser → Stages** ([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**). Enum:
[Phaser Stages](../parameter-options.md#phaser-stages).

| Item           | Value                                             |
| -------------- | ------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 54 <value> F7`       |
| Value encoding | **`00`–`05`** — **1..6 Stages**                   |
| Confirmed      | Hardware TX (step **`00`–`05`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 54 00 F7 # 1 Stage
F0 00 20 33 01 00 71 00 54 03 F7 # 4 Stages
F0 00 20 33 01 00 71 00 54 05 F7 # 6 Stages
```

### Phaser Spread (`cmd=0x71`, param `0x5A`) {#phaser-spread-cmd0x71-param-0x5a}

**EDIT FX → Phaser → Spread** ([panel](../parameter-options.md#phaser-panel-visibility) — **Mix** ≠ **Off**).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5A <value> F7`        |
| Panel range    | **`0`–`127`** → `stored = value`                   |
| Confirmed      | Hardware TX (sweep **`00`–`7F`** on part **`0F`**) |

```text
F0 00 20 33 01 00 71 00 5A 00 F7 # 0
F0 00 20 33 01 00 71 00 5A 7F F7 # 127
```

### Others {#others}

**EDIT FX → Others**. EFFECTS focus: [`6E`/`76`/`04`](#effects-select)
(Distortion **`00`** … Others **`04`** on param **`0x76`**).

Panel layout: [Others panel
visibility](../parameter-options.md#others-panel-visibility). Sub-page order
(panel-confirmed on TI mk2):

1. **Filter Bank**
2. **Vocoder**
3. **Input Follower**

**No SysEx** when paging among **Filter Bank** / **Vocoder** / **Input Follower**
— LCD navigation only; focus stays **`6E`/`76`/`04`**.

| Sub-page           | Status                  | Notes                                                                                  |
| ------------------ | ----------------------- | -------------------------------------------------------------------------------------- |
| **Filter Bank**    | **All types** confirmed | [Filter Bank](#filter-bank) — **`13`–`19`** on **`6E`**                                |
| **Vocoder**        | **`00`–`06`** confirmed | [Vocoder](#vocoder) — **Mode** **`71`/`27`**; other rows **`6E`/`28`–`3A`**            |
| **Input Follower** | **`01`–`03`** confirmed | [Input Follower](#input-follower) — **`71`/`26`**, **`70`/`36`**, **`38`**, **`3A`** |

#### Filter Bank {#filter-bank}

**EDIT FX → Others → Filter Bank**. [Panel
visibility](../parameter-options.md#filter-bank-panel-visibility). All parameters
below use **`cmd=0x6E`** (part single buffer).

| Type                         | Notes                                                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Ring Modulator** (`01`)    | [Mix](#filter-bank-mix-cmd0x6e-param-0x14), [Frequency](#filter-bank-frequency-bipolar-cmd0x6e-param-0x15), [Stereo Phase](#filter-bank-stereo-phase-cmd0x6e-param-0x16)                                                       |
| **Frequency Shifter** (`02`) | Above + [Shape L](#filter-bank-shape-l-cmd0x6e-param-0x17) / [Shape R](#filter-bank-shape-r-cmd0x6e-param-0x18)                                                                                                                |
| **Vowel Filter** (`03`)      | [Mix](#filter-bank-mix-cmd0x6e-param-0x14), [Frequency](#filter-bank-vowel-frequency-cmd0x6e-param-0x15), [Resonance](#filter-bank-resonance-cmd0x6e-param-0x19), [Stereo Phase](#filter-bank-stereo-phase-cmd0x6e-param-0x16) |
| **Comb Filter** (`04`)       | Mix, [Comb Frequency](#filter-bank-comb-frequency-cmd0x6e-param-0x15), Resonance, Stereo Phase                                                                                                                                 |
| **Pole XFade** (`05`–`08`)   | [Frequency (direct)](#filter-bank-frequency-direct-cmd0x6e-param-0x15), Resonance, [Filter Type](#filter-bank-filter-type-cmd0x6e-param-0x17)                                                                                  |
| **VariSlope** (`09`–`0B`)    | Frequency (direct), Resonance, [Poles](#filter-bank-poles-cmd0x6e-param-0x17), [Slope](#filter-bank-slope-cmd0x6e-param-0x18)                                                                                                  |

| Control  | Notes                                                                                                |
| -------- | ---------------------------------------------------------------------------------------------------- |
| **Type** | [`6E`/`13`](#filter-bank-type-cmd0x6e-param-0x13) — [enum](../parameter-options.md#filter-bank-type) |

### Filter Bank Type (`cmd=0x6E`, param `0x13`) {#filter-bank-type-cmd0x6e-param-0x13}

**EDIT FX → Others → Filter Bank → Type**. Part single buffer (**`6E`**, not Page
A/B). Enum: [Filter Bank Type](../parameter-options.md#filter-bank-type).

| Item           | Value                                                     |
| -------------- | --------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 13 <value> F7`               |
| Value encoding | **`00`–`0B`** — dense type list ( **`00`** = Off )        |
| Confirmed      | Hardware TX (step **`00`–`0B`** after **`6E`/`76`/`04`**) |

```text
F0 00 20 33 01 00 6E 00 13 00 F7 # Off
F0 00 20 33 01 00 6E 00 13 01 F7 # Ring Modulator
F0 00 20 33 01 00 6E 00 13 02 F7 # Frequency Shifter
F0 00 20 33 01 00 6E 00 13 03 F7 # Vowel Filter
F0 00 20 33 01 00 6E 00 13 04 F7 # Comb Filter
F0 00 20 33 01 00 6E 00 13 05 F7 # 1 Pole XFade
F0 00 20 33 01 00 6E 00 13 06 F7 # 2 Pole XFade
F0 00 20 33 01 00 6E 00 13 07 F7 # 4 Pole XFade
F0 00 20 33 01 00 6E 00 13 08 F7 # 6 Pole XFade
F0 00 20 33 01 00 6E 00 13 09 F7 # LP VariSlope
F0 00 20 33 01 00 6E 00 13 0A F7 # HP VariSlope
F0 00 20 33 01 00 6E 00 13 0B F7 # BP VariSlope
```

### Filter Bank Mix (`cmd=0x6E`, param `0x14`) {#filter-bank-mix-cmd0x6e-param-0x14}

**EDIT FX → Others → Filter Bank → Mix** ([Ring Modulator](../parameter-options.md#filter-bank-ring-modulator-01),
[Frequency Shifter](../parameter-options.md#filter-bank-frequency-shifter-02),
[Vowel Filter](../parameter-options.md#filter-bank-vowel-filter-03),
[Comb Filter](../parameter-options.md#filter-bank-comb-filter-04)). LCD:
[Filter Bank Mix (LCD)](../parameter-options.md#filter-bank-mix-lcd).

| Item           | Value                                                             |
| -------------- | ----------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 14 <value> F7`                       |
| Value encoding | **`00`** Off; **`01`–`7F`** → **%** (same as Character Intensity) |
| Confirmed      | Panel-confirmed ( **`01`**, **`02`**, **`7F`** anchors )          |

```text
F0 00 20 33 01 00 6E 00 14 00 F7 # Off
F0 00 20 33 01 00 6E 00 14 01 F7 # 0.8 %
F0 00 20 33 01 00 6E 00 14 7F F7 # 100.0 %
```

### Filter Bank Frequency — bipolar (`cmd=0x6E`, param `0x15`) {#filter-bank-frequency-bipolar-cmd0x6e-param-0x15}

**EDIT FX → Others → Filter Bank → Frequency** on
[Ring Modulator](../parameter-options.md#filter-bank-ring-modulator-01) /
[Frequency Shifter](../parameter-options.md#filter-bank-frequency-shifter-02).
Decode **`6E`/`15`** using **`6E`/`13`** — see also [Comb](#filter-bank-comb-frequency-cmd0x6e-param-0x15),
[Vowel](#filter-bank-vowel-frequency-cmd0x6e-param-0x15), [direct](#filter-bank-frequency-direct-cmd0x6e-param-0x15).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 15 <value> F7` |
| Panel range    | **−64..+63** → `stored = ui + 64`           |
| Confirmed      | Panel-confirmed — **`40`** = **+0**         |

```text
F0 00 20 33 01 00 6E 00 15 00 F7 # −64
F0 00 20 33 01 00 6E 00 15 40 F7 # +0
F0 00 20 33 01 00 6E 00 15 7F F7 # +63
```

### Filter Bank Comb Frequency (`cmd=0x6E`, param `0x15`) {#filter-bank-comb-frequency-cmd0x6e-param-0x15}

**EDIT FX → Others → Filter Bank → Frequency** on [Comb Filter](../parameter-options.md#filter-bank-comb-filter-04)
(`13`/`04`). LCD:
[Filter Bank Comb Frequency](../parameter-options.md#filter-bank-comb-frequency).

| Item           | Value                                                                           |
| -------------- | ------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 15 <value> F7`                                     |
| Panel range    | **C0..C8** chromatic — **`00`** = **C0** … **`5F`** = **B7**, **`60`** = **C8** |
| Confirmed      | Hardware TX — panel stops at **`60`** / **C8**                                  |

```text
F0 00 20 33 01 00 6E 00 15 00 F7 # C0
F0 00 20 33 01 00 6E 00 15 01 F7 # C#0
F0 00 20 33 01 00 6E 00 15 5F F7 # B7
F0 00 20 33 01 00 6E 00 15 60 F7 # C8
```

### Filter Bank Frequency — direct (`cmd=0x6E`, param `0x15`) {#filter-bank-frequency-direct-cmd0x6e-param-0x15}

**EDIT FX → Others → Filter Bank → Frequency** on [Pole XFade](../parameter-options.md#filter-bank-pole-xfade-05-08)
/ [VariSlope](../parameter-options.md#filter-bank-varislope-09-0b). LCD:
[Filter Bank Frequency (direct)](../parameter-options.md#filter-bank-frequency-direct).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 15 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Confirmed      | Panel-confirmed                             |

```text
F0 00 20 33 01 00 6E 00 15 00 F7 # 0
F0 00 20 33 01 00 6E 00 15 40 F7 # 64
F0 00 20 33 01 00 6E 00 15 7F F7 # 127
```

### Filter Bank Vowel Frequency (`cmd=0x6E`, param `0x15`) {#filter-bank-vowel-frequency-cmd0x6e-param-0x15}

**EDIT FX → Others → Filter Bank → Frequency** on [Vowel Filter](../parameter-options.md#filter-bank-vowel-filter-03)
(`13`/`03`). Same param byte as bipolar **Frequency** on other types — decode
using **`13`**. LCD:
[Filter Bank Vowel Frequency](../parameter-options.md#filter-bank-vowel-frequency).

| Item           | Value                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 15 <value> F7`                                                      |
| Panel range    | **0..100.0 %** + vowel glyph — **`00`** = **0 %**, **`40`** = **50.0 %**, **`7F`** = **100.0 %** |
| Confirmed      | Panel-confirmed (full sweep + glyph segments)                                                    |

```text
F0 00 20 33 01 00 6E 00 15 00 F7 # 0 % — <u>
F0 00 20 33 01 00 6E 00 15 40 F7 # 50.0 % — <i>
F0 00 20 33 01 00 6E 00 15 7F F7 # 100.0 % — <u>
```

### Filter Bank Stereo Phase (`cmd=0x6E`, param `0x16`) {#filter-bank-stereo-phase-cmd0x6e-param-0x16}

**EDIT FX → Others → Filter Bank → Stereo Phase** ([Ring Modulator](../parameter-options.md#filter-bank-ring-modulator-01),
[Frequency Shifter](../parameter-options.md#filter-bank-frequency-shifter-02),
[Vowel Filter](../parameter-options.md#filter-bank-vowel-filter-03),
[Comb Filter](../parameter-options.md#filter-bank-comb-filter-04)).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 16 <value> F7` |
| Panel range    | **−64..+63** → `stored = ui + 64`           |
| Confirmed      | Panel-confirmed — **`40`** = **+0**         |

```text
F0 00 20 33 01 00 6E 00 16 00 F7 # −64
F0 00 20 33 01 00 6E 00 16 40 F7 # +0
F0 00 20 33 01 00 6E 00 16 7F F7 # +63
```

### Filter Bank Resonance (`cmd=0x6E`, param `0x19`) {#filter-bank-resonance-cmd0x6e-param-0x19}

**EDIT FX → Others → Filter Bank → Resonance** on [Vowel Filter](../parameter-options.md#filter-bank-vowel-filter-03),
[Comb Filter](../parameter-options.md#filter-bank-comb-filter-04),
[Pole XFade](../parameter-options.md#filter-bank-pole-xfade-05-08),
[VariSlope](../parameter-options.md#filter-bank-varislope-09-0b). LCD:
[Filter Bank Resonance (LCD)](../parameter-options.md#filter-bank-resonance-lcd).

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 19 <value> F7`                                        |
| Panel range    | **0..100.0 %** — **`00`** = **0 %**, **`40`** = **50.0 %**, **`7F`** = **100.0 %** |
| Confirmed      | Panel-confirmed                                                                    |

```text
F0 00 20 33 01 00 6E 00 19 00 F7 # 0 %
F0 00 20 33 01 00 6E 00 19 40 F7 # 50.0 %
F0 00 20 33 01 00 6E 00 19 7F F7 # 100.0 %
```

### Filter Bank Filter Type (`cmd=0x6E`, param `0x17`) {#filter-bank-filter-type-cmd0x6e-param-0x17}

**EDIT FX → Others → Filter Bank → Filter Type** on [Pole XFade](../parameter-options.md#filter-bank-pole-xfade-05-08).
Same byte as [Shape L](#filter-bank-shape-l-cmd0x6e-param-0x17) on Frequency Shifter.
LCD: [Filter Bank XFade Filter Type](../parameter-options.md#filter-bank-xfade-filter-type).

| Item           | Value                                                                            |
| -------------- | -------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 17 <value> F7`                                      |
| Panel range    | **`00`** Low Pass; **`01`–`7E`** numeric; **`40`** Band Pass; **`7F`** High Pass |
| Confirmed      | Panel-confirmed                                                                  |

```text
F0 00 20 33 01 00 6E 00 17 00 F7 # Low Pass
F0 00 20 33 01 00 6E 00 17 40 F7 # Band Pass
F0 00 20 33 01 00 6E 00 17 7F F7 # High Pass
```

### Filter Bank Poles (`cmd=0x6E`, param `0x17`) {#filter-bank-poles-cmd0x6e-param-0x17}

**EDIT FX → Others → Filter Bank → Poles** on [VariSlope](../parameter-options.md#filter-bank-varislope-09-0b).
LCD: [Filter Bank VariSlope Poles (LCD)](../parameter-options.md#filter-bank-varislope-poles-lcd).

| Item           | Value                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 17 <value> F7`                                    |
| Panel range    | **2.00..6.00** — **`00`** = **2.00**, **`40`** = **4.00**, **`7F`** = **6.00** |
| Confirmed      | Panel-confirmed                                                                |

```text
F0 00 20 33 01 00 6E 00 17 00 F7 # 2.00
F0 00 20 33 01 00 6E 00 17 40 F7 # 4.00
F0 00 20 33 01 00 6E 00 17 7F F7 # 6.00
```

### Filter Bank Slope (`cmd=0x6E`, param `0x18`) {#filter-bank-slope-cmd0x6e-param-0x18}

**EDIT FX → Others → Filter Bank → Slope** on [VariSlope](../parameter-options.md#filter-bank-varislope-09-0b).
Same byte as [Shape R](#filter-bank-shape-r-cmd0x6e-param-0x18) on Frequency Shifter.
LCD: [Filter Bank VariSlope Slope](../parameter-options.md#filter-bank-varislope-slope).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 18 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Confirmed      | Panel-confirmed — **`40`** = **64**         |

```text
F0 00 20 33 01 00 6E 00 18 00 F7 # 0
F0 00 20 33 01 00 6E 00 18 40 F7 # 64
F0 00 20 33 01 00 6E 00 18 7F F7 # 127
```

### Filter Bank Shape L (`cmd=0x6E`, param `0x17`) {#filter-bank-shape-l-cmd0x6e-param-0x17}

**EDIT FX → Others → Filter Bank → Shape L**
([Frequency Shifter](../parameter-options.md#filter-bank-frequency-shifter-02) only — on Pole XFade this
byte is [Filter Type](#filter-bank-filter-type-cmd0x6e-param-0x17); on VariSlope,
[Poles](#filter-bank-poles-cmd0x6e-param-0x17)).

| Item           | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 17 <value> F7`                  |
| Panel range    | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64` |
| Confirmed      | Panel-confirmed — **`40`** = **+0 %**                        |

```text
F0 00 20 33 01 00 6E 00 17 00 F7 # −100.0 %
F0 00 20 33 01 00 6E 00 17 40 F7 # +0 %
F0 00 20 33 01 00 6E 00 17 7F F7 # +100.0 %
```

### Filter Bank Shape R (`cmd=0x6E`, param `0x18`) {#filter-bank-shape-r-cmd0x6e-param-0x18}

**EDIT FX → Others → Filter Bank → Shape R**
([Frequency Shifter](../parameter-options.md#filter-bank-frequency-shifter-02) only — on VariSlope this
byte is [Slope](#filter-bank-slope-cmd0x6e-param-0x18)).

| Item           | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 18 <value> F7`                  |
| Panel range    | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64` |
| Confirmed      | Panel-confirmed — **`40`** = **+0 %**                        |

```text
F0 00 20 33 01 00 6E 00 18 00 F7 # −100.0 %
F0 00 20 33 01 00 6E 00 18 40 F7 # +0 %
F0 00 20 33 01 00 6E 00 18 7F F7 # +100.0 %
```

#### Vocoder {#vocoder}

**EDIT FX → Others → Vocoder**. [Panel
visibility](../parameter-options.md#vocoder-panel-visibility). **Mode** and
**Input Select** (Input Follower) use **`cmd=0x71`** (Page B). All other rows
below use **`cmd=0x70`** (Page A). **Not** **`cmd=0x6E`** for these controls on
TI mk2 SysEx capture.

When **Mode** ≠ **Off**, **FILTERS** is disabled on the panel — LCD
**`Vocoder active. Filters are disabled`** (see
[Filters SELECT](../filters.md#filters-select)).

**Spread** (`70`/`2F`) and **Q-Factor** (`70`/`2B`) panel **TX** also emits
Filter 2 Keyfollow / Filter 2 Resonance messages — **ignored** when Vocoder is
active. Dump offsets differ from Filter 1 **`2E`** / **`2A`** slots — see
[single.md](../dumps/single.md#fx-2).

| Mode                                  | Notes                                         |
| ------------------------------------- | --------------------------------------------- |
| **Off** (`00`)                        | [Mode](#vocoder-mode-cmd0x71-param-0x27) only |
| **Oscillator** … **In R** (`01`–`06`) | Mode + nine rows below                        |

| Control              | `cmd`/`param`                                             | Dump offset |
| -------------------- | --------------------------------------------------------- | ----------- |
| **Mode**             | [`71`/`27`](#vocoder-mode-cmd0x71-param-0x27)             | `0x0AF`     |
| **Spread**           | [`70`/`2F`](#vocoder-spread-cmd0x70-param-0x2f)           | `0x037`     |
| **Q-Factor**         | [`70`/`2B`](#vocoder-q-factor-cmd0x70-param-0x2b)         | `0x033`     |
| **Center Freq**      | [`70`/`28`](#vocoder-center-freq-cmd0x70-param-0x28)      | `0x030`     |
| **Balance**          | [`70`/`30`](#vocoder-balance-cmd0x70-param-0x30)          | `0x038`     |
| **Mod Offset**       | [`70`/`29`](#vocoder-mod-offset-cmd0x70-param-0x29)       | `0x031`     |
| **Carrier Attack**   | [`70`/`36`](#vocoder-carrier-attack-cmd0x70-param-0x36)   | `0x03E`     |
| **Carrier Release**  | [`70`/`37`](#vocoder-carrier-release-cmd0x70-param-0x37)  | `0x03F`     |
| **Spectral Balance** | [`70`/`39`](#vocoder-spectral-balance-cmd0x70-param-0x39) | `0x041`     |
| **Bands**            | [`70`/`3A`](#vocoder-bands-cmd0x70-param-0x3a)            | `0x042`     |

**`<part>`:** **`0x40`** = Single edit buffer; **`0x00`** = Multi Part 1 live
edit — same **`cmd`/`param`/`value`** bytes.

### Vocoder Mode (`cmd=0x71`, param `0x27`) {#vocoder-mode-cmd0x71-param-0x27}

**EDIT FX → Others → Vocoder → Mode**. Page B
**`0x27`**. Enum: [Vocoder Mode](../parameter-options.md#vocoder-mode). Param
**`0x27`** on **`0x6E`** is a different control — use **`cmd`** to
disambiguate.

| Item           | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 71 <part> 27 <value> F7`                  |
| Value encoding | **`00`–`06`** — **`00`** Off; no other rows when Off         |
| Confirmed      | Hardware **TX** + **`sendmidi` RX** (TI mk2) — **`00`–`06`** |

```text
F0 00 20 33 01 00 71 00 27 00 F7 # Off
F0 00 20 33 01 00 71 00 27 01 F7 # Oscillator
F0 00 20 33 01 00 71 00 27 02 F7 # Osc Hold
F0 00 20 33 01 00 71 00 27 03 F7 # Noise
F0 00 20 33 01 00 71 00 27 04 F7 # In L
F0 00 20 33 01 00 71 00 27 05 F7 # In L+R
F0 00 20 33 01 00 71 00 27 06 F7 # In R
```

```text
F0 00 20 33 01 00 71 40 27 00 F7 # Off (Single edit buffer)
F0 00 20 33 01 00 71 40 27 01 F7 # Oscillator
F0 00 20 33 01 00 71 00 27 01 F7 # Oscillator (Multi Part 1)
```

### Vocoder Center Freq (`cmd=0x70`, param `0x28`) {#vocoder-center-freq-cmd0x70-param-0x28}

**EDIT FX → Others → Vocoder → Center Freq** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 28 <value> F7` |
| Panel range    | **−64..+63** → `stored = ui + 64`           |
| Dump offset    | `0x030`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 28 00 F7 # −64
F0 00 20 33 01 00 70 40 28 40 F7 # +0
F0 00 20 33 01 00 70 40 28 7F F7 # +63
```

### Vocoder Mod Offset (`cmd=0x70`, param `0x29`) {#vocoder-mod-offset-cmd0x70-param-0x29}

**EDIT FX → Others → Vocoder → Mod Offset** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 29 <value> F7` |
| Panel range    | **−64..+63** → `stored = ui + 64`           |
| Dump offset    | `0x031`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 29 00 F7 # −64
F0 00 20 33 01 00 70 40 29 40 F7 # +0
F0 00 20 33 01 00 70 40 29 7F F7 # +63
```

### Vocoder Q-Factor (`cmd=0x70`, param `0x2B`) {#vocoder-q-factor-cmd0x70-param-0x2b}

**EDIT FX → Others → Vocoder → Q-Factor** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**). Panel **TX** also
sends [Filter 2 Resonance](../filters.md#filter-2-resonance-cmd0x70-param-0x2b)
**`70`/`2B`** — the applied vocoder message uses **`70`/`2B`**, not
**`70`/`2A`** (Filter 1 Resonance).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 2B <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Dump offset    | `0x033`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 2B 00 F7 # 0
F0 00 20 33 01 00 70 40 2B 7F F7 # 127
```

**Not** [Filter 1 Resonance](../filters.md#filter-1-resonance-cmd0x70-param-0x2a)
(**`70`/`2A`**) when **Vocoder** is active.

### Vocoder Spread (`cmd=0x70`, param `0x2F`) {#vocoder-spread-cmd0x70-param-0x2f}

**EDIT FX → Others → Vocoder → Spread** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**). Panel **TX** uses
**`70`/`2F`**, not [Filter 1 Keyfollow](../filters.md#filter-1-keyfollow-cmd0x70-param-0x2e)
**`70`/`2E`**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 2F <value> F7` |
| Panel range    | **−64..+63** → `stored = ui + 64`           |
| Dump offset    | `0x037`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 2F 00 F7 # −64
F0 00 20 33 01 00 70 40 2F 40 F7 # +0
F0 00 20 33 01 00 70 40 2F 7F F7 # +63
```

### Vocoder Balance (`cmd=0x70`, param `0x30`) {#vocoder-balance-cmd0x70-param-0x30}

**EDIT FX → Others → Vocoder → Balance** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 30 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Dump offset    | `0x038`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 30 00 F7 # 0
F0 00 20 33 01 00 70 40 30 7F F7 # 127
```

### Vocoder Carrier Attack (`cmd=0x70`, param `0x36`) {#vocoder-carrier-attack-cmd0x70-param-0x36}

**EDIT FX → Others → Vocoder → Carrier Attack** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 36 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Dump offset    | `0x03E` — same byte as [Input Follower Attack](#input-follower-attack-cmd0x70-param-0x36) |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 36 00 F7 # 0
F0 00 20 33 01 00 70 40 36 7F F7 # 127
```

### Vocoder Carrier Release (`cmd=0x70`, param `0x37`) {#vocoder-carrier-release-cmd0x70-param-0x37}

**EDIT FX → Others → Vocoder → Carrier Release** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 37 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Dump offset    | `0x03F`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 37 00 F7 # 0
F0 00 20 33 01 00 70 40 37 7F F7 # 127
```

### Vocoder Spectral Balance (`cmd=0x70`, param `0x39`) {#vocoder-spectral-balance-cmd0x70-param-0x39}

**EDIT FX → Others → Vocoder → Spectral Balance** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 39 <value> F7` |
| Panel range    | **`0`–`127`** → `stored = value`            |
| Dump offset    | `0x041`                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)            |

```text
F0 00 20 33 01 00 70 40 39 00 F7 # 0
F0 00 20 33 01 00 70 40 39 7F F7 # 127
```

### Vocoder Bands (`cmd=0x70`, param `0x3A`) {#vocoder-bands-cmd0x70-param-0x3a}

**EDIT FX → Others → Vocoder → Bands** ([Oscillator](../parameter-options.md#vocoder-oscillator-osc-hold) /
**Osc Hold** / **Noise** / **In L** / **In L+R** / **In R**). Enum: [Vocoder Bands](../parameter-options.md#vocoder-bands).

| Item           | Value                                                      |
| -------------- | ---------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 3A <value> F7`                |
| Value encoding | **`00`–`1F`** → panel **`01`–`32`** (`bands = stored + 1`) |
| Dump offset    | `0x042` — same byte as [Input Follower Release](#input-follower-release-cmd0x70-param-0x3a) |
| Confirmed      | Hardware TX + dump diff (TI mk2)                           |

```text
F0 00 20 33 01 00 70 40 3A 00 F7 # 01
F0 00 20 33 01 00 70 40 3A 1F F7 # 32
```

#### Input Follower {#input-follower}

**EDIT FX → Others → Input Follower**. [Panel
visibility](../parameter-options.md#input-follower-panel-visibility). **Input
Select** uses **`cmd=0x71`**; **Attack**, **Release**, and **Sensitivity** use
**`cmd=0x70`**. **Not** **`cmd=0x6E`** on TI mk2 SysEx capture.

| Control          | `cmd`/`param`                                                | Dump offset |
| ---------------- | ------------------------------------------------------------ | ----------- |
| **Input Select** | [`71`/`26`](#input-follower-input-select-cmd0x71-param-0x26) | `0x0AE`     |
| **Attack**       | [`70`/`36`](#input-follower-attack-cmd0x70-param-0x36)       | `0x03E`     |
| **Release**      | [`70`/`3A`](#input-follower-release-cmd0x70-param-0x3a)      | `0x042`     |
| **Sensitivity**  | [`70`/`38`](#input-follower-sensitivity-cmd0x70-param-0x38)  | `0x040`     |

Same **`param`** bytes as [Vocoder](#vocoder) rows on **`70`** — decode by
**EDIT FX** sub-page (**Input Follower** vs **Vocoder**).

### Input Follower Input Select (`cmd=0x71`, param `0x26`) {#input-follower-input-select-cmd0x71-param-0x26}

**EDIT FX → Others → Input Follower → Input Select**. Enum:
[Input Follower Input Select](../parameter-options.md#input-follower-input-select).

| Item           | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 26 <value> F7`                 |
| Value encoding | **`00`** Off; **`01`** In L; **`02`** In L+R; **`03`** In R |
| Dump offset    | `0x0AE`                                                     |
| Confirmed      | Hardware TX + dump diff (TI mk2)                            |

```text
F0 00 20 33 01 00 71 40 26 00 F7 # Off (Single edit buffer)
F0 00 20 33 01 00 71 40 26 02 F7 # In L+R
```

**Not** [Ring Modulator Volume](../oscillators.md#ring-modulator-volume-0x32-cmd0x70--cc-38)
(`70`/`26`).

### Input Follower Attack (`cmd=0x70`, param `0x36`) {#input-follower-attack-cmd0x70-param-0x36}

**EDIT FX → Others → Input Follower → Attack** when [Input
Select](#input-follower-input-select-cmd0x71-param-0x26) ≠ **Off**.

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 36 <value> F7`        |
| Panel range    | **0..127** → `stored = lcd`                        |
| Dump offset    | `0x03E`                                            |
| Confirmed      | Hardware TX + dump diff (TI mk2)                    |

```text
F0 00 20 33 01 00 70 40 36 00 F7 # 0
F0 00 20 33 01 00 70 40 36 7F F7 # 127
```

### Input Follower Release (`cmd=0x70`, param `0x3A`) {#input-follower-release-cmd0x70-param-0x3a}

**EDIT FX → Others → Input Follower → Release** when **Input Select** ≠ **Off**.

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 3A <value> F7`        |
| Panel range    | **0..127** → `stored = lcd`                        |
| Dump offset    | `0x042`                                            |
| Confirmed      | Hardware TX + dump diff (TI mk2)                    |

```text
F0 00 20 33 01 00 70 40 3A 00 F7 # 0
F0 00 20 33 01 00 70 40 3A 7F F7 # 127
```

### Input Follower Sensitivity (`cmd=0x70`, param `0x38`) {#input-follower-sensitivity-cmd0x70-param-0x38}

**EDIT FX → Others → Input Follower → Sensitivity** when **Input Select** ≠
**Off**. Percent curve: [Input Follower Sensitivity
(LCD)](../parameter-options.md#input-follower-sensitivity-lcd).

| Item           | Value                                                    |
| -------------- | -------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 38 <value> F7`              |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`     |
| Dump offset    | `0x040`                                                  |
| Confirmed      | Hardware TX + dump diff (TI mk2)                         |

```text
F0 00 20 33 01 00 70 40 38 00 F7 # 0 %
F0 00 20 33 01 00 70 40 38 7F F7 # 100.0 %
```

### Delay

**EDIT FX → Delay**. EFFECTS focus: [`6E`/`75`/`00`](#effects-select).

Panel layout: [Delay panel
visibility](../parameter-options.md#delay-panel-visibility).

#### Classic (`00`) — Send ≠ Off

| Control        | Notes                                                                                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Send**       | [Delay Send (LCD)](../parameter-options.md#delay-send-lcd); [`70`/`71`](#delay-send-cmd0x70-param-0x71)                                                                                                                             |
| **Feedback**   | **0.0..100.0 %** — [`70`/`73`](#delay-feedback)                                                                                                                                                                                     |
| **Mode**       | [Delay Mode](../parameter-options.md#delay-mode) — **`01`–`16`**; [`70`/`70`](#delay-mode-cmd0x70-param-0x70); **Pattern …** = no **Clock**                                                                                         |
| **Coloration** | **−64..+63** → `stored = ui + 64` — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77); [anchors](../parameter-options.md#delay-coloration)                                                                                      |
| **Clock**      | [Delay Clock](../parameter-options.md#delay-clock) — Simple/Ping Pong only; **`71`/`14`**; **`00`** = Off                                                                                                                           |
| **Delay Time** | Simple/Ping Pong + **Clock** Off only — [`70`/`72`](#delay-tape-time-cmd0x70-param-0x72); **not** on **Pattern** (`06`–`16`; panel **Pattern 5+5**)                                                                                 |
| **LFO**        | [Delay LFO](../parameter-options.md#delay-lfo) — **Rate** [`70`/`74`](#delay-lfo-rate-cmd0x70-param-0x74), **Depth** [`70`/`75`](#delay-lfo-depth-cmd0x70-param-0x75), **LFO Wave** [`70`/`76`](#delay-lfo-wave-cmd0x70-param-0x76) |

#### Tape Clocked (`01`) — Send ≠ Off

| Control         | Notes                                                                                                                                            |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Send**        | [Delay Send (LCD)](../parameter-options.md#delay-send-lcd) — Off, −46.2 dB … **0/−24.0 dB**, Effect; [`70`/`71`](#delay-send-cmd0x70-param-0x71) |
| **Feedback**    | **0.0..200.0 %** — [`70`/`73`](#delay-feedback); **`40`** = 100.0 %                                                                              |
| **Left Clock**  | [Delay Tape Left Clock](../parameter-options.md#delay-tape-left-clock) — **`6E`/`0D`**; `00`–`05`                                                |
| **Right Clock** | [Delay Tape Right Clock](../parameter-options.md#delay-tape-right-clock) — **`6E`/`0E`**; same menu                                              |
| **Frequency**   | **`0`–`127`** — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77)                                                                            |
| **Bandwidth**   | **`0`–`127`** — [`6E`/`11`](#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                            |
| **Modulation**  | **0.0..100.0 %** — [`70`/`75`](#delay-tape-modulation-cmd0x70-param-0x75)                                                                        |

No **Time** or **Ratio** on **Tape Clocked**.

#### Tape Free (`02`) / Tape Doppler (`03`) — Send ≠ Off

| Control        | Notes                                                                                                                                                             |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Send**       | [Delay Send (LCD)](../parameter-options.md#delay-send-lcd); [`70`/`71`](#delay-send-cmd0x70-param-0x71) — same curve all **Types** (panel: **Tape Doppler** `03`) |
| **Feedback**   | **0.0..200.0 %** — [`70`/`73`](#delay-feedback); same as Tape Clocked (panel: **Tape Doppler** `03`)                                                              |
| **Time**       | Same as Classic **Delay Time** — **0.0..693.6 ms**, [`70`/`72`](#delay-tape-time-cmd0x70-param-0x72); [LCD table](../parameter-options.md#delay-tape-time)        |
| **Ratio**      | [Delay Tape Ratio](../parameter-options.md#delay-tape-ratio) — **`6E`/`0C`**; `00`–`06` (panel: **Tape Doppler** `03`)                                            |
| **Frequency**  | **`0`–`127`** — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77) (panel: **Tape Doppler** `03`)                                                              |
| **Bandwidth**  | **`0`–`127`** — [`6E`/`11`](#delay-tape-bandwidth-cmd0x6e-param-0x11) (panel: **Tape Doppler** `03`)                                                              |
| **Modulation** | **0.0..100.0 %** — [`70`/`75`](#delay-tape-modulation-cmd0x70-param-0x75) (panel: **Tape Doppler** `03`)                                                          |

No **Left Clock** / **Right Clock** (Tape Clocked only).

### Delay Type (`cmd=0x6E`, param `0x0A`) {#delay-type-cmd0x6e}

**EDIT FX → Delay → Type**. Part-sound buffer (**`6E`**, not Page A).

| Item           | Value                                                            |
| -------------- | ---------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0A <value> F7`                      |
| Value encoding | [Delay Type](../parameter-options.md#delay-type) — **`00`–`03`** |
| Confirmed      | Hardware TX                                                      |

```text
F0 00 20 33 01 00 6E 00 0A 00 F7 # Classic
F0 00 20 33 01 00 6E 00 0A 01 F7 # Tape Clocked
F0 00 20 33 01 00 6E 00 0A 02 F7 # Tape Free
F0 00 20 33 01 00 6E 00 0A 03 F7 # Tape Doppler
```

### Delay Mode (`cmd=0x70`, param `0x70`) {#delay-mode-cmd0x70-param-0x70}

**EDIT FX → Delay → Mode** (**Type** = Classic). Enum:
[Delay Mode](../parameter-options.md#delay-mode) — wire **`01`–`16`**, not
**`00`**.
Not `6E`/`0A` (**Type**).

| Item           | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 70 <value> F7`             |
| Confirmed      | Hardware TX (**`05`–`16`** stepped; enum **`01`–`16`**) |

```text
F0 00 20 33 01 00 70 00 70 01 F7 # Simple Delay
F0 00 20 33 01 00 70 00 70 05 F7 # Ping Pong 8:7
F0 00 20 33 01 00 70 00 70 06 F7 # Pattern 1+1
F0 00 20 33 01 00 70 00 70 16 F7 # Pattern 5+5
```

### Delay Send (`cmd=0x70`, param `0x71`) {#delay-send-cmd0x70-param-0x71}

**EDIT FX → Delay → Send** (all types). Page **A#113** = **`0x71`**. LCD index =
wire byte — [Delay Send (LCD)](../parameter-options.md#delay-send-lcd).

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 71 <value> F7`         |
| Confirmed      | Hardware TX — **Off** ↔ **Effect** (`00`–`7F`–`00`) |

```text
F0 00 20 33 01 00 70 00 71 00 F7 # Off
F0 00 20 33 01 00 70 00 71 7F F7 # Effect
```

### Delay Feedback (`cmd=0x70`, param `0x73`) {#delay-feedback}

**EDIT FX → Delay → Feedback**. Page **A#115** = **`0x73`**. Same byte for all
**Types**; scale depends on **Type** — see
[Delay Feedback](../parameter-options.md#delay-feedback).

#### Classic (`00`) — `stored = round(pct × 127 / 100)`

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 73 <value> F7`          |
| Confirmed      | Hardware TX — **0 %** ↔ **100.0 %** (`00`–`7F`–`00`) |

```text
F0 00 20 33 01 00 70 00 73 00 F7 # 0.0 %
F0 00 20 33 01 00 70 00 73 7F F7 # 100.0 %
```

#### Tape (`01`–`03`) — `stored = round(pct × 127 / 200)`

| Item           | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 73 <value> F7`            |
| Endpoints      | **`00`** = 0 %, **`40`** = 100.0 %, **`7F`** = 200.0 % |
| Confirmed      | Hardware TX (Tape Clocked / Free captures)             |

```text
F0 00 20 33 01 00 70 00 73 40 F7 # 100.0 % (Tape)
F0 00 20 33 01 00 70 00 73 7F F7 # 200.0 % (Tape)
```

### Delay Tape Left Clock (`cmd=0x6E`, param `0x0D`) {#delay-tape-left-clock-cmd0x6e}

**Tape Clocked → Left Clock**. Options:
[Delay Tape Left Clock](../parameter-options.md#delay-tape-left-clock).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0D <value> F7` |
| Confirmed      | Hardware TX (`00`–`05` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0D 00 F7 # 1/32
F0 00 20 33 01 00 6E 00 0D 05 F7 # 5/16
```

### Delay Time (`cmd=0x70`, param `0x72`) {#delay-tape-time-cmd0x70-param-0x72}

**Classic → Delay Time** (Simple/Ping Pong, **Clock** Off only — **not** Pattern
modes), **Tape Free / Doppler → Time** — same param. **0.0..693.6 ms** — see
[Delay Time (ms)](../parameter-options.md#delay-tape-time).

| Item           | Value                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 72 <value> F7`                                    |
| Confirmed      | Hardware TX — **Tape Free** full sweep (`00`–`7F`); LCD anchors in option list |

```text
F0 00 20 33 01 00 70 00 72 00 F7 # 0.0 ms
F0 00 20 33 01 00 70 00 72 40 F7 # 349.5 ms
F0 00 20 33 01 00 70 00 72 7F F7 # 693.6 ms
```

### Delay Tape Ratio (`cmd=0x6E`, param `0x0C`) {#delay-tape-ratio-cmd0x6e}

**Tape Free / Tape Doppler → Ratio**. Options:
[Delay Tape Ratio](../parameter-options.md#delay-tape-ratio).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0C <value> F7` |
| Confirmed      | Hardware TX (`00`–`06` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0C 00 F7 # 1/4
F0 00 20 33 01 00 6E 00 0C 06 F7 # 4/1
```

### Delay Coloration / Tape Frequency (`cmd=0x70`, param `0x77`) {#delay-tape-frequency-cmd0x70-param-0x77}

Page **A#119** = **`0x77`**. Same wire byte; encoding depends on **Type** — see
[Delay Coloration](../parameter-options.md#delay-coloration),
[Tape Frequency](../parameter-options.md#delay-tape-frequency).

#### Classic — Coloration (`stored = ui + 64`, **−64..+63**)

**EDIT FX → Delay → Coloration**.

| Item           | Value                                                      |
| -------------- | ---------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 77 <value> F7`                |
| Endpoints      | **`00`** = −64, **`40`** = +0, **`7F`** = +63              |
| Confirmed      | Hardware TX — **−64** ↔ **+63** ↔ **−64** (`00`–`7F`–`00`) |

```text
F0 00 20 33 01 00 70 00 77 00 F7 # −64
F0 00 20 33 01 00 70 00 77 40 F7 # +0
F0 00 20 33 01 00 70 00 77 7F F7 # +63
```

#### Tape — Frequency (`stored = lcd`, **`0`–`127`**)

**Tape Clocked**, **Tape Free**, **Tape Doppler** — not Classic. Panel
**`0`–`127`**
(**Tape Doppler** `03` confirmed).

| Item           | Value                                                 |
| -------------- | ----------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 77 <value> F7`           |
| Confirmed      | Hardware TX (Frequency sweep); panel **Tape Doppler** |

```text
F0 00 20 33 01 00 70 00 77 00 F7 # 0
F0 00 20 33 01 00 70 00 77 7F F7 # 127
```

### Delay Tape Bandwidth (`cmd=0x6E`, param `0x11`) {#delay-tape-bandwidth-cmd0x6e-param-0x11}

**Tape** types (**Clocked** / **Free** / **Doppler**). Panel **`0`–`127`**
(**Tape Doppler** `03` confirmed).

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 11 <value> F7`         |
| Confirmed      | Hardware TX (sweep to `7F`); panel **Tape Doppler** |

```text
F0 00 20 33 01 00 6E 00 11 00 F7
F0 00 20 33 01 00 6E 00 11 7F F7
```

### Delay Tape Modulation (`cmd=0x70`, param `0x75`) {#delay-tape-modulation-cmd0x70-param-0x75}

**Tape** types (**Clocked** / **Free** / **Doppler**). **0.0..100.0 %** — same
encoding as
[Delay LFO Depth](#delay-lfo-depth-cmd0x70-param-0x75) (**`75`**, **Classic**
LFO page);
distinct from [Delay Feedback](#delay-feedback) on Tape (**0..200 %** on
**`73`**).
Panel **Tape Doppler** (`03`) confirmed.

| Item           | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 75 <value> F7`            |
| Confirmed      | Hardware TX (modulation sweep); panel **Tape Doppler** |

```text
F0 00 20 33 01 00 70 00 75 00 F7 # 0 %
F0 00 20 33 01 00 70 00 75 7F F7 # 100.0 %
```

### Delay Tape Right Clock (`cmd=0x6E`, param `0x0E`) {#delay-tape-right-clock-cmd0x6e}

**Tape Clocked → Right Clock**. Same labels as Left — param **`0x0E`**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0E <value> F7` |
| Confirmed      | Hardware TX (`00`–`05` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0E 00 F7 # 1/32
F0 00 20 33 01 00 6E 00 0E 05 F7 # 5/16
```

### Delay LFO {#delay-lfo}

**Rate**, **Depth**, and **LFO Wave** — one panel page; see
[Delay LFO](../parameter-options.md#delay-lfo).

### Delay LFO Rate (`cmd=0x70`, param `0x74`) {#delay-lfo-rate-cmd0x70-param-0x74}

**EDIT FX → Delay → Rate** ([Delay LFO](#delay-lfo)). Page **A#116** =
**`0x74`**. Not **`0x70`** ([Mode](#delay-mode-cmd0x70-param-0x70)).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 74 <value> F7` |
| Value encoding | Direct **`0`–`127`** (`stored = lcd`)       |
| Confirmed      | Hardware TX (Rate sweep **`00`–`7F`**)      |

```text
F0 00 20 33 01 00 70 00 74 00 F7 # Rate 0
F0 00 20 33 01 00 70 00 74 7F F7 # Rate 127
```

### Delay LFO Depth (`cmd=0x70`, param `0x75`) {#delay-lfo-depth-cmd0x70-param-0x75}

**EDIT FX → Delay → Depth** ([Delay LFO](#delay-lfo)). Page **A#117** =
**`0x75`**.
Same param byte as [Tape Modulation](#delay-tape-modulation-cmd0x70-param-0x75)
on
**Tape** types only.

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 75 <value> F7`          |
| Value encoding | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Endpoints      | **`00`** = 0 %, **`7F`** = 100.0 %                   |
| Confirmed      | Hardware TX (Depth sweep **`00`–`7F`**)              |

```text
F0 00 20 33 01 00 70 00 75 00 F7 # Depth 0 %
F0 00 20 33 01 00 70 00 75 7F F7 # Depth 100.0 %
```

### Delay LFO Wave (`cmd=0x70`, param `0x76`) {#delay-lfo-wave-cmd0x70-param-0x76}

**EDIT FX → Delay → LFO Wave**. Page **A#118** = **`0x76`**. Options:
[Delay LFO Wave](../parameter-options.md#delay-lfo-wave).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 76 <value> F7` |
| Value encoding | Wire byte **`00`–`05`** (enum)              |
| Confirmed      | Hardware TX (wave stepped **`00`–`05`**)    |

```text
F0 00 20 33 01 00 70 00 76 00 F7 # Sine
F0 00 20 33 01 00 70 00 76 05 F7 # S&G
```

### Reverb

**EDIT FX → Reverb**. EFFECTS focus: [`6E`/`75`/`01`](#effects-select).

Panel layout: [Reverb panel
visibility](../parameter-options.md#reverb-panel-visibility).

**Mode = Off (`00`)** — **Mode** and **Send** only (TI reference).

**Send = Off** — does **not** hide **Clock**, **Time**, **Damping**,
**Coloration**,
or **Predelay** (unlike Delay **Send**).

#### Mode = Reverb, Feedback 1, or Feedback 2

**Feedback 2** — same panel rows as **Feedback 1** (mk2 confirmed).

| Control        | Notes                                                                        |
| -------------- | ---------------------------------------------------------------------------- |
| **Mode**       | [`6E`/`01`](#reverb-mode-cmd0x6e)                                            |
| **Send**       | [`6E`/`02`](#reverb-send-cmd0x6e) — **`00`** Off … **`7F`** Effect           |
| **Type**       | [`6E`/`03`](#reverb-type-cmd0x6e) — all room types; does not hide other rows |
| **Clock**      | [`6E`/`08`](#reverb-clock-cmd0x6e)                                           |
| **Time**       | [`6E`/`04`](#reverb-time-cmd0x6e) — **0..127**                               |
| **Damping**    | [`6E`/`05`](#reverb-damping-cmd0x6e) — **0..100.0 %**                        |
| **Coloration** | [`6E`/`06`](#reverb-coloration-cmd0x6e) — **−64..+63**                       |
| **Predelay**   | [`6E`/`07`](#reverb-predelay-cmd0x6e) — **Clock** Off only                   |
| **Feedback**   | [`6E`/`09`](#reverb-feedback-cmd0x6e) — **Feedback 1/2** only; **0..127**    |

---

### Reverb Mode (`cmd=0x6E`, param `0x01`) {#reverb-mode-cmd0x6e}

**EDIT FX → Reverb → Mode**. Part-sound buffer (**`6E`**, like [Delay
Type](#delay-type-cmd0x6e)).
Enum: [Reverb Mode](../parameter-options.md#reverb-mode). **Not** param
**`0x03`**
(that is [Type](#reverb-type-cmd0x6e)).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 01 <value> F7` |
| Value encoding | Wire byte **`00`–`03`**                     |
| Confirmed      | Hardware TX (**`01`–`03`** stepped)         |

```text
F0 00 20 33 01 00 6E 00 01 01 F7 # Reverb
F0 00 20 33 01 00 6E 00 01 02 F7 # Feedback 1
F0 00 20 33 01 00 6E 00 01 03 F7 # Feedback 2
```

### Reverb Type (`cmd=0x6E`, param `0x03`) {#reverb-type-cmd0x6e}

**EDIT FX → Reverb → Type** (**Mode** = Reverb). Enum:
[Reverb Type](../parameter-options.md#reverb-type).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 03 <value> F7`        |
| Value encoding | Wire byte **`00`–`03`**                            |
| Confirmed      | Hardware TX (**`00`–`03`**; Hall → Ambience sweep) |

```text
F0 00 20 33 01 00 6E 00 03 00 F7 # Ambience
F0 00 20 33 01 00 6E 00 03 01 F7 # Small Room
F0 00 20 33 01 00 6E 00 03 02 F7 # Large Room
F0 00 20 33 01 00 6E 00 03 03 F7 # Hall
```

### Reverb Clock (`cmd=0x6E`, param `0x08`) {#reverb-clock-cmd0x6e}

**EDIT FX → Reverb → Clock**. Syncs **Predelay**. Same **`<value>`** map as
[Delay Clock](../parameter-options.md#delay-clock) but **`6E`/`08`** (not
`71`/`14`).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 08 <value> F7` |
| Confirmed      | Hardware TX (**Off** → **3/4** → **Off**)   |

```text
F0 00 20 33 01 00 6E 00 08 00 F7 # Off
F0 00 20 33 01 00 6E 00 08 10 F7 # 3/4
```

### Reverb Time (`cmd=0x6E`, param `0x04`) {#reverb-time-cmd0x6e}

**EDIT FX → Reverb → Time** (**Mode** = Reverb). Tail length **0..127**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 04 <value> F7` |
| Value encoding | **`stored = lcd`**                          |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)           |

```text
F0 00 20 33 01 00 6E 00 04 00 F7 # 0
F0 00 20 33 01 00 6E 00 04 44 F7 # 68
F0 00 20 33 01 00 6E 00 04 7F F7 # 127
```

### Reverb Damping (`cmd=0x6E`, param `0x05`) {#reverb-damping-cmd0x6e}

**EDIT FX → Reverb → Damping** (**Mode** = Reverb). **0.0..100.0 %** — see
[Reverb Damping](../parameter-options.md#reverb-damping).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 05 <value> F7` |
| Value encoding | `stored = round(pct × 127 / 100)`           |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)           |

```text
F0 00 20 33 01 00 6E 00 05 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 05 14 F7 # 15.6 % (panel)
F0 00 20 33 01 00 6E 00 05 7F F7 # 100.0 %
```

### Reverb Coloration (`cmd=0x6E`, param `0x06`) {#reverb-coloration-cmd0x6e}

**EDIT FX → Reverb → Coloration** (**Mode** = Reverb). **−64..+63** — see
[Reverb Coloration](../parameter-options.md#reverb-coloration).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 06 <value> F7` |
| Value encoding | `stored = ui + 64`                          |
| Confirmed      | Hardware TX (sweep **+63** → **−64**)       |

```text
F0 00 20 33 01 00 6E 00 06 40 F7 # +0
F0 00 20 33 01 00 6E 00 06 7F F7 # +63
F0 00 20 33 01 00 6E 00 06 00 F7 # −64
```

### Reverb Predelay (`cmd=0x6E`, param `0x07`) {#reverb-predelay-cmd0x6e}

**EDIT FX → Reverb → Predelay** (**Clock** = Off). **0.0..500.0 ms** — see
[Reverb Predelay](../parameter-options.md#reverb-predelay).

| Item           | Value                                                                   |
| -------------- | ----------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 07 <value> F7`                             |
| Value encoding | **`stored = lcd`**; valid **`00`–`5C`**; `lcd_ms ≈ stored × 500.0 / 92` |
| Confirmed      | Hardware TX (sweep **0.0** → **500.0** ms; max wire **`5C`**)           |

```text
F0 00 20 33 01 00 6E 00 07 00 F7 # 0.0 ms
F0 00 20 33 01 00 6E 00 07 20 F7 # 174.8 ms
F0 00 20 33 01 00 6E 00 07 40 F7 # 349.5 ms
F0 00 20 33 01 00 6E 00 07 5C F7 # 500.0 ms
```

### Reverb Feedback (`cmd=0x6E`, param `0x09`) {#reverb-feedback-cmd0x6e}

**EDIT FX → Reverb → Feedback** (**Mode** = **Feedback 1** or **Feedback 2**).
**0..127** — see [Reverb
Feedback](../parameter-options.md#reverb-feedback).

| Item           | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 09 <value> F7`            |
| Value encoding | **`stored = lcd`**                                     |
| Confirmed      | Hardware TX (**Feedback 2** mode, sweep **`00`–`7F`**) |

```text
F0 00 20 33 01 00 6E 00 09 00 F7 # 0
F0 00 20 33 01 00 6E 00 09 7F F7 # 127
```

### Reverb Send (`cmd=0x6E`) {#reverb-send-cmd0x6e}

`cmd=0x6E` is used while editing a **part’s sound** (part/single edit
buffer), not while storing a full Multi program.
Reverb Send is **not** in the 267-byte `DUMP_MULTI`.

| Param ID | Field       | Notes                 |
| -------- | ----------- | --------------------- |
| `0x02`   | Reverb Send | See value table below |

| Item           | Value                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 02 <value> F7`                                                 |
| Scope          | Part edit / single edit buffer (not stored in `DUMP_MULTI`)                                 |
| Value encoding | **`stored = index`** — same LCD map as [Delay Send](../parameter-options.md#delay-send-lcd) |
| Key points     | **`00`** Off, **`60`** 0/0 dB, **`7F`** Effect                                              |
| Confirmed      | Hardware TX — Reverb path spot-checks match Delay Send table                                |

```text
F0 00 20 33 01 00 6E 00 02 00 F7 # Off
F0 00 20 33 01 00 6E 00 02 01 F7 # −46.2 dB
F0 00 20 33 01 00 6E 00 02 60 F7 # 0/0 dB
F0 00 20 33 01 00 6E 00 02 7F F7 # Effect
```

LCD ↔ **`stored`**: [Reverb Send (LCD)](../parameter-options.md#reverb-send-lcd).

### Low EQ

**EDIT FX → Low EQ**. EFFECTS focus: [`6E`/`75`/`02`](#effects-select). Both
controls use **Page B** (`cmd=0x71`). Distinct from
Page A **Filter 2 Envelope Amount** on **`70`/`2D`**.

| Control            | Live edit                                         |
| ------------------ | ------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`2D`](#eq-low-frequency-cmd0x71-param-0x2d) |
| **Gain**           | [`71`/`5F`](#eq-low-gain-cmd0x71-param-0x5f)      |

### EQ Low Frequency (`cmd=0x71`, param `0x2D`) {#eq-low-frequency-cmd0x71-param-0x2d}

**EDIT FX → Low EQ → Frequency (Hz)**. Page **B#45** = **`0x2D`**. Hz curve:
[EQ Low Frequency](../parameter-options.md#eq-low-frequency).

| Item           | Value                                                                                  |
| -------------- | -------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 2D <value> F7`                                            |
| Panel range    | **32..458 Hz** — log-spaced; see [LCD table](../parameter-options.md#eq-low-frequency) |
| Confirmed      | Hardware TX — anchors below (TI mk2)                                                   |

```text
F0 00 20 33 01 00 71 00 2D 00 F7 # 32 Hz
F0 00 20 33 01 00 71 00 2D 10 F7 # 45 Hz
F0 00 20 33 01 00 71 00 2D 14 F7 # 49 Hz
F0 00 20 33 01 00 71 00 2D 79 F7 # 404 Hz
F0 00 20 33 01 00 71 00 2D 7E F7 # 458 Hz
F0 00 20 33 01 00 71 00 2D 7F F7 # 458 Hz
```

[Soft Knob Destinations](../parameter-options.md#soft-knob-destinations)
use
different wire bytes (e.g. **Filter 2 Env Amount** = **`2D`** in **`71`/`3E`**)
than
these live-edit param IDs.

### EQ Low Gain (`cmd=0x71`, param `0x5F`) {#eq-low-gain-cmd0x71-param-0x5f}

**EDIT FX → Low EQ → Gain**. Page **B#95** = **`0x5F`**. Encoding:
[EQ Low Gain](../parameter-options.md#eq-low-gain).

| Item           | Value                                                 |
| -------------- | ----------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5F <value> F7`           |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**           |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB  |
| Confirmed      | Hardware TX (sweep **−16 dB** → **Off** → **+16 dB**) |

```text
F0 00 20 33 01 00 71 00 5F 00 F7 # −16 dB
F0 00 20 33 01 00 71 00 5F 40 F7 # Off
F0 00 20 33 01 00 71 00 5F 7F F7 # +16 dB
```

### Mid EQ

**EDIT FX → Mid EQ**. EFFECTS focus: [`6E`/`75`/`03`](#effects-select). All
three controls use **Page B** (`cmd=0x71`).

| Control            | Live edit                                         |
| ------------------ | ------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`5D`](#eq-mid-frequency-cmd0x71-param-0x5d) |
| **Gain**           | [`71`/`5C`](#eq-mid-gain-cmd0x71-param-0x5c)      |
| **Q-Factor**       | [`71`/`5E`](#eq-mid-q-factor-cmd0x71-param-0x5e)  |

### EQ Mid Frequency (`cmd=0x71`, param `0x5D`) {#eq-mid-frequency-cmd0x71-param-0x5d}

**EDIT FX → Mid EQ → Frequency (Hz)**. Page **B#93** = **`0x5D`**. Hz curve:
[EQ Mid Frequency](../parameter-options.md#eq-mid-frequency).

| Item           | Value                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5D <value> F7`                                                 |
| Panel range    | **19 Hz..24.0 kHz** — log-spaced; see [LCD table](../parameter-options.md#eq-mid-frequency) |
| Confirmed      | Hardware TX — anchors below (TI mk2)                                                        |

```text
F0 00 20 33 01 00 71 00 5D 00 F7 # 19 Hz
F0 00 20 33 01 00 71 00 5D 01 F7 # 20 Hz
F0 00 20 33 01 00 71 00 5D 40 F7 # 707 Hz
F0 00 20 33 01 00 71 00 5D 60 F7 # 4238 Hz
F0 00 20 33 01 00 71 00 5D 6F F7 # 9810 Hz
F0 00 20 33 01 00 71 00 5D 70 F7 # 10.3 kHz
F0 00 20 33 01 00 71 00 5D 78 F7 # 17.1 kHz
F0 00 20 33 01 00 71 00 5D 7F F7 # 24.0 kHz
```

### EQ Mid Gain (`cmd=0x71`, param `0x5C`) {#eq-mid-gain-cmd0x71-param-0x5c}

**EDIT FX → Mid EQ → Gain**. Page **B#92** = **`0x5C`**. Same encoding as
[EQ Low Gain](#eq-low-gain-cmd0x71-param-0x5f) — see
[EQ Mid Gain](../parameter-options.md#eq-mid-gain).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5C <value> F7`          |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**          |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB |
| Confirmed      | Hardware TX (same sweep pattern as Low Gain)         |

```text
F0 00 20 33 01 00 71 00 5C 00 F7 # −16 dB
F0 00 20 33 01 00 71 00 5C 40 F7 # Off
F0 00 20 33 01 00 71 00 5C 7F F7 # +16 dB
```

### EQ Mid Q-Factor (`cmd=0x71`, param `0x5E`) {#eq-mid-q-factor-cmd0x71-param-0x5e}

**EDIT FX → Mid EQ → Q-Factor**. Page **B#94** = **`0x5E`**. Anchors:
[EQ Mid Q-Factor](../parameter-options.md#eq-mid-q-factor).

| Item           | Value                                                                                 |
| -------------- | ------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5E <value> F7`                                           |
| Panel range    | **0.28..15.4** — log-spaced; see [LCD table](../parameter-options.md#eq-mid-q-factor) |
| Confirmed      | Hardware TX — anchors below (TI mk2)                                                  |

```text
F0 00 20 33 01 00 71 00 5E 00 F7 # 0.28
F0 00 20 33 01 00 71 00 5E 10 F7 # 0.45
F0 00 20 33 01 00 71 00 5E 20 F7 # 0.71
F0 00 20 33 01 00 71 00 5E 40 F7 # 1.58
F0 00 20 33 01 00 71 00 5E 50 F7 # 2.82
F0 00 20 33 01 00 71 00 5E 60 F7 # 5.01
F0 00 20 33 01 00 71 00 5E 70 F7 # 8.91
F0 00 20 33 01 00 71 00 5E 7E F7 # 14.9
F0 00 20 33 01 00 71 00 5E 7F F7 # 15.4
```

### High EQ

**EDIT FX → High EQ**. EFFECTS focus: [`6E`/`75`/`04`](#effects-select).
**Frequency** and **Gain** only (no **Q** on mk2 panel). Both use **Page B**
(`cmd=0x71`).

| Control            | Live edit                                          |
| ------------------ | -------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`2E`](#eq-high-frequency-cmd0x71-param-0x2e) |
| **Gain**           | [`71`/`60`](#eq-high-gain-cmd0x71-param-0x60)      |

### EQ High Frequency (`cmd=0x71`, param `0x2E`) {#eq-high-frequency-cmd0x71-param-0x2e}

**EDIT FX → High EQ → Frequency (Hz)**. Page **B#46** = **`0x2E`**. Hz curve:
[EQ High Frequency](../parameter-options.md#eq-high-frequency).

| Item           | Value                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 2E <value> F7`                                                    |
| Panel range    | **1831 Hz..24.0 kHz** — log-spaced; see [LCD table](../parameter-options.md#eq-high-frequency) |
| Confirmed      | Hardware TX — anchors below (TI mk2)                                                           |

```text
F0 00 20 33 01 00 71 00 2E 00 F7 # 1831 Hz
F0 00 20 33 01 00 71 00 2E 0C F7 # 2355 Hz
F0 00 20 33 01 00 71 00 2E 1F F7 # 3436 Hz
F0 00 20 33 01 00 71 00 2E 3B F7 # 6183 Hz
F0 00 20 33 01 00 71 00 2E 3E F7 # 6724 Hz
F0 00 20 33 01 00 71 00 2E 40 F7 # 7012 Hz
F0 00 20 33 01 00 71 00 2E 7F F7 # 24.0 kHz
```

**Not** Page A **Filter 1 Keyfollow** (`70`/`2E`).

### EQ High Gain (`cmd=0x71`, param `0x60`) {#eq-high-gain-cmd0x71-param-0x60}

**EDIT FX → High EQ → Gain**. Page **B#96** = **`0x60`**. Same encoding as
[EQ Low Gain](#eq-low-gain-cmd0x71-param-0x5f) — see
[EQ High Gain](../parameter-options.md#eq-high-gain).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 60 <value> F7`          |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**          |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB |
| Confirmed      | Hardware TX (same sweep pattern as Low/Mid Gain)     |

```text
F0 00 20 33 01 00 71 00 60 00 F7 # −16 dB
F0 00 20 33 01 00 71 00 60 40 F7 # Off
F0 00 20 33 01 00 71 00 60 7F F7 # +16 dB
```
