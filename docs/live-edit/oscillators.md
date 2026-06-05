# Oscillators

Edit Single — **Oscillators** (Osc 1–3), **Noise**, **Ring Modulator**, **Sub
Oscillator**, mixer levels.

Part of [Live Edit](README.md). Enumerated options:
[parameter-options.md](../parameter-options.md).
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

## Panel reference

**LCD:** **OSCILLATORS** → **Oscillator 1** / **2** / **Common** / **Mixer**.

Parameters are a **nested tree**: **Mode** → (for Classic) **Shape** →
controls on sub-menus **1–2** (Classic), **1–3** (Wavetable, Grain Simple,
Formant Simple), or **1–4** (Grain Complex, Formant Complex). Document only
rows that appear on the panel for the active Mode/Shape.

Capture path: **`Mode` / `Shape` / `Control` → LCD value**. Use **+/−** when
possible. Knob sweeps: use the **last** SysEx line. Master inventory:
[single-dump.md — Oscillators](../dumps/single.md#oscillators).

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

| LCD (Mode)      | `cmd` | `param` | `<value>` | Confirmed |
| --------------- | ----- | ------- | --------- | --------- |
| Classic         | `6E`  | `1E`    | `00`      | ✓         |
| Hypersaw        | `6E`  | `1E`    | `01`      | ✓         |
| Wavetable       | `6E`  | `1E`    | `02`      | ✓         |
| Wavetable PWM   | `6E`  | `1E`    | `03`      | ✓         |
| Grain Simple    | `6E`  | `1E`    | `04`      | ✓         |
| Grain Complex   | `6E`  | `1E`    | `05`      | ✓         |
| Formant Simple  | `6E`  | `1E`    | `06`      | ✓         |
| Formant Complex | `6E`  | `1E`    | `07`      | ✓         |

Modes **`02`–`07`** — fill LCD labels when stepped with **+/−**. Param
**`0x1E`**
on **`0x6E`** only (not **`0x71`** Filter 1 env polarity).

```text
F0 00 20 33 01 00 6E 00 1E 00 F7   # Mode Classic
F0 00 20 33 01 00 6E 00 1E 01 F7   # Mode Hypersaw
F0 00 20 33 01 00 6E 00 1E 02 F7   # Mode Wavetable
F0 00 20 33 01 00 6E 00 1E 03 F7   # Mode Wavetable PWM (panel: Wave PWM)
F0 00 20 33 01 00 6E 00 1E 04 F7   # Mode Grain Simple
F0 00 20 33 01 00 6E 00 1E 05 F7   # Mode Grain Complex
F0 00 20 33 01 00 6E 00 1E 06 F7   # Mode Formant Simple
F0 00 20 33 01 00 6E 00 1E 07 F7   # Mode Formant Complex
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
then **saw/pulse** blend. **Pulse Width** (`12`, WAF80) appears on the panel
when
**Shape ≥ `40`** (Sawtooth and Saw>Pulse — not at Spectral Wave `00`).
**Pulse Width** **`70`/`12`** — formulas in
[Pulse Width](#pulse-width-shape--sawtooth); LCD lookup table in
[parameter-options.md](../parameter-options.md#osc-1-classic--pulse-width-lcd).

| LCD                | `<value>` | Confirmed |
| ------------------ | --------- | --------- |
| Sawtooth           | `40`      | ✓         |
| Saw>Pulse 2 %      | `41`      | ✓         |
| Saw>Pulse 3 %      | `42`      | ✓         |
| Saw>Pulse 5 %      | `43`      | ✓         |
| Saw>Pulse 6 %      | `44`      | ✓         |
| Saw>Pulse 2 %…98 % | `41`–`7E` | ✓ (table) |
| Pulse              | `7F`      | ✓         |

**Saw/Pulse mix** uses **hex** bytes **`0x44`–`0x7E`** (+1 per **+/−**).
Easy mistake: the log’s trailing **`dec`** is the **decimal equivalent** of
that hex byte (`0x44` → 68 dec, `0x5A` → 90 dec) — not a separate index.
A label list keyed as decimal **44–66** was wrong; the wire run was
**hex `44`–`5A`** for this sweep.

**Read the log:**

```text
… 70 00 11 5A dec
           ^^      ← document **0x5A** (not decimal 90, not “66”)
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

| Control     | `cmd` | `param` | Encoding / notes                                                          | Confirmed |
| ----------- | ----- | ------- | ------------------------------------------------------------------------- | --------- |
| Shape       | `70`  | `11`    | Mix; `00` = pure wave                                                     | ✓         |
| Wave Select | `70`  | `13`    | **`00`–`3F`**: Sine, Triangle, Wave 3…Wave 64                             | ✓         |
| Pulsewidth  | —     | —       | Panel hidden at **`00`**; see [Pulse Width](#pulse-width-shape--sawtooth) | —         |
| Semitone    | `70`  | `14`    | **−48..+48** → `stored = ui + 64`                                         | ✓         |
| Key Follow  | `70`  | `15`    | **−64..+63** → `stored = ui + 64`                                         | ✓         |
| Balance     | `70`  | `21`    | **−100..+100 %** → see [Balance](#balance-osc-1-classic)                  | ✓         |

**Menu 1** — **Norm** on Key Follow is a fixed **+32** (`60`) scale tick,
not per-patch default (store test: saved **−21** → `2B`, reload —
**Norm** still **+32**). **Menu 2** — report if any controls remain.

**Semitone** (`14`): **−48..+48** → `stored = semitone + 64` (**`10`..`70`**).

```text
F0 00 20 33 01 00 70 00 14 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 14 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 14 70 F7   # Semitone +48
```

**Key Follow** (`15`): **−64..+63** → `stored = ui + 64`
(**`00`..`7F`**). Panel **Norm** = **+32** → **`60`** (fixed scale
tick, not per-patch default).

```text
F0 00 20 33 01 00 70 00 15 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 15 40 F7   # Key Follow 0
F0 00 20 33 01 00 70 00 15 60 F7   # Key Follow Norm (+32)
F0 00 20 33 01 00 70 00 15 7F F7   # Key Follow +63
```

#### Balance (Osc 1 Classic)

**`cmd=0x70` `param=0x21`** — **−100.0 %..+100.0 %** (not Filter Balance
**`0x30`**).

```text
stored = round((pct + 100) × 127 / 200)
pct    = stored × 200 / 127 − 100
```

```text
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100.0 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance +0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100.0 %
```

#### Controls at Shape ≥ Sawtooth (`40`)

**Pulse Width** on the panel when **Shape ≥ `40`** (Sawtooth / Saw>Pulse /
Pulse).

#### Pulse Width (Shape ≥ Sawtooth)

| Control     | `cmd` | `param` | Confirmed |
| ----------- | ----- | ------- | --------- |
| Pulse Width | `70`  | `12`    | ✓         |

**Wire** (`stored` = **`00`–`7F`**, +1 per detent):

```text
pct = 50 + stored × 50 / 127
stored = round((pct − 50) × 127 / 50)    # clamp 00..7F
```

**LCD** (panel readout, **Shape ≥ `40`**): `lcd = round(pct + 0.4, 0.1)`.
Endpoints **`00`** / **`7F`** show **50.0 %** / **100 %** on the wire
values directly. Same label can appear on two detents. Partial **wire → LCD**
map:
[parameter-options.md — Osc 1 Pulse Width
LCD](../parameter-options.md#osc-1-classic--pulse-width-lcd).

```text
F0 00 20 33 01 00 70 00 12 00 F7   # min 50.0 %
F0 00 20 33 01 00 70 00 12 7F F7   # max 100 %
```

### Oscillator 1 — Hypersaw

**Mode `<value>` = `01`**. No **Shape** / **Wave Select** (Classic-only).
**Sub-menus:** **1–2**. Page A **`0x11`** = **Density** here (Classic uses
the same index for **Shape**).

| Control        | `cmd` | `param` | Encoding                                          | Confirmed |
| -------------- | ----- | ------- | ------------------------------------------------- | --------- |
| Density        | `70`  | `11`    | **1.0..9.0** — see below                          | ✓         |
| Local Detune   | `70`  | `12`    | **0..127** → `stored = lcd`                       | ✓         |
| Sync           | `70`  | `1C`    | Off **`00`** / On **`01`**                        | ✓         |
| Sync Frequency | `70`  | `1B`    | **0..127** when **Sync On**; `stored = lcd`       | ✓         |
| Semitone       | `70`  | `14`    | Same as [Classic](#oscillator-1--classic)         | ✓         |
| Key Follow     | `70`  | `15`    | Same as Classic                                   | ✓         |
| Balance        | `70`  | `21`    | Same as [Classic Balance](#balance-osc-1-classic) | ✓         |

**Density** (`11` in Hypersaw only): **1.0..9.0**, +1 wire per detent
**`00`–`7F`**.

```text
internal = 1 + stored × 8 / 127          # SysEx / engine (00 → 1.0, 7F → 9.0)
scale    = stored / 127
lcd      ≈ round(1 + (internal − 1) × scale, 0.1)
```

**LCD formula status:** `lcd ≈ round(1 + (internal − 1) × scale, 0.1)`
lands **`40`**, **`74`–`76`**, **`7B`**, **`7F`**. **`58`–`6C`**
often **~0.1–0.5 below** predicted; **`44`–`57`**, **`74`+** are within
**~0.1**. Duplicate labels appear on some detents (**`5C`/`5D`**,
**`67`/`68`**, **`77`/`78`**, etc.). Full **128**-entry map:
[parameter-options.md — Density
LCD](../parameter-options.md#osc-1-hypersaw--density-lcd).

**Do not** use `stored = round((lcd − 1) × 127 / 8)` from LCD alone
(e.g. LCD **3.0** → **`3F`**, not **`20`**).

```text
F0 00 20 33 01 00 70 00 11 00 F7   # Density 1.0
F0 00 20 33 01 00 70 00 11 3F F7   # Density 3.0 (LCD)
F0 00 20 33 01 00 70 00 11 7F F7   # Density 9.0
```

**Local Detune** (`12` in Hypersaw only): same Page A index as Classic
**Pulse Width** (**`12`** there is **50.0 %** … **100 %**). Only interpret
**`12`** with **Mode `01`**.

Panel **0..127** (unsigned, not bipolar). **Wire = LCD** (one detent per step
**`00`–`7F`**).

```text
stored = lcd    # 0..127
lcd    = stored
```

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 80  | `50`      | ✓         |

```text
F0 00 20 33 01 00 70 00 12 00 F7   # Local Detune 0
F0 00 20 33 01 00 70 00 12 50 F7   # Local Detune 80
F0 00 20 33 01 00 70 00 12 7F F7   # Local Detune 127 (max wire)
```

**Sync** (`1C` in Hypersaw): panel **Off** / **On**. WAF80 CC **28** lists
**Osc2 Sync** **0/1** — same wire pattern on Osc 1 here.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| Off | `00`      | ✓         |
| On  | `01`      | ✓         |

```text
F0 00 20 33 01 00 70 00 1C 00 F7   # Sync Off
F0 00 20 33 01 00 70 00 1C 01 F7   # Sync On
```

**Sync Frequency** (`1B`, conditional on **Sync On**): dump
**Oscillator 1+2 X-Sync Frequency**. Hidden when **Sync Off**. Panel
**0..127** — **`stored = lcd`** (same as **Local Detune**).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 64  | `40`      | ✓         |
| 127 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 70 00 1B 00 F7   # Sync Frequency 0
F0 00 20 33 01 00 70 00 1B 40 F7   # Sync Frequency 64
F0 00 20 33 01 00 70 00 1B 7F F7   # Sync Frequency 127
```

**FilterEnv>Sync** (`1E` when **Sync On**): same wire and **−100..+100 %**
curve as Osc 2 **FilterEnv>FM** / **FilterEnv>Sync** (see
[Oscillator 2 — Classic](#oscillator-2--classic)).

**Semitone**, **Key Follow**, **Balance** — same **`14` / `15` / `21`**
and encodings as Classic (verified in **Mode `01`** sweeps: Semitone
**`10`..`70`** → **−48..+48**, Key Follow **`00`..`7F`** → **−64..+63**,
Balance **`00`/`40`/`7F`** → **−100 % / 0 % / +100 %**).

### Oscillator 1 — Wavetable

**Mode `<value>` = `02`**. **Sub-menus:** **1–3**. Panel: **Index**,
**Wavetable**, **Interpolation**, **Semitone**, **Key Follow**, **Balance**
(no Classic **Shape** / Hypersaw **Density** / **Sync**).

| Control       | `cmd` | `param` | Encoding                                          | Confirmed |
| ------------- | ----- | ------- | ------------------------------------------------- | --------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`                       | ✓         |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (100 names); see below         | ✓         |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`                       | ✓         |
| Semitone      | `70`  | `14`    | Same as [Classic](#oscillator-1--classic)         | ✓†        |
| Key Follow    | `70`  | `15`    | Same as Classic                                   | ✓†        |
| Balance       | `70`  | `21`    | Same as [Classic Balance](#balance-osc-1-classic) | ✓†        |

† Panel present in Wavetable mode; encoding matches Classic (not re-swept in
mode **`02`**).

**Index** (`11` in Wavetable / Wave PWM): same Page A index as Classic
**Shape** / Hypersaw **Density**. **`stored = lcd`** (**`00`–`7F`**).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 127 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 70 00 11 00 F7   # Index 0
F0 00 20 33 01 00 70 00 11 7F F7   # Index 127
```

Stepped **`00`→`38`** (+1 per detent) then fast sweep to **`7F`** — no
anomalies vs **1:1** encoding.

**Wavetable** (`13` in Wavetable mode): same Page A index as Classic **Wave
Select**.
**`stored`** = wavetable index (**0**–**99** → **`00`–`63`**). Panel order
matches
[parameter-options.md — Wavetable
Names](../parameter-options.md#wavetable-names)
(hardware verified: full sweep **Sine** → **Domina7rix**).

| LCD             | `<value>` | Confirmed |
| --------------- | --------- | --------- |
| Sine (0)        | `00`      | ✓         |
| Domina7rix (99) | `63`      | ✓         |

```text
F0 00 20 33 01 00 70 00 13 00 F7   # Wavetable index 0 (Sine)
F0 00 20 33 01 00 70 00 13 63 F7   # Wavetable index 99 (Domina7rix)
```

**Interpolation** (`6E` / `2C`): **0..127**, **`stored = lcd`**. Uses
**`cmd=0x6E`**
(part buffer), not **`0x70`** Page A — same param index **`0x2C`** as [Filter 1
Envelope Amount](filters.md#filter-1-envelope-amount-cmd0x70-param-0x2c) on
**`0x70`**.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 127 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 6E 00 2C 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 2C 7F F7   # Interpolation 127
```

### Oscillator 1 — Wavetable PWM

**Mode `<value>` = `03`**. Panel label **Wave PWM**. **Sub-menus:** **1–3**.

| Control       | `cmd` | `param` | Encoding                                        | Confirmed |
| ------------- | ----- | ------- | ----------------------------------------------- | --------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd` (same as Wavetable) | ✓         |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names as Wavetable)    | ✓         |
| Pulse Width   | `70`  | `12`    | **0..127** → `stored = lcd`                     | ✓         |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd` (same as Wavetable) | ✓         |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`                     | ✓         |
| Semitone      | `70`  | `14`    | Same as Classic                                 | ✓†        |
| Key Follow    | `70`  | `15`    | Same as Classic                                 | ✓†        |
| Balance       | `70`  | `21`    | Same as Classic                                 | ✓†        |

† Assumed same as Classic / Hypersaw / Wavetable (panel match; not re-swept
in mode **`03`**).

**`0x12` is mode-dependent:** Classic **Pulse Width** (**50.0 %..100 %**),
Hypersaw
**Local Detune** (**`70`/`12`**, **0..127**), Wave PWM **Pulse Width**
(**`70`/`12`**, **0..127**).

**Pulse Width** (Wave PWM, `70`/`12`):

```text
F0 00 20 33 01 00 70 00 12 00 F7   # Pulse Width 0
F0 00 20 33 01 00 70 00 12 7F F7   # Pulse Width 127
```

**Local Detune** (Wave PWM only on **`6E`/`2B`** — not **`70`/`12`**; Hypersaw
uses
**`70`/`12`** for Local Detune):

```text
F0 00 20 33 01 00 6E 00 2B 00 F7   # Local Detune 0
F0 00 20 33 01 00 6E 00 2B 7F F7   # Local Detune 127
```

**Index**, **Wavetable**, **Interpolation** — same wire rules as
[Wavetable](#oscillator-1--wavetable) (reconfirmed in mode **`03`** sweeps).

### Oscillator 1 — Grain Simple

**Mode `<value>` = `04`**. **Sub-menus:** **1–3**. Panel: **Index**,
**Wavetable**,
**F-Shift**, **Interpolation**, **Semitone**, **Key Follow**, **Balance**.

| Control       | `cmd` | `param` | Encoding                                        | Confirmed |
| ------------- | ----- | ------- | ----------------------------------------------- | --------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd` (same as Wavetable) | ✓†        |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names)                 | ✓†        |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64`               | ✓         |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`                     | ✓         |
| Semitone      | `70`  | `14`    | Same as Classic                                 | ✓†        |
| Key Follow    | `70`  | `15`    | Same as Classic                                 | ✓†        |
| Balance       | `70`  | `21`    | Same as Classic                                 | ✓†        |

† Same wire/encoding as Wavetable; not re-swept in mode **`04`** (Wavetable
left on **Domina7rix** → **`13`/`63`**).

**F-Shift** (`6E`/`2A`): **−64..+63** → `stored = ui + 64`
(**`00`–`7F`**), same bipolar pattern as **Key Follow**. Same param index
**`0x2A`** as [Filter 1
Resonance](filters.md#filter-1-resonance-cmd0x70-param-0x2a)
on **`0x70`** — use **`cmd`** to disambiguate.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| −64 | `00`      | ✓         |
| +0  | `40`      | ✓         |
| +63 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 6E 00 2A 00 F7   # F-Shift −64
F0 00 20 33 01 00 6E 00 2A 40 F7   # F-Shift +0
F0 00 20 33 01 00 6E 00 2A 7F F7   # F-Shift +63
F0 00 20 33 01 00 6E 00 2C 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 2C 7F F7   # Interpolation 127
```

### Oscillator 1 — Grain Complex

**Mode `<value>` = `05`**. **Sub-menus:** **1–4**. Same as
[Grain Simple](#oscillator-1--grain-simple) plus **F-Spread** and **Local
Detune**.

| Control       | `cmd` | `param` | Encoding                                     | Confirmed |
| ------------- | ----- | ------- | -------------------------------------------- | --------- |
| Index         | `70`  | `11`    | Same as Wavetable / Grain Simple (assumed)   | —         |
| Wavetable     | `70`  | `13`    | Same enum as Wavetable (assumed)             | —         |
| F-Shift       | `6E`  | `2A`    | Same as Grain Simple; current **+63** = `7F` | ✓†        |
| F-Spread      | `6E`  | `25`    | **0..127** → `stored = lcd`                  | ✓         |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`                  | ✓         |
| Interpolation | `6E`  | `2C`    | Same as Grain Simple (assumed)               | —         |
| Semitone      | `70`  | `14`    | Same as Classic (assumed)                    | —         |
| Key Follow    | `70`  | `15`    | Same as Classic (assumed)                    | —         |
| Balance       | `70`  | `21`    | Same as Classic (assumed)                    | —         |

† **F-Shift** carried over while changing from Grain Simple; not re-swept in
mode **`05`**.

**F-Spread** (`6E`/`25`): newly visible in Grain Complex. Panel **0..127** —
**`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 00 25 00 F7   # F-Spread 0
F0 00 20 33 01 00 6E 00 25 7F F7   # F-Spread 127
```

**Local Detune** (`6E`/`2B`): same slot as Wave PWM **Local Detune**. Panel
**0..127** — **`stored = lcd`**.

```text
F0 00 20 33 01 00 6E 00 2B 00 F7   # Local Detune 0
F0 00 20 33 01 00 6E 00 2B 7F F7   # Local Detune 127
```

### Oscillator 1 — Formant Simple

**Mode `<value>` = `06`**. **Sub-menus:** **1–3**.

| Control       | `cmd` | `param` | Encoding                          | Confirmed |
| ------------- | ----- | ------- | --------------------------------- | --------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       | ✓         |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names)   | ✓         |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` | ✓         |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       | ✓         |
| Semitone      | `70`  | `14`    | Same as Classic                   | ✓         |
| Key Follow    | `70`  | `15`    | Same as Classic                   | ✓         |
| Balance       | `70`  | `21`    | Same as Classic                   | ✓         |

No **F-Spread** control in Formant Simple (unlike Grain Complex / Formant
Complex).
Sweeps in mode **`06`** showed only the controls above.

### Oscillator 1 — Formant Complex

**Mode `<value>` = `07`**. **Sub-menus:** **1–4**. Same as
[Formant Simple](#oscillator-1--formant-simple) plus **F-Spread** and
**Local Detune**.

| Control       | `cmd` | `param` | Encoding                          | Confirmed |
| ------------- | ----- | ------- | --------------------------------- | --------- |
| Index         | `70`  | `11`    | **0..127** → `stored = lcd`       | ✓         |
| Wavetable     | `70`  | `13`    | Enum **`00`–`63`** (same names)   | ✓         |
| F-Shift       | `6E`  | `2A`    | **−64..+63** → `stored = ui + 64` | ✓         |
| F-Spread      | `6E`  | `25`    | **0..127** → `stored = lcd`       | ✓         |
| Local Detune  | `6E`  | `2B`    | **0..127** → `stored = lcd`       | ✓         |
| Interpolation | `6E`  | `2C`    | **0..127** → `stored = lcd`       | ✓         |
| Semitone      | `70`  | `14`    | Same as Classic                   | ✓         |
| Key Follow    | `70`  | `15`    | Same as Classic                   | ✓         |
| Balance       | `70`  | `21`    | Same as Classic                   | ✓         |

Sweeps in mode **`07`** matched the same encodings as Grain Complex / Formant
Simple for all shared controls.

### Oscillator 2

Same Mode / Shape / table pattern as **Oscillator 1**, but Oscillator 2 uses a
different mode selector and shifted Page A parameter IDs.

### Oscillator 2 — Mode

| LCD (Mode)      | `cmd` | `param` | `<value>` | Confirmed |
| --------------- | ----- | ------- | --------- | --------- |
| Classic         | `6E`  | `23`    | `00`      | ✓         |
| Hypersaw        | `6E`  | `23`    | `01`      | ✓         |
| Wavetable       | `6E`  | `23`    | `02`      | ✓         |
| Wavetable PWM   | `6E`  | `23`    | `03`      | ✓         |
| Grain Simple    | `6E`  | `23`    |           |           |
| Grain Complex   | `6E`  | `23`    |           |           |
| Formant Simple  | `6E`  | `23`    |           |           |
| Formant Complex | `6E`  | `23`    |           |           |

```text
F0 00 20 33 01 00 6E 00 23 00 F7   # Osc 2 Mode Classic
F0 00 20 33 01 00 6E 00 23 01 F7   # Osc 2 Mode Hypersaw
F0 00 20 33 01 00 6E 00 23 02 F7   # Osc 2 Mode Wavetable
F0 00 20 33 01 00 6E 00 23 03 F7   # Osc 2 Mode Wavetable PWM
```

### Oscillator 2 — Classic

**Mode `<value>` = `00`**. Expected Page A IDs from WAF80: **Shape** `16`,
**Pulse Width** `17`, **Wave Select** `18`, **Semitone** `19`, **Detune** `1A`,
**FM Amount** `1B`, **Sync** `1C`, **FilterEnv>Pitch** `1D`,
**FilterEnv>FM** `1E`, **Key Follow** `1F`, **Balance** `21`. Confirm on
hardware before copying Osc 1 formulas.

| Control         | `cmd` | `param` | Encoding                                                                    | Confirmed |
| --------------- | ----- | ------- | --------------------------------------------------------------------------- | --------- |
| Shape           | `70`  | `16`    | Same Classic Shape table as Osc 1                                           | partial   |
| Pulse Width     | `70`  | `17`    | Shape-dependent; likely Classic PW                                          | —         |
| Wave Select     | `70`  | `18`    | **`00`–`3F`** enum; Sine = `00`                                             | partial   |
| Semitone        | `70`  | `19`    | **−48..+48** → `stored = ui + 64`                                           | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`                                                 | ✓         |
| FM Mode         | `71`  | `22`    | Enum; see below                                                             | partial   |
| FM Amount       | `70`  | `1B`    | **Sync Off:** **0.0..100.0 %**; **Sync On:** **Sync Frequency** **0..127**  | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | **−100..+100 %**; see formula below                                         | ✓         |
| Sync            | `70`  | `1C`    | Off **`00`** / On **`01`**                                                  | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | **Sync Off:** **FilterEnv>FM**; **Sync On:** **FilterEnv>Sync** (same wire) | ✓         |
| Key Follow      | `70`  | `1F`    | **−64..+63** → `stored = ui + 64`                                           | ✓         |
| Balance         | `70`  | `21`    | **−100..+100 %** → see Osc 1 Balance                                        | ✓         |

**Shape** (`16`): same Classic Shape regions as Osc 1. Anchor confirmed:

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Shape Spectral Wave
```

**Wave Select** (`18`): applies when **Shape = Spectral Wave** / Wave>Saw
region,
same 64-wave enum as Osc 1 Classic. Anchor confirmed:

```text
F0 00 20 33 01 00 70 00 18 00 F7   # Wave Select Sine
```

**Semitone** (`19`): **−48..+48** → `stored = semitone + 64`
(**`10`..`70`**).

```text
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
```

**Key Follow** (`1F`): **−64..+63** → `stored = ui + 64`
(**`00`..`7F`**). Panel **Norm** is expected at **+32** → **`60`**.

```text
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 40 F7   # Key Follow 0
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
```

**Balance** (`21`): same oscillator balance encoding as Osc 1 Classic.

```text
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

**Detune** (`1A`): **0..127** → `stored = lcd`.

```text
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
```

**FM Mode** (`71`/`22`): Page B enum (not Page A).

| LCD          | `<value>` | Confirmed |
| ------------ | --------- | --------- |
| Pos Triangle | `00`      | ✓         |
| Triangle     | `01`      | ✓         |
| Wave         | `02`      | ✓         |
| Noise        | `03`      | ✓         |
| In L         | `04`      | ✓         |
| In L+R       | `05`      | ✓         |
| In R         | `06`      | ✓         |

```text
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode Pos Triangle
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode Triangle
F0 00 20 33 01 00 71 00 22 02 F7   # FM Mode Wave
F0 00 20 33 01 00 71 00 22 03 F7   # FM Mode Noise
F0 00 20 33 01 00 71 00 22 04 F7   # FM Mode In L
F0 00 20 33 01 00 71 00 22 05 F7   # FM Mode In L+R
F0 00 20 33 01 00 71 00 22 06 F7   # FM Mode In R
```

**FM Amount / Sync Frequency** (`1B`): panel label depends on **Sync** (`1C`).

| **Sync** | Panel control      | Encoding                                              |
| -------- | ------------------ | ----------------------------------------------------- |
| Off      | **FM Amount**      | **0.0..100.0 %** → `stored = round(pct × 127 / 100)`  |
| On       | **Sync Frequency** | **0..127** → `stored = lcd`                           |

```text
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0 % (Sync Off)
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 100.0 % (Sync Off)
F0 00 20 33 01 00 70 00 1B 00 F7   # Sync Frequency 0 (Sync On)
F0 00 20 33 01 00 70 00 1B 7F F7   # Sync Frequency 127 (Sync On)
```

**FilterEnv>Pitch** (`1D`): panel **−100.0..+100.0 %**, wire **`00..7F`**.

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh:      pct = +100.0 %
```

```text
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
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
as **FilterEnv>Pitch** (`1D`). WAF80 Page A **30** = *FM Filt Env Amt*.

| **Sync** | Panel control      |
| -------- | ------------------ |
| Off      | **FilterEnv>FM**   |
| On       | **FilterEnv>Sync** |

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh:      pct = +100.0 %
```

```text
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM or FilterEnv>Sync −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM or FilterEnv>Sync 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM or FilterEnv>Sync +100.0 %
```

**Sync** (`1C`): boolean toggle.

```text
F0 00 20 33 01 00 70 00 1C 00 F7   # Sync Off
F0 00 20 33 01 00 70 00 1C 01 F7   # Sync On
```

### Oscillator 2 — Hypersaw

**Mode `<value>` = `01`**. Page A **`0x16`** = **Density** here
(Classic uses the same index for **Shape**); **`0x17`** = **Local Detune**
(Classic uses the same index for **Pulse Width**).

| Control         | `cmd` | `param` | Encoding                                           | Confirmed |
| --------------- | ----- | ------- | -------------------------------------------------- | --------- |
| Density         | `70`  | `16`    | **1.0..9.0**; same curve as Osc 1 Hypersaw Density | ✓         |
| Local Detune    | `70`  | `17`    | **0..127** → `stored = lcd`                        | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                              | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`                        | ✓         |
| Sync Frequency  | `70`  | `1B`    | **0..127** when **Sync On**; `stored = lcd`        | ✓         |
| Sync            | `70`  | `1C`    | Off **`00`** / On **`01`**                         | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch              | ✓         |
| FilterEnv>Sync  | `70`  | `1E`    | When **Sync On**; same wire/curve as FilterEnv>FM  | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                              | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                              | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Density 1.0
F0 00 20 33 01 00 70 00 16 7F F7   # Density 9.0
F0 00 20 33 01 00 70 00 17 00 F7   # Local Detune 0
F0 00 20 33 01 00 70 00 17 7F F7   # Local Detune 127
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # Sync Frequency 0
F0 00 20 33 01 00 70 00 1B 7F F7   # Sync Frequency 127
F0 00 20 33 01 00 70 00 1C 00 F7   # Sync Off
F0 00 20 33 01 00 70 00 1C 01 F7   # Sync On
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>Sync −100.0 % (Sync On)
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>Sync 0 % (Sync On)
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>Sync +100.0 % (Sync On)
```

### Oscillator 2 — Wavetable

**Mode `<value>` = `02`**. Page A **`0x16`** = **Index** here
(Classic uses the same index for **Shape**; Hypersaw uses it for **Density**).
Page A **`0x18`** selects the wavetable.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| FM Mode         | `71`  | `22`    | Enum; see below                       | partial   |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
```

**FM Mode** (`71`/`22`) in Wavetable mode:

| LCD      | `<value>` | Confirmed |
| -------- | --------- | --------- |
| FreqMod  | `00`      | ✓         |
| PhaseMod | `01`      | ✓         |

### Oscillator 2 — Wavetable PWM

**Mode `<value>` = `03`**. Same Wavetable select/index pattern as Osc 2
Wavetable, with **Pulse Width** on Page A **`0x17`** and **Local Detune** on
part-buffer **`0x3F`**.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| Pulse Width     | `70`  | `17`    | **0..127** → `stored = lcd`           | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FM Mode         | `71`  | `22`    | Same as Osc 2 Wavetable FM Mode       | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 70 00 17 00 F7   # Pulse Width 0
F0 00 20 33 01 00 70 00 17 7F F7   # Pulse Width 127
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 6E 00 3F 00 F7   # Local Detune 0
F0 00 20 33 01 00 6E 00 3F 7F F7   # Local Detune 127
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

### Oscillator 2 — Grain Simple

**Mode `<value>` = `04`**. Same Wavetable select/index pattern as Osc 2
Wavetable, with **F-Shift** on part-buffer **`0x3E`**.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`     | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FM Mode         | `71`  | `22`    | Same as Osc 2 Wavetable FM Mode       | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 6E 00 3E 00 F7   # F-Shift −64
F0 00 20 33 01 00 6E 00 3E 40 F7   # F-Shift +0
F0 00 20 33 01 00 6E 00 3E 7F F7   # F-Shift +63
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

### Oscillator 2 — Grain Complex

**Mode `<value>` = `05`**. Same Wavetable select/index pattern as Osc 2
Grain Simple, adding **F-Spread** on part-buffer **`0x39`** and
**Local Detune** on part-buffer **`0x3F`**.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`     | ✓         |
| F-Spread        | `6E`  | `39`    | **0..127** → `stored = lcd`           | ✓         |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`           | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FM Mode         | `71`  | `22`    | Same as Osc 2 Wavetable FM Mode       | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 6E 00 3E 00 F7   # F-Shift −64
F0 00 20 33 01 00 6E 00 3E 40 F7   # F-Shift +0
F0 00 20 33 01 00 6E 00 3E 7F F7   # F-Shift +63
F0 00 20 33 01 00 6E 00 39 00 F7   # F-Spread 0
F0 00 20 33 01 00 6E 00 39 7F F7   # F-Spread 127
F0 00 20 33 01 00 6E 00 3F 00 F7   # Local Detune 0
F0 00 20 33 01 00 6E 00 3F 7F F7   # Local Detune 127
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

### Oscillator 2 — Formant Simple

**Mode `<value>` = `06`**. Same Wavetable select/index pattern as Osc 2
Grain Simple. **F-Spread** and **Local Detune** are not present in this mode.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`     | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FM Mode         | `71`  | `22`    | Same as Osc 2 Wavetable FM Mode       | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 6E 00 3E 00 F7   # F-Shift −64
F0 00 20 33 01 00 6E 00 3E 40 F7   # F-Shift +0
F0 00 20 33 01 00 6E 00 3E 7F F7   # F-Shift +63
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

### Oscillator 2 — Formant Complex

**Mode `<value>` = `07`**. Same Wavetable select/index pattern as Osc 2
Formant Simple, adding **F-Spread** on part-buffer **`0x39`** and
**Local Detune** on part-buffer **`0x3F`**.

| Control         | `cmd` | `param` | Encoding                              | Confirmed |
| --------------- | ----- | ------- | ------------------------------------- | --------- |
| Index           | `70`  | `16`    | **0..127** → `stored = lcd`           | ✓         |
| Wavetable       | `70`  | `18`    | **`00`–`63`** enum; Sine..Domina7rix  | ✓         |
| F-Shift         | `6E`  | `3E`    | **−64..+63** → `stored = ui + 64`     | ✓         |
| F-Spread        | `6E`  | `39`    | **0..127** → `stored = lcd`           | ✓         |
| Local Detune    | `6E`  | `3F`    | **0..127** → `stored = lcd`           | ✓         |
| Interpolation   | `6E`  | `40`    | **0..127** → `stored = lcd`           | ✓         |
| Semitone        | `70`  | `19`    | Same as Osc 2 Classic                 | ✓         |
| Detune          | `70`  | `1A`    | **0..127** → `stored = lcd`           | ✓         |
| FM Amount       | `70`  | `1B`    | **0..127** → `stored = lcd`           | ✓         |
| FM Mode         | `71`  | `22`    | Same as Osc 2 Wavetable FM Mode       | ✓         |
| FilterEnv>Pitch | `70`  | `1D`    | Same as Osc 2 Classic FilterEnv>Pitch | ✓         |
| FilterEnv>FM    | `70`  | `1E`    | Same as Osc 2 Classic FilterEnv>FM    | ✓         |
| Key Follow      | `70`  | `1F`    | Same as Osc 2 Classic                 | ✓         |
| Balance         | `70`  | `21`    | Same as Osc 2 Classic                 | ✓         |

```text
F0 00 20 33 01 00 70 00 16 00 F7   # Index 0
F0 00 20 33 01 00 70 00 16 7F F7   # Index 127
F0 00 20 33 01 00 70 00 18 00 F7   # Wavetable Sine
F0 00 20 33 01 00 70 00 18 63 F7   # Wavetable Domina7rix
F0 00 20 33 01 00 6E 00 3E 00 F7   # F-Shift −64
F0 00 20 33 01 00 6E 00 3E 40 F7   # F-Shift +0
F0 00 20 33 01 00 6E 00 3E 7F F7   # F-Shift +63
F0 00 20 33 01 00 6E 00 39 00 F7   # F-Spread 0
F0 00 20 33 01 00 6E 00 39 7F F7   # F-Spread 127
F0 00 20 33 01 00 6E 00 3F 00 F7   # Local Detune 0
F0 00 20 33 01 00 6E 00 3F 7F F7   # Local Detune 127
F0 00 20 33 01 00 6E 00 40 00 F7   # Interpolation 0
F0 00 20 33 01 00 6E 00 40 7F F7   # Interpolation 127
F0 00 20 33 01 00 70 00 19 10 F7   # Semitone −48
F0 00 20 33 01 00 70 00 19 40 F7   # Semitone +0
F0 00 20 33 01 00 70 00 19 70 F7   # Semitone +48
F0 00 20 33 01 00 70 00 1A 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 1A 7F F7   # Detune 127
F0 00 20 33 01 00 70 00 1B 00 F7   # FM Amount 0
F0 00 20 33 01 00 70 00 1B 7F F7   # FM Amount 127
F0 00 20 33 01 00 71 00 22 00 F7   # FM Mode FreqMod
F0 00 20 33 01 00 71 00 22 01 F7   # FM Mode PhaseMod
F0 00 20 33 01 00 70 00 1D 00 F7   # FilterEnv>Pitch −100.0 %
F0 00 20 33 01 00 70 00 1D 40 F7   # FilterEnv>Pitch 0 %
F0 00 20 33 01 00 70 00 1D 7F F7   # FilterEnv>Pitch +100.0 %
F0 00 20 33 01 00 70 00 1E 00 F7   # FilterEnv>FM −100.0 %
F0 00 20 33 01 00 70 00 1E 40 F7   # FilterEnv>FM 0 %
F0 00 20 33 01 00 70 00 1E 7F F7   # FilterEnv>FM +100.0 %
F0 00 20 33 01 00 70 00 1F 00 F7   # Key Follow −64
F0 00 20 33 01 00 70 00 1F 7F F7   # Key Follow +63
F0 00 20 33 01 00 70 00 21 00 F7   # Balance −100 %
F0 00 20 33 01 00 70 00 21 40 F7   # Balance 0 %
F0 00 20 33 01 00 70 00 21 7F F7   # Balance +100 %
```

### Oscillator 3

**Mode/Wave** (`71`/`29`): enum. Values **`06`–`43`** are the Wave
choices **Wave 3** through **Wave 64**:

```text
stored = wave_number + 3        # Wave 3 -> 06, Wave 64 -> 43
wave_number = stored - 3        # for stored 06h..43h
```

| LCD             | `<value>` | Confirmed               |
| --------------- | --------- | ----------------------- |
| Off             | `00`      | ✓                       |
| Slave           | `01`      | ✓                       |
| Saw             | `02`      | ✓                       |
| Pulse           | `03`      | ✓                       |
| Sine            | `04`      | ✓                       |
| Triangle        | `05`      | ✓                       |
| Wave 3          | `06`      | ✓                       |
| Wave 4          | `07`      | ✓                       |
| Wave 5..Wave 64 | `08`–`43` | inferred contiguous run |

```text
F0 00 20 33 01 00 71 00 29 00 F7   # Oscillator 3 Mode/Wave Off
F0 00 20 33 01 00 71 00 29 01 F7   # Oscillator 3 Mode/Wave Slave
F0 00 20 33 01 00 71 00 29 02 F7   # Oscillator 3 Mode/Wave Saw
F0 00 20 33 01 00 71 00 29 03 F7   # Oscillator 3 Mode/Wave Pulse
F0 00 20 33 01 00 71 00 29 04 F7   # Oscillator 3 Mode/Wave Sine
F0 00 20 33 01 00 71 00 29 05 F7   # Oscillator 3 Mode/Wave Triangle
F0 00 20 33 01 00 71 00 29 06 F7   # Oscillator 3 Mode/Wave Wave 3
F0 00 20 33 01 00 71 00 29 43 F7   # Oscillator 3 Mode/Wave Wave 64
```

**Visible controls by Mode/Wave:**

| Mode/Wave             | Controls shown           | Confirmed |
| --------------------- | ------------------------ | --------- |
| Off                   | none                     | ✓         |
| Slave                 | none                     | ✓         |
| Saw / Pulse / Sine    | Semitone, Volume, Detune | ✓         |
| Triangle / Wave 3..64 | Semitone, Volume, Detune | ✓         |

For **Saw** through **Wave 64** (`02`–`43`), these controls share the same
Page B parameter IDs:

| Control  | `cmd` | `param` | Encoding                          | Confirmed |
| -------- | ----- | ------- | --------------------------------- | --------- |
| Semitone | `71`  | `2B`    | **−48..+48** → `stored = ui + 64` | ✓         |
| Volume   | `71`  | `2A`    | **0..127** → `stored = lcd`       | ✓         |
| Detune   | `71`  | `2C`    | **0..−127** → `stored = −ui`      | ✓         |

```text
F0 00 20 33 01 00 71 00 2B 10 F7   # Oscillator 3 Semitone −48
F0 00 20 33 01 00 71 00 2B 40 F7   # Oscillator 3 Semitone +0
F0 00 20 33 01 00 71 00 2B 70 F7   # Oscillator 3 Semitone +48
F0 00 20 33 01 00 71 00 2A 00 F7   # Oscillator 3 Volume 0
F0 00 20 33 01 00 71 00 2A 7F F7   # Oscillator 3 Volume 127
F0 00 20 33 01 00 71 00 2C 00 F7   # Oscillator 3 Detune 0
F0 00 20 33 01 00 71 00 2C 7F F7   # Oscillator 3 Detune −127
```

## Noise

**Oscillators → Noise**. Page A parameters (WAF80 CC **37** = Volume; TI adds
**Color** at index **39** / **`0x27`** between Ring Mod and Cutoff).

### Noise Volume (`0x25`, `cmd=0x70` / CC 37)

Panel **Off**, then **1..127**; wire matches the numeric value (**`00`** = Off).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| Off | `00`      | ✓         |
| 1   | `01`      | ✓         |
| 127 | `7F`      | ✓         |

```text
stored = lcd    # 1..127; 00 = Off
```

```text
F0 00 20 33 01 00 70 00 25 00 F7   # Noise Volume Off
F0 00 20 33 01 00 70 00 25 01 F7   # Noise Volume 1
F0 00 20 33 01 00 70 00 25 7F F7   # Noise Volume 127
```

### Noise Color (`0x27`, `cmd=0x70`)

Panel **−64..+63** → **`stored = ui + 64`** (same bipolar pattern as
[Key Follow](#oscillator-2--classic) / [Osc
Volume](edit-single.md#osc-volume-0x24-cmd0x70)).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| −64 | `00`      | ✓         |
| 0   | `40`      | ✓         |
| +63 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 70 00 27 00 F7   # Noise Color −64
F0 00 20 33 01 00 70 00 27 40 F7   # Noise Color 0
F0 00 20 33 01 00 70 00 27 7F F7   # Noise Color +63
```

## Ring Modulator

**Oscillators → Ring Modulator**. Page A param **`0x26`** (WAF80 CC **38** —
Ringmodulator Volume).

### Ring Modulator Volume (`0x26`, `cmd=0x70` / CC 38)

Panel **Off**, then **1..127**; wire matches the numeric value (**`00`** = Off).
Same encoding as [Noise Volume](#noise-volume-0x25-cmd0x70--cc-37).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| Off | `00`      | ✓         |
| 1   | `01`      | ✓         |
| 2   | `02`      | ✓         |
| 127 | `7F`      | ✓         |

```text
stored = lcd    # 1..127; 00 = Off
```

```text
F0 00 20 33 01 00 70 00 26 00 F7   # Ring Modulator Volume Off
F0 00 20 33 01 00 70 00 26 01 F7   # Ring Modulator Volume 1
F0 00 20 33 01 00 70 00 26 02 F7   # Ring Modulator Volume 2
F0 00 20 33 01 00 70 00 26 7F F7   # Ring Modulator Volume 127
```

## Sub Oscillator

**Oscillators → Sub Oscillator**. Page A **`0x22`** (Volume, WAF80 CC **34**)
and **`0x23`** (Shape, CC **35**). **Not** Page B **`71` / `0x23`** (that is
[Phase Init](edit-single.md#phase-init-0x23-cmd0x71)).

### Sub Oscillator Volume (`0x22`, `cmd=0x70` / CC 34)

Panel **0..127**; wire matches the numeric value (**`00`** = **0**, not “Off”).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 127 | `7F`      | ✓         |

```text
stored = lcd    # 0..127
```

```text
F0 00 20 33 01 00 70 00 22 00 F7   # Sub Oscillator Volume 0
F0 00 20 33 01 00 70 00 22 7F F7   # Sub Oscillator Volume 127
```

Also available as **MIDI CC 34** when Page A = **Controller Data** — see
[control-change.md](control-change.md#sub-oscillator-volume-cc-34).

### Sub Oscillator Shape (`0x23`, `cmd=0x70` / CC 35)

Two shapes only; no further values on the panel.

| LCD       | `<value>` | Confirmed |
| --------- | --------- | --------- |
| Square    | `00`      | ✓         |
| Triangle  | `01`      | ✓         |

```text
F0 00 20 33 01 00 70 00 23 00 F7   # Shape Square
F0 00 20 33 01 00 70 00 23 01 F7   # Shape Triangle
```

### Mixer (Oscillators menu)

### Oscillator Section Volume (`cmd=0x71`, param `0x7F`) {#oscillator-section-volume-cmd0x71-param-0x7f}

**Oscillators → Mixer → Oscillator Section Volume** (main osc mixer level).
Same bipolar range as [Saturation — Osc
Volume](filters.md#saturation--osc-volume-cmd0x70-param-0x24)
but edited via **Page B** SysEx here, not **`70` / `24`**.

| Item                    | Value                                           |
| ----------------------- | ----------------------------------------------- |
| Message (last in burst) | `F0 00 20 33 01 00 71 40 7F 00 F7`              |
| Scope byte              | `0x40` (verify — expected `0x00` for Part 1)    |
| Param ID                | `0x7F`                                          |
| Value encoding          | Bipolar **`stored = ui + 64`** (`−64` → `0x00`) |
| Confirmed               | Hardware TX, landing **−64** → `0x00`           |

```text
F0 00 20 33 01 00 71 40 7F 00 F7   # Oscillator Section Volume −64
```

**Sub Oscillator Volume** — see [Sub Oscillator](#sub-oscillator) (`70` / `0x22`
or CC 34).
