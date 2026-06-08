# Oscillators

Edit Single — **Oscillators** (Osc 1–3), **Noise**, **Ring Modulator**, **Sub
Oscillator**, **Punch**, **Osc Volume**, **Unison**, and mixer levels.

Part of [Documentation](../../../README.md#documentation). Enumerated options:
[parameter-options.md](../../reference/parameter-options.md).
Parameter map: [Single parameter map](../../dumps/single.md#single-parameter-map)
· Multi: [Edit Multi](../multis.md).

Paging: [virus.md](../../../misc/virus.md#paging) (`0x70` Page A, `0x71` Page B,
`0x6E` part buffer, `0x6F` extended, `0x72` Multi). Param IDs depend on **`cmd`**.

SysEx examples target the [Single edit buffer](README.md) (**`<part>` =
**`0x40`**). To edit a Multi part instead, see
[README — Multi parts](README.md#multi-edit-buffer-parts).

**LCD:** **OSCILLATORS** → **Oscillator 1** / **2** / **Common** / **Mixer**.

Parameters are a **nested tree**: **Mode** → (for Classic) **Shape** →
controls on sub-menus **1–2** (Classic), **1–3** (Wavetable, Grain Simple,
Formant Simple), or **1–4** (Grain Complex, Formant Complex). Document only
rows that appear on the panel for the active Mode/Shape.

## Contents

* [SELECT (`71`/`7F`)](#select-717f)
  * [LCD “landing zones” (same label, different wire)](#lcd-landing-zones-same-label-different-wire)
  * [Oscillator 1 — Mode](#oscillator-1--mode)
  * [Oscillator 1 — Classic](#oscillator-1--classic)
    * [Shape (`0x11`) — wave / saw blend + pure saw](#shape-0x11--wave--saw-blend--pure-saw)
    * [LCD % vs wire](#lcd--vs-wire)
    * [Controls at Shape = Spectral Wave (`00`)](#controls-at-shape--spectral-wave-00)
    * [Balance (Osc 1 Classic)](#balance-osc-1-classic)
    * [Controls at Shape ≥ Sawtooth (`40`)](#controls-at-shape--sawtooth-40)
    * [Pulse Width (Shape ≥ Sawtooth)](#pulse-width-shape--sawtooth)
  * [Oscillator 1 — Hypersaw](#oscillator-1--hypersaw)
  * [Oscillator 1 — Wavetable](#oscillator-1--wavetable)
  * [Oscillator 1 — Wavetable PWM](#oscillator-1--wavetable-pwm)
  * [Oscillator 1 — Grain Simple](#oscillator-1--grain-simple)
  * [Oscillator 1 — Grain Complex](#oscillator-1--grain-complex)
  * [Oscillator 1 — Formant Simple](#oscillator-1--formant-simple)
  * [Oscillator 1 — Formant Complex](#oscillator-1--formant-complex)
  * [Oscillator 2](#oscillator-2)
  * [Oscillator 2 — Mode](#oscillator-2--mode)
  * [Oscillator 2 — Classic](#oscillator-2--classic)
    * [Shape (`0x16`) — wave / saw blend + pure saw](#shape-0x16--wave--saw-blend--pure-saw)
    * [Pulse Width (`0x17`) — Shape ≥ Sawtooth](#pulse-width-0x17--shape--sawtooth)
    * [Wave Select (`0x18`) — Spectral / Wave>Saw region](#wave-select-0x18--spectral--wavesaw-region)
  * [Oscillator 2 — Hypersaw](#oscillator-2--hypersaw)
  * [Oscillator 2 — Wavetable](#oscillator-2--wavetable)
  * [Oscillator 2 — Wavetable PWM](#oscillator-2--wavetable-pwm)
  * [Oscillator 2 — Grain Simple](#oscillator-2--grain-simple)
  * [Oscillator 2 — Grain Complex](#oscillator-2--grain-complex)
  * [Oscillator 2 — Formant Simple](#oscillator-2--formant-simple)
  * [Oscillator 2 — Formant Complex](#oscillator-2--formant-complex)
  * [Oscillator 3](#oscillator-3)
* [Noise](#noise)
  * [Noise Volume](#noise-volume)
  * [Noise Color](#noise-color)
* [Ring Modulator](#ring-modulator)
  * [Ring Modulator Volume](#ring-modulator-volume)
* [Sub Oscillator](#sub-oscillator)
  * [Sub Oscillator Volume](#sub-oscillator-volume)
  * [Sub Oscillator Shape](#sub-oscillator-shape)
  * [Punch Intensity](#punch-intensity)
  * [Osc Volume](#osc-volume)
  * [Mixer (Oscillators menu)](#mixer-oscillators-menu)
  * [Oscillator Section Volume](#oscillator-section-volume)
* [Unison](#unison)
  * [Voices](#voices)
  * [Detune](#detune)
  * [Pan Spread](#pan-spread)
  * [LFO Phase Offset](#lfo-phase-offset)

---

## SELECT (`71`/`7F`)

**OSCILLATORS** section — front-panel **SELECT** cycles which oscillator the
edit page targets. Live edit **`cmd=0x71`**, param **`0x7F`** (Page B). Enum:
[Oscillators SELECT](../../reference/parameter-options.md#oscillators-select).

| Item           | Value                                            |
| -------------- | ------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 71 <part> 7F <value> F7`      |
| Value encoding | **`00`** Osc 1 · **`01`** Osc 2 · **`02`** Osc 3 |

```text
F0 00 20 33 01 00 71 40 7F 01 F7 # 7F/01 — Oscillator 2
F0 00 20 33 01 00 71 40 7F 02 F7 # 7F/02 — Oscillator 3
```

Same **`cmd`/`param`** as [Oscillator Section
Volume](#oscillator-section-volume) — **SELECT** uses
**`00`–`02`** as index; **Mixer → Oscillator Section Volume** uses bipolar
**`stored = ui + 64`** on the same byte.

### LCD “landing zones” (same label, different wire)

On many TI controls the **panel shows one LCD value on several consecutive
detents** while the **SysEx byte still steps +1** each time (`00`–`7F` on the
wire). That does **not** feel like the knob is “stuck” — turn rate still feels
normal — because **display updates and wire resolution are decoupled**: the
firmware keeps fine internal steps for sound and automation, but only changes
the readout when the value crosses the next **0.1**-style label (or a named
tick like **Norm**). While the LCD holds **1.7**, the engine may still walk
**`15` → `16` → `17`** without you noticing each hex step.

This is **usability engineering** for physical knobs (high sensitivity, limited
precision): wide **landing zones** for values humans often want (**+0**,
**Norm**,
round percents) without tedious micro-adjustment, while the backend still uses
the full **128**-step range.

Examples from this repo:

| Control                   | Landing users care about | Wire (examples)                                   |
| ------------------------- | ------------------------ | ------------------------------------------------- |
| Semitone                  | **+0**                   | **`40`** (not the only byte, but a stable center) |
| Key Follow                | **Norm (+32)**           | **`60`** (between **`5F`** / **`61`**)            |
| Balance                   | **0 %**                  | **`40`**                                          |
| Hypersaw Density          | round **1.x–8.x**        | e.g. **`15`/`16`** → 1.7, **`3F`/`40`** → 3.0     |
| Classic Shape (Saw>Pulse) | sparse **%**             | many **+1/+2** LCD steps                          |

**Implication for tools:** map **wire → LCD** with a full detent table (or
capture),
not `stored = f(lcd)` from one formula alone. For **automation**, send the
**wire**
byte; for **UI display**, use the table or accept that several wires show the
same
string.

### Oscillator 1 — Mode

| LCD (Mode)      | `cmd` | `param` | `<value>` |
| --------------- | ----- | ------- | --------- |
| Classic         | `6E`  | `1E`    | `00`      |
| Hypersaw        | `6E`  | `1E`    | `01`      |
| Wavetable       | `6E`  | `1E`    | `02`      |
| Wavetable PWM   | `6E`  | `1E`    | `03`      |
| Grain Simple    | `6E`  | `1E`    | `04`      |
| Grain Complex   | `6E`  | `1E`    | `05`      |
| Formant Simple  | `6E`  | `1E`    | `06`      |
| Formant Complex | `6E`  | `1E`    | `07`      |

Modes **`02`–`07`** — fill LCD labels when stepped with **+/−**. Param
**`0x1E`**
on **`0x6E`** only (not **`0x71`** Filter 1 env polarity).

```text
F0 00 20 33 01 00 6E 40 1E 00 F7 # Mode Classic
F0 00 20 33 01 00 6E 40 1E 01 F7 # Mode Hypersaw
F0 00 20 33 01 00 6E 40 1E 02 F7 # Mode Wavetable
F0 00 20 33 01 00 6E 40 1E 03 F7 # Mode Wavetable PWM (panel: Wave PWM)
F0 00 20 33 01 00 6E 40 1E 04 F7 # Mode Grain Simple
F0 00 20 33 01 00 6E 40 1E 05 F7 # Mode Grain Complex
F0 00 20 33 01 00 6E 40 1E 06 F7 # Mode Formant Simple
F0 00 20 33 01 00 6E 40 1E 07 F7 # Mode Formant Complex
```

### Oscillator 1 — Classic

**Mode `<value>` = `00`**. **Shape** / **Wave Select** / **Pulse Width** — see
below.

**Sub-menus:** **1–2** (LCD pages).

#### Shape (`0x11`) — wave / saw blend + pure saw

**`70` / `11`**. Classic **Shape** is three regions on one control:

| Region               | `<value>` | LCD (examples)                                            |
| -------------------- | --------- | --------------------------------------------------------- |
| Pure **Wave Select** | `00`      | Spectral Wave                                             |
| **Wave / saw mix**   | `01`–`3F` | Wave>Saw 1 % … Wave>Saw 98 %                              |
| Pure **saw**         | `40`      | Sawtooth                                                  |
| **Saw / pulse mix**  | `41`–`7E` | Saw>Pulse … *(LCD % skips integers; **`41`–`7F`** table)* |
| Pure **pulse**       | `7F`      | Pulse                                                     |

**Wave>Saw 98 %** (`3F`) = top of **wave/saw** mix only. **`40`–`41`+** add
**saw**
then **saw/pulse** blend. **Pulse Width** appears on the panel
when
**Shape ≥ `40`** (Sawtooth and Saw>Pulse — not at Spectral Wave `00`).
**Pulse Width** **`70`/`12`** — formulas in
[Pulse Width](#pulse-width-shape--sawtooth); LCD lookup table in
[parameter-options.md](../../reference/parameter-options.md#osc-1-classic--pulse-width--lcd).

| LCD                | `<value>` |
| ------------------ | --------- |
| Sawtooth           | `40`      |
| Saw>Pulse 2 %      | `41`      |
| Saw>Pulse 3 %      | `42`      |
| Saw>Pulse 5 %      | `43`      |
| Saw>Pulse 6 %      | `44`      |
| Saw>Pulse 2 %…98 % | `41`–`7E` |
| Pulse              | `7F`      |

**Saw/Pulse mix** uses **hex** bytes **`0x44`–`0x7E`** (+1 per **+/−**).
Easy mistake: the log’s trailing **`dec`** is the **decimal equivalent** of
that hex byte (`0x44` → 68 dec, `0x5A` → 90 dec) — not a separate index.
A label list keyed as decimal **44–66** was wrong; the wire run was
**hex `44`–`5A`** for this sweep.

**Read the log:**

```text
… 70 00 11 5A dec
 ^^ ← document **0x5A** (not decimal 90, not “66”)
```

**Hex `0x41`–`0x7F`** (Osc 1 Classic Shape, full saw/pulse sweep):

| `<value>` (hex) | LCD label      |
| --------------- | -------------- |
| `41`            | Saw>Pulse 2 %  |
| `42`            | Saw>Pulse 3 %  |
| `43`            | Saw>Pulse 5 %  |
| `44`            | Saw>Pulse 6 %  |
| `45`            | Saw>Pulse 8 %  |
| `46`            | Saw>Pulse 10 % |
| `47`            | Saw>Pulse 11 % |
| `48`            | Saw>Pulse 13 % |
| `49`            | Saw>Pulse 14 % |
| `4A`            | Saw>Pulse 16 % |
| `4B`            | Saw>Pulse 17 % |
| `4C`            | Saw>Pulse 19 % |
| `4D`            | Saw>Pulse 21 % |
| `4E`            | Saw>Pulse 22 % |
| `4F`            | Saw>Pulse 24 % |
| `50`            | Saw>Pulse 25 % |
| `51`            | Saw>Pulse 27 % |
| `52`            | Saw>Pulse 29 % |
| `53`            | Saw>Pulse 30 % |
| `54`            | Saw>Pulse 32 % |
| `55`            | Saw>Pulse 33 % |
| `56`            | Saw>Pulse 35 % |
| `57`            | Saw>Pulse 37 % |
| `58`            | Saw>Pulse 38 % |
| `59`            | Saw>Pulse 40 % |
| `5A`            | Saw>Pulse 41 % |
| `5B`            | Saw>Pulse 43 % |
| `5C`            | Saw>Pulse 44 % |
| `5D`            | Saw>Pulse 46 % |
| `5E`            | Saw>Pulse 48 % |
| `5F`            | Saw>Pulse 49 % |
| `60`            | Saw>Pulse 51 % |
| `61`            | Saw>Pulse 52 % |
| `62`            | Saw>Pulse 54 % |
| `63`            | Saw>Pulse 56 % |
| `64`            | Saw>Pulse 57 % |
| `65`            | Saw>Pulse 59 % |
| `66`            | Saw>Pulse 60 % |
| `67`            | Saw>Pulse 62 % |
| `68`            | Saw>Pulse 63 % |
| `69`            | Saw>Pulse 65 % |
| `6A`            | Saw>Pulse 67 % |
| `6B`            | Saw>Pulse 68 % |
| `6C`            | Saw>Pulse 70 % |
| `6D`            | Saw>Pulse 71 % |
| `6E`            | Saw>Pulse 73 % |
| `6F`            | Saw>Pulse 75 % |
| `70`            | Saw>Pulse 76 % |
| `71`            | Saw>Pulse 78 % |
| `72`            | Saw>Pulse 79 % |
| `73`            | Saw>Pulse 81 % |
| `74`            | Saw>Pulse 83 % |
| `75`            | Saw>Pulse 84 % |
| `76`            | Saw>Pulse 86 % |
| `77`            | Saw>Pulse 87 % |
| `78`            | Saw>Pulse 89 % |
| `79`            | Saw>Pulse 90 % |
| `7A`            | Saw>Pulse 92 % |
| `7B`            | Saw>Pulse 94 % |
| `7C`            | Saw>Pulse 95 % |
| `7D`            | Saw>Pulse 97 % |
| `7E`            | Saw>Pulse 98 % |
| `7F`            | Pulse          |

All rows are **`cmd=0x70` `param=0x11` (Shape)** on Osc 1 Classic.
**+1** hex per **+/−** from **`41`** through **`7E`** (61 steps,
LCD **2 %→98 %**), then **`7F`** = pure Pulse.

#### LCD % vs wire

Each detent is one byte; the LCD **integer** skips values (7 %, 9 %, …)
because the display steps **+1 or +2** per **+/−** only. **`41`→`7E`**:
**26×+1** and **35×+2** (96 points over 61 steps). No reliable one-line
formula — use the table. Example:
**`71`→`7E`**: **`+1 +2 +2 +1 +2 +1 +2 +1 +2 +2 +1 +2 +1`**.

**Wave Select** (`13`) applies in the **`00` / `01`–`3F`** regions. Controls
below
were captured at **Shape = `00`**.

#### Controls at Shape = Spectral Wave (`00`)

| Control     | `cmd` | `param` | Encoding / notes                                                          |
| ----------- | ----- | ------- | ------------------------------------------------------------------------- |
| Shape       | `70`  | `11`    | Mix; `00` = pure wave                                                     |
| Wave Select | `70`  | `13`    | **`00`–`3F`**: Sine, Triangle, Wave 3…Wave 64                             |
| Pulsewidth  | —     | —       | Panel hidden at **`00`**; see [Pulse Width](#pulse-width-shape--sawtooth) |
| Semitone    | `70`  | `14`    | **−48..+48** → `stored = ui + 64`                                         |
| Key Follow  | `70`  | `15`    | **−64..+63** → `stored = ui + 64`                                         |
| Balance     | `70`  | `21`    | **−100..+100 %** → see [Balance](#balance-osc-1-classic)                  |

**Menu 1** — **Norm** on Key Follow is a fixed **+32** (`60`) scale tick,
not per-patch default (store test: saved **−21** → `2B`, reload —
**Norm** still **+32**). **Menu 2** — report if any controls remain.

**Semitone** (`14`): **−48..+48** → `stored = semitone + 64` (**`10`..`70`**).

```text
F0 00 20 33 01 00 70 40 14 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 14 40 F7 # Semitone +0
F0 00 20 33 01 00 70 40 14 70 F7 # Semitone +48
```

**Key Follow** (`15`): **−64..+63** → `stored = ui + 64`. Panel **Norm** labels
**+32** (wire **`0x60`**) — not the wire center (**+0** @ **`0x40`**).

```text
F0 00 20 33 01 00 70 40 15 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 15 40 F7 # Key Follow +0
F0 00 20 33 01 00 70 40 15 60 F7 # Key Follow Norm (+32)
F0 00 20 33 01 00 70 40 15 7F F7 # Key Follow +63
```

Full wire map:
[Key Follow with Norm label](../reference/parameter-options.md#key-follow-with-norm-label).

#### Balance (Osc 1 Classic)

**`cmd=0x70` `param=0x21`** — **−100.0 %..+100.0 %** (not Filter Balance
**`0x30`**).

```text
stored = round((pct + 100) × 127 / 200)
pct = stored × 200 / 127 − 100
```

```text
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 40 F7 # Balance +0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

#### Controls at Shape ≥ Sawtooth (`40`)

**Pulse Width** on the panel when **Shape ≥ `40`** (Sawtooth / Saw>Pulse /
Pulse).

#### Pulse Width (Shape ≥ Sawtooth)

| Control     | `cmd` | `param` |
| ----------- | ----- | ------- |
| Pulse Width | `70`  | `12`    |

**Wire** (`stored` = **`00`–`7F`**, +1 per detent):

```text
pct = 50 + stored × 50 / 127
stored = round((pct − 50) × 127 / 50) # clamp 00..7F
```

**LCD** (panel readout, **Shape ≥ `40`**): `lcd = round(pct + 0.4, 0.1)`.
Endpoints **`00`** / **`7F`** show **50.0 %** / **100 %** on the wire
values directly. Same label can appear on two detents. Partial **wire → LCD**
map:
[parameter-options.md — Osc 1 Pulse Width
LCD](../../reference/parameter-options.md#osc-1-classic--pulse-width--lcd).

```text
```

Single edit buffer (**`<part>=0x40`**) — same **`<value>`** map (spot-check ✓):

```text
F0 00 20 33 01 00 70 40 12 00 F7 # 50.0 %
F0 00 20 33 01 00 70 40 12 40 F7 # 75.6 %
F0 00 20 33 01 00 70 40 12 7F F7 # 100 %
```

### Oscillator 1 — Hypersaw

**Mode `<value>` = `01`**. No **Shape** / **Wave Select** (Classic-only).
**Sub-menus:** **1–2**. Page A **`0x11`** = **Density** here (Classic uses
the same index for **Shape**).

| Control        | `cmd` | `param` | Encoding                                          |
| -------------- | ----- | ------- | ------------------------------------------------- |
| Density        | `70`  | `11`    | **1.0..9.0** — see below                          |
| Local Detune   | `70`  | `12`    | **0..127** → `stored = lcd`                       |
| Sync           | `70`  | `1C`    | Off **`00`** / On **`01`**                        |
| Sync Frequency | `70`  | `1B`    | **0..127** when **Sync On**; `stored = lcd`       |
| Semitone       | `70`  | `14`    | Same as [Classic](#oscillator-1--classic)         |
| Key Follow     | `70`  | `15`    | Same as Classic                                   |
| Balance        | `70`  | `21`    | Same as [Classic Balance](#balance-osc-1-classic) |

**Density** (`11` in Hypersaw only): **1.0..9.0**, +1 wire per detent
**`00`–`7F`**.

```text
internal = 1 + stored × 8 / 127 # SysEx / engine (00 → 1.0, 7F → 9.0)
scale = stored / 127
lcd ≈ round(1 + (internal − 1) × scale, 0.1)
```

**LCD formula status:** `lcd ≈ round(1 + (internal − 1) × scale, 0.1)`
lands **`40`**, **`74`–`76`**, **`7B`**, **`7F`**. **`58`–`6C`**
often **~0.1–0.5 below** predicted; **`44`–`57`**, **`74`+** are within
**~0.1**. Duplicate labels appear on some detents (**`5C`/`5D`**,
**`67`/`68`**, **`77`/`78`**, etc.). Full **128**-entry map:
[parameter-options.md — Density
LCD](../../reference/parameter-options.md#osc-1-hypersaw--density--lcd).

**Do not** use `stored = round((lcd − 1) × 127 / 8)` from LCD alone
(e.g. LCD **3.0** → **`3F`**, not **`20`**).

```text
```

Single edit buffer (**`<part>=0x40`**) — same **`<value>`** map (spot-check ✓):

```text
F0 00 20 33 01 00 70 40 11 00 F7 # Density 1.0
F0 00 20 33 01 00 70 40 11 3F F7 # Density 3.0
F0 00 20 33 01 00 70 40 11 7F F7 # Density 9.0
```

**Local Detune** (`12` in Hypersaw only): same Page A index as Classic
**Pulse Width** (**`12`** there is **50.0 %** … **100 %**). Only interpret
**`12`** with **Mode `01`**.

Panel **0..127** (unsigned, not bipolar). **Wire = LCD** (one detent per step
**`00`–`7F`**).

```text
stored = lcd # 0..127
lcd = stored
```

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 80  | `50`      |

```text
F0 00 20 33 01 00 70 40 12 50 F7 # Local Detune 80
```

**Sync** (`1C` in Hypersaw): panel **Off** / **On**.
**Osc2 Sync** **0/1** — same wire pattern on Osc 1 here.

| LCD | `<value>` |
| --- | --------- |
| Off | `00`      |
| On  | `01`      |

```text
```

Single edit buffer (**`<part>=0x40`**) — same **`<value>`** map (spot-check ✓,
EDIT OSC → Osc 1 sub-menu):

```text
F0 00 20 33 01 00 70 40 1C 00 F7 # Sync Off
F0 00 20 33 01 00 70 40 1C 01 F7 # Sync On
```

**Sync Frequency** (`1B`, conditional on **Sync On**): dump
**Oscillator 1+2 X-Sync Frequency**. Hidden when **Sync Off**. Panel
**0..127** — **`stored = lcd`** (same as **Local Detune**).

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 64  | `40`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 70 40 1B 00 F7 # Sync Frequency 0
F0 00 20 33 01 00 70 40 1B 40 F7 # Sync Frequency 64
F0 00 20 33 01 00 70 40 1B 7F F7 # Sync Frequency 127
```

**FilterEnv>Sync** (`1E` when **Sync On**): same wire and **−100..+100 %**
curve as Osc 2 **FilterEnv>FM** / **FilterEnv>Sync** (see
[Oscillator 2 — Classic](#oscillator-2--classic)).

**Semitone**, **Key Follow**, **Balance** — same **`14` / `15` / `21`**
and encodings as Classic (Semitone
**`10`..`70`** → **−48..+48**, Key Follow **`00`..`7F`** → **−64..+63**,
Balance **`00`/`40`/`7F`** → **−100 % / 0 % / +100 %**).

### Oscillator 1 — Wavetable

**Mode `<value>` = `02`**. **Sub-menus:** **1–3**. No Classic **Shape** /
Hypersaw **Density** / **Sync**.

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | **`00`–`63`**; Sine..Domina7rix   |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | **−48..+48** → `stored = ui + 64` |
| Key Follow    | `70`  | `15`    | **−64..+63** → `stored = ui + 64` |
| Balance       | `70`  | `21`    | **−100.0 %..+100.0 %**            |

**Index** (`11`): same Page A index as Classic **Shape** / Hypersaw
**Density**. Stepped **`00`→`38`** (+1 per detent) then sweep to **`7F`** — no
anomalies vs **1:1** encoding.

```text
```

**Wavetable** (`13`): same Page A index as Classic **Wave Select**. Names:
[parameter-options.md — Wavetable
Names](../../reference/parameter-options.md#wavetable-names).

```text
F0 00 20 33 01 00 70 40 13 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 13 63 F7 # Wavetable Domina7rix
```

**Interpolation** (`6E`/`2C`): part-buffer byte — not **`0x70`** Page A (same
index as [Filter 1 Envelope Amount](filters.md#filter-1-envelope-amount)
on **`0x70`**).

```text
F0 00 20 33 01 00 6E 40 2C 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 2C 7F F7 # Interpolation 127
```

**Semitone**, **Key Follow**, **Balance** — same encodings as
[Classic](#oscillator-1--classic); re-swept in mode **`02`**.

```text
F0 00 20 33 01 00 70 40 14 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 14 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 15 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 15 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

### Oscillator 1 — Wavetable PWM

**Mode `<value>` = `03`**. Panel label **Wave PWM**. **Sub-menus:** **1–3**.
Same index/wavetable/interpolation as [Wavetable](#oscillator-1--wavetable);
adds **Pulse Width** on Page A **`0x12`** and **Local Detune** on part-buffer
**`0x2B`**.

**`0x12` is mode-dependent:** Classic **Pulse Width** (**50.0 %..100 %**),
Hypersaw **Local Detune** (**0..127** on **`70`/`12`**), Wave PWM **Pulse
Width** (**0..127** on **`70`/`12`**).

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | **`00`–`63`**; Sine..Domina7rix   |
| Pulse Width   | `70`  | `12`    | **0..127** → `stored = lcd`       |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | **−48..+48** → `stored = ui + 64` |
| Key Follow    | `70`  | `15`    | **−64..+63** → `stored = ui + 64` |
| Balance       | `70`  | `21`    | **−100.0 %..+100.0 %**            |

```text
F0 00 20 33 01 00 70 40 13 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 13 63 F7 # Wavetable Domina7rix
F0 00 20 33 01 00 6E 40 2C 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 2C 7F F7 # Interpolation 127
F0 00 20 33 01 00 6E 40 2B 00 F7 # Local Detune 0
F0 00 20 33 01 00 6E 40 2B 7F F7 # Local Detune 127
F0 00 20 33 01 00 70 40 14 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 14 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 15 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 15 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

**Local Detune** is on **`6E`/`2B`** only in Wave PWM — not **`70`/`12`**
(Hypersaw uses **`70`/`12`** for Local Detune).

### Oscillator 1 — Grain Simple

**Mode `<value>` = `04`**. **Sub-menus:** **1–3**. Same panel set as
[Formant Simple](#oscillator-1--formant-simple) (no **F-Spread** / **Local
Detune** — those are Complex modes only).

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | **`00`–`63`**; Sine..Domina7rix   |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | **−48..+48** → `stored = ui + 64` |
| Key Follow    | `70`  | `15`    | **−64..+63** → `stored = ui + 64` |
| Balance       | `70`  | `21`    | **−100.0 %..+100.0 %**            |

**F-Shift** (`6E`/`2A`): same param index as [Filter 1
Resonance](filters.md#filter-1-resonance) on **`0x70`** —
use **`cmd`** to disambiguate.

```text
F0 00 20 33 01 00 70 40 13 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 13 63 F7 # Wavetable Domina7rix
F0 00 20 33 01 00 6E 40 2A 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 2A 40 F7 # F-Shift +0
F0 00 20 33 01 00 6E 40 2A 7F F7 # F-Shift +63
F0 00 20 33 01 00 6E 40 2C 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 2C 7F F7 # Interpolation 127
F0 00 20 33 01 00 70 40 14 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 14 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 15 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 15 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

### Oscillator 1 — Grain Complex

**Mode `<value>` = `05`**. **Sub-menus:** **1–4**. Same as
[Grain Simple](#oscillator-1--grain-simple) plus **F-Spread** (`6E`/`25`) and
**Local Detune** (`6E`/`2B`). No **Detune** / **FM** / **FilterEnv** on the
panel (those appear on Osc 2 grain modes only).

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | **`00`–`63`**; Sine..Domina7rix   |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` |
| F-Spread      | `6E`  | `25`    | **0..127** → `stored = lcd`       |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`       |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | **−48..+48** → `stored = ui + 64` |
| Key Follow    | `70`  | `15`    | **−64..+63** → `stored = ui + 64` |
| Balance       | `70`  | `21`    | **−100.0 %..+100.0 %**            |

**Index**, **Wavetable** — same as [Wavetable](#oscillator-1--wavetable)
(**`11`**, **`13`**).

```text
F0 00 20 33 01 00 70 40 13 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 13 63 F7 # Wavetable Domina7rix
```

**F-Shift** (`6E`/`2A`) — same as Grain Simple.

```text
F0 00 20 33 01 00 6E 40 2A 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 2A 7F F7 # F-Shift +63
```

**F-Spread** (`6E`/`25`), **Local Detune** (`6E`/`2B`): Grain Complex only.
**`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 40 25 00 F7 # F-Spread 0
F0 00 20 33 01 00 6E 40 25 7F F7 # F-Spread 127
F0 00 20 33 01 00 6E 40 2B 00 F7 # Local Detune 0
F0 00 20 33 01 00 6E 40 2B 7F F7 # Local Detune 127
```

**Interpolation**, **Semitone**, **Key Follow**, **Balance** — re-swept in mode
**`05`**; same encodings as Wavetable / Classic.

```text
F0 00 20 33 01 00 6E 40 2C 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 2C 7F F7 # Interpolation 127
F0 00 20 33 01 00 70 40 14 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 14 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 15 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 15 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

### Oscillator 1 — Formant Simple

**Mode `<value>` = `06`**. **Sub-menus:** **1–3**.

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names)   |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | Same as Classic                   |
| Key Follow    | `70`  | `15`    | Same as Classic                   |
| Balance       | `70`  | `21`    | Same as Classic                   |

No **F-Spread** control in Formant Simple (unlike Grain Complex / Formant
Complex).
Sweeps in mode **`06`** showed only the controls above.

### Oscillator 1 — Formant Complex

**Mode `<value>` = `07`**. **Sub-menus:** **1–4**. Same as
[Formant Simple](#oscillator-1--formant-simple) plus **F-Spread** and
**Local Detune**.

| Control       | `cmd` | `param` | Encoding                          |
| ------------- | ----- | ------- | --------------------------------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names)   |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` |
| F-Spread      | `6E`  | `25`    | **0..127** → `stored = lcd`       |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`       |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       |
| Semitone      | `70`  | `14`    | Same as Classic                   |
| Key Follow    | `70`  | `15`    | Same as Classic                   |
| Balance       | `70`  | `21`    | Same as Classic                   |

Sweeps in mode **`07`** matched the same encodings as Grain Complex / Formant
Simple for all shared controls.

### Oscillator 2

Same Mode / Shape / table pattern as **Oscillator 1**, but Oscillator 2 uses a
different mode selector and shifted Page A parameter IDs.

### Oscillator 2 — Mode

| LCD (Mode)      | `cmd` | `param` | `<value>` |
| --------------- | ----- | ------- | --------- |
| Classic         | `6E`  | `23`    | `00`      |
| Hypersaw        | `6E`  | `23`    | `01`      |
| Wavetable       | `6E`  | `23`    | `02`      |
| Wavetable PWM   | `6E`  | `23`    | `03`      |
| Grain Simple    | `6E`  | `23`    | `04`      |
| Grain Complex   | `6E`  | `23`    | `05`      |
| Formant Simple  | `6E`  | `23`    | `06`      |
| Formant Complex | `6E`  | `23`    | `07`      |

```text
F0 00 20 33 01 00 6E 40 23 00 F7 # Osc 2 Mode Classic
F0 00 20 33 01 00 6E 40 23 01 F7 # Osc 2 Mode Hypersaw
F0 00 20 33 01 00 6E 40 23 02 F7 # Osc 2 Mode Wavetable
F0 00 20 33 01 00 6E 40 23 03 F7 # Osc 2 Mode Wavetable PWM
F0 00 20 33 01 00 6E 40 23 04 F7 # Osc 2 Mode Grain Simple
F0 00 20 33 01 00 6E 40 23 05 F7 # Osc 2 Mode Grain Complex
F0 00 20 33 01 00 6E 40 23 06 F7 # Osc 2 Mode Formant Simple
F0 00 20 33 01 00 6E 40 23 07 F7 # Osc 2 Mode Formant Complex
```

### Oscillator 2 — Classic

**Mode `<value>` = `00`**. Page A IDs: **Shape** `16`, **Pulse Width** `17`,
**Wave Select** `18`, **Semitone** `19`, **Detune** `1A`, **FM Amount** `1B`,
**Sync** `1C`, **FilterEnv>Pitch** `1D`, **FilterEnv>FM** `1E`, **Key Follow**
`1F`, **Balance** `21`.

| Control         | `cmd` | `param` | Encoding                                                                    |
| --------------- | ----- | ------- | --------------------------------------------------------------------------- |
| Shape           | `70`  | `16`    | Same Classic Shape table as Osc 1 — see below                               |
| Pulse Width     | `70`  | `17`    | **50.0 %..100 %** when Shape ≥ `40` — same as Osc 1 **`12`**                |
| Wave Select     | `70`  | `18`    | **`00`–`3F`** — same 64-wave enum as Osc 1 **`13`**                         |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`                                           |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`                                                 |
| FM Mode         | `71`  | `22`    | Enum; see below                                                             |
| FM Amount       | `70`  | `1B`    | **Sync Off:** **0.0..100.0 %**; **Sync On:** **Sync Frequency** **0..127**  |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %**; see formula below                                         |
| Sync            | `70`  | `1C`    | Off **`00`** / On **`01`**                                                  |
| FilterEnv>FM    | `70`  | `1E`    | **Sync Off:** **FilterEnv>FM**; **Sync On:** **FilterEnv>Sync** (same wire) |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`                                           |
| Balance         | `70`  | `21`    | **−100..+100 %** → see Osc 1 Balance                                        |

#### Shape (`0x16`) — wave / saw blend + pure saw

**`70` / `16`**. Same three regions as [Osc 1 Classic Shape](#shape-0x11--wave--saw-blend--pure-saw)
(**`70` / `11`** there):

| Region               | `<value>` | LCD (examples)                                            |
| -------------------- | --------- | --------------------------------------------------------- |
| Pure **Wave Select** | `00`      | Spectral Wave                                             |
| **Wave / saw mix**   | `01`–`3F` | Wave>Saw 1 % … Wave>Saw 98 %                              |
| Pure **saw**         | `40`      | Sawtooth                                                  |
| **Saw / pulse mix**  | `41`–`7E` | Saw>Pulse … *(same skip pattern as Osc 1; **`41`–`7F`**)* |
| Pure **pulse**       | `7F`      | Pulse                                                     |

**Pulse Width** (`17`) appears when **Shape ≥ `40`** (same rule as Osc 1
**`12`**).

| LCD           | `<value>` |
| ------------- | --------- |
| Spectral Wave | `00`      |
| Wave>Saw 97 % | `3E`      |
| Wave>Saw 98 % | `3F`      |
| Sawtooth      | `40`      |
| Saw>Pulse 2 % | `41`      |
| Pulse         | `7F`      |

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Shape Spectral Wave
F0 00 20 33 01 00 70 40 16 3E F7 # Shape Wave>Saw 97 %
F0 00 20 33 01 00 70 40 16 3F F7 # Shape Wave>Saw 98 %
F0 00 20 33 01 00 70 40 16 40 F7 # Shape Sawtooth
F0 00 20 33 01 00 70 40 16 41 F7 # Shape Saw>Pulse 2 %
F0 00 20 33 01 00 70 40 16 7F F7 # Shape Pulse
```

#### Pulse Width (`0x17`) — Shape ≥ Sawtooth

**`70` / `17`**. Panel when **Shape ≥ `40`**. Same encoding as [Osc 1 Pulse
Width](#pulse-width-shape--sawtooth) (**`70` / `12`**):

```text
pct = 50 + stored × 50 / 127
stored = round((pct − 50) × 127 / 50) # clamp 00..7F
```

Endpoints **`00`** / **`7F`** = **50.0 %** / **100 %**. LCD curve and duplicate
detents: [parameter-options.md — Osc 1 Pulse Width
LCD](../../reference/parameter-options.md#osc-1-classic--pulse-width--lcd) (same panel
behavior).

```text
F0 00 20 33 01 00 70 40 17 00 F7 # Pulse Width 50.0 %
F0 00 20 33 01 00 70 40 17 7F F7 # Pulse Width 100 %
```

#### Wave Select (`0x18`) — Spectral / Wave>Saw region

**`70` / `18`**. When **Shape** is **Spectral Wave** or in the **Wave>Saw**
mix region. **`stored`** = wave index **`00`–`3F`** (64 waves) — same labels and
wire order as [Osc 1 Wave Select](#controls-at-shape--spectral-wave-00)
(**`70` / `13`**).

| LCD      | `<value>` |
| -------- | --------- |
| Sine     | `00`      |
| Triangle | `01`      |
| Wave 8   | `07`      |
| Wave 22  | `15`      |
| Wave 64  | `3F`      |

```text
F0 00 20 33 01 00 70 40 18 00 F7 # Wave Select Sine
F0 00 20 33 01 00 70 40 18 01 F7 # Wave Select Triangle
F0 00 20 33 01 00 70 40 18 07 F7 # Wave Select Wave 8
F0 00 20 33 01 00 70 40 18 15 F7 # Wave Select Wave 22
F0 00 20 33 01 00 70 40 18 3F F7 # Wave Select Wave 64
```

**Semitone** (`19`): **−48..+48** → `stored = semitone + 64`
(**`10`..`70`**).

```text
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 40 F7 # Semitone +0
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
```

**Key Follow** (`1F`): **−64..+63** → `stored = ui + 64`
(**`00`..`7F`**). Panel **Norm** is expected at **+32** → **`60`**.

```text
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 40 F7 # Key Follow 0
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
```

**Balance** (`21`): same oscillator balance encoding as Osc 1 Classic.

```text
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100 %
F0 00 20 33 01 00 70 40 21 40 F7 # Balance 0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100 %
```

**Detune** (`1A`): **0..127** → `stored = lcd`.

```text
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
```

**FM Mode** (`71`/`22`): Page B enum (not Page A).

| LCD          | `<value>` |
| ------------ | --------- |
| Pos Triangle | `00`      |
| Triangle     | `01`      |
| Wave         | `02`      |
| Noise        | `03`      |
| In L         | `04`      |
| In L+R       | `05`      |
| In R         | `06`      |

```text
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode Pos Triangle
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode Triangle
F0 00 20 33 01 00 71 40 22 02 F7 # FM Mode Wave
F0 00 20 33 01 00 71 40 22 03 F7 # FM Mode Noise
F0 00 20 33 01 00 71 40 22 04 F7 # FM Mode In L
F0 00 20 33 01 00 71 40 22 05 F7 # FM Mode In L+R
F0 00 20 33 01 00 71 40 22 06 F7 # FM Mode In R
```

**FM Amount / Sync Frequency** (`1B`): panel label depends on **Sync** (`1C`).

| **Sync** | Panel control      | Encoding                                             |
| -------- | ------------------ | ---------------------------------------------------- |
| Off      | **FM Amount**      | **0.0..100.0 %** → `stored = round(pct × 127 / 100)` |
| On       | **Sync Frequency** | **0..127** → `stored = lcd`                          |

```text
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0 % (Sync Off)
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 100.0 % (Sync Off)
F0 00 20 33 01 00 70 40 1B 00 F7 # Sync Frequency 0 (Sync On)
F0 00 20 33 01 00 70 40 1B 7F F7 # Sync Frequency 127 (Sync On)
```

**FilterEnv>Pitch** (`1D`): panel **−100.0..+100.0 %**, wire **`00..7F`**.

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh: pct = +100.0 %
```

```text
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 40 F7 # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
```

Button-step anchors:

```text
01h -> −98.4 %
10h -> −75.0 %
20h -> −50.0 %
30h -> −25.0 %
3Fh -> −1.6 %
41h -> +1.6 %
50h -> +25.0 %
60h -> +50.0 %
70h -> +75.0 %
77h -> +85.9 %
78h -> +87.5 %
79h -> +89.1 %
7Ah -> +90.6 %
7Bh -> +92.2 %
7Ch -> +93.8 %
7Dh -> +95.3 %
7Eh -> +96.9 %
7Fh -> +100.0 %
```

**FilterEnv>FM / FilterEnv>Sync** (`1E`): one wire slot; LCD relabels with
**Sync**
(same pattern as **`1B`**). Panel **−100.0..+100.0 %** in both cases — same
curve
as **FilterEnv>Pitch** (`1D`). | **Sync** | Panel control |
| -------- |
| Off | **FilterEnv>FM** |
| On | **FilterEnv>Sync** |

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh: pct = +100.0 %
```

```text
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM or FilterEnv>Sync −100.0 %
F0 00 20 33 01 00 70 40 1E 40 F7 # FilterEnv>FM or FilterEnv>Sync 0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM or FilterEnv>Sync +100.0 %
```

**Sync** (`1C`): boolean toggle.

```text
```

### Oscillator 2 — Hypersaw

**Mode `<value>` = `01`**. Page A **`0x16`** = **Density** here
(Classic uses the same index for **Shape**); **`0x17`** = **Local Detune**
(Classic uses the same index for **Pulse Width**).

| Control         | `cmd` | `param` | Encoding                                           |
| --------------- | ----- | ------- | -------------------------------------------------- |
| Density         | `70`  | `16`    | **1.0..9.0**; same curve as Osc 1 Hypersaw Density |
| Local Detune    | `70`  | `17`    | **0..127** → `stored = lcd`                        |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                              |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`                        |
| Sync Frequency  | `70`  | `1B`    | **0..127** when **Sync On**; `stored = lcd`        |
| Sync            | `70`  | `1C`    | Off **`00`** / On **`01`**                         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch              |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                              |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                              |

**Density** (`16` in Hypersaw only): same Page A index as Osc 2 Classic
**Shape** — mirror of Osc 1 (**`11`** there). **1.0..9.0**, +1 wire per detent
**`00`–`7F`**:

```text
internal = 1 + stored × 8 / 127 # 00 → 1.0, 7F → 9.0
lcd ≈ round(1 + (internal − 1) × (stored / 127), 0.1)
```

Full **wire → LCD** map: [parameter-options.md — Osc 1 Hypersaw
Density LCD](../../reference/parameter-options.md#osc-1-hypersaw--density--lcd) (same panel
curve).

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Density 1.0
F0 00 20 33 01 00 70 40 16 7F F7 # Density 9.0
```

**Local Detune** (`17` in Hypersaw only): same Page A index as Classic **Pulse
Width** — only interpret **`17`** with **Mode `01`**. **0..127** →
**`stored = lcd`**.

```text
F0 00 20 33 01 00 70 40 17 00 F7 # Local Detune 0
F0 00 20 33 01 00 70 40 17 7F F7 # Local Detune 127
```

**Sync** (`1C`):

| LCD | `<value>` |
| --- | --------- |
| Off | `00`      |
| On  | `01`      |

```text
```

**Sync Frequency** (`1B`, when **Sync On**): **0..127** → `stored = lcd`
(hardware sweep **`00`–`7F`**).

```text
F0 00 20 33 01 00 70 40 1B 00 F7 # Sync Frequency 0
F0 00 20 33 01 00 70 40 1B 7F F7 # Sync Frequency 127
```

**Panel note:** **`1E` (FilterEnv>FM / FilterEnv>Sync)** is **Classic-only** on
Osc 2 — not shown in **Hypersaw** mode, even with **Sync On**. (Osc 1 Hypersaw
may still expose **FilterEnv>Sync** on **`1E`** when **Sync On** — see
[Oscillator 1 — Hypersaw](#oscillator-1--hypersaw).)

```text
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 40 F7 # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
```

### Oscillator 2 — Wavetable

**Mode `<value>` = `02`**. **Sub-menus:** **1–3** (panel layout). Page A
**`0x16`** = **Index** (Classic **Shape** / Hypersaw **Density** share this
index); **`0x18`** = **Wavetable** select.

| Control         | `cmd` | `param` | Encoding                             |
| --------------- | ----- | ------- | ------------------------------------ |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`          |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`          |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`    |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`    |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %** — see Classic |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`          |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only      |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`          |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula   |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula   |

**Index** (`16`): **`stored = lcd`** (**`00`–`7F`**).

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
```

**Wavetable** (`18`): **`stored`** = table index **`00`–`63`**. Names match
[parameter-options.md — Wavetable
Names](../../reference/parameter-options.md#wavetable-names) (**Sine** → **Domina7rix**).

```text
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
```

**Interpolation** (`6E`/`40`): part-buffer byte (not Page A). **`stored =
lcd`**.

```text
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
```

**Semitone** (`19`), **Key Follow** (`1F`), **Balance** (`21`) — same encodings
as [Osc 2 Classic](#oscillator-2--classic) (re-swept in mode **`02`**).

```text
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 40 F7 # Semitone +0
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
```

**Detune** (`1A`), **FM Amount** (`1B`): **`stored = lcd`** (**`00`–`7F`**).

```text
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
```

**FM Mode** (`71`/`22`): Page B — **only two** options in Wavetable mode (not
the seven **Classic** FM sources on the same param):

| LCD      | `<value>` |
| -------- | --------- |
| FreqMod  | `00`      |
| PhaseMod | `01`      |

```text
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
```

**FilterEnv>Pitch** (`1D`), **FilterEnv>FM** (`1E`): **−100.0 %..+100.0 %** —
same formula as Osc 2 Classic **FilterEnv>Pitch** / **FilterEnv>FM** (`1D` /
`1E`).

```text
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

### Oscillator 2 — Wavetable PWM

**Mode `<value>` = `03`**. Panel label **Wave PWM**. **Sub-menus:** **1–3**.
Same index/wavetable pattern as [Osc 2 Wavetable](#oscillator-2--wavetable);
adds **Pulse Width** on Page A **`0x17`** and **Local Detune** on part-buffer
**`0x3F`**.

**`0x17` is mode-dependent:** Classic **Pulse Width** (**50.0 %..100 %** when
Shape ≥ `40`), Hypersaw **Local Detune** (**0..127**), Wave PWM **Pulse Width**
(**0..127**).

| Control         | `cmd` | `param` | Encoding                           |
| --------------- | ----- | ------- | ---------------------------------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`        |
| Wavetable       | `70`  | `18`    | **`00`–`63`**; Sine..Domina7rix    |
| Pulse Width     | `70`  | `17`    | **0..127** → `stored = lcd`        |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`        |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`        |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`  |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`  |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %**             |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`        |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only    |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`        |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula |

**Index**, **Wavetable** — same as Osc 2 Wavetable (**`16`**, **`18`**).

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
```

**Pulse Width** (`17` in Wave PWM only): **`stored = lcd`** — not the Classic
**50.0 %..100 %** curve.

```text
F0 00 20 33 01 00 70 40 17 00 F7 # Pulse Width 0
F0 00 20 33 01 00 70 40 17 7F F7 # Pulse Width 127
```

**Interpolation** (`6E`/`40`), **Local Detune** (`6E`/`3F`): part-buffer;
**`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
F0 00 20 33 01 00 6E 40 3F 00 F7 # Local Detune 0
F0 00 20 33 01 00 6E 40 3F 7F F7 # Local Detune 127
```

**Semitone**, **Key Follow**, **Balance**, **Detune**, **FM Amount**,
**FilterEnv>Pitch**, **FilterEnv>FM** — same encodings as Osc 2 Wavetable /
Classic (re-swept in mode **`03`**).

```text
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

### Oscillator 2 — Grain Simple

**Mode `<value>` = `04`**. **Sub-menus:** **1–3**. Same index/wavetable pattern
as [Osc 2 Wavetable](#oscillator-2--wavetable); adds **F-Shift** on
part-buffer **`0x3E`** (Osc 1 Grain Simple uses **`6E`/`2A`**).

| Control         | `cmd` | `param` | Encoding                           |
| --------------- | ----- | ------- | ---------------------------------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`        |
| Wavetable       | `70`  | `18`    | **`00`–`63`**; Sine..Domina7rix    |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`  |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`        |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`  |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`  |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %**             |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`        |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only    |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`        |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula |

**Index**, **Wavetable** — same as Osc 2 Wavetable.

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
```

**F-Shift** (`6E`/`3E`): **−64..+63** → `stored = ui + 64` (**`00`..`7F`**).

```text
F0 00 20 33 01 00 6E 40 3E 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 3E 40 F7 # F-Shift +0
F0 00 20 33 01 00 6E 40 3E 7F F7 # F-Shift +63
```

**Interpolation** (`6E`/`40`): **`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
```

**Semitone**, **Key Follow**, **Balance**, **Detune**, **FM Mode**, **FM
Amount**, **FilterEnv>Pitch**, **FilterEnv>FM** — same encodings as Osc 2
Wavetable (re-swept in mode **`04`**).

```text
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

### Oscillator 2 — Grain Complex

**Mode `<value>` = `05`**. **Sub-menus:** **1–4**. Same as
[Osc 2 Grain Simple](#oscillator-2--grain-simple) plus **F-Spread** on
part-buffer **`0x39`** and **Local Detune** on **`0x3F`** (Osc 1 uses
**`6E`/`25`** and **`6E`/`2B`**).

| Control         | `cmd` | `param` | Encoding                           |
| --------------- | ----- | ------- | ---------------------------------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`        |
| Wavetable       | `70`  | `18`    | **`00`–`63`**; Sine..Domina7rix    |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`  |
| F-Spread        | `6E`  | `39`    | **0..127** → `stored = lcd`        |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`        |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`        |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`  |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`  |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %**             |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`        |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only    |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`        |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula |

**Index**, **Wavetable**, **F-Shift** — same as Grain Simple.

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
F0 00 20 33 01 00 6E 40 3E 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 3E 7F F7 # F-Shift +63
```

**F-Spread** (`6E`/`39`), **Local Detune** (`6E`/`3F`): Grain Complex only.
**`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 40 39 00 F7 # F-Spread 0
F0 00 20 33 01 00 6E 40 39 7F F7 # F-Spread 127
F0 00 20 33 01 00 6E 40 3F 00 F7 # Local Detune 0
F0 00 20 33 01 00 6E 40 3F 7F F7 # Local Detune 127
```

**Interpolation** (`6E`/`40`) and shared Page A / Page B controls — same as
Grain Simple / Wavetable (re-swept in mode **`05`**).

```text
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

### Oscillator 2 — Formant Simple

**Mode `<value>` = `06`**. **Sub-menus:** **1–3**. Same panel layout and wire
map as [Osc 2 Grain Simple](#oscillator-2--grain-simple) — no **F-Spread** or
**Local Detune** (those appear in Formant Complex only).

| Control         | `cmd` | `param` | Encoding                           |
| --------------- | ----- | ------- | ---------------------------------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`        |
| Wavetable       | `70`  | `18`    | **`00`–`63`**; Sine..Domina7rix    |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`  |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`        |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`  |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`  |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %**             |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`        |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only    |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`        |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula |

Same SysEx examples as Grain Simple — re-swept in mode **`06`**:

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
F0 00 20 33 01 00 6E 40 3E 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 3E 7F F7 # F-Shift +63
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

### Oscillator 2 — Formant Complex

**Mode `<value>` = `07`**. **Sub-menus:** **1–4**. Same panel layout and wire
map as [Osc 2 Grain Complex](#oscillator-2--grain-complex) — adds **F-Spread**
(`6E`/`39`) and **Local Detune** (`6E`/`3F`) to the Formant Simple set.

| Control         | `cmd` | `param` | Encoding                           |
| --------------- | ----- | ------- | ---------------------------------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`        |
| Wavetable       | `70`  | `18`    | **`00`–`63`**; Sine..Domina7rix    |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`  |
| F-Spread        | `6E`  | `39`    | **0..127** → `stored = lcd`        |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`        |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`        |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`  |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`  |
| Balance         | `70`  | `21`    | **−100.0 %..+100.0 %**             |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`        |
| FM Mode         | `71`  | `22`    | **FreqMod** / **PhaseMod** only    |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`        |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %** — Classic formula |
| FilterEnv>FM    | `70`  | `1E`    | **−100..+100 %** — Classic formula |

Same SysEx examples as Grain Complex — re-swept in mode **`07`**:

```text
F0 00 20 33 01 00 70 40 16 00 F7 # Index 0
F0 00 20 33 01 00 70 40 16 7F F7 # Index 127
F0 00 20 33 01 00 70 40 18 00 F7 # Wavetable Sine
F0 00 20 33 01 00 70 40 18 63 F7 # Wavetable Domina7rix
F0 00 20 33 01 00 6E 40 3E 00 F7 # F-Shift −64
F0 00 20 33 01 00 6E 40 3E 7F F7 # F-Shift +63
F0 00 20 33 01 00 6E 40 39 00 F7 # F-Spread 0
F0 00 20 33 01 00 6E 40 39 7F F7 # F-Spread 127
F0 00 20 33 01 00 6E 40 3F 00 F7 # Local Detune 0
F0 00 20 33 01 00 6E 40 3F 7F F7 # Local Detune 127
F0 00 20 33 01 00 6E 40 40 00 F7 # Interpolation 0
F0 00 20 33 01 00 6E 40 40 7F F7 # Interpolation 127
F0 00 20 33 01 00 70 40 19 10 F7 # Semitone −48
F0 00 20 33 01 00 70 40 19 70 F7 # Semitone +48
F0 00 20 33 01 00 70 40 1F 00 F7 # Key Follow −64
F0 00 20 33 01 00 70 40 1F 7F F7 # Key Follow +63
F0 00 20 33 01 00 70 40 21 00 F7 # Balance −100.0 %
F0 00 20 33 01 00 70 40 21 7F F7 # Balance +100.0 %
F0 00 20 33 01 00 70 40 1A 00 F7 # Detune 0
F0 00 20 33 01 00 70 40 1A 7F F7 # Detune 127
F0 00 20 33 01 00 71 40 22 00 F7 # FM Mode FreqMod
F0 00 20 33 01 00 71 40 22 01 F7 # FM Mode PhaseMod
F0 00 20 33 01 00 70 40 1B 00 F7 # FM Amount 0
F0 00 20 33 01 00 70 40 1B 7F F7 # FM Amount 127
F0 00 20 33 01 00 70 40 1D 00 F7 # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 40 1D 7F F7 # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 40 1E 00 F7 # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 40 1E 7F F7 # FilterEnv>FM +100.0 %
```

**Oscillator 2** — all eight modes documented above.

### Oscillator 3

**Mode/Wave** (`71`/`29`): enum. Values **`06`–`43`** are the Wave
choices **Wave 3** through **Wave 64**:

```text
stored = wave_number + 3 # Wave 3 -> 06, Wave 64 -> 43
wave_number = stored - 3 # for stored 06h..43h
```

| LCD             | `<value>` |
| --------------- | --------- |
| Off             | `00`      |
| Slave           | `01`      |
| Saw             | `02`      |
| Pulse           | `03`      |
| Sine            | `04`      |
| Triangle        | `05`      |
| Wave 3          | `06`      |
| Wave 4          | `07`      |
| Wave 5..Wave 64 | `08`–`43` |

```text
F0 00 20 33 01 00 71 40 29 00 F7 # Oscillator 3 Mode/Wave Off
F0 00 20 33 01 00 71 40 29 01 F7 # Oscillator 3 Mode/Wave Slave
F0 00 20 33 01 00 71 40 29 02 F7 # Oscillator 3 Mode/Wave Saw
F0 00 20 33 01 00 71 40 29 03 F7 # Oscillator 3 Mode/Wave Pulse
F0 00 20 33 01 00 71 40 29 04 F7 # Oscillator 3 Mode/Wave Sine
F0 00 20 33 01 00 71 40 29 05 F7 # Oscillator 3 Mode/Wave Triangle
F0 00 20 33 01 00 71 40 29 06 F7 # Oscillator 3 Mode/Wave Wave 3
F0 00 20 33 01 00 71 40 29 43 F7 # Oscillator 3 Mode/Wave Wave 64
```

**Visible controls by Mode/Wave:**

| Mode/Wave             | Controls shown           |
| --------------------- | ------------------------ |
| Off                   | none                     |
| Slave                 | none                     |
| Saw / Pulse / Sine    | Semitone, Volume, Detune |
| Triangle / Wave 3..64 | Semitone, Volume, Detune |

For **Saw** through **Wave 64** (`02`–`43`), these controls share the same
Page B parameter IDs:

| Control  | `cmd` | `param` | Encoding                          |
| -------- | ----- | ------- | --------------------------------- |
| Semitone | `71`  | `2B`    | **−48..+48** → `stored = ui + 64` |
| Volume   | `71`  | `2A`    | **0..127** → `stored = lcd`       |
| Detune   | `71`  | `2C`    | **0..−127** → `stored = −ui`      |

```text
F0 00 20 33 01 00 71 40 2B 10 F7 # Oscillator 3 Semitone −48
F0 00 20 33 01 00 71 40 2B 40 F7 # Oscillator 3 Semitone +0
F0 00 20 33 01 00 71 40 2B 70 F7 # Oscillator 3 Semitone +48
F0 00 20 33 01 00 71 40 2A 00 F7 # Oscillator 3 Volume 0
F0 00 20 33 01 00 71 40 2A 7F F7 # Oscillator 3 Volume 127
F0 00 20 33 01 00 71 40 2C 00 F7 # Oscillator 3 Detune 0
F0 00 20 33 01 00 71 40 2C 7F F7 # Oscillator 3 Detune −127
```

## Noise

**Oscillators → Noise**. Page A parameters.

### Noise Volume

**Live edit:** `cmd=0x70`, param `0x25` (CC 37).

Panel **Off**, then **1..127**; wire matches the numeric value (**`00`** = Off).

| LCD | `<value>` |
| --- | --------- |
| Off | `00`      |
| 1   | `01`      |
| 127 | `7F`      |

```text
stored = lcd # 1..127; 00 = Off
```

```text
F0 00 20 33 01 00 70 40 25 00 F7 # Noise Volume Off
F0 00 20 33 01 00 70 40 25 01 F7 # Noise Volume 1
F0 00 20 33 01 00 70 40 25 7F F7 # Noise Volume 127
```

### Noise Color

**Live edit:** `cmd=0x70`, param `0x27`.

Panel **−64..+63** → **`stored = ui + 64`** (same bipolar pattern as
[Key Follow](#oscillator-2--classic) / [Osc Volume](#osc-volume)).

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| 0   | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 70 40 27 00 F7 # Noise Color −64
F0 00 20 33 01 00 70 40 27 40 F7 # Noise Color 0
F0 00 20 33 01 00 70 40 27 7F F7 # Noise Color +63
```

## Ring Modulator

**Oscillators → Ring Modulator**. Page A param **`0x32`** (not CC **38** =
**`0x26`** — that was an inventory typo).

### Ring Modulator Volume

**Live edit:** `cmd=0x70`, param `0x32` (CC 38).

Panel **Off**, then **1..127**; wire matches the numeric value (**`00`** = Off).
Same encoding as [Noise Volume](#noise-volume).

**`<part>`:** Multi Part *n* → **`0x00`–`0x0F`**; Single edit buffer →
**`0x40`**. Param **`0x32`** is unchanged — only the part index switches with
the active edit context (panel-verified).

| LCD | `<value>` |
| --- | --------- |
| Off | `00`      |
| 1   | `01`      |
| 2   | `02`      |
| 127 | `7F`      |

```text
stored = lcd # 1..127; 00 = Off
```

```text
F0 00 20 33 01 00 70 01 32 00 F7 # Ring Modulator Volume Off (Multi Part 2)
F0 00 20 33 01 00 70 40 32 00 F7 # Ring Modulator Volume Off
F0 00 20 33 01 00 70 40 32 01 F7 # Ring Modulator Volume 1
F0 00 20 33 01 00 70 40 32 7F F7 # Ring Modulator Volume 127
```

## Sub Oscillator

**Oscillators → Sub Oscillator**. Page A **`0x22`**
and **`0x23`** (Shape, CC **35**). **Not** Page B **`71` / `0x23`** (that is
[Phase Init](single.md#phase-init)).

### Sub Oscillator Volume

**Live edit:** `cmd=0x70`, param `0x22` (CC 34).

Panel **0..127**; wire matches the numeric value (**`00`** = **0**, not “Off”).

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
stored = lcd # 0..127
```

```text
F0 00 20 33 01 00 70 40 22 00 F7 # Sub Oscillator Volume 0
F0 00 20 33 01 00 70 40 22 7F F7 # Sub Oscillator Volume 127
```

Also available as **MIDI CC 34** when Page A = **Controller Data**.

### Sub Oscillator Shape

**Live edit:** `cmd=0x70`, param `0x23` (CC 35).

Two shapes only; no further values on the panel.

| LCD      | `<value>` |
| -------- | --------- |
| Square   | `00`      |
| Triangle | `01`      |

```text
F0 00 20 33 01 00 70 40 23 00 F7 # Shape Square
F0 00 20 33 01 00 70 40 23 01 F7 # Shape Triangle
```

### Punch Intensity

**Live edit:** `cmd=0x71`, param `0x24`.

**Oscillators → Punch → Punch Intensity**. Page B param **`0x24`**. Panel **0.0..100.0 %** — **not** the same byte as
[Osc Volume](#osc-volume) (`cmd=0x70`). **`<part>`:** Single edit buffer
**`0x40`** (Multi Part *n* → **`0x00`–`0x0F`**).

```text
for 00h..7Eh: pct = stored × 100 / 128
for 7Fh: pct = 100.0 %
stored = round(pct × 128 / 100) # cap at 7Fh for 100.0 %
```

Eighth-step anchors (hardware LCD, 2026-06):

| Wire | LCD %  | Wire | LCD %   |
| ---- | ------ | ---- | ------- |
| `00` | 0.0 %  | `20` | 25.0 %  |
| `03` | 2.3 %  | `30` | 37.5 %  |
| `09` | 7.0 %  | `40` | 50.0 %  |
| `10` | 12.5 % | `50` | 62.5 %  |
| `11` | 13.4 % | `60` | 75.0 %  |
| `1C` | 21.9 % | `70` | 87.5 %  |
| `1A` | 20.3 % | `78` | 93.8 %  |
| `7E` | 98.4 % | `7F` | 100.0 % |

**LCD quirk:** at **`04`** the panel showed **3.9 %** (expected **3.1 %** from
`× 100 / 128`); at **`05`** it showed **3.1 %** (expected **3.9 %**) — labels
appear **swapped** for that pair only; wire bytes still follow the `/128` curve.

```text
F0 00 20 33 01 00 71 40 24 00 F7 # Punch 0.0 %
F0 00 20 33 01 00 71 40 24 40 F7 # Punch 50.0 %
F0 00 20 33 01 00 71 40 24 7F F7 # Punch 100.0 %
```

### Osc Volume

**Live edit:** `cmd=0x70`, param `0x24`.

**Oscillators → EDIT → Common → Osc Volume**. Same parameter as
[Saturation — Osc Volume](filters.md#saturation--osc-volume):
panel **−64..+63**, wire **`stored = ui + 64`**.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| 0   | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 70 40 24 00 F7 # Osc Volume −64
F0 00 20 33 01 00 70 40 24 40 F7 # Osc Volume 0
F0 00 20 33 01 00 70 40 24 7F F7 # Osc Volume +63
```

### Mixer (Oscillators menu)

### Oscillator Section Volume

**Live edit:** `cmd=0x71`, param `0x7F`.

**Oscillators → Mixer → Oscillator Section Volume** (main osc mixer level).
Same **`71`/`7F`** wire as [SELECT (`71`/`7F`)](#select-717f) — volume
uses bipolar **`stored = ui + 64`**, not index **`00`–`02`**. Same bipolar
range as [Saturation — Osc
Volume](filters.md#saturation--osc-volume)
but edited via **Page B** SysEx here, not **`70` / `24`**.

| Item                    | Value                                                 |
| ----------------------- | ----------------------------------------------------- |
| Message (last in burst) | `F0 00 20 33 01 00 71 40 7F 00 F7`                    |
| Scope byte              | **`0x40`** Single edit buffer (Multi Part 1 → `0x00`) |
| Param ID                | `0x7F`                                                |
| Dump offset             | **`0x107`** (Single edit buffer **`30 00 40`**)       |
| Value encoding          | Bipolar **`stored = ui + 64`** (`−64` → `0x00`)       |

```text
F0 00 20 33 01 00 71 40 7F 00 F7 # Oscillator Section Volume −64
```

**Sub Oscillator Volume** — see [Sub Oscillator](#sub-oscillator) (`70` / `0x22`
or CC 34).

## Unison

**Edit Single → Unison** — top-level **Edit Single** sub-menu. **Not** under
**EDIT OSC** (Osc 1 / Osc 2 / Ring Mod / Noise / Common). No oscillator mode
must be enabled first: set **Voices** to **Off** or **Twin**–**8** directly from
this menu.

Stacks **extra detuned copies** of the whole oscillator section for the patch
(not per-osc **Sync** on Osc 2). Live edit uses **`cmd=0x6F`**, params
**`0x78`–`0x7B`**. Older docs wrongly listed **`cmd=0x70` / `0x61`–`0x64`**
(CC numbers mistaken for param bytes — same class of error as Ring Mod
**`0x26`** vs **`0x32`**).

**`<part>`:** Multi Part *n* → **`0x00`–`0x0F`**; Single edit buffer →
**`0x40`**.

**Single Dump offsets** (Single edit buffer **`30 00 40`**):
**`0x201`** Voices · **`0x202`** Detune · **`0x203`** Pan Spread ·
**`0x204`** LFO Phase.

### Voices

**Live edit:** `cmd=0x6F`, param `0x78`.

Panel **Voices**.

| LCD  | `<value>` |
| ---- | --------- |
| Off  | `00`      |
| Twin | `01`      |
| 3    | `02`      |
| 4    | `03`      |
| 5    | `04`      |
| 6    | `05`      |
| 7    | `06`      |
| 8    | `07`      |

```text
F0 00 20 33 01 00 6F 40 78 00 F7 # Voices Off
F0 00 20 33 01 00 6F 40 78 07 F7 # Voices 8
```

When **Voices** is **Twin** (`01`) or higher, **Detune** appears on the panel.
When **Off**, **Detune** is hidden (wire value may still be stored).

### Detune

**Live edit:** `cmd=0x6F`, param `0x79`.

**0..127** → `stored = lcd`. Panel visible only when **Voices** ≥ **Twin**.

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 6F 40 79 00 F7 # Detune 0
F0 00 20 33 01 00 6F 40 79 7F F7 # Detune 127
```

### Pan Spread

**Live edit:** `cmd=0x6F`, param `0x7A`.

Panel **0.0..100.0 %** — always visible (even when **Voices** = **Off**).

```text
for 00h..7Eh: pct = stored × 100 / 128
for 7Fh: pct = 100.0 %
```

```text
F0 00 20 33 01 00 6F 40 7A 00 F7 # Pan Spread 0.0 %
F0 00 20 33 01 00 6F 40 7A 7F F7 # Pan Spread 100.0 %
```

**Not** Filter Common [Pan Spread](filters.md#pan-spread) (`6E`/`7A` under Split routing).

### LFO Phase Offset

**Live edit:** `cmd=0x6F`, param `0x7B`.

Panel **Unison LFO Phase**. **−64..+63** → `stored = ui + 64`.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| 0   | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6F 40 7B 00 F7 # LFO Phase −64
F0 00 20 33 01 00 6F 40 7B 40 F7 # LFO Phase 0
F0 00 20 33 01 00 6F 40 7B 7F F7 # LFO Phase +63
```
