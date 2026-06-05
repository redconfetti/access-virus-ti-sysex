# Effects (Edit FX)

Edit FX — **Delay**, **Reverb**, **EQ**, **Distortion**, **Character**,
**Chorus**, **Phaser**, **Others** (focus + documented blocks).

Part of [Live Edit](README.md). Enumerated options:
[parameter-option-lists.md](../parameter-option-lists.md).
Dump worksheet: [Single parameter map](../dumps/single.md#single-parameter-map)
· Multi: [Edit Multi](edit-multi.md).

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7   # multi / common (some params)
F0 00 20 33 01 00 71 <part> <param> <value> F7   # Page B single (some params)
F0 00 20 33 01 00 70 <part> <param> <value> F7   # Page A single (when global Page A = SysEx)
F0 00 20 33 01 00 6E <part> <param> <value> F7   # part single edit buffer
```

Param IDs are **not global** — the same hex ID can mean different settings under
different `cmd` bytes.

## Edit FX (Effects)

Panel **EDIT FX** (after **Common**). SysEx **`cmd` / `param`** per control —
capture as you step through sub-menus.

### EFFECTS section focus (`cmd=0x6E`) {#effects-section-focus}

The front-panel **EFFECTS** area has two **SELECT** groups. Each group’s
highlighted effect is switched with **`cmd=0x6E`** on the part single buffer
(same buffer as [Delay Type](#delay-type-cmd0x6e), [Reverb
Mode](#reverb-mode-cmd0x6e),
etc.). This **does not** change parameter values — only which effect the **three
knobs** and LCD labels target.

| Group                              | `param`    | Enum                                                                        |
| ---------------------------------- | ---------- | --------------------------------------------------------------------------- |
| **1** (Delay / Reverb / EQ …)      | **`0x75`** | [EFFECTS focus group 1](../parameter-option-lists.md#effects-focus-group-1) |
| **2** (Distortion / Character / …) | **`0x76`** | [EFFECTS focus group 2](../parameter-option-lists.md#effects-focus-group-2) |

| Item           | Value                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> <param> <value> F7`                                               |
| Confirmed      | Hardware TX + **`sendmidi`** — groups **1** and **2**, **`00`–`04`** each change selection     |
| UI latency     | EFFECTS **LED** / focus update often **> 0.5 s** after TX; use **≥ 1 s** between test messages |

```text
F0 00 20 33 01 00 6E 00 75 00 F7   # Group 1 → Delay
F0 00 20 33 01 00 6E 00 75 01 F7   # Group 1 → Reverb
F0 00 20 33 01 00 6E 00 75 02 F7   # Group 1 → Low EQ
F0 00 20 33 01 00 6E 00 75 03 F7   # Group 1 → Mid EQ
F0 00 20 33 01 00 6E 00 75 04 F7   # Group 1 → High EQ
F0 00 20 33 01 00 6E 00 76 00 F7   # Group 2 → Distortion
F0 00 20 33 01 00 6E 00 76 01 F7   # Group 2 → Character
F0 00 20 33 01 00 6E 00 76 02 F7   # Group 2 → Chorus
F0 00 20 33 01 00 6E 00 76 03 F7   # Group 2 → Phaser
F0 00 20 33 01 00 6E 00 76 04 F7   # Group 2 → Others (Vocoder / Input Follower / Filter Bank)
```

**Not** global [Memory Protect](edit-config.md#memory-protect-0x76) (`73`/`76`).
**Not** [Delay LFO Wave](../parameter-option-lists.md#delay-lfo-wave)
(`70`/`76`).

Knob routing per focus: [Delay EFFECTS knobs](#delay-effects-knobs) when group
**1**
= **Delay**; [Distortion soft-knob
runtime](edit-single.md#soft-knob-runtime-distortion-intensity) when
group **2** = **Distortion**; Reverb / EQ / Chorus / Phaser / **Others** knob
maps
**TBD** as captured.

### Distortion

**EDIT FX → Distortion**. Focus **EFFECTS** group **2** with
[`6E`/`76`/`00`](#effects-section-focus) before knob edits target this block.

Panel layout: [Distortion panel
visibility](../parameter-option-lists.md#distortion-panel-visibility).

| Control                   | Notes                                                                                                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Type**                  | [`71`/`64`](#distortion-type-cmd0x71-param-0x64) — **`00`** = Off                                                                                     |
| **Mix**                   | [`6E`/`48`](#distortion-mix-cmd0x6e-param-0x48) — standard / minimal / reducer / overdrive                                                            |
| **Intensity** / **Drive** | [`71`/`65`](#distortion-intensity-cmd0x71-param-0x65) — **Intensity** (standard / minimal / reducer); **Drive** (overdrive `14`–`19`)                 |
| **Tone**                  | [`6E`/`4A`](#distortion-tone-cmd0x6e-param-0x4a) — overdrive with Tone (`14`/`16`/`17`/`18`)                                                          |
| **Treble Boost**          | [`6E`/`46`](#distortion-treble-boost-cmd0x6e-param-0x46) — [standard types](../parameter-option-lists.md#standard-types--same-four-percent-rows) only |
| **High Cut**              | [`6E`/`47`](#distortion-high-cut-cmd0x6e-param-0x47) — standard + [overdrive](../parameter-option-lists.md#overdrive-types--drive-mix-high-cut)       |
| **Quality**               | [`6E`/`49`](#distortion-quality-cmd0x6e-param-0x49) — **Bit** / **Rate Reducer** (`13`/`12`) only                                                     |

### Distortion Type (`cmd=0x71`, param `0x64`) {#distortion-type-cmd0x71-param-0x64}

**EDIT FX → Distortion → Type**. Page **B#100** = **`0x64`**. Enum:
[Distortion Type](../parameter-option-lists.md#distortion-type) (**`stored =
<value>`**,
not a dense index).

| Item           | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 64 <value> F7`                          |
| Value encoding | Wire byte per option table (**`00`** Off … **`19`** Chili Overdrive) |
| Confirmed      | Hardware TX (menu step-through; matches panel labels)                |

```text
F0 00 20 33 01 00 71 00 64 00 F7   # Off
F0 00 20 33 01 00 71 00 64 0C F7   # Wide
F0 00 20 33 01 00 71 00 64 01 F7   # Light
F0 00 20 33 01 00 71 00 64 03 F7   # Medium
F0 00 20 33 01 00 71 00 64 04 F7   # Hard
F0 00 20 33 01 00 71 00 64 05 F7   # Digital
F0 00 20 33 01 00 71 00 64 06 F7   # Wave Shaper
F0 00 20 33 01 00 71 00 64 07 F7   # Rectifier
F0 00 20 33 01 00 71 00 64 12 F7   # Rate Reducer
F0 00 20 33 01 00 71 00 64 13 F7   # Bit Reducer
F0 00 20 33 01 00 71 00 64 0D F7   # Soft Bounce
F0 00 20 33 01 00 71 00 64 0E F7   # Hard Bounce
F0 00 20 33 01 00 71 00 64 0F F7   # Sine Fold
F0 00 20 33 01 00 71 00 64 10 F7   # Triangle Fold
F0 00 20 33 01 00 71 00 64 11 F7   # Sawtooth Fold
F0 00 20 33 01 00 71 00 64 0A F7   # Low Pass
F0 00 20 33 01 00 71 00 64 0B F7   # High Pass
F0 00 20 33 01 00 71 00 64 08 F7   # Bit Reducer Old
F0 00 20 33 01 00 71 00 64 09 F7   # Rate Reducer Old
F0 00 20 33 01 00 71 00 64 14 F7   # Mint Overdrive
F0 00 20 33 01 00 71 00 64 15 F7   # Curry Overdrive
F0 00 20 33 01 00 71 00 64 16 F7   # Saffron Overdrive
F0 00 20 33 01 00 71 00 64 17 F7   # Onion Overdrive
F0 00 20 33 01 00 71 00 64 18 F7   # Pepper Overdrive
F0 00 20 33 01 00 71 00 64 19 F7   # Chili Overdrive
```

### Distortion Mix (`cmd=0x6E`, param `0x48`) {#distortion-mix-cmd0x6e-param-0x48}

**EDIT FX → Distortion → Mix** ([panel
visibility](../parameter-option-lists.md#distortion-panel-visibility) — standard
/ minimal / reducer / overdrive).
Part buffer **`6E`**.

| Item           | Value                                                                                   |
| -------------- | --------------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 48 <value> F7`                                             |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`                                    |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**; standard types incl. **Wave Shaper** / **Rectifier**) |

```text
F0 00 20 33 01 00 6E 00 48 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 48 48 F7   # 56.3 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 48 7F F7   # 100.0 %
```

Param id and value both **`48`** in the last example — **`6E <part> 48
<value>`** (Page
**B** param **`0x48`**, wire value **`0x48`**).

### Distortion Intensity (`cmd=0x71`, param `0x65`) {#distortion-intensity-cmd0x71-param-0x65}

**EDIT FX → Distortion → Intensity** ([panel
visibility](../parameter-option-lists.md#distortion-panel-visibility) — standard
/ minimal / reducer). On [overdrive
types](../parameter-option-lists.md#overdrive-types--drive-mix-high-cut) the
panel label is **Drive** (same byte).
Page **B#101** = **`0x65`**. Same byte as [soft-knob
runtime](edit-single.md#soft-knob-runtime-distortion-intensity).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 65 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 71 00 65 00 F7   # 0.0 %
F0 00 20 33 01 00 71 00 65 65 F7   # 78.9 % (Wide; panel-confirmed)
F0 00 20 33 01 00 71 00 65 7F F7   # 100.0 %
```

Param id and value both **`65`** in the middle example — **`71 <part> 65
<value>`**.

### Distortion Treble Boost (`cmd=0x6E`, param `0x46`) {#distortion-treble-boost-cmd0x6e-param-0x46}

**EDIT FX → Distortion → Treble Boost** ([standard
types](../parameter-option-lists.md#distortion-panel-visibility)).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 46 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 6E 00 46 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 46 40 F7   # 50.0 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 46 7F F7   # 100.0 %
```

### Distortion Tone (`cmd=0x6E`, param `0x4A`) {#distortion-tone-cmd0x6e-param-0x4a}

**EDIT FX → Distortion → Tone** ([overdrive types with
Tone](../parameter-option-lists.md#overdrive-types--drive-mix-high-cut) —
**Mint** / **Saffron** / **Onion** / **Pepper**; not **Curry** / **Chili**).

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 4A <value> F7`                                        |
| Panel range    | **−100.0..+100.0 %**; **`40`** = +0 %                                              |
| Endpoints      | **`00`** → −100.0 %, **`7F`** → +100.0 %                                           |
| Confirmed      | Hardware TX (sweep on **`64 16`** / **`64 17`** / **`64 18`**; **`40`** at center) |

```text
F0 00 20 33 01 00 6E 00 4A 00 F7   # −100.0 %
F0 00 20 33 01 00 6E 00 4A 40 F7   # +0 % (panel-confirmed)
F0 00 20 33 01 00 6E 00 4A 7F F7   # +100.0 %
```

### Distortion High Cut (`cmd=0x6E`, param `0x47`) {#distortion-high-cut-cmd0x6e-param-0x47}

**EDIT FX → Distortion → High Cut** ([standard
types](../parameter-option-lists.md#standard-types--same-four-percent-rows) and
[overdrive
types](../parameter-option-lists.md#overdrive-types--drive-mix-high-cut)).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 47 <value> F7`          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)                    |

```text
F0 00 20 33 01 00 6E 00 47 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 47 40 F7   # 50.0 % (Wide; panel-confirmed)
F0 00 20 33 01 00 6E 00 47 7F F7   # 100.0 %
```

### Distortion Quality (`cmd=0x6E`, param `0x49`) {#distortion-quality-cmd0x6e-param-0x49}

**EDIT FX → Distortion → Quality** (**Type** = **Bit Reducer** or **Rate
Reducer**).
Replaces **Treble Boost** / **High Cut** on those types — see
[Distortion panel
visibility](../parameter-option-lists.md#distortion-panel-visibility).

| Item           | Value                                                                                |
| -------------- | ------------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 49 <value> F7`                                          |
| Panel range    | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`                                 |
| Confirmed      | Hardware TX (**Rate** / **Bit Reducer**; sweep **`00`–`7F`**; **50.0 %** → **`40`**) |

```text
F0 00 20 33 01 00 6E 00 49 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 49 40 F7   # 50.0 % (Rate / Bit Reducer; panel-confirmed)
F0 00 20 33 01 00 6E 00 49 7F F7   # 100.0 %
```

### Delay

Panel layout: [Delay panel
visibility](../parameter-option-lists.md#delay-panel-visibility).

#### EFFECTS section knobs (Delay selected) {#delay-effects-knobs}

With **EFFECTS** group **1** = **Delay**
([`6E`/`75`/`00`](#effects-section-focus)),
the
three front-panel knobs drive the same live-edit bytes as **EDIT FX → Delay**
(Page
**A**, `cmd=0x70`). TI mk2 confirmed:

| Knob | LCD label          | `param`    | Encoding                                                                                         |
| ---- | ------------------ | ---------- | ------------------------------------------------------------------------------------------------ |
| 1    | **Delay Send**     | **`0x71`** | [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd) — **`00`** Off … **`7F`** Effect |
| 2    | **Delay Color**    | **`0x77`** | Classic **Coloration** — **`stored = ui + 64`** (**−64..+63**)                                   |
| 3    | **Delay Feedback** | **`0x73`** | Classic **0.0..100.0 %** — `stored = round(pct × 127 / 100)`                                     |

Same **`70`/`77`** byte is **Tape Frequency** when **Type** ≠ Classic — knob
label
stays **Delay Color** only for Classic-style routing; confirm **Type** on panel.

**Send = Off (`00`)** — all **Types**: panel shows **Type**, **Send**, and
**Feedback** only (no **Delay Time** / **Time**, **Mode**, etc.). Set **Send**
to a
non-**Off** value before type-specific rows appear.

| Control      | Notes                                                                                                                         |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| **Type**     | [Delay Type](../parameter-option-lists.md#delay-type) — [`6E`/`0A`](#delay-type-cmd0x6e)                                      |
| **Send**     | [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd) — [`70`/`71`](#delay-send-cmd0x70-param-0x71); **`00`** = Off |
| **Feedback** | [`70`/`73`](#delay-feedback) — **Classic** **0..100 %** / **Tape** **0..200 %**                                               |

#### Classic (`00`) — Send ≠ Off

| Control        | Notes                                                                                                                                                                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Send**       | [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd); [`70`/`71`](#delay-send-cmd0x70-param-0x71)                                                                                                                             |
| **Feedback**   | **0.0..100.0 %** — [`70`/`73`](#delay-feedback)                                                                                                                                                                                          |
| **Mode**       | [Delay Mode](../parameter-option-lists.md#delay-mode) — **`01`–`16`**; [`70`/`70`](#delay-mode-cmd0x70-param-0x70); **Pattern …** = no **Clock**                                                                                         |
| **Coloration** | **−64..+63** → `stored = ui + 64` — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77); [anchors](../parameter-option-lists.md#delay-coloration)                                                                                      |
| **Clock**      | [Delay Clock](../parameter-option-lists.md#delay-clock) — Simple/Ping Pong only; **`71`/`14`**; **`00`** = Off                                                                                                                           |
| **Delay Time** | Simple/Ping Pong + **Clock** Off only — [`70`/`72`](#delay-tape-time-cmd0x70-param-0x72); **not** on **Pattern** (`06`–`16`; panel **Pattern 5+5**)                                                                                      |
| **LFO**        | [Delay LFO](../parameter-option-lists.md#delay-lfo) — **Rate** [`70`/`74`](#delay-lfo-rate-cmd0x70-param-0x74), **Depth** [`70`/`75`](#delay-lfo-depth-cmd0x70-param-0x75), **LFO Wave** [`70`/`76`](#delay-lfo-wave-cmd0x70-param-0x76) |

#### Tape Clocked (`01`) — Send ≠ Off

| Control         | Notes                                                                                                                                                 |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Send**        | [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd) — Off, −46.2 dB … **0/−24.0 dB**, Effect; [`70`/`71`](#delay-send-cmd0x70-param-0x71) |
| **Feedback**    | **0.0..200.0 %** — [`70`/`73`](#delay-feedback); **`40`** = 100.0 %                                                                                   |
| **Left Clock**  | [Delay Tape Left Clock](../parameter-option-lists.md#delay-tape-left-clock) — **`6E`/`0D`**; `00`–`05`                                                |
| **Right Clock** | [Delay Tape Right Clock](../parameter-option-lists.md#delay-tape-right-clock) — **`6E`/`0E`**; same menu                                              |
| **Frequency**   | **`0`–`127`** — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77)                                                                                 |
| **Bandwidth**   | **`0`–`127`** — [`6E`/`11`](#delay-tape-bandwidth-cmd0x6e-param-0x11)                                                                                 |
| **Modulation**  | **0.0..100.0 %** — [`70`/`75`](#delay-tape-modulation-cmd0x70-param-0x75)                                                                             |

No **Time** or **Ratio** on **Tape Clocked**.

#### Tape Free (`02`) / Tape Doppler (`03`) — Send ≠ Off

| Control        | Notes                                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Send**       | [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd); [`70`/`71`](#delay-send-cmd0x70-param-0x71) — same curve all **Types** (panel: **Tape Doppler** `03`) |
| **Feedback**   | **0.0..200.0 %** — [`70`/`73`](#delay-feedback); same as Tape Clocked (panel: **Tape Doppler** `03`)                                                                   |
| **Time**       | Same as Classic **Delay Time** — **0.0..693.6 ms**, [`70`/`72`](#delay-tape-time-cmd0x70-param-0x72); [LCD table](../parameter-option-lists.md#delay-tape-time)        |
| **Ratio**      | [Delay Tape Ratio](../parameter-option-lists.md#delay-tape-ratio) — **`6E`/`0C`**; `00`–`06` (panel: **Tape Doppler** `03`)                                            |
| **Frequency**  | **`0`–`127`** — [`70`/`77`](#delay-tape-frequency-cmd0x70-param-0x77) (panel: **Tape Doppler** `03`)                                                                   |
| **Bandwidth**  | **`0`–`127`** — [`6E`/`11`](#delay-tape-bandwidth-cmd0x6e-param-0x11) (panel: **Tape Doppler** `03`)                                                                   |
| **Modulation** | **0.0..100.0 %** — [`70`/`75`](#delay-tape-modulation-cmd0x70-param-0x75) (panel: **Tape Doppler** `03`)                                                               |

No **Left Clock** / **Right Clock** (Tape Clocked only).

### Delay Type (`cmd=0x6E`, param `0x0A`) {#delay-type-cmd0x6e}

**EDIT FX → Delay → Type**. Part-sound buffer (**`6E`**, not Page A).

| Item           | Value                                                                 |
| -------------- | --------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0A <value> F7`                           |
| Value encoding | [Delay Type](../parameter-option-lists.md#delay-type) — **`00`–`03`** |
| Confirmed      | Hardware TX                                                           |

```text
F0 00 20 33 01 00 6E 00 0A 00 F7   # Classic
F0 00 20 33 01 00 6E 00 0A 01 F7   # Tape Clocked
F0 00 20 33 01 00 6E 00 0A 02 F7   # Tape Free
F0 00 20 33 01 00 6E 00 0A 03 F7   # Tape Doppler
```

### Delay Mode (`cmd=0x70`, param `0x70`) {#delay-mode-cmd0x70-param-0x70}

**EDIT FX → Delay → Mode** (**Type** = Classic). Enum:
[Delay Mode](../parameter-option-lists.md#delay-mode) — wire **`01`–`16`**, not
**`00`**.
Not `6E`/`0A` (**Type**).

| Item           | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 70 <value> F7`             |
| Confirmed      | Hardware TX (**`05`–`16`** stepped; enum **`01`–`16`**) |

```text
F0 00 20 33 01 00 70 00 70 01 F7   # Simple Delay
F0 00 20 33 01 00 70 00 70 05 F7   # Ping Pong 8:7
F0 00 20 33 01 00 70 00 70 06 F7   # Pattern 1+1
F0 00 20 33 01 00 70 00 70 16 F7   # Pattern 5+5
```

### Delay Send (`cmd=0x70`, param `0x71`) {#delay-send-cmd0x70-param-0x71}

**EDIT FX → Delay → Send** (all types). Also **EFFECTS → Delay** knob 1 —
[Delay EFFECTS knobs](#delay-effects-knobs). Page **A#113** = **`0x71`**. LCD
index =
wire byte — [Delay Send (LCD)](../parameter-option-lists.md#delay-send-lcd).

| Item           | Value                                                                       |
| -------------- | --------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 71 <value> F7`                                 |
| Confirmed      | Hardware TX — **Off** ↔ **Effect** (`00`–`7F`–`00`); EDIT FX + EFFECTS knob |

```text
F0 00 20 33 01 00 70 00 71 00 F7   # Off
F0 00 20 33 01 00 70 00 71 7F F7   # Effect
```

### Delay Feedback (`cmd=0x70`, param `0x73`) {#delay-feedback}

**EDIT FX → Delay → Feedback**. Page **A#115** = **`0x73`**. Same byte for all
**Types**; scale depends on **Type** — see
[Delay Feedback](../parameter-option-lists.md#delay-feedback).

#### Classic (`00`) — `stored = round(pct × 127 / 100)`

| Item           | Value                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 73 <value> F7`                                    |
| Confirmed      | Hardware TX — **0 %** ↔ **100.0 %** (`00`–`7F`–`00`); EDIT FX + EFFECTS knob 3 |

```text
F0 00 20 33 01 00 70 00 73 00 F7   # 0.0 %
F0 00 20 33 01 00 70 00 73 7F F7   # 100.0 %
```

#### Tape (`01`–`03`) — `stored = round(pct × 127 / 200)`

| Item           | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 73 <value> F7`            |
| Endpoints      | **`00`** = 0 %, **`40`** = 100.0 %, **`7F`** = 200.0 % |
| Confirmed      | Hardware TX (Tape Clocked / Free captures)             |

```text
F0 00 20 33 01 00 70 00 73 40 F7   # 100.0 % (Tape)
F0 00 20 33 01 00 70 00 73 7F F7   # 200.0 % (Tape)
```

### Delay Tape Left Clock (`cmd=0x6E`, param `0x0D`) {#delay-tape-left-clock-cmd0x6e}

**Tape Clocked → Left Clock**. Options:
[Delay Tape Left Clock](../parameter-option-lists.md#delay-tape-left-clock).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0D <value> F7` |
| Confirmed      | Hardware TX (`00`–`05` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0D 00 F7   # 1/32
F0 00 20 33 01 00 6E 00 0D 05 F7   # 5/16
```

### Delay Time (`cmd=0x70`, param `0x72`) {#delay-tape-time-cmd0x70-param-0x72}

**Classic → Delay Time** (Simple/Ping Pong, **Clock** Off only — **not** Pattern
modes), **Tape Free / Doppler → Time** — same param. **0.0..693.6 ms** — see
[Delay Time (ms)](../parameter-option-lists.md#delay-tape-time).

| Item           | Value                                                                          |
| -------------- | ------------------------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 70 <part> 72 <value> F7`                                    |
| Confirmed      | Hardware TX — **Tape Free** full sweep (`00`–`7F`); LCD anchors in option list |

```text
F0 00 20 33 01 00 70 00 72 00 F7   # 0.0 ms
F0 00 20 33 01 00 70 00 72 40 F7   # 349.5 ms
F0 00 20 33 01 00 70 00 72 7F F7   # 693.6 ms
```

### Delay Tape Ratio (`cmd=0x6E`, param `0x0C`) {#delay-tape-ratio-cmd0x6e}

**Tape Free / Tape Doppler → Ratio**. Options:
[Delay Tape Ratio](../parameter-option-lists.md#delay-tape-ratio).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0C <value> F7` |
| Confirmed      | Hardware TX (`00`–`06` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0C 00 F7   # 1/4
F0 00 20 33 01 00 6E 00 0C 06 F7   # 4/1
```

### Delay Coloration / Tape Frequency (`cmd=0x70`, param `0x77`) {#delay-tape-frequency-cmd0x70-param-0x77}

Page **A#119** = **`0x77`**. Same wire byte; encoding depends on **Type** — see
[Delay Coloration](../parameter-option-lists.md#delay-coloration),
[Tape Frequency](../parameter-option-lists.md#delay-tape-frequency).

#### Classic — Coloration (`stored = ui + 64`, **−64..+63**)

**EDIT FX → Delay → Coloration**. Also **EFFECTS → Delay** knob 2 (**Delay
Color**) —
[Delay EFFECTS knobs](#delay-effects-knobs).

| Item           | Value                                                                              |
| -------------- | ---------------------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 77 <value> F7`                                        |
| Endpoints      | **`00`** = −64, **`40`** = +0, **`7F`** = +63                                      |
| Confirmed      | Hardware TX — **−64** ↔ **+63** ↔ **−64** (`00`–`7F`–`00`); EDIT FX + EFFECTS knob |

```text
F0 00 20 33 01 00 70 00 77 00 F7   # −64
F0 00 20 33 01 00 70 00 77 40 F7   # +0
F0 00 20 33 01 00 70 00 77 7F F7   # +63
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
F0 00 20 33 01 00 70 00 77 00 F7   # 0
F0 00 20 33 01 00 70 00 77 7F F7   # 127
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
F0 00 20 33 01 00 70 00 75 00 F7   # 0 %
F0 00 20 33 01 00 70 00 75 7F F7   # 100.0 %
```

### Delay Tape Right Clock (`cmd=0x6E`, param `0x0E`) {#delay-tape-right-clock-cmd0x6e}

**Tape Clocked → Right Clock**. Same labels as Left — param **`0x0E`**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 0E <value> F7` |
| Confirmed      | Hardware TX (`00`–`05` stepped)             |

```text
F0 00 20 33 01 00 6E 00 0E 00 F7   # 1/32
F0 00 20 33 01 00 6E 00 0E 05 F7   # 5/16
```

### Delay LFO {#delay-lfo}

**Rate**, **Depth**, and **LFO Wave** — one panel page; see
[Delay LFO](../parameter-option-lists.md#delay-lfo).

### Delay LFO Rate (`cmd=0x70`, param `0x74`) {#delay-lfo-rate-cmd0x70-param-0x74}

**EDIT FX → Delay → Rate** ([Delay LFO](#delay-lfo)). Page **A#116** =
**`0x74`**. Not **`0x70`** ([Mode](#delay-mode-cmd0x70-param-0x70)).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 74 <value> F7` |
| Value encoding | Direct **`0`–`127`** (`stored = lcd`)       |
| Confirmed      | Hardware TX (Rate sweep **`00`–`7F`**)      |

```text
F0 00 20 33 01 00 70 00 74 00 F7   # Rate 0
F0 00 20 33 01 00 70 00 74 7F F7   # Rate 127
```

### Delay LFO Depth (`cmd=0x70`, param `0x75`) {#delay-lfo-depth-cmd0x70-param-0x75}

**EDIT FX → Delay → Depth** ([Delay LFO](#delay-lfo)). Page **A#117** =
**`0x75`**.
Same param byte as [Tape Modulation](#delay-tape-modulation-cmd0x70-param-0x75)
on
**Tape** types only.

| Item           | Value                                                    |
| -------------- | -------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 75 <value> F7`              |
| Value encoding | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`     |
| Endpoints      | **`00`** = 0 %, **`7F`** = 100.0 %                       |
| Confirmed      | Hardware TX (Depth sweep **`00`–`7F`**)                  |

```text
F0 00 20 33 01 00 70 00 75 00 F7   # Depth 0 %
F0 00 20 33 01 00 70 00 75 7F F7   # Depth 100.0 %
```

### Delay LFO Wave (`cmd=0x70`, param `0x76`) {#delay-lfo-wave-cmd0x70-param-0x76}

**EDIT FX → Delay → LFO Wave**. Page **A#118** = **`0x76`**. Options:
[Delay LFO Wave](../parameter-option-lists.md#delay-lfo-wave).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 70 <part> 76 <value> F7` |
| Value encoding | Wire byte **`00`–`05`** (enum)              |
| Confirmed      | Hardware TX (wave stepped **`00`–`05`**)    |

```text
F0 00 20 33 01 00 70 00 76 00 F7   # Sine
F0 00 20 33 01 00 70 00 76 05 F7   # S&G
```

### Reverb

Panel layout: [Reverb panel
visibility](../parameter-option-lists.md#reverb-panel-visibility).

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
Enum: [Reverb Mode](../parameter-option-lists.md#reverb-mode). **Not** param
**`0x03`**
(that is [Type](#reverb-type-cmd0x6e)).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 01 <value> F7` |
| Value encoding | Wire byte **`00`–`03`**                     |
| Confirmed      | Hardware TX (**`01`–`03`** stepped)         |

```text
F0 00 20 33 01 00 6E 00 01 01 F7   # Reverb
F0 00 20 33 01 00 6E 00 01 02 F7   # Feedback 1
F0 00 20 33 01 00 6E 00 01 03 F7   # Feedback 2
```

### Reverb Type (`cmd=0x6E`, param `0x03`) {#reverb-type-cmd0x6e}

**EDIT FX → Reverb → Type** (**Mode** = Reverb). Enum:
[Reverb Type](../parameter-option-lists.md#reverb-type).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 03 <value> F7`        |
| Value encoding | Wire byte **`00`–`03`**                            |
| Confirmed      | Hardware TX (**`00`–`03`**; Hall → Ambience sweep) |

```text
F0 00 20 33 01 00 6E 00 03 00 F7   # Ambience
F0 00 20 33 01 00 6E 00 03 01 F7   # Small Room
F0 00 20 33 01 00 6E 00 03 02 F7   # Large Room
F0 00 20 33 01 00 6E 00 03 03 F7   # Hall
```

### Reverb Clock (`cmd=0x6E`, param `0x08`) {#reverb-clock-cmd0x6e}

**EDIT FX → Reverb → Clock**. Syncs **Predelay**. Same **`<value>`** map as
[Delay Clock](../parameter-option-lists.md#delay-clock) but **`6E`/`08`** (not
`71`/`14`).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 08 <value> F7` |
| Confirmed      | Hardware TX (**Off** → **3/4** → **Off**)   |

```text
F0 00 20 33 01 00 6E 00 08 00 F7   # Off
F0 00 20 33 01 00 6E 00 08 10 F7   # 3/4
```

### Reverb Time (`cmd=0x6E`, param `0x04`) {#reverb-time-cmd0x6e}

**EDIT FX → Reverb → Time** (**Mode** = Reverb). Tail length **0..127**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 04 <value> F7` |
| Value encoding | **`stored = lcd`**                          |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)           |

```text
F0 00 20 33 01 00 6E 00 04 00 F7   # 0
F0 00 20 33 01 00 6E 00 04 44 F7   # 68
F0 00 20 33 01 00 6E 00 04 7F F7   # 127
```

### Reverb Damping (`cmd=0x6E`, param `0x05`) {#reverb-damping-cmd0x6e}

**EDIT FX → Reverb → Damping** (**Mode** = Reverb). **0.0..100.0 %** — see
[Reverb Damping](../parameter-option-lists.md#reverb-damping).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 05 <value> F7` |
| Value encoding | `stored = round(pct × 127 / 100)`           |
| Confirmed      | Hardware TX (sweep **`00`–`7F`**)           |

```text
F0 00 20 33 01 00 6E 00 05 00 F7   # 0.0 %
F0 00 20 33 01 00 6E 00 05 14 F7   # 15.6 % (panel)
F0 00 20 33 01 00 6E 00 05 7F F7   # 100.0 %
```

### Reverb Coloration (`cmd=0x6E`, param `0x06`) {#reverb-coloration-cmd0x6e}

**EDIT FX → Reverb → Coloration** (**Mode** = Reverb). **−64..+63** — see
[Reverb Coloration](../parameter-option-lists.md#reverb-coloration).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 06 <value> F7` |
| Value encoding | `stored = ui + 64`                          |
| Confirmed      | Hardware TX (sweep **+63** → **−64**)       |

```text
F0 00 20 33 01 00 6E 00 06 40 F7   # +0
F0 00 20 33 01 00 6E 00 06 7F F7   # +63
F0 00 20 33 01 00 6E 00 06 00 F7   # −64
```

### Reverb Predelay (`cmd=0x6E`, param `0x07`) {#reverb-predelay-cmd0x6e}

**EDIT FX → Reverb → Predelay** (**Clock** = Off). **0.0..500.0 ms** — see
[Reverb Predelay](../parameter-option-lists.md#reverb-predelay).

| Item           | Value                                                                   |
| -------------- | ----------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 07 <value> F7`                             |
| Value encoding | **`stored = lcd`**; valid **`00`–`5C`**; `lcd_ms ≈ stored × 500.0 / 92` |
| Confirmed      | Hardware TX (sweep **0.0** → **500.0** ms; max wire **`5C`**)           |

```text
F0 00 20 33 01 00 6E 00 07 00 F7   # 0.0 ms
F0 00 20 33 01 00 6E 00 07 20 F7   # 174.8 ms
F0 00 20 33 01 00 6E 00 07 40 F7   # 349.5 ms
F0 00 20 33 01 00 6E 00 07 5C F7   # 500.0 ms
```

### Reverb Feedback (`cmd=0x6E`, param `0x09`) {#reverb-feedback-cmd0x6e}

**EDIT FX → Reverb → Feedback** (**Mode** = **Feedback 1** or **Feedback 2**).
**0..127** — see [Reverb
Feedback](../parameter-option-lists.md#reverb-feedback).

| Item           | Value                                                  |
| -------------- | ------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 09 <value> F7`            |
| Value encoding | **`stored = lcd`**                                     |
| Confirmed      | Hardware TX (**Feedback 2** mode, sweep **`00`–`7F`**) |

```text
F0 00 20 33 01 00 6E 00 09 00 F7   # 0
F0 00 20 33 01 00 6E 00 09 7F F7   # 127
```

### Reverb Send (`cmd=0x6E`) {#reverb-send-cmd0x6e}

`cmd=0x6E` is used while editing a **part’s sound** (part/single edit
buffer), not while storing a full Multi program.
Reverb Send is **not** in the 267-byte `DUMP_MULTI`.

| Param ID | Field       | Notes                 |
| -------- | ----------- | --------------------- |
| `0x02`   | Reverb Send | See value table below |

| Item           | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 02 <value> F7`                          |
| Scope          | Part edit / single edit buffer (not stored in `DUMP_MULTI`)          |
| Value range    | Direct byte `0..127`                                                 |
| Key points     | **`00`** = Off, **`60`** = 0/0 dB, **`7F`** = Effect                 |
| Confirmed      | Hardware TX (**Send** sweep **`00`–`7F`**; endpoints + sparse steps) |

```text
F0 00 20 33 01 00 6E 00 02 00 F7   # Off
F0 00 20 33 01 00 6E 00 02 60 F7   # 0/0 dB (unity)
F0 00 20 33 01 00 6E 00 02 7F F7   # Effect
```

LCD ↔ **`stored`**: [Reverb Send
(LCD)](../parameter-option-lists.md#reverb-send-lcd)
(sparse panel rows; full label table still open).

### Low EQ

**EDIT FX → Low EQ**. Both controls use **Page B** (`cmd=0x71`). Distinct from
Page A **Filter 2 Envelope Amount** on **`70`/`2D`**.

| Control            | Live edit                                         |
| ------------------ | ------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`2D`](#eq-low-frequency-cmd0x71-param-0x2d) |
| **Gain**           | [`71`/`5F`](#eq-low-gain-cmd0x71-param-0x5f)      |

### EQ Low Frequency (`cmd=0x71`, param `0x2D`) {#eq-low-frequency-cmd0x71-param-0x2d}

**EDIT FX → Low EQ → Frequency (Hz)**. Page **B#45** = **`0x2D`**. Hz curve:
[EQ Low Frequency](../parameter-option-lists.md#eq-low-frequency).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 2D <value> F7`          |
| Panel range    | **32..458 Hz** (log-spaced LCD; **`stored` ≠ Hz**)   |
| Endpoints      | **`00`** → 32 Hz, **`7F`** → 458 Hz                  |
| Confirmed      | Hardware TX (sweep up to **`7F`**, down to **`00`**) |

```text
F0 00 20 33 01 00 71 00 2D 00 F7   # 32 Hz
F0 00 20 33 01 00 71 00 2D 7F F7   # 458 Hz
```

[Soft Knob Destinations](../parameter-option-lists.md#soft-knob-destinations)
use
different wire bytes (e.g. **Filter 2 Env Amount** = **`2D`** in **`71`/`3E`**)
than
these live-edit param IDs.

### EQ Low Gain (`cmd=0x71`, param `0x5F`) {#eq-low-gain-cmd0x71-param-0x5f}

**EDIT FX → Low EQ → Gain**. Page **B#95** = **`0x5F`**. Encoding:
[EQ Low Gain](../parameter-option-lists.md#eq-low-gain).

| Item           | Value                                                 |
| -------------- | ----------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5F <value> F7`           |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**           |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB  |
| Confirmed      | Hardware TX (sweep **−16 dB** → **Off** → **+16 dB**) |

```text
F0 00 20 33 01 00 71 00 5F 00 F7   # −16 dB
F0 00 20 33 01 00 71 00 5F 40 F7   # Off
F0 00 20 33 01 00 71 00 5F 7F F7   # +16 dB
```

### Mid EQ

**EDIT FX → Mid EQ**. All three controls use **Page B** (`cmd=0x71`).

| Control            | Live edit                                         |
| ------------------ | ------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`5D`](#eq-mid-frequency-cmd0x71-param-0x5d) |
| **Gain**           | [`71`/`5C`](#eq-mid-gain-cmd0x71-param-0x5c)      |
| **Q-Factor**       | [`71`/`5E`](#eq-mid-q-factor-cmd0x71-param-0x5e)  |

### EQ Mid Frequency (`cmd=0x71`, param `0x5D`) {#eq-mid-frequency-cmd0x71-param-0x5d}

**EDIT FX → Mid EQ → Frequency (Hz)**. Page **B#93** = **`0x5D`**. Hz curve:
[EQ Mid Frequency](../parameter-option-lists.md#eq-mid-frequency).

| Item           | Value                                                    |
| -------------- | -------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5D <value> F7`              |
| Panel range    | **19 Hz..24.0 kHz** (log-spaced LCD; max shows **kHz**)  |
| Endpoints      | **`00`** → 19 Hz, **`3E`** → 632 Hz, **`7F`** → 24.0 kHz |
| Confirmed      | Hardware TX (sweep **`7F`** → **`00`** → **`3E`**)       |

```text
F0 00 20 33 01 00 71 00 5D 00 F7   # 19 Hz
F0 00 20 33 01 00 71 00 5D 3E F7   # 632 Hz
F0 00 20 33 01 00 71 00 5D 7F F7   # 24.0 kHz
```

### EQ Mid Gain (`cmd=0x71`, param `0x5C`) {#eq-mid-gain-cmd0x71-param-0x5c}

**EDIT FX → Mid EQ → Gain**. Page **B#92** = **`0x5C`**. Same encoding as
[EQ Low Gain](#eq-low-gain-cmd0x71-param-0x5f) — see
[EQ Mid Gain](../parameter-option-lists.md#eq-mid-gain).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5C <value> F7`          |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**          |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB |
| Confirmed      | Hardware TX (same sweep pattern as Low Gain)         |

```text
F0 00 20 33 01 00 71 00 5C 00 F7   # −16 dB
F0 00 20 33 01 00 71 00 5C 40 F7   # Off
F0 00 20 33 01 00 71 00 5C 7F F7   # +16 dB
```

### EQ Mid Q-Factor (`cmd=0x71`, param `0x5E`) {#eq-mid-q-factor-cmd0x71-param-0x5e}

**EDIT FX → Mid EQ → Q-Factor**. Page **B#94** = **`0x5E`**. Anchors:
[EQ Mid Q-Factor](../parameter-option-lists.md#eq-mid-q-factor).

| Item           | Value                                              |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 5E <value> F7`        |
| Panel range    | **0.28..15.4** (non-linear LCD)                    |
| Endpoints      | **`00`** → 0.28, **`40`** → 1.58, **`7F`** → 15.4  |
| Confirmed      | Hardware TX (sweep **`00`** → **`7F`** → **`40`**) |

```text
F0 00 20 33 01 00 71 00 5E 00 F7   # Q 0.28
F0 00 20 33 01 00 71 00 5E 40 F7   # Q 1.58
F0 00 20 33 01 00 71 00 5E 7F F7   # Q 15.4
```

### High EQ

**EDIT FX → High EQ**. **Frequency** and **Gain** only (no **Q** on mk2 panel).
Both use **Page B** (`cmd=0x71`).

| Control            | Live edit                                          |
| ------------------ | -------------------------------------------------- |
| **Frequency (Hz)** | [`71`/`2E`](#eq-high-frequency-cmd0x71-param-0x2e) |
| **Gain**           | [`71`/`60`](#eq-high-gain-cmd0x71-param-0x60)      |

### EQ High Frequency (`cmd=0x71`, param `0x2E`) {#eq-high-frequency-cmd0x71-param-0x2e}

**EDIT FX → High EQ → Frequency (Hz)**. Page **B#46** = **`0x2E`**. Hz curve:
[EQ High Frequency](../parameter-option-lists.md#eq-high-frequency).

| Item           | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 2E <value> F7`                 |
| Panel range    | **1831 Hz..24.0 kHz** (log-spaced LCD)                      |
| Endpoints      | **`00`** → 1831 Hz, **`40`** → 7012 Hz, **`7F`** → 24.0 kHz |
| Confirmed      | Hardware TX (sweep **`7F`** → **`00`** → **`40`**)          |

```text
F0 00 20 33 01 00 71 00 2E 00 F7   # 1831 Hz
F0 00 20 33 01 00 71 00 2E 40 F7   # 7012 Hz
F0 00 20 33 01 00 71 00 2E 7F F7   # 24.0 kHz
```

**Not** Page A **Filter 1 Keyfollow** (`70`/`2E`).

### EQ High Gain (`cmd=0x71`, param `0x60`) {#eq-high-gain-cmd0x71-param-0x60}

**EDIT FX → High EQ → Gain**. Page **B#96** = **`0x60`**. Same encoding as
[EQ Low Gain](#eq-low-gain-cmd0x71-param-0x5f) — see
[EQ High Gain](../parameter-option-lists.md#eq-high-gain).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 60 <value> F7`          |
| Panel range    | **−16..+16 dB**; **Off** (0 dB) at **`40`**          |
| Endpoints      | **`00`** → −16 dB, **`40`** → Off, **`7F`** → +16 dB |
| Confirmed      | Hardware TX (same sweep pattern as Low/Mid Gain)     |

```text
F0 00 20 33 01 00 71 00 60 00 F7   # −16 dB
F0 00 20 33 01 00 71 00 60 40 F7   # Off
F0 00 20 33 01 00 71 00 60 7F F7   # +16 dB
```
