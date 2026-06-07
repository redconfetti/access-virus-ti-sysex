# Modulators

Edit Single — **Modulators** (**EDIT LFO** on the panel; LFO 1–3 settings and
modulation amounts).

Part of [Live Edit](README.md). Enumerated options:
[parameter-options.md](../parameter-options.md).
Dump worksheet: [Single parameter map](../dumps/single.md#lfo)
· Multi: [Edit Multi](edit-multi.md).

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7 # multi / common (some params)
F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B single (some params)
F0 00 20 33 01 00 70 <part> <param> <value> F7 # Page A single (when global Page A = SysEx)
F0 00 20 33 01 00 6E <part> <param> <value> F7 # part single edit buffer
```

Param IDs are **not global** — the same hex ID can mean different settings under
different `cmd` bytes.

Page **B#7–13** (*Lfo3* settings …) remain **TBD** for dump correlation.
Documented LFO settings: [LFO live edit routing](../parameter-options.md#lfo-live-edit-routing),
[LFO Clock](../parameter-options.md#lfo-clock),
[LFO Shape](../parameter-options.md#lfo-shape),
[LFO settings](../parameter-options.md#lfo-settings).

**Cmd byte:** LFO 1 settings use **`0x71`** (Page B). LFO 2 settings (except
**Clock**) use **`0x70`** (Page A). LFO 3 settings use **`0x71`** (Page B) at
params **`0x07`–`0x0A`** plus **Clock** **`0x15`**. See routing table.

## Panel reference

**LCD:** **EDIT LFO** — per-LFO settings (**Rate**, **Clock**, **Shape**, …) and
separate **LFO Modulation** amount pages. Inventory rows:
[single.md — LFO](../dumps/single.md#lfo).

Capture path: **`LFO n` / control → LCD value**. Use **+/−** when possible. Knob
sweeps: use the **last** SysEx line of a burst.

### SELECT

**TBD** — confirm whether **EDIT LFO** has a front-panel **SELECT** (LFO 1 / 2 /
3) with live SysEx, as on **OSCILLATORS** / **FILTERS** / **EFFECTS**.

## LFO 1

**EDIT LFO → LFO 1**. Settings rows from the worksheet (capture order):

### Clock (`cmd=0x71`, param `0x12`) {#lfo-1-clock-cmd0x71-param-0x12}

**EDIT LFO → LFO 1 → Clock** (worksheet **Clock Divider**). Enum:
[LFO Clock](../parameter-options.md#lfo-clock) — knob minimum = **Off** (`00`);
then **1/64** … **16/1** (`01`–`15`).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 12 <value> F7` |
| Confirmed | Hardware TX (TI mk2; all **22** menu rows) |

```text
F0 00 20 33 01 00 71 40 12 00 F7 # Off
F0 00 20 33 01 00 71 40 12 01 F7 # 1/64
F0 00 20 33 01 00 71 40 12 15 F7 # 16/1
```

**Rate** appears on the panel only when **Clock** = **Off** — see
[Rate](#lfo-1-rate-cmd0x71-param-0x43).

### Rate (`cmd=0x71`, param `0x43`) {#lfo-1-rate-cmd0x71-param-0x43}

**EDIT LFO → LFO 1 → Rate** (worksheet **LFO 1 Rate**). Visible when
[Clock](#lfo-1-clock-cmd0x71-param-0x12) = **Off**. **`0`–`127`** →
`stored = lcd` — [LFO Rate](../parameter-options.md#lfo-rate).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 43 <value> F7` |
| Confirmed | Hardware TX (TI mk2; endpoints **`00`**, **`7F`**) |

```text
F0 00 20 33 01 00 71 40 43 00 F7 # 0
F0 00 20 33 01 00 71 40 43 7F F7 # 127
```

### Shape (`cmd=0x71`, param `0x44`) {#lfo-1-shape-cmd0x71-param-0x44}

**EDIT LFO → LFO 1 → Shape** (worksheet **Waveform Shape**). Enum:
[LFO Shape](../parameter-options.md#lfo-shape) — **`00`–`43`**
([Delay LFO Wave](../parameter-options.md#delay-lfo-wave) **`00`–`05`**, then
**Wave 3** … **Wave 64** at **`06`–`43`**).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 44 <value> F7` |
| Confirmed | Hardware TX (TI mk2; endpoints + Wave 11/19/32) |

```text
F0 00 20 33 01 00 71 40 44 00 F7 # Sine
F0 00 20 33 01 00 71 40 44 01 F7 # Triangle
F0 00 20 33 01 00 71 40 44 0E F7 # Wave 11
F0 00 20 33 01 00 71 40 44 16 F7 # Wave 19
F0 00 20 33 01 00 71 40 44 23 F7 # Wave 32
F0 00 20 33 01 00 71 40 44 43 F7 # Wave 64
```

### Contour (`cmd=0x71`, param `0x47`) {#lfo-1-contour-cmd0x71-param-0x47}

**EDIT LFO → LFO 1 → Contour** (worksheet **Waveform Contour**). Bipolar
**`−64..+63`** → `stored = ui + 64` — [LFO settings → Contour](../parameter-options.md#contour-0x47).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 47 <value> F7` |
| Confirmed | Hardware TX (TI mk2; endpoints **`00`**, **`7F`**) |

```text
F0 00 20 33 01 00 71 40 47 00 F7 # −64
F0 00 20 33 01 00 71 40 47 40 F7 # 0
F0 00 20 33 01 00 71 40 47 7F F7 # +63
```

### Mode (`cmd=0x71`, param `0x46`) {#lfo-1-mode-cmd0x71-param-0x46}

**EDIT LFO → LFO 1 → Mode**. Enum: [LFO settings → Mode](../parameter-options.md#mode-0x46).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 46 <value> F7` |
| Confirmed | Hardware TX (TI mk2) |

```text
F0 00 20 33 01 00 71 40 46 00 F7 # Poly
F0 00 20 33 01 00 71 40 46 01 F7 # Mono
```

### Envelope Mode (`cmd=0x71`, param `0x45`) {#lfo-1-envelope-mode-cmd0x71-param-0x45}

**EDIT LFO → LFO 1 → Envelope Mode** (worksheet toggle). Enum:
[LFO settings → Envelope Mode](../parameter-options.md#envelope-mode-0x45).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 45 <value> F7` |
| Confirmed | Hardware TX (TI mk2) |

```text
F0 00 20 33 01 00 71 40 45 00 F7 # Off
F0 00 20 33 01 00 71 40 45 01 F7 # On
```

### Trigger Phase (`cmd=0x71`, param `0x49`) {#lfo-1-trigger-phase-cmd0x71-param-0x49}

**EDIT LFO → LFO 1 → Trigger Phase**. **`00`** = **Off**; **`01`–`7F`** = phase
**1** … **127** — [LFO settings → Trigger Phase](../parameter-options.md#trigger-phase-0x49).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 49 <value> F7` |
| Confirmed | Hardware TX (TI mk2; **Off**, **1**, **127**) |

```text
F0 00 20 33 01 00 71 40 49 00 F7 # Off
F0 00 20 33 01 00 71 40 49 01 F7 # 1
F0 00 20 33 01 00 71 40 49 7F F7 # 127
```

### Key Follow (`cmd=0x71`, param `0x48`) {#lfo-1-key-follow-cmd0x71-param-0x48}

**EDIT LFO → LFO 1 → Key Follow**. **`00`** = **Off**; **`01`–`7F`** =
**0.8..100.0 %** — [LFO settings → Key Follow](../parameter-options.md#key-follow-0x48).

| Item | Value |
| --- | --- |
| Message format | `F0 00 20 33 01 00 71 <part> 48 <value> F7` |
| Confirmed | Hardware TX (TI mk2; **Off**, **0.8 %**, **100.0 %**) |

```text
F0 00 20 33 01 00 71 40 48 00 F7 # Off
F0 00 20 33 01 00 71 40 48 01 F7 # 0.8 %
F0 00 20 33 01 00 71 40 48 7F F7 # 100.0 %
```

| Panel control | Live edit | Status |
| --- | --- | --- |
| Rate | `71` / `0x43` | ✓ — [Rate](#lfo-1-rate-cmd0x71-param-0x43) ( **Clock** = **Off** only) |
| Clock Divider | `71` / `0x12` | ✓ — [Clock](#lfo-1-clock-cmd0x71-param-0x12) (minimum = **Off**) |
| Keyfollow | `71` / `0x48` | ✓ — [Key Follow](#lfo-1-key-follow-cmd0x71-param-0x48) |
| Trigger Phase | `71` / `0x49` | ✓ — [Trigger Phase](#lfo-1-trigger-phase-cmd0x71-param-0x49) |
| Waveform Shape | `71` / `0x44` | ✓ — [Shape](#lfo-1-shape-cmd0x71-param-0x44) |
| Waveform Contour | `71` / `0x47` | ✓ — [Contour](#lfo-1-contour-cmd0x71-param-0x47) |
| Mode | `71` / `0x46` | ✓ — [Mode](#lfo-1-mode-cmd0x71-param-0x46) |
| Envelope Mode | `71` / `0x45` | ✓ — [Envelope Mode](#lfo-1-envelope-mode-cmd0x71-param-0x45) |

### LFO 1 Destination {#lfo-1-destination}

**EDIT LFO → LFO 1 → LFO 1 Destination** — [LFO 1 Destination](../parameter-options.md#lfo-1-destination).

| Panel control | Live edit | Status |
| --- | --- | --- |
| Osc 1 Pitch | `70` / `0x4A` | ✓ |
| Osc 2 Pitch | `70` / `0x4B` | ✓ |
| Osc 1+2 Pitch | `70` / `4A` + `4B` | ✓ linked (same value to both) |
| Pulse Width | `70` / `0x4C` | ✓ |
| Resonance | `70` / `0x4D` | ✓ |
| Filter Gain | `70` / `0x4E` | ✓ |
| Assign Target | `71` / `0x4F` | ✓ — [Assign Target](../parameter-options.md#assign-target-0x4f) |
| Amount | `71` / `0x50` | ✓ |

```text
F0 00 20 33 01 00 70 40 4A 43 F7 # Osc 1 Pitch +4.7 %
F0 00 20 33 01 00 70 40 4B 43 F7 # Osc 2 Pitch +4.7 % (linked)
F0 00 20 33 01 00 71 40 4F 00 F7 # Assign Target Off
F0 00 20 33 01 00 71 40 50 40 F7 # Amount +0.0 %
```

## LFO 2

**EDIT LFO → LFO 2** — same panel settings and value encodings as LFO 1.
**Clock** uses **`cmd=0x71`**; all other settings use **`cmd=0x70`**. Param
bytes: [LFO live edit routing](../parameter-options.md#lfo-live-edit-routing).

| Panel control | Live edit | Status |
| --- | --- | --- |
| Rate | `70` / `0x4F` | ✓ (**Clock** = **Off** only) |
| Clock Divider | `71` / `0x13` | ✓ — [LFO Clock](../parameter-options.md#lfo-clock) |
| Keyfollow | `70` / `0x54` | ✓ |
| Trigger Phase | `70` / `0x55` | ✓ |
| Waveform Shape | `70` / `0x50` | ✓ |
| Waveform Contour | `70` / `0x53` | ✓ |
| Mode | `70` / `0x52` | ✓ |
| Envelope Mode | `70` / `0x51` | ✓ |

```text
F0 00 20 33 01 00 71 40 13 00 F7 # Clock Off
F0 00 20 33 01 00 71 40 13 05 F7 # Clock 1/4
F0 00 20 33 01 00 71 40 13 15 F7 # Clock 16/1
F0 00 20 33 01 00 70 40 4F 00 F7 # Rate 0
F0 00 20 33 01 00 70 40 50 00 F7 # Shape Sine
F0 00 20 33 01 00 70 40 51 00 F7 # Envelope Mode Off
F0 00 20 33 01 00 70 40 52 00 F7 # Mode Poly
F0 00 20 33 01 00 70 40 53 00 F7 # Contour −64
F0 00 20 33 01 00 70 40 54 00 F7 # Key Follow Off
F0 00 20 33 01 00 70 40 55 00 F7 # Trigger Phase Off
```

### LFO 2 Destination {#lfo-2-destination}

**EDIT LFO → LFO 2 → LFO 2 Destination** — [LFO 2 Destination](../parameter-options.md#lfo-2-destination).

| Panel control | Live edit | Status |
| --- | --- | --- |
| Cutoff 1 | `70` / `0x58` | ✓ |
| Cutoff 2 | `70` / `0x59` | ✓ |
| Cutoff 1+2 | `70` / `58` + `59` | ✓ linked (same value to both) |
| Shape 1+2 | `70` / `0x56` | ✓ |
| FM Amount | `70` / `0x57` | ✓ |
| Panorama | `70` / `0x5A` | ✓ |
| Assign Target | `71` / `0x51` | ✓ — [Assign Target](../parameter-options.md#assign-target-0x51) |
| Amount | `71` / `0x52` | ✓ |

```text
F0 00 20 33 01 00 70 40 58 53 F7 # Cutoff 1 +29.7 %
F0 00 20 33 01 00 70 40 59 53 F7 # Cutoff 2 +29.7 % (linked)
F0 00 20 33 01 00 71 40 51 00 F7 # Assign Target Off
F0 00 20 33 01 00 71 40 52 40 F7 # Amount +0.0 %
```

## LFO 3

**EDIT LFO → LFO 3** — compact settings page on **`cmd=0x71`**. Same **value**
encodings as LFO 1/2 where controls exist. **No** Envelope Mode, Contour, or
Trigger Phase. [Routing table](../parameter-options.md#lfo-live-edit-routing).

| Panel control | Live edit | Status |
| --- | --- | --- |
| Rate | `71` / `0x07` | ✓ (**Clock** = **Off** only) |
| Clock Divider | `71` / `0x15` | ✓ — [LFO Clock](../parameter-options.md#lfo-clock) |
| Keyfollow | `71` / `0x0A` | ✓ |
| Waveform Shape | `71` / `0x08` | ✓ |
| Mode | `71` / `0x09` | ✓ |

```text
F0 00 20 33 01 00 71 40 15 00 F7 # Clock Off
F0 00 20 33 01 00 71 40 15 05 F7 # Clock 1/4
F0 00 20 33 01 00 71 40 15 15 F7 # Clock 16/1
F0 00 20 33 01 00 71 40 07 00 F7 # Rate 0
F0 00 20 33 01 00 71 40 08 00 F7 # Shape Sine
F0 00 20 33 01 00 71 40 09 00 F7 # Mode Poly
F0 00 20 33 01 00 71 40 0A 00 F7 # Key Follow Off
```

### LFO 3 Destination {#lfo-3-destination}

**EDIT LFO → LFO 3 → LFO 3 Destination** sub-menu. All **`cmd=0x71`** — see
[LFO 3 Destination](../parameter-options.md#lfo-3-destination).

| Panel control | Live edit | Status |
| --- | --- | --- |
| Assign Target | `71` / `0x0B` | ✓ |
| Amount | `71` / `0x0C` | ✓ |
| Fade In | `71` / `0x0D` | ✓ |

```text
F0 00 20 33 01 00 71 40 0B 00 F7 # Assign Target Osc 1 Pitch
F0 00 20 33 01 00 71 40 0B 06 F7 # Assign Target Sync Phase
F0 00 20 33 01 00 71 40 0C 00 F7 # Amount 0 %
F0 00 20 33 01 00 71 40 0C 7F F7 # Amount 100.0 %
F0 00 20 33 01 00 71 40 0D 00 F7 # Fade In 0
F0 00 20 33 01 00 71 40 0D 7F F7 # Fade In 127
```
