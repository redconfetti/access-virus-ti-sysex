# Filters

Edit Single — **Filters** (Common, Filter 1/2, Filter/Amp envelopes,
**Saturation**).

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
different `cmd` bytes.

## Panel reference

**LCD:** **FILTERS** → **Filter 1** / **Filter 2** / **Common** / **Filter 1
envelope**. Filter 1, Filter 2, **Common**, and **Filter 1 ADSR** confirmed on
TI mk2 desktop; remaining **FILTERS** rows (e.g. modulation, velocity targets) —
see
[testing.md — Filters queue](../testing.md#filters--order-filter-1-first).

### SELECT (`71`/`7A`) {#filters-select}

**FILTERS** section — **SELECT** toggles **Filter 1** / **Filter 2** (press
both together for **Filter 1 + Filter 2**). Also sets which filter the front-
panel **Resonance** and **Envelope Amount** knobs edit. Live edit **`cmd=0x71`**,
param **`0x7A`**. Enum:
[Filters SELECT](../parameter-options.md#filters-select).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 7A <value> F7` |
| Value encoding | **`00`** Filter 1 · **`01`** Filter 2 · **`02`** Filter 1 + 2 |
| Confirmed | Hardware TX (TI mk2) |

```text
F0 00 20 33 01 00 71 00 7A 00 F7 # 7A/00 — Filter 1
F0 00 20 33 01 00 71 00 7A 01 F7 # 7A/01 — Filter 2
F0 00 20 33 01 00 71 00 7A 02 F7 # 7A/02 — Filter 1 + Filter 2
```

**Not** **Not**
[Pan Spread](#pan-spread-cmd0x6e-param-0x7a) (`6E`/`7A` — same param byte,
different **`cmd`**).

When [Vocoder Mode](../parameter-options.md#vocoder-mode) ≠ **Off**, the
**FILTERS** section is unavailable — LCD **`Vocoder active. Filters are
disabled`**.

### Filter 1 Cutoff (`cmd=0x70`, param `0x28`)

**FILTERS → EDIT → Filter 1 → Cutoff**.
**`0x28`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 28 <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | Direct **`0`–`127`** (UI **0** → `00`; sweep max → `7F`) |
| Confirmed | Hardware TX, Page A/B = **SysEx** |

```text
F0 00 20 33 01 00 70 00 28 00 F7 # Cutoff 0 (landing)
F0 00 20 33 01 00 70 00 28 7F F7 # Cutoff max (127 on wire)
```

LCD may show **128** at the top of the range; highest byte on the wire is
**`0x7F`**.

### Filter 1 Resonance (`cmd=0x70`, param `0x2A`) {#filter-1-resonance-cmd0x70-param-0x2a}

**FILTERS → EDIT → Filter 1 → Resonance**.
**`0x2A`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2A <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | Direct **`0`–`127`** (UI **127** → `7F`) |
| Confirmed | Hardware TX |

```text
F0 00 20 33 01 00 70 00 2A 7F F7 # Resonance 127 (landing)
```

### Filter 1 Mode (`cmd=0x70`, param `0x33`)

**FILTERS → EDIT → Filter 1 → Mode** (or **Filter 1 Mode**).
index **51** = **`0x33`**. Classic 1999: **0** LP, **1** HP, **2** BP, **3** BS.
TI mk2 adds more modes — capture **every** LCD label until the list repeats.

| UI (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| Low Pass | `00` | ✓ |
| High Pass | `01` | ✓ |
| Band Pass | `02` | ✓ |
| Band Stop | `03` | ✓ |
| Analog 1 Pole | `04` | ✓ |
| Analog 2 Pole | `05` | ✓ |
| Analog 3 Pole | `06` | ✓ |
| Analog 4 Pole | `07` | ✓ |

**TI mk2 desktop (INIT, Filter 1):** **8** modes, **`00`–`07`** sequential. No
further
options after Analog 4 Pole on hardware tested. **Filter 2 Mode** (`0x34`) has
only
**four** modes (LP/HP/BP/BS) — see below. There is **no** separate **Analog
Mode**
on/off — analog filtering is selected via Filter 1 mode names (not a VC/CSV
toggle).

```text
F0 00 20 33 01 00 70 00 33 00 F7 # Low Pass
F0 00 20 33 01 00 70 00 33 01 F7 # High Pass
F0 00 20 33 01 00 70 00 33 02 F7 # Band Pass
F0 00 20 33 01 00 70 00 33 03 F7 # Band Stop
F0 00 20 33 01 00 70 00 33 04 F7 # Analog 1 Pole
F0 00 20 33 01 00 70 00 33 05 F7 # Analog 2 Pole
F0 00 20 33 01 00 70 00 33 06 F7 # Analog 3 Pole
F0 00 20 33 01 00 70 00 33 07 F7 # Analog 4 Pole
```

### Filter 1 Envelope Amount (`cmd=0x70`, param `0x2C`) {#filter-1-envelope-amount-cmd0x70-param-0x2c}

**FILTERS → EDIT → Filter 1 → Envelope Amount**. Page
**A**
index **44** = **`0x2C`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2C <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | **Linear percent:** `stored = round(percent × 127 / 100)` |
| Confirmed | Hardware TX |

| LCD (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| 0.0 % | `00` | ✓ |
| 50.0 % | `40` | ✓ |
| 100.0 % | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 2C 00 F7 # 0.0 %
F0 00 20 33 01 00 70 00 2C 40 F7 # 50.0 %
F0 00 20 33 01 00 70 00 2C 7F F7 # 100.0 %
```

### Filter 1 Keyfollow (`cmd=0x70`, param `0x2E`)

**FILTERS → EDIT → Filter 1 → Keyfollow**.
**`0x2E`**;
range **−64..+63** (bipolar).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2E <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | **Bipolar:** `stored = ui + 64` (UI **−64..+63**) |
| Confirmed | Hardware TX |

| LCD (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| −64 | `00` | ✓ |
| +0 | `40` | ✓ |
| +63 | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 2E 00 F7 # −64
F0 00 20 33 01 00 70 00 2E 40 F7 # +0
F0 00 20 33 01 00 70 00 2E 7F F7 # +63
```

### Filter 1 Envelope Polarity (`cmd=0x71`, param `0x1E`)

**FILTERS → EDIT → Filter 1 → Env Polarity**.
(filter env polarity); TI uses **`cmd=0x71`** (Page B), not **`0x70`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 1E <value> F7` |
| Scope (Part 1) | **`0x00`** |

| LCD (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| Negative | `00` | ✓ |
| Positive | `01` | ✓ |

```text
F0 00 20 33 01 00 71 00 1E 00 F7 # Negative
F0 00 20 33 01 00 71 00 1E 01 F7 # Positive
```

### Filter 2 Offset (`cmd=0x70`, param `0x29`)

**FILTERS → EDIT → Filter 2 → Offset** (relative cutoff vs Filter 1). Page
**A** param **`0x29`**. Bipolar **−64..+63**:
`stored = ui + 64` (same as Filter 1 Keyfollow). No separate Filter 2
Cutoff on TI.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 29 <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | **Bipolar:** `stored = ui + 64` |
| Confirmed | Hardware TX |

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| −64 | `00` | ✓ |
| +0 | `40` | ✓ |
| +63 | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 29 00 F7 # −64
F0 00 20 33 01 00 70 00 29 40 F7 # +0
F0 00 20 33 01 00 70 00 29 7F F7 # +63
```

### Filter 2 Mode (`cmd=0x70`, param `0x34`)

**FILTERS → EDIT → Filter 2 → Mode**.
**`0x34`**.
Classic **Filter2 Mode**: LP / HP / BP / BS only — **no** Analog 1–4 Pole on TI.

| UI (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| Low Pass | `00` | ✓ |
| High Pass | `01` | ✓ |
| Band Pass | `02` | ✓ |
| Band Stop | `03` | ✓ |

```text
F0 00 20 33 01 00 70 00 34 00 F7 # Low Pass
F0 00 20 33 01 00 70 00 34 01 F7 # High Pass
F0 00 20 33 01 00 70 00 34 02 F7 # Band Pass
F0 00 20 33 01 00 70 00 34 03 F7 # Band Stop
```

### Filter 2 Resonance (`cmd=0x70`, param `0x2B`)

**FILTERS → EDIT → Filter 2 → Resonance**.
**`0x2B`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2B <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | Direct **`0`–`127`** |
| Confirmed | Hardware TX |

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| 0 | `00` | ✓ |
| 127 | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 2B 00 F7 # 0
F0 00 20 33 01 00 70 00 2B 7F F7 # 127
```

### Filter 2 Envelope Amount (`cmd=0x70`, param `0x2D`)

**FILTERS → EDIT → Filter 2 → Envelope Amount**.
**`0x2D`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2D <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | **Linear percent:** `stored = round(percent × 127 / 100)` |
| Confirmed | Hardware TX |

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| 0 % | `00` | ✓ |
| 50 % | `40` | ✓ |
| 100 % | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 2D 00 F7 # 0 %
F0 00 20 33 01 00 70 00 2D 40 F7 # 50 %
F0 00 20 33 01 00 70 00 2D 7F F7 # 100 %
```

### Filter 2 Keyfollow (`cmd=0x70`, param `0x2F`)

**FILTERS → EDIT → Filter 2 → Keyfollow**.
**`0x2F`**.

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 70 <part> 2F <value> F7` |
| Scope (Part 1) | **`0x00`** |
| Value encoding | **Bipolar:** `stored = ui + 64` |
| Confirmed | Hardware TX |

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| −64 | `00` | ✓ |
| +0 | `40` | ✓ |
| +63 | `7F` | ✓ |

```text
F0 00 20 33 01 00 70 00 2F 00 F7 # −64
F0 00 20 33 01 00 70 00 2F 40 F7 # +0
F0 00 20 33 01 00 70 00 2F 7F F7 # +63
```

### Filter 2 Envelope Polarity (`cmd=0x71`, param `0x1F`)

**FILTERS → EDIT → Filter 2 → Env Polarity**. Page **B** param **`0x1F`**
(Filter 1 polarity is **`0x1E`** on the same **`cmd=0x71`**).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 1F <value> F7` |
| Scope (Part 1) | **`0x00`** |

| LCD (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| Negative | `00` | ✓ |
| Positive | `01` | ✓ |

```text
F0 00 20 33 01 00 71 00 1F 00 F7 # Negative
F0 00 20 33 01 00 71 00 1F 01 F7 # Positive
```

## Filter Common

**LCD:** **FILTERS** → **Common** (after Filter 1 / 2). Confirmed on TI mk2
desktop unless noted.

### Filter Routing (`cmd=0x70`, param `0x35`)

.

| UI (reported) | `<value>` | Confirmed |
| --- | --- | --- |
| Serial 4 | `00` | ✓ |
| Serial 6 | `01` | ✓ |
| Parallel 4 | `02` | ✓ |
| Split Mode | `03` | ✓ |

```text
F0 00 20 33 01 00 70 00 35 00 F7 # Serial 4
F0 00 20 33 01 00 70 00 35 03 F7 # Split Mode
```

### Filter Balance (`cmd=0x70`, param `0x30`)

. Bipolar **−64..+63**:
`stored = ui + 64`.

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| −64 | `00` | ✓ |
| +0 | `40` | ✓ |
| +63 | `7F` | ✓ |

### Filter Cutoff Link (`cmd=0x71`, param `0x20`)

Page **B** **`0x20`**.

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| Off | `00` | ✓ |
| On | `01` | ✓ |

### Filter Key Follow Base (`cmd=0x71`, param `0x21`)

Page **B** **`0x21`**. **Semitone index** from **C-1** (`00`) through **G9**
(`7F`) — chromatic steps, not bipolar offset.

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| C-1 | `00` | ✓ |
| C0 | `0C` | ✓ |
| C4 | `3C` | ✓ |
| G9 | `7F` | ✓ |

### Pan Spread (`cmd=0x6E`, param `0x7A`)

TI control. **Only on the panel when
[Filter Routing](#filter-routing-cmd0x70-param-0x35) = Split Mode.** Direct
**0–127**. Same param ID **`0x7A`** as
[Filters SELECT](#filters-select)
(`71`/`7A`) but **different `cmd`** — always check the command byte.

| UI | `<value>` | Confirmed |
| --- | --- | --- |
| 0 | `00` | ✓ |
| 127 | `7F` | ✓ |

```text
F0 00 20 33 01 00 6E 00 7A 00 F7 # 0
F0 00 20 33 01 00 6E 00 7A 7F F7 # 127
```

### Saturation — Osc Volume (`cmd=0x70`, param `0x24`) {#saturation--osc-volume-cmd0x70-param-0x24}

**FILTERS → Saturation** (sub-menu; also a dedicated front-panel knob). Page
**A** param **`0x24`**. Bipolar **−64..+63**:
`stored = ui + 64`. LCD center shows **`<0>`** (not “+0”).

| LCD | `<value>` | Confirmed |
| --- | --- | --- |
| −64 | `00` | ✓ |
| `<0>` | `40` | ✓ |
| +63 | `7F` | ✓ |

**Also:**
[Oscillator Section
Volume](oscillators.md#oscillator-section-volume-cmd0x71-param-0x7f)
from **Oscillators → Mixer** uses **`71` / `7F`** (different message). Oscillator
page **SELECT**: [SELECT (`71`/`7F`)](oscillators.md#oscillators-select).

## Filter 1 envelope (ADSR) {#filter-1-envelope-adsr}

**LCD:** **FILTERS** → **Filter Envelope** — ADSR for **Filter 1** (distinct
from **Filter 1 → Envelope Amount** `0x2C` on the Filter 1 edit page). Params
**`0x36`–`0x3A`**. All use **`cmd=0x70`**, scope
**`0x00`** (Part 1).

### Attack (`0x36`) / Decay (`0x37`) / Release (`0x3A`)

Direct **0–127** (UI matches wire).

| Stage | Param | UI 0 | UI 127 |
| --- | --- | --- | --- |
| Attack | `36` | `00` | `7F` |
| Decay | `37` | `00` | `7F` |
| Release | `3A` | `00` | `7F` |

### Sustain (`0x38`)

**Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD | `<value>` |
| --- | --- |
| 0 % | `00` |
| 50.0 % | `40` |
| 100.0 % | `7F` |

### Sustain Slope (`0x39`)

Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --- |
| −64 | `00` |
| +0 | `40` |
| +63 | `7F` |

```text
F0 00 20 33 01 00 70 00 36 00 F7 # Attack 0
F0 00 20 33 01 00 70 00 37 7F F7 # Decay 127
F0 00 20 33 01 00 70 00 38 40 F7 # Sustain 50 %
F0 00 20 33 01 00 70 00 39 40 F7 # Sustain Slope +0
F0 00 20 33 01 00 70 00 3A 7F F7 # Release 127
```

## Amplifier envelope (ADSR) {#amplifier-envelope-adsr}

**LCD:** **Amp Envelope** (Single Edit).
**`0x3B`–`0x3F`**. Same encodings as [Filter 1
envelope](#filter-1-envelope-adsr).
**`cmd=0x70`**, scope **`0x00`** (Part 1).

### Attack (`0x3B`) / Decay (`0x3C`) / Release (`0x3F`)

Direct **0–127**.

| Stage | Param | UI 0 | UI 127 |
| --- | --- | --- | --- |
| Attack | `3B` | `00` | `7F` |
| Decay | `3C` | `00` | `7F` |
| Release | `3F` | `00` | `7F` |

### Sustain (`0x3D`)

**Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD | `<value>` |
| --- | --- |
| 0 % | `00` |
| 50.0 % | `40` |
| 100.0 % | `7F` |

### Sustain Slope (`0x3E`)

Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --- |
| −64 | `00` |
| +0 | `40` |
| +63 | `7F` |

```text
F0 00 20 33 01 00 70 00 3B 7F F7 # Attack 127
F0 00 20 33 01 00 70 00 3D 40 F7 # Sustain 50 %
F0 00 20 33 01 00 70 00 3F 00 F7 # Release 0
```
