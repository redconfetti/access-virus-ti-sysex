# Edit Single

Edit Single — **Common**, **Envelope 3/4**, **Velocity Map**, **Soft Knobs**,
and related patch settings.

Part of [Documentation](../../../README.md#documentation). Enumerated options:
[parameter-options.md](../../reference/parameter-options.md).
Parameter map: [Single parameter map](../../dumps/single.md#single-parameter-map)
· Multi: [Edit Multi](../multis.md).

Paging: [virus.md](../../../misc/virus.md#paging) (`0x70` Page A, `0x71` Page B,
`0x6E` part buffer, `0x6F` extended, `0x72` Multi). Param IDs depend on **`cmd`**.

SysEx examples target the [Single edit buffer](README.md) (**`<part>` =
**`0x40`**). To edit a Multi part instead, see
[README — Multi parts](README.md#multi-edit-buffer-parts).

## Contents

* [Common (Edit Single)](#common-edit-single)
  * [Multi Tempo / Master Clock](#multi-tempo--master-clock)
  * [Patch Volume](#patch-volume)
  * [Panorama](#panorama)
  * [Transpose / Patch Transpose](#transpose--patch-transpose)
  * [Key Mode](#key-mode)
  * [Phase Init](#phase-init)
  * [Portamento](#portamento)
  * [Smooth Mode](#smooth-mode)
  * [Bend Down](#bend-down)
  * [Bend Up](#bend-up)
  * [Bender Scale](#bender-scale)
* [Envelope 3 (ADSR)](#envelope-3-adsr)
  * [Attack (`0x50`) / Decay (`0x51`) / Release](#attack-0x50--decay-0x51--release)
  * [Sustain](#sustain)
  * [Sustain Slope](#sustain-slope)
* [Envelope 4 (ADSR)](#envelope-4-adsr)
  * [Attack (`0x55`) / Decay (`0x56`) / Release](#attack-0x55--decay-0x56--release)
  * [Sustain](#sustain-1)
  * [Sustain Slope](#sustain-slope-1)
* [Velocity Map (Edit Single)](#velocity-map-edit-single)
* [Surround (Edit Single)](#surround-edit-single)
  * [Output](#output)
  * [Balance](#balance)
* [Categories (Edit Single)](#categories-edit-single)
* [Soft Knobs (Edit Single)](#soft-knobs-edit-single)
  * [Soft Knob 1](#soft-knob-1)
  * [Soft Knob 2](#soft-knob-2)
  * [Soft Knob 3](#soft-knob-3)
  * [Soft-knob runtime: Distortion Intensity](#soft-knob-runtime-distortion-intensity)

---

## Common (Edit Single)

Per-part **Common** page settings (Edit Single). Pitch-bender and smooth-mode
bytes **are** stored in **Single Dump**; they are **not** in per-part **Multi Dump** slices — see
[multis.md](../multis.md).

### Multi Tempo / Master Clock

**Live edit:** `cmd=0x72`, param `0x0F`.

**Edit Single → Common → Multi Tempo** (panel **Master Clock** for the loaded
Multi). Same live edit as [Master Clock
Tempo](../multis.md#master-clock-tempo)
in Edit Multi — global, not per-part.

| BPM | `<value>` |
| --- | --------- |
| 63  | `00`      |
| 120 | `39`      |
| 190 | `7F`      |

```text
stored = bpm - 63 # 63..190 → 00..7F
```

```text
F0 00 20 33 01 00 72 00 0F 00 F7 # Multi Tempo 63 bpm
F0 00 20 33 01 00 72 00 0F 39 F7 # Multi Tempo 120 bpm
F0 00 20 33 01 00 72 00 0F 7F F7 # Multi Tempo 190 bpm
```

Dump offset in **Multi Dump**: **`0x18`** (`stored` same; follows name at
`0x0D`–`0x16` and null at `0x17`).

### Patch Volume

**Live edit:** `cmd=0x70`, param `0x5B` (CC 91).

**Edit Single → Common → Patch Volume**. Page A param **`0x5B`** (decimal **91**
= CC number). Panel **0..127**; wire matches LCD (**not** a percent curve).
Dump offset **`0x063`** (`-INIT-` default **`0x64`** = 100).

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
stored = lcd # 0..127
```

With **Page A = Controller Data**, the panel sends **CC 91** instead of SysEx.
Distinct from Multi **Part Level** (`0x99 + part` / live `0x27`).

```text
F0 00 20 33 01 00 70 40 5B 00 F7 # Patch Volume 0
F0 00 20 33 01 00 70 40 5B 7F F7 # Patch Volume 127
```

### Panorama

**Live edit:** `cmd=0x70`, param `0x0A` (CC 10).

**Edit Single → Common → Panorama**. Page A param **`0x0A`** (decimal **10** =
CC number). Bipolar pan **−64..+63** (panel **L< 100.0 %** … **100.0 % >R**):
`stored = ui + 64`. Dump offset **`0x012`**.

| LCD (reported) | `<value>` |
| -------------- | --------- |
| L< 100.0 %     | `00`      |
| `<0>`          | `40`      |
| 100.0 % >R     | `7F`      |

Full **wire → LCD** table (**`00`–`7F`**, hardware-confirmed): [Panorama
LCD](../../reference/parameter-options.md#edit-single--panorama-lcd).
Right **`41`–`7E`** mirrors left **`0x80 − R`** (`L<` → `% >R`); endpoints
**`00`** /
**`7F`** = **100.0 %**.

```text
F0 00 20 33 01 00 70 40 0A 00 F7 # Panorama L< 100.0 %
F0 00 20 33 01 00 70 40 0A 01 F7 # Panorama L< 98.4 %
F0 00 20 33 01 00 70 40 0A 40 F7 # Panorama <0>
F0 00 20 33 01 00 70 40 0A 7E F7 # Panorama 96.9 % >R
F0 00 20 33 01 00 70 40 0A 7F F7 # Panorama 100.0 % >R
```

With **Page A = Controller Data**, the panel sends **CC 10** instead of SysEx.
Distinct from **Velocity → Panorama** (`71`/`3D`) and Edit Multi panorama
(`72`/`2B`).

### Transpose / Patch Transpose

**Live edit:** `cmd=0x70`, param `0x5D` (CC 93).

Edit Single → Common → **Transpose** (same as **Patch Transpose**). Page A param
**`0x5D`** (decimal **93** = CC number). UI **−64..+63** → `stored = ui + 64`.
Dump offset **`0x065`** (`30 00 40` / `<part>=0x40`).

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

With **Page A = Controller Data**, the panel sends **CC 93** instead of SysEx.
Distinct from Edit Multi **Transpose** (`72` / `0x25`, dump `0x79 + part`).

```text
F0 00 20 33 01 00 70 40 5D 00 F7 # Transpose −64
F0 00 20 33 01 00 70 40 5D 40 F7 # Transpose +0
F0 00 20 33 01 00 70 40 5D 7F F7 # Transpose +63
```

Full wire map:
[Bipolar centered (±64 @ 0x40)](../reference/parameter-options.md#bipolar-centered-64--0x40).

### Key Mode

**Live edit:** `cmd=0x70`, param `0x5E` (CC 94).

**Key Mode** (Page A param **94** / `0x5E`). Virus panel: **Oscillators** →
**EDIT** → Common → **Key Mode**; also a **MONO** shortcut on the
oscillator section (see below). Dump offset **`0x066`**.

| Value | Mode   | CC 94 | SysEx (`Page A` = SysEx)  |
| ----- | ------ | ----- | ------------------------- |
| `00`  | Poly   | `0`   | `F0 … 70 <part> 5E 00 F7` |
| `01`  | Mono 1 | `1`   | `F0 … 70 <part> 5E 01 F7` |
| `02`  | Mono 2 | `2`   | `F0 … 70 <part> 5E 02 F7` |
| `03`  | Mono 3 | `3`   | `F0 … 70 <part> 5E 03 F7` |
| `04`  | Mono 4 | `4`   | `F0 … 70 <part> 5E 04 F7` |
| `05`  | Hold   | `5`   | `F0 … 70 <part> 5E 05 F7` |

Scope byte is the edited **part** (`00` for Part 1 in captures). Global
**MIDI Controller Page A** = **Controller Data** → **CC 94** on the part
channel instead; **SysEx** → **`cmd=0x70`** as above.

**MONO button (hardware shortcut)**

| Action       | Messages                                                                  |
| ------------ | ------------------------------------------------------------------------- |
| MONO **on**  | `F0 … 70 <part> 5E <last-mono> F7` → last selected **Mono 1..4**          |
| MONO **off** | `F0 … 6E <part> 7A <last-mono> F7`, then `F0 … 70 <part> 5E 00 F7` → Poly |

The MONO shortcut remembers the last selected mono mode. Example capture:
after selecting **Mono 4** (`5E 04`), MONO off sent **`6E/7A 04`** followed
by **`70/5E 00`** (Poly), and MONO on restored **`70/5E 04`**. Treat
**`6E` / `0x7A`** here as companion shortcut state for the remembered mono
mode; the actual Key Mode value is still **`70` / `0x5E`**.

### Phase Init

**Live edit:** `cmd=0x71`, param `0x23`.

**Oscillators → EDIT → Common → Phase Init**. Page B parameter **`0x23`**.
Panel **Off**, then **1..127**.

| LCD | `<value>` |
| --- | --------- |
| Off | `00`      |
| 1   | `01`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 71 40 23 00 F7 # Phase Init Off
F0 00 20 33 01 00 71 40 23 01 F7 # Phase Init 1
F0 00 20 33 01 00 71 40 23 7F F7 # Phase Init 127
```

### Portamento

**Live edit:** `cmd=0x70`, param `0x05` (CC 5).

**Oscillators → EDIT → Common → Portamento**. Page A param **`0x05`**. Panel **Off**, then **1..127**; wire matches the
numeric value (**not** a percent curve).

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
F0 00 20 33 01 00 70 40 05 00 F7 # Portamento Off
F0 00 20 33 01 00 70 40 05 01 F7 # Portamento 1
F0 00 20 33 01 00 70 40 05 7F F7 # Portamento 127
```

### Smooth Mode

**Live edit:** `cmd=0x71`, param `0x19`.

Edit Single → Common → **Smooth Mode** (Page B **#25** *Control Smooth Mode*).
**`stored = index`** — full list in
[Control Smooth Mode / clock
quantize](../../reference/parameter-options.md#control-smooth-mode--clock-quantize).
Dump offset **`0x0A1`**.

```text
F0 00 20 33 01 00 71 40 19 00 F7 # Off
F0 00 20 33 01 00 71 40 19 04 F7 # Quantise 1/64
F0 00 20 33 01 00 71 40 19 14 F7 # Quantise 1/1
```

Some hosts cannot send **Off** (`00`). Do not confuse with global **All EQs**
(`73` / `0x19`).

### Bend Down

**Live edit:** `cmd=0x71`, param `0x1B`.

Edit Single → Common → **Bend Down** (Page B **#27**). **−64..+63** →
`stored = ui + 64`. Dump offset **`0x0A3`** (not in **Multi Dump**).

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 40 1B 00 F7 # Bend Down −64
F0 00 20 33 01 00 71 40 1B 40 F7 # Bend Down +0
F0 00 20 33 01 00 71 40 1B 7F F7 # Bend Down +63
```

### Bend Up

**Live edit:** `cmd=0x71`, param `0x1A`.

Edit Single → Common → **Bend Up** (Page B **#26**). Same encoding as Bend Down.
Dump offset **`0x0A2`**.

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 40 1A 00 F7 # Bend Up −64
F0 00 20 33 01 00 71 40 1A 40 F7 # Bend Up +0
F0 00 20 33 01 00 71 40 1A 7F F7 # Bend Up +63
```

Also documented for Edit Multi: [multis.md — Bend Up / Bend
Down](../multis.md#bend-up).

### Bender Scale

**Live edit:** `cmd=0x71`, param `0x1C`.

Edit Single → Common → **Bender Scale** (Page B **#28**). **`stored = index`** —
see [Bender Scale](../../reference/parameter-options.md#bender-scale). Dump offset **`0x0A4`**.

| Mode        | `<value>` |
| ----------- | --------- |
| Linear      | `00`      |
| Exponential | `01`      |

```text
F0 00 20 33 01 00 71 40 1C 00 F7 # Linear
F0 00 20 33 01 00 71 40 1C 01 F7 # Exponential
```

## Envelope 3 (ADSR)

**Edit Single → Envelope 3**. Same encodings as
[Filter 1 envelope](filters.md#filter-1-envelope-adsr) / [Amplifier
envelope](filters.md#amplifier-envelope-adsr),
but on the **part edit buffer** — **`cmd=0x6E`**, not **`cmd=0x70`**.

| Control       | `cmd` | `param` | Encoding                                    |
| ------------- | ----- | ------- | ------------------------------------------- |
| Attack        | `6E`  | `50`    | **0..127** → `stored = lcd`                 |
| Decay         | `6E`  | `51`    | **0..127** → `stored = lcd`                 |
| Sustain       | `6E`  | `52`    | **0.0..100.0 %** → `round(pct × 127 / 100)` |
| Sustain Slope | `6E`  | `53`    | **−64..+63** → `stored = ui + 64`           |
| Release       | `6E`  | `54`    | **0..127** → `stored = lcd`                 |

### Attack (`0x50`) / Decay (`0x51`) / Release

**Live edit:** `cmd=0x6E`, params `0x50` / `0x51` / `0x54`.

**Edit Single → Envelope 3** — Attack, Decay, Release. Direct **0–127** (UI matches wire).

```text
F0 00 20 33 01 00 6E 40 50 00 F7 # Attack 0
F0 00 20 33 01 00 6E 40 50 7F F7 # Attack 127
F0 00 20 33 01 00 6E 40 51 00 F7 # Decay 0
F0 00 20 33 01 00 6E 40 51 7F F7 # Decay 127
F0 00 20 33 01 00 6E 40 54 00 F7 # Release 0
F0 00 20 33 01 00 6E 40 54 7F F7 # Release 127
```

### Sustain

**Live edit:** `cmd=0x6E`, param `0x52`.

**Edit Single → Envelope 3 → Sustain**. **Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 50.0 %  | `40`      |
| 100.0 % | `7F`      |

### Sustain Slope

**Live edit:** `cmd=0x6E`, param `0x53`.

**Edit Single → Envelope 3 → Sustain Slope**. Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6E 40 52 00 F7 # Sustain 0 %
F0 00 20 33 01 00 6E 40 52 40 F7 # Sustain 50.0 %
F0 00 20 33 01 00 6E 40 52 7F F7 # Sustain 100.0 %
F0 00 20 33 01 00 6E 40 53 00 F7 # Sustain Slope −64
F0 00 20 33 01 00 6E 40 53 40 F7 # Sustain Slope +0
F0 00 20 33 01 00 6E 40 53 7F F7 # Sustain Slope +63
```

## Envelope 4 (ADSR)

**Edit Single → Envelope 4**. Same encodings and **`cmd=0x6E`** part-buffer
layout as [Envelope 3](#envelope-3-adsr), next param block **`0x55`–`0x59`**.

| Control       | `cmd` | `param` | Encoding                                    |
| ------------- | ----- | ------- | ------------------------------------------- |
| Attack        | `6E`  | `55`    | **0..127** → `stored = lcd`                 |
| Decay         | `6E`  | `56`    | **0..127** → `stored = lcd`                 |
| Sustain       | `6E`  | `57`    | **0.0..100.0 %** → `round(pct × 127 / 100)` |
| Sustain Slope | `6E`  | `58`    | **−64..+63** → `stored = ui + 64`           |
| Release       | `6E`  | `59`    | **0..127** → `stored = lcd`                 |

### Attack (`0x55`) / Decay (`0x56`) / Release

**Live edit:** `cmd=0x6E`, params `0x55` / `0x56` / `0x59`.

**Edit Single → Envelope 4** — Attack, Decay, Release. Direct **0–127** (UI matches wire).

```text
F0 00 20 33 01 00 6E 40 55 00 F7 # Attack 0
F0 00 20 33 01 00 6E 40 55 7F F7 # Attack 127
F0 00 20 33 01 00 6E 40 56 00 F7 # Decay 0
F0 00 20 33 01 00 6E 40 56 7F F7 # Decay 127
F0 00 20 33 01 00 6E 40 59 00 F7 # Release 0
F0 00 20 33 01 00 6E 40 59 7F F7 # Release 127
```

### Sustain

**Live edit:** `cmd=0x6E`, param `0x57`.

**Edit Single → Envelope 4 → Sustain**. **Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 50.0 %  | `40`      |
| 100.0 % | `7F`      |

### Sustain Slope

**Live edit:** `cmd=0x6E`, param `0x58`.

**Edit Single → Envelope 4 → Sustain Slope**. Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6E 40 57 00 F7 # Sustain 0 %
F0 00 20 33 01 00 6E 40 57 40 F7 # Sustain 50.0 %
F0 00 20 33 01 00 6E 40 57 7F F7 # Sustain 100.0 %
F0 00 20 33 01 00 6E 40 58 00 F7 # Sustain Slope −64
F0 00 20 33 01 00 6E 40 58 40 F7 # Sustain Slope +0
F0 00 20 33 01 00 6E 40 58 7F F7 # Sustain Slope +63
```

**Note:** **`cmd=0x6F`** **`7C`/`7D`/`7E`** are **Inputs** (see
[Inputs](../global.md#inputs-edit-single)). Other **`6F`** params (e.g.
**`78`/`79`/`7A`**)
for Envelope 4 — the
**`6E` `55`–`59`** block matches full ADSR sweeps on hardware.

## Velocity Map (Edit Single)

**Edit Single → Velocity Map.** All targets use **`cmd=0x71`** (Page B), part
**`00`**, and the same **±100.0 %** bipolar curve as Osc 2 **FilterEnv>Pitch**
(`70`/`1D`)
and **FilterEnv>FM** (`70`/`1E`):

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh: pct = +100.0 %
```

| LCD label          | `cmd` | `param` |
| ------------------ | ----- | ------- |
| Volume             | `71`  | `3C`    |
| Panorama           | `71`  | `3D`    |
| FM Amount          | `71`  | `32`    |
| Osc 1 Shape        | `71`  | `2F`    |
| Osc 2 Shape        | `71`  | `30`    |
| Pulse Width        | `71`  | `31`    |
| Filter1 Env Amount | `71`  | `36`    |
| Resonance 1        | `71`  | `38`    |
| Filter2 Env Amount | `71`  | `37`    |
| Resonance 2        | `71`  | `39`    |

The
**Velocity Map** menu exposes the **10** rows above; **`71`/`33`–`35`**
were not swept in capture and may be unused or reserved on this
firmware. There is **no** separate **FM/Sync** row — **FM Amount** applies
regardless of Osc **Sync** state.

```text
F0 00 20 33 01 00 71 40 3C 00 F7 # Volume −100.0 %
F0 00 20 33 01 00 71 40 3C 40 F7 # Volume 0 %
F0 00 20 33 01 00 71 40 3C 7F F7 # Volume +100.0 %
F0 00 20 33 01 00 71 40 32 40 F7 # FM Amount 0 %
F0 00 20 33 01 00 71 40 32 7F F7 # FM Amount +100.0 %
F0 00 20 33 01 00 71 40 2F 00 F7 # Osc 1 Shape −100.0 %
F0 00 20 33 01 00 71 40 2F 40 F7 # Osc 1 Shape 0 %
F0 00 20 33 01 00 71 40 2F 7F F7 # Osc 1 Shape +100.0 %
```

Single edit buffer (**`<part>=0x40`**) — same map (spot-check ✓):

```text
F0 00 20 33 01 00 71 40 32 00 F7 # FM Amount −100.0 %
```

The same **`00` / `40` / `7F`** anchors apply to every row in the table.

## Surround (Edit Single)

**Edit Single → Surround.** This is the patch **secondary output**
bus (rear/surround send in a multi-output setup — separate from the main
**Output Routing** path on **`72`/`29`** in Multi mode). Same wire as
**Edit Multi → Secondary Output**: **`cmd=0x73`**, param **`0x2D`**. In Single
mode use **`<part>=0x40`** (Single edit buffer — same scope as other Single
sound edits). Enum:
[Secondary output
routing](../../reference/parameter-options.md#secondary-output-routing).
**Output** is **not in Single Dump**. **Balance** **is** in the dump at **`0x0C2`**
(`71`/`3A`).

### Output

**Live edit:** `cmd=0x73`, param `0x2D`.

Enum: [Secondary output
routing](../../reference/parameter-options.md#secondary-output-routing)
(**Off** … **Out 3 R** = `00`–`09`; USB through `12`).

```text
F0 00 20 33 01 00 73 40 2D 00 F7 # Output Off
F0 00 20 33 01 00 73 40 2D 04 F7 # Out 2 L
F0 00 20 33 01 00 73 40 2D 09 F7 # Out 3 R
```

Edit Multi Part 1 uses **`73 00 2D`** (Part 1 scope). Values are
the same enum.

### Balance

**Live edit:** `cmd=0x71`, param `0x3A`.

**Surround → Balance** (rear/surround channel placement). Bipolar
**−64..+63**: `stored = ui + 64` (same family as Filter Keyfollow).
Dump offset **`0x0C2`**.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 40 3A 00 F7 # Balance −64
F0 00 20 33 01 00 71 40 3A 40 F7 # Balance +0
F0 00 20 33 01 00 71 40 3A 7F F7 # Balance +63
```

Mod matrix destination **116** / **118** = **Surround Balance** (amount
modulation) — same parameter family, different UI path.

## Categories (Edit Single)

**Edit Single → Categories.** Patch **search/filter tags** (**Search by
Category**). **`cmd=0x71`**, part **`00`** (Single edit buffer **`0x40`**
also works). Dump **`0x103`** (Cat 1) / **`0x104`** (Cat 2).

| Panel      | `param` |
| ---------- | ------- |
| Name Cat 1 | `7B`    |
| Name Cat 2 | `7C`    |

Both use [Patch name
categories](../../reference/parameter-options.md#patch-name-categories)
(**Off** … **Favourites 3**, `00`–`16`).

```text
F0 00 20 33 01 00 71 40 7B 00 F7 # Name Cat 1 Off
F0 00 20 33 01 00 71 40 7B 01 F7 # Name Cat 1 Acid
F0 00 20 33 01 00 71 40 7C 16 F7 # Name Cat 2 Favourites 3
```

## Soft Knobs (Edit Single)

Three hardware knobs under the LCD. **Edit Single** only configures them; there
is
**no separate “Amount” menu row** — turning a knob edits the **assigned
destination** parameter in real time.

Dump offsets (**`<part>=0x40`**):
**Function As…** **`0x0C6`** / **`0x0C7`** / **`0x0C8`**; **Name**
**`0x0BB`** / **`0x0BC`** / **`0x0BD`**. Knob 3 **Function As…** shares
**`0x0C8`** with [Mod Matrix slot 1 Source](mod-matrix.md) (`71`/`40`).

**Function As…** uses a **destination wire byte** (see
[Soft Knob Destinations](../../reference/parameter-options.md#soft-knob-destinations)).
The **value** SysEx slot is usually a **different `param`** on **`cmd=0x71`**
(see [soft-knob runtime example](#soft-knob-runtime-distortion-intensity) when
**Function As…** = Distortion Intensity; full **EFFECTS → Distortion** mapping
deferred until the Effects module pass).

Example (Soft Knob 1): **Function As…** = Distortion Intensity (`71`/`3E`/`57`),
**Name** = Distort (`71`/`33`/…). Outside Edit Single the LCD shows **Distort**
above knob 1; sweeping the knob sends **`71`/`65`** (**0 %** → `00`,
**100.0 %** → `7F`).

| Knob | **Function As…** `param` | **Name** `param` |
| ---- | ------------------------ | ---------------- |
| 1    | `3E`                     | `33`             |
| 2    | `3F`                     | `34`             |
| 3    | `40`                     | `35`             |

### Soft Knob 1

| Control          | `cmd` | `param` | Notes                                                                                                                                                  |
| ---------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Function As…** | `71`  | `3E`    | Wire byte per [Soft Knob Destinations](../../reference/parameter-options.md#soft-knob-destinations) (not list index); e.g. Distortion Intensity → `57` |
| **Name**         | `71`  | `33`    | Wire byte per [Soft Knob Names](../../reference/parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off          |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (≠ Function As wire); example → [`65`](#soft-knob-runtime-distortion-intensity)                             |

```text
F0 00 20 33 01 00 71 40 3E 57 F7 # Knob 1 Function As Distortion Intensity
F0 00 20 33 01 00 71 40 65 00 F7 # Distortion Intensity 0 %
F0 00 20 33 01 00 71 40 65 7F F7 # Distortion Intensity 100.0 %
F0 00 20 33 01 00 71 40 3E 00 F7 # Knob 1 Function As Off
F0 00 20 33 01 00 71 40 3E 40 F7 # Aftertouch
F0 00 20 33 01 00 71 40 3E 7F F7 # Freq Shifter Mix (index 59)
F0 00 20 33 01 00 71 40 3E 58 F7 # FreqShifter Frequency (index 61)
F0 00 20 33 01 00 71 40 3E 46 F7 # Velo > Volume (index 127)
F0 00 20 33 01 00 71 40 33 00 F7 # Name >Para
F0 00 20 33 01 00 71 40 33 01 F7 # Name +3rds
F0 00 20 33 01 00 71 40 33 47 F7 # Name Width (wire 47)
F0 00 20 33 01 00 71 40 33 57 F7 # Name Speaker (wire 57)
```

### Soft Knob 2

| Control          | `cmd` | `param` | Notes                                                                                                                                         |
| ---------------- | ----- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function As…** | `71`  | `3F`    | Same destination list as Knob 1                                                                                                               |
| **Name**         | `71`  | `34`    | Wire byte per [Soft Knob Names](../../reference/parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (per destination)                                                                                  |

```text
F0 00 20 33 01 00 71 40 3F 00 F7 # Knob 2 Function As Off
F0 00 20 33 01 00 71 40 3F 46 F7 # Velo > Volume (index 127)
F0 00 20 33 01 00 71 40 34 00 F7 # Name >Para
F0 00 20 33 01 00 71 40 34 01 F7 # Name +3rds
F0 00 20 33 01 00 71 40 34 47 F7 # Name Width
```

### Soft Knob 3

| Control          | `cmd` | `param` | Notes                                                                                                                                         |
| ---------------- | ----- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function As…** | `71`  | `40`    | Same destination list as Knob 1                                                                                                               |
| **Name**         | `71`  | `35`    | Wire byte per [Soft Knob Names](../../reference/parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (per destination)                                                                                  |

```text
F0 00 20 33 01 00 71 40 40 00 F7 # Knob 3 Function As Off
F0 00 20 33 01 00 71 40 40 46 F7 # Velo > Volume (index 127)
F0 00 20 33 01 00 71 40 35 00 F7 # Name >Para
F0 00 20 33 01 00 71 40 35 47 F7 # Name Width
```

### Soft-knob runtime: Distortion Intensity

Same value param as
[EDIT FX → Distortion →
Intensity](effects.md#distortion-intensity)
(**`71`/`65`**). **Type** is
[`71`/`64`](effects.md#distortion-type).

When **Function As…** =
[Distortion Intensity](../../reference/parameter-options.md#soft-knob-destinations)
(wire
**`57`** on `71`/`3E`/`3F`/`40`), the knob sends **`71`/`65`**:

| UI      | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 100.0 % | `7F`      |

**0.0..100.0 %** → `stored = round(pct × 127 / 100)` (endpoints **`00`** /
**`7F`**). Destination wire **`57`** ≠ value param **`65`**.

```text
F0 00 20 33 01 00 71 40 65 00 F7 # 0 % (soft knob)
F0 00 20 33 01 00 71 40 65 7F F7 # 100.0 % (soft knob)
```
