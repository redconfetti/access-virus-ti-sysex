# Edit Single

Edit Single — **Common**, **Unison**, **Envelope 3/4**, **Velocity Map**, **Soft
Knobs**, and related patch settings.

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

## Common (Edit Single)

Per-part **Common** page settings (Edit Single). Not stored in
**`DUMP_MULTI`** (hardware-tested for Bend Up/Down — see
[edit-multi.md](edit-multi.md)).

### Transpose / Patch Transpose (`0x5D`, `cmd=0x70` / CC 93)

Edit Single → Common → **Transpose** (same as **Patch Transpose**). Page A param
**`0x5D`** (decimal **93** = CC number). **−64..+63** → `stored = ui + 64`.

| UI   | `<value>` | Confirmed |
| ---- | --------- | --------- |
| −64  | `00`      | ✓         |
| +0   | `40`      | ✓         |
| +63  | `7F`      | ✓         |

With **Page A = Controller Data**, the panel sends **CC 93** instead of SysEx.
Distinct from Edit Multi **Transpose** (`72` / `0x25`, dump `0x79 + part`). See
[control-change.md — Patch Transpose](control-change.md#patch-transpose-cc-93).

```text
F0 00 20 33 01 00 70 00 5D 00 F7   # Transpose −64
F0 00 20 33 01 00 70 00 5D 40 F7   # Transpose +0
F0 00 20 33 01 00 70 00 5D 7F F7   # Transpose +63
```

### Key Mode (`0x5E`, `cmd=0x70` / CC 94)

**Key Mode** (Page A param **94** / `0x5E`). Virus panel: **Oscillators** →
**EDIT** → Common → **Key Mode**; also a **MONO** shortcut on the
oscillator section (see below).

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
channel instead; **SysEx** → **`cmd=0x70`** as above. See
[control-change.md — Key Mode](control-change.md#key-mode-cc-94).

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

### Phase Init (`0x23`, `cmd=0x71`) {#phase-init-0x23-cmd0x71}

**Oscillators → EDIT → Common → Phase Init**. Page B parameter **`0x23`**.
Panel **Off**, then **1..127**.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| Off | `00`      | ✓         |
| 1   | `01`      | ✓         |
| 127 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 71 00 23 00 F7   # Phase Init Off
F0 00 20 33 01 00 71 00 23 01 F7   # Phase Init 1
F0 00 20 33 01 00 71 00 23 7F F7   # Phase Init 127
```

### Portamento (`0x05`, `cmd=0x70` / CC 5)

**Oscillators → EDIT → Common → Portamento**. Page A param **`0x05`** (WAF80 CC
**5** — Portamento Time). Panel **Off**, then **1..127**; wire matches the
numeric value (**not** a percent curve).

| LCD  | `<value>` | Confirmed |
| ---- | --------- | --------- |
| Off  | `00`      | ✓         |
| 1    | `01`      | ✓         |
| 2    | `02`      | ✓         |
| 127  | `7F`      | ✓         |

```text
stored = lcd    # 1..127; 00 = Off
```

```text
F0 00 20 33 01 00 70 00 05 00 F7   # Portamento Off
F0 00 20 33 01 00 70 00 05 01 F7   # Portamento 1
F0 00 20 33 01 00 70 00 05 7F F7   # Portamento 127
```

### Punch Intensity (`0x24`, `cmd=0x71`)

**Oscillators → Punch → Punch Intensity**. Page B param **`0x24`** (WAF80 Page
B **#36**). Panel **0.0..100.0 %** — **not** the same byte as
[Osc Volume](#osc-volume-0x24-cmd0x70) (`cmd=0x70`).

```text
for 00h..7Eh: pct = stored × 100 / 128
for 7Fh:      pct = 100.0 %
stored       = round(pct × 128 / 100)   # cap at 7Fh for 100.0 %
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
F0 00 20 33 01 00 71 00 24 00 F7   # Punch 0.0 %
F0 00 20 33 01 00 71 00 24 40 F7   # Punch 50.0 %
F0 00 20 33 01 00 71 00 24 7F F7   # Punch 100.0 %
```

### Osc Volume (`0x24`, `cmd=0x70`) {#osc-volume-0x24-cmd0x70}

**Oscillators → EDIT → Common → Osc Volume**. Same parameter as
[Saturation — Osc Volume](filters.md#saturation--osc-volume-cmd0x70-param-0x24):
panel **−64..+63**, wire **`stored = ui + 64`**.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| −64 | `00`      | ✓         |
| 0   | `40`      | ✓         |
| +63 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 70 00 24 00 F7   # Osc Volume −64
F0 00 20 33 01 00 70 00 24 40 F7   # Osc Volume 0
F0 00 20 33 01 00 70 00 24 7F F7   # Osc Volume +63
```

### Smooth Mode (`0x19`, `cmd=0x71`)

Edit Single → Common → **Smooth Mode** (Page B **#25** *Control Smooth Mode*).
**`stored = index`** — full list in
[Control Smooth Mode / clock
quantize](../parameter-options.md#control-smooth-mode--clock-quantize).

```text
F0 00 20 33 01 00 71 00 19 00 F7   # Off
F0 00 20 33 01 00 71 00 19 04 F7   # Quantise 1/64
F0 00 20 33 01 00 71 00 19 14 F7   # Quantise 1/1
```

Some hosts cannot send **Off** (`00`) — [aura-notes.md](../aura-notes.md). Do
not
confuse with global **All EQs** (`73` / `0x19`).

### Bend Down (`0x1B`, `cmd=0x71`)

Edit Single → Common → **Bend Down** (Page B **#27**). **−64..+63** →
`stored = ui + 64`. Not in **`DUMP_MULTI`**.

| UI  | `<value>` | Confirmed |
| --- | --------- | --------- |
| −64 | `00`      | ✓         |
| +0  | `40`      | ✓         |
| +63 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 71 00 1B 00 F7   # Bend Down −64
F0 00 20 33 01 00 71 00 1B 40 F7   # Bend Down +0
F0 00 20 33 01 00 71 00 1B 7F F7   # Bend Down +63
```

### Bend Up (`0x1A`, `cmd=0x71`)

Edit Single → Common → **Bend Up** (Page B **#26**). Same encoding as Bend Down.

| UI  | `<value>` | Confirmed |
| --- | --------- | --------- |
| −64 | `00`      | ✓         |
| +0  | `40`      | ✓         |
| +63 | `7F`      | ✓         |

```text
F0 00 20 33 01 00 71 00 1A 00 F7   # Bend Up −64
F0 00 20 33 01 00 71 00 1A 40 F7   # Bend Up +0
F0 00 20 33 01 00 71 00 1A 7F F7   # Bend Up +63
```

Also documented for Edit Multi: [edit-multi.md — Bend Up / Bend
Down](edit-multi.md#bend-up-0x1a-cmd0x71).

### Bender Scale (`0x1C`, `cmd=0x71`)

Edit Single → Common → **Bender Scale** (Page B **#28**). **`stored = index`** —
see [Bender Scale](../parameter-options.md#bender-scale).

| Mode          | `<value>` | Confirmed |
| ------------- | --------- | --------- |
| Linear        | `00`      | ✓         |
| Exponential   | `01`      | ✓         |

```text
F0 00 20 33 01 00 71 00 1C 00 F7   # Linear
F0 00 20 33 01 00 71 00 1C 01 F7   # Exponential
```

### Multi Tempo / Master Clock (`0x0F`, `cmd=0x72`)

**Edit Single → Common → Multi Tempo** (panel **Master Clock** for the loaded
Multi). Same live edit as [Master Clock
Tempo](edit-multi.md#master-clock-tempo-0x0f)
in Edit Multi — global, not per-part.

| BPM  | `<value>` | Confirmed                      |
| ---- | --------- | ------------------------------ |
| 63   | `00`      | ✓                              |
| 120  | `39`      | (INIT default in `DUMP_MULTI`) |
| 190  | `7F`      | ✓                              |

```text
stored = bpm - 63    # 63..190 → 00..7F
```

```text
F0 00 20 33 01 00 72 00 0F 00 F7   # Multi Tempo 63 bpm
F0 00 20 33 01 00 72 00 0F 39 F7   # Multi Tempo 120 bpm
F0 00 20 33 01 00 72 00 0F 7F F7   # Multi Tempo 190 bpm
```

Dump offset in **`DUMP_MULTI`**: **`0x17`** (`stored` same).

### Patch Volume (`0x5B`, `cmd=0x70` / CC 91)

**Edit Single → Common → Patch Volume**. Page A param **`0x5B`** (decimal **91**
= CC number). Panel **0..127**; wire matches LCD (**not** a percent curve).

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 127 | `7F`      | ✓         |

```text
stored = lcd    # 0..127
```

With **Page A = Controller Data**, the panel sends **CC 91** instead of SysEx.
See [control-change.md — Patch Volume](control-change.md#patch-volume-cc-91).
Distinct from Multi **Part Level** (`0x99 + part` / live `0x27`).

```text
F0 00 20 33 01 00 70 00 5B 00 F7   # Patch Volume 0
F0 00 20 33 01 00 70 00 5B 7F F7   # Patch Volume 127
```

### Panorama (`0x0A`, `cmd=0x70` / CC 10)

**Edit Single → Common → Panorama**. Page A param **`0x0A`** (decimal **10** =
CC number). Bipolar pan **−64..+63** (panel **L< 100.0 %** … **100.0 % >R**):
`stored = ui + 64`.

| LCD (reported) | `<value>` | Confirmed |
| -------------- | --------- | --------- |
| L< 100.0 %     | `00`      | ✓         |
| `<0>`          | `40`      | ✓         |
| 100.0 % >R     | `7F`      | ✓         |

Full **wire → LCD** table (**`00`–`7F`**, hardware-confirmed): [Panorama
LCD](../parameter-options.md#edit-single--panorama-lcd).
Right **`41`–`7E`** mirrors left **`0x80 − R`** (`L<` → `% >R`); endpoints
**`00`** /
**`7F`** = **100.0 %**.

```text
F0 00 20 33 01 00 70 00 0A 00 F7   # Panorama L< 100.0 %
F0 00 20 33 01 00 70 00 0A 01 F7   # Panorama L< 98.4 %
F0 00 20 33 01 00 70 00 0A 40 F7   # Panorama <0>
F0 00 20 33 01 00 70 00 0A 7E F7   # Panorama 96.9 % >R
F0 00 20 33 01 00 70 00 0A 7F F7   # Panorama 100.0 % >R
```

With **Page A = Controller Data**, the panel sends **CC 10** instead of SysEx.
Distinct from **Velocity → Panorama** (`71`/`3D`) and Edit Multi panorama
(`72`/`2B`).

## Unison

**Edit Single → Unison** (top-level sub-menu, not under Osc 1 / Osc 2 / Osc 3).
Stacks **extra voices** for the patch (detuned copies of the oscillator
section),
not a per-oscillator mode like **Sync** on Osc 2. WAF80 Page A **97–100** →
**`0x61`–`0x64`** on **`cmd=0x70`**.

### Voices (`0x61`, `cmd=0x70` / CC 97)

Panel **Voices** (WAF80 *Unison Mode* was **0/1** only; TI adds voice count).

| LCD   | `<value>` | Confirmed |
| ----- | --------- | --------- |
| Off   | `00`      | ✓         |
| Twin  | `01`      | ✓         |
| 3     | `02`      | ✓         |
| 4     | `03`      | ✓         |
| 5     | `04`      | inferred  |
| 6     | `05`      | inferred  |
| 7     | `06`      | inferred  |
| 8     | `07`      | ✓         |

```text
F0 00 20 33 01 00 70 00 61 00 F7   # Voices Off
F0 00 20 33 01 00 70 00 61 01 F7   # Voices Twin
F0 00 20 33 01 00 70 00 61 07 F7   # Voices 8
```

When **Voices** is **Twin** (`01`) or higher, **Detune** appears on the panel.
When **Off**, **Detune** is hidden (wire value may still be stored).

### Detune (`0x62`, `cmd=0x70` / CC 98)

**0..127** → `stored = lcd`. Panel visible only when **Voices** ≥ **Twin**.

| LCD | `<value>` | Confirmed |
| --- | --------- | --------- |
| 0   | `00`      | ✓         |
| 127 | `7F`      | partial   |

```text
F0 00 20 33 01 00 70 00 62 00 F7   # Detune 0
F0 00 20 33 01 00 70 00 62 7F F7   # Detune 127
```

### Pan Spread (`0x63`, `cmd=0x70` / CC 99)

Panel **0.0..100.0 %** — always visible (even when **Voices** = **Off**).
WAF80 lists **0–127** on the wire; treat percent curve as **Punch-like** until
hardware anchors confirm otherwise:

```text
for 00h..7Eh: pct = stored × 100 / 128
for 7Fh:      pct = 100.0 %
```

```text
F0 00 20 33 01 00 70 00 63 00 F7   # Pan Spread 0.0 %
F0 00 20 33 01 00 70 00 63 7F F7   # Pan Spread 100.0 %
```

### LFO Phase Offset (`0x64`, `cmd=0x70` / CC 100)

WAF80 **−64..+63** → `stored = ui + 64`. Panel control **Unison LFO Phase**
(not reported in latest sweep — confirm on hardware).

```text
F0 00 20 33 01 00 70 00 64 00 F7   # LFO Phase −64 (expected)
F0 00 20 33 01 00 70 00 64 40 F7   # LFO Phase 0 (expected)
F0 00 20 33 01 00 70 00 64 7F F7   # LFO Phase +63 (expected)
```

## Envelope 3 (ADSR)

**Edit Single → Envelope 3**. Same encodings as
[Filter 1 envelope](filters.md#filter-1-envelope-adsr) / [Amplifier
envelope](filters.md#amplifier-envelope-adsr),
but on the **part edit buffer** — **`cmd=0x6E`**, not **`cmd=0x70`**.

| Control       | `cmd` | `param` | Encoding                                      | Confirmed |
| ------------- | ----- | ------- | --------------------------------------------- | --------- |
| Attack        | `6E`  | `50`    | **0..127** → `stored = lcd`                   | ✓         |
| Decay         | `6E`  | `51`    | **0..127** → `stored = lcd`                   | ✓         |
| Sustain       | `6E`  | `52`    | **0.0..100.0 %** → `round(pct × 127 / 100)`   | ✓         |
| Sustain Slope | `6E`  | `53`    | **−64..+63** → `stored = ui + 64`             | ✓         |
| Release       | `6E`  | `54`    | **0..127** → `stored = lcd`                   | ✓         |

### Attack (`0x50`) / Decay (`0x51`) / Release (`0x54`)

Direct **0–127** (UI matches wire).

```text
F0 00 20 33 01 00 6E 00 50 00 F7   # Attack 0
F0 00 20 33 01 00 6E 00 50 7F F7   # Attack 127
F0 00 20 33 01 00 6E 00 51 00 F7   # Decay 0
F0 00 20 33 01 00 6E 00 51 7F F7   # Decay 127
F0 00 20 33 01 00 6E 00 54 00 F7   # Release 0
F0 00 20 33 01 00 6E 00 54 7F F7   # Release 127
```

### Sustain (`0x52`)

**Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 50.0 %  | `40`      |
| 100.0 % | `7F`      |

### Sustain Slope (`0x53`)

Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6E 00 52 00 F7   # Sustain 0 %
F0 00 20 33 01 00 6E 00 52 40 F7   # Sustain 50.0 %
F0 00 20 33 01 00 6E 00 52 7F F7   # Sustain 100.0 %
F0 00 20 33 01 00 6E 00 53 00 F7   # Sustain Slope −64
F0 00 20 33 01 00 6E 00 53 40 F7   # Sustain Slope +0
F0 00 20 33 01 00 6E 00 53 7F F7   # Sustain Slope +63
```

## Envelope 4 (ADSR)

**Edit Single → Envelope 4**. Same encodings and **`cmd=0x6E`** part-buffer
layout as [Envelope 3](#envelope-3-adsr), next param block **`0x55`–`0x59`**.

| Control       | `cmd` | `param` | Encoding                                      | Confirmed |
| ------------- | ----- | ------- | --------------------------------------------- | --------- |
| Attack        | `6E`  | `55`    | **0..127** → `stored = lcd`                   | ✓         |
| Decay         | `6E`  | `56`    | **0..127** → `stored = lcd`                   | ✓         |
| Sustain       | `6E`  | `57`    | **0.0..100.0 %** → `round(pct × 127 / 100)`   | ✓         |
| Sustain Slope | `6E`  | `58`    | **−64..+63** → `stored = ui + 64`             | ✓         |
| Release       | `6E`  | `59`    | **0..127** → `stored = lcd`                   | ✓         |

### Attack (`0x55`) / Decay (`0x56`) / Release (`0x59`)

Direct **0–127** (UI matches wire).

```text
F0 00 20 33 01 00 6E 00 55 00 F7   # Attack 0
F0 00 20 33 01 00 6E 00 55 7F F7   # Attack 127
F0 00 20 33 01 00 6E 00 56 00 F7   # Decay 0
F0 00 20 33 01 00 6E 00 56 7F F7   # Decay 127
F0 00 20 33 01 00 6E 00 59 00 F7   # Release 0
F0 00 20 33 01 00 6E 00 59 7F F7   # Release 127
```

### Sustain (`0x57`)

**Linear percent:** `stored = round(percent × 127 / 100)`.

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 50.0 %  | `40`      |
| 100.0 % | `7F`      |

### Sustain Slope (`0x58`)

Bipolar **−64..+63**: `stored = ui + 64`.

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6E 00 57 00 F7   # Sustain 0 %
F0 00 20 33 01 00 6E 00 57 40 F7   # Sustain 50.0 %
F0 00 20 33 01 00 6E 00 57 7F F7   # Sustain 100.0 %
F0 00 20 33 01 00 6E 00 58 00 F7   # Sustain Slope −64
F0 00 20 33 01 00 6E 00 58 40 F7   # Sustain Slope +0
F0 00 20 33 01 00 6E 00 58 7F F7   # Sustain Slope +63
```

**Note:** **`cmd=0x6F`** **`7C`/`7D`/`7E`** are **Inputs** (see
[Inputs](edit-config.md#inputs-edit-single)). Other **`6F`** params (e.g.
**`78`/`79`/`7A`**)
appear in some captures but are **unconfirmed** for Envelope 4 — the
**`6E` `55`–`59`** block matches full ADSR sweeps on hardware.

## Velocity Map (Edit Single)

**Edit Single → Velocity Map.** All targets use **`cmd=0x71`** (Page B), part
**`00`**, and the same **±100.0 %** bipolar curve as Osc 2 **FilterEnv>Pitch**
(`70`/`1D`)
and **FilterEnv>FM** (`70`/`1E`):

```text
for 00h..7Eh: pct = (stored - 64) × 100 / 64
for 7Fh:      pct = +100.0 %
```

| LCD label              | `cmd` | `param` | WAF80 B# | Confirmed |
| ---------------------- | ----- | ------- | -------- | --------- |
| Volume                 | `71`  | `3C`    | 60       | ✓         |
| Panorama               | `71`  | `3D`    | 61       | ✓         |
| FM Amount              | `71`  | `32`    | 50       | ✓         |
| Osc 1 Shape            | `71`  | `2F`    | 47       | ✓         |
| Osc 2 Shape            | `71`  | `30`    | 48       | ✓         |
| Pulse Width            | `71`  | `31`    | 49       | ✓         |
| Filter1 Env Amount     | `71`  | `36`    | 54       | ✓         |
| Resonance 1            | `71`  | `38`    | 56       | ✓         |
| Filter2 Env Amount     | `71`  | `37`    | 55       | ✓         |
| Resonance 2            | `71`  | `39`    | 57       | ✓         |

WAF80 lists **B#47–57** as “velocity amounts” (11 slots). On TI mk2 the
**Velocity Map** menu exposes the **10** rows above; **`71`/`33`–`35`**
(B#51–53) were not swept in capture and may be unused or reserved on this
firmware.

```text
F0 00 20 33 01 00 71 00 3C 00 F7   # Volume −100.0 %
F0 00 20 33 01 00 71 00 3C 40 F7   # Volume 0 %
F0 00 20 33 01 00 71 00 3C 7F F7   # Volume +100.0 %
F0 00 20 33 01 00 71 00 32 00 F7   # FM Amount −100.0 %
F0 00 20 33 01 00 71 00 32 40 F7   # FM Amount 0 %
F0 00 20 33 01 00 71 00 32 7F F7   # FM Amount +100.0 %
F0 00 20 33 01 00 71 00 2F 00 F7   # Osc 1 Shape −100.0 %
F0 00 20 33 01 00 71 00 2F 40 F7   # Osc 1 Shape 0 %
F0 00 20 33 01 00 71 00 2F 7F F7   # Osc 1 Shape +100.0 %
```

The same **`00` / `40` / `7F`** anchors apply to every row in the table.

## Surround (Edit Single)

**Edit Single → Surround.** On TI mk2 this is the patch **secondary output**
bus (rear/surround send in a multi-output setup — separate from the main
**Output Routing** path on **`72`/`29`** in Multi mode). Same wire as
**Edit Multi → Secondary Output** and AURA’s “Secondary Output”:
**`cmd=0x73`**, param **`0x2D`**, part **`00`** in Single captures. Enum:
[Secondary output
routing](../parameter-options.md#secondary-output-routing).
**Not in `DUMP_MULTI`** / **`DUMP_SINGLE` offset TBD** (edit-buffer only in
hardware tests so far).

### Output (`0x2D`, `cmd=0x73`)

Enum: [Secondary output
routing](../parameter-options.md#secondary-output-routing)
(**Off** … **Out 3 R** = `00`–`09`; USB through `12`).

```text
F0 00 20 33 01 00 73 00 2D 00 F7   # Output Off
F0 00 20 33 01 00 73 00 2D 01 F7   # Out 1 L
F0 00 20 33 01 00 73 00 2D 09 F7   # Out 3 R
```

### Balance (`0x3A`, `cmd=0x71`)

**Surround → Balance** (rear/surround channel placement). Bipolar
**−64..+63**: `stored = ui + 64` (same family as Filter Keyfollow).

| LCD | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 00 3A 00 F7   # Balance −64
F0 00 20 33 01 00 71 00 3A 40 F7   # Balance +0
F0 00 20 33 01 00 71 00 3A 7F F7   # Balance +63
```

Mod matrix destination **116** / **118** = **Surround Balance** (amount
modulation) — same parameter family, different UI path.

## Categories (Edit Single)

**Edit Single → Categories.** Patch **search/filter tags** for Virus Control
browser (**Search by Category**). **`cmd=0x71`**, part **`00`**.

| Panel       | `param` | Confirmed |
| ----------- | ------- | --------- |
| Name Cat 1  | `7B`    | ✓         |
| Name Cat 2  | `7C`    | ✓         |

Both use [Patch name
categories](../parameter-options.md#patch-name-categories)
(**Off** … **Favourites 3**, `00`–`16`).

```text
F0 00 20 33 01 00 71 00 7B 00 F7   # Name Cat 1 Off
F0 00 20 33 01 00 71 00 7B 01 F7   # Name Cat 1 Acid
F0 00 20 33 01 00 71 00 7C 16 F7   # Name Cat 2 Favourites 3
```

## Soft Knobs (Edit Single)

Three hardware knobs under the LCD. **Edit Single** only configures them; there
is
**no separate “Amount” menu row** — turning a knob edits the **assigned
destination** parameter in real time.

**Function As…** uses a **destination wire byte** (see
[Soft Knob Destinations](../parameter-options.md#soft-knob-destinations)).
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

| Control          | `cmd` | `param` | Notes                                                                                                                                          |
| ---------------- | ----- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Function As…** | `71`  | `3E`    | Wire byte per [Soft Knob Destinations](../parameter-options.md#soft-knob-destinations) (not list index); e.g. Distortion Intensity → `57`      |
| **Name**         | `71`  | `33`    | Wire byte per [Soft Knob Names](../parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off               |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (≠ Function As wire); example → [`65`](#soft-knob-runtime-distortion-intensity)                     |

```text
F0 00 20 33 01 00 71 00 3E 57 F7   # Knob 1 Function As Distortion Intensity
F0 00 20 33 01 00 71 00 65 00 F7   # Distortion Intensity 0 % (knob sweep)
F0 00 20 33 01 00 71 00 65 7F F7   # Distortion Intensity 100.0 % (knob sweep)
F0 00 20 33 01 00 71 00 3E 00 F7   # Knob 1 Function As Off
F0 00 20 33 01 00 71 00 3E 40 F7   # Aftertouch
F0 00 20 33 01 00 71 00 3E 7F F7   # Freq Shifter Mix (index 59)
F0 00 20 33 01 00 71 00 3E 58 F7   # FreqShifter Frequency (index 61)
F0 00 20 33 01 00 71 00 3E 46 F7   # Velo > Volume (index 127)
F0 00 20 33 01 00 71 00 33 00 F7   # Name >Para
F0 00 20 33 01 00 71 00 33 01 F7   # Name +3rds
F0 00 20 33 01 00 71 00 33 47 F7   # Name Width (wire 47)
F0 00 20 33 01 00 71 00 33 57 F7   # Name Speaker (wire 57)
```

### Soft Knob 2

| Control          | `cmd` | `param` | Notes                                                                                                                                 |
| ---------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Function As…** | `71`  | `3F`    | Same destination list as Knob 1 (WAF80 **B#63** *Definable2 Single*)                                                                  |
| **Name**         | `71`  | `34`    | Wire byte per [Soft Knob Names](../parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off      |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (per destination)                                                                          |

```text
F0 00 20 33 01 00 71 00 3F 00 F7   # Knob 2 Function As Off
F0 00 20 33 01 00 71 00 3F 46 F7   # Velo > Volume (index 127)
F0 00 20 33 01 00 71 00 34 00 F7   # Name >Para
F0 00 20 33 01 00 71 00 34 01 F7   # Name +3rds
F0 00 20 33 01 00 71 00 34 47 F7   # Name Width
```

### Soft Knob 3

| Control          | `cmd` | `param` | Notes                                                                                                                                 |
| ---------------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Function As…** | `71`  | `40`    | Same destination list as Knob 1                                                                                                       |
| **Name**         | `71`  | `35`    | Wire byte per [Soft Knob Names](../parameter-options.md#soft-knob-names) (not list index); LCD label when **Function As…** ≠ Off      |
| *(runtime)*      | `71`  | *value* | Physical knob → destination **value** slot (per destination)                                                                          |

```text
F0 00 20 33 01 00 71 00 40 00 F7   # Knob 3 Function As Off
F0 00 20 33 01 00 71 00 40 46 F7   # Velo > Volume (index 127)
F0 00 20 33 01 00 71 00 35 00 F7   # Name >Para
F0 00 20 33 01 00 71 00 35 47 F7   # Name Width
```

### Soft-knob runtime: Distortion Intensity {#soft-knob-runtime-distortion-intensity}

Captured via **Soft Knob 1** sweep — same value param as
[EDIT FX → Distortion →
Intensity](effects.md#distortion-intensity-cmd0x71-param-0x65)
(**`71`/`65`**). **Type** is
[`71`/`64`](effects.md#distortion-type-cmd0x71-param-0x64).

When **Function As…** =
[Distortion Intensity](../parameter-options.md#soft-knob-destinations)
(wire
**`57`** on `71`/`3E`/`3F`/`40`), the knob sends **`71`/`65`**:

| UI        | `<value>` | Confirmed |
| --------- | --------- | --------- |
| 0 %       | `00`      | ✓         |
| 100.0 %   | `7F`      | ✓         |

**0.0..100.0 %** → `stored = round(pct × 127 / 100)` (endpoints **`00`** /
**`7F`**). Destination wire **`57`** ≠ value param **`65`**.

```text
F0 00 20 33 01 00 71 00 65 00 F7   # 0 % (soft knob)
F0 00 20 33 01 00 71 00 65 7F F7   # 100.0 % (soft knob)
```
