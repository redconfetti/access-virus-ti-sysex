# Modulators

Edit Single — **Modulators** (**EDIT LFO** on the panel; LFO 1–3 settings and
destination amounts) and **Modulation Matrix** (six slots).

**Modulation Matrix:** [mod-matrix.md](mod-matrix.md).

Part of [Documentation](../../../README.md#documentation). Enumerated options:
[parameter-options.md](../../reference/parameter-options.md).
Parameter map: [Single parameter map](../../dumps/single.md#lfo)
· Multi: [Edit Multi](../multis.md).

Paging: [virus.md](../../../misc/virus.md#paging) (`0x70` Page A, `0x71` Page B, `0x6E` part buffer, `0x6F` extended, `0x72` Multi). Param IDs depend on **`cmd`**.

Page **B#7–13** (*Lfo3* settings …) dump offsets: see
[Single parameter map — LFO](../../dumps/single.md#lfo).
Documented LFO settings: [LFO live edit routing](../../reference/parameter-options.md#lfo-live-edit-routing),
[LFO Clock](../../reference/parameter-options.md#lfo-clock),
[LFO Shape](../../reference/parameter-options.md#lfo-shape),
[LFO settings](../../reference/parameter-options.md#lfo-settings).

**Cmd byte:** LFO 1 settings use **`0x71`** (Page B). LFO 2 settings (except
**Clock**) use **`0x70`** (Page A). LFO 3 settings use **`0x71`** (Page B) at
params **`0x07`–`0x0A`** plus **Clock** **`0x15`**. See routing table.

**LCD:** **EDIT LFO** — per-LFO settings (**Rate**, **Clock**, **Shape**, …) and
separate **LFO Modulation** amount pages.

## LFO 1

**EDIT LFO → LFO 1**.

### Clock

**Live edit:** `cmd=0x71`, param `0x12`.

**EDIT LFO → LFO 1 → Clock**. Enum:
[LFO Clock](../../reference/parameter-options.md#lfo-clock) — knob minimum = **Off** (`00`);
then **1/64** … **16/1** (`01`–`15`).

| Item | Value |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 12 <value> F7` |

```text
F0 00 20 33 01 00 71 40 12 00 F7 # Off
F0 00 20 33 01 00 71 40 12 01 F7 # 1/64
F0 00 20 33 01 00 71 40 12 15 F7 # 16/1
```

**Rate** appears on the panel only when **Clock** = **Off** — see
[Rate](#rate).

### Rate

**Live edit:** `cmd=0x71`, param `0x43`.

**EDIT LFO → LFO 1 → Rate**. Visible when
[Clock](#clock) = **Off**. **`0`–`127`** →
`stored = lcd` — [LFO Rate](../../reference/parameter-options.md#lfo-rate).

| Item | Value |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 43 <value> F7` |

```text
F0 00 20 33 01 00 71 40 43 00 F7 # 0
F0 00 20 33 01 00 71 40 43 7F F7 # 127
```

### Shape

**Live edit:** `cmd=0x71`, param `0x44`.

**EDIT LFO → LFO 1 → Shape**. Enum:
[LFO Shape](../../reference/parameter-options.md#lfo-shape) — **`00`–`43`**
([Delay LFO Wave](../../reference/parameter-options.md#delay-lfo-1-wave-1) **`00`–`05`**, then
**Wave 3** … **Wave 64** at **`06`–`43`**).

| Item | Value |
| -------------- | ----------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 44 <value> F7` |

```text
F0 00 20 33 01 00 71 40 44 00 F7 # Sine
F0 00 20 33 01 00 71 40 44 01 F7 # Triangle
F0 00 20 33 01 00 71 40 44 0E F7 # Wave 11
F0 00 20 33 01 00 71 40 44 16 F7 # Wave 19
F0 00 20 33 01 00 71 40 44 23 F7 # Wave 32
F0 00 20 33 01 00 71 40 44 43 F7 # Wave 64
```

### Contour

**Live edit:** `cmd=0x71`, param `0x47`.

**EDIT LFO → LFO 1 → Contour**. Bipolar
**`−64..+63`** → `stored = ui + 64` — [LFO settings → Contour](../../reference/parameter-options.md#contour-1).

| Item | Value |
| -------------- | -------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 47 <value> F7` |

```text
F0 00 20 33 01 00 71 40 47 00 F7 # −64
F0 00 20 33 01 00 71 40 47 40 F7 # 0
F0 00 20 33 01 00 71 40 47 7F F7 # +63
```

### Mode

**Live edit:** `cmd=0x71`, param `0x46`.

**EDIT LFO → LFO 1 → Mode**. Enum: [LFO settings → Mode](../../reference/parameter-options.md#mode-0x46).

| Item | Value |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 46 <value> F7` |

```text
F0 00 20 33 01 00 71 40 46 00 F7 # Poly
F0 00 20 33 01 00 71 40 46 01 F7 # Mono
```

### Envelope Mode

**Live edit:** `cmd=0x71`, param `0x45`.

**EDIT LFO → LFO 1 → Envelope Mode**. Enum:
[LFO settings → Envelope Mode](../../reference/parameter-options.md#envelope-mode-1).

| Item | Value |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 45 <value> F7` |

```text
F0 00 20 33 01 00 71 40 45 00 F7 # Off
F0 00 20 33 01 00 71 40 45 01 F7 # On
```

### Trigger Phase

**Live edit:** `cmd=0x71`, param `0x49`.

**EDIT LFO → LFO 1 → Trigger Phase**. **`00`** = **Off**; **`01`–`7F`** = phase
**1** … **127** — [LFO settings → Trigger Phase](../../reference/parameter-options.md#trigger-phase-1).

| Item | Value |
| -------------- | --------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 49 <value> F7` |

```text
F0 00 20 33 01 00 71 40 49 00 F7 # Off
F0 00 20 33 01 00 71 40 49 01 F7 # 1
F0 00 20 33 01 00 71 40 49 7F F7 # 127
```

### Key Follow

**Live edit:** `cmd=0x71`, param `0x48`.

**EDIT LFO → LFO 1 → Key Follow**. **`00`** = **Off**; **`01`–`7F`** =
**0.8..100.0 %** — [LFO settings → Key Follow](../../reference/parameter-options.md#key-follow-0x48).

| Item | Value |
| -------------- | ----------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 48 <value> F7` |

```text
F0 00 20 33 01 00 71 40 48 00 F7 # Off
F0 00 20 33 01 00 71 40 48 01 F7 # 0.8 %
F0 00 20 33 01 00 71 40 48 7F F7 # 100.0 %
```

| Panel control | Live edit | Status |
| ---------------- | ------------- | ---------------------------------------------------------------------- |
| Rate | `71` / `0x43` | ✓ — [Rate](#rate) ( **Clock** = **Off** only) |
| Clock Divider | `71` / `0x12` | ✓ — [Clock](#clock) (minimum = **Off**) |
| Keyfollow | `71` / `0x48` | ✓ — [Key Follow](#key-follow) |
| Trigger Phase | `71` / `0x49` | ✓ — [Trigger Phase](#trigger-phase) |
| Waveform Shape | `71` / `0x44` | ✓ — [Shape](#shape) |
| Waveform Contour | `71` / `0x47` | ✓ — [Contour](#contour) |
| Mode | `71` / `0x46` | ✓ — [Mode](#mode) |
| Envelope Mode | `71` / `0x45` | ✓ — [Envelope Mode](#envelope-mode) |

### LFO 1 Destination

**EDIT LFO → LFO 1 → LFO 1 Destination** — [LFO 1 Destination](../../reference/parameter-options.md#lfo-1-destination-1).

| Panel control | Live edit | Status |
| ------------- | ------------------ | --------------------------------------------------------------- |
| Osc 1 Pitch | `70` / `0x4A` | ✓ |
| Osc 2 Pitch | `70` / `0x4B` | ✓ |
| Osc 1+2 Pitch | `70` / `4A` + `4B` | ✓ linked (same value to both) |
| Pulse Width | `70` / `0x4C` | ✓ |
| Resonance | `70` / `0x4D` | ✓ |
| Filter Gain | `70` / `0x4E` | ✓ |
| Assign Target | `71` / `0x4F` | ✓ — [Assign Target](../../reference/parameter-options.md#assign-target) |
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
bytes: [LFO live edit routing](../../reference/parameter-options.md#lfo-live-edit-routing).

| Panel control | Live edit | Status |
| ---------------- | ------------- | -------------------------------------------------- |
| Rate | `70` / `0x4F` | ✓ (**Clock** = **Off** only) |
| Clock Divider | `71` / `0x13` | ✓ — [LFO Clock](../../reference/parameter-options.md#lfo-clock) |
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

### LFO 2 Destination

**EDIT LFO → LFO 2 → LFO 2 Destination** — [LFO 2 Destination](../../reference/parameter-options.md#lfo-2-destination-1).

| Panel control | Live edit | Status |
| ------------- | ------------------ | --------------------------------------------------------------- |
| Cutoff 1 | `70` / `0x58` | ✓ |
| Cutoff 2 | `70` / `0x59` | ✓ |
| Cutoff 1+2 | `70` / `58` + `59` | ✓ linked (same value to both) |
| Shape 1+2 | `70` / `0x56` | ✓ |
| FM Amount | `70` / `0x57` | ✓ |
| Panorama | `70` / `0x5A` | ✓ |
| Assign Target | `71` / `0x51` | ✓ — [Assign Target](../../reference/parameter-options.md#assign-target-1) |
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
Trigger Phase. [Routing table](../../reference/parameter-options.md#lfo-live-edit-routing).

| Panel control | Live edit | Status |
| -------------- | ------------- | -------------------------------------------------- |
| Rate | `71` / `0x07` | ✓ (**Clock** = **Off** only) |
| Clock Divider | `71` / `0x15` | ✓ — [LFO Clock](../../reference/parameter-options.md#lfo-clock) |
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

### LFO 3 Destination

**EDIT LFO → LFO 3 → LFO 3 Destination** sub-menu. All **`cmd=0x71`** — see
[LFO 3 Destination](../../reference/parameter-options.md#lfo-3-destination-1).

| Panel control | Live edit | Status |
| ------------- | ------------- | ------ |
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
