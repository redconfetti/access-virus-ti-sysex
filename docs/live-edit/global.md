# Global Live Edit

Global and CONFIG-menu SysEx (**`cmd=0x73`**, MIDI setup, system toggles). Part
of [Documentation](../../README.md#documentation).

```text
F0 00 20 33 01 <device_id> 73 00 <param> <value> F7
```

Menus: **System**, **Random PG**, **MIDI**, **Receive/Transmit MIDI Dump**,
**MIDI Control**, **Inputs 1/2**, **Audio Clock**, **Soft Knob** global
behavior, **Knob Behavior**, **Global Tuning** — plus device-wide **`cmd=0x73`**
parameters below.

Patch-level **Inputs** (Atomizer / Input Mode / Input Select) are under [Edit
Single → Inputs](#inputs-edit-single) when editing a Single program.

---

## Inputs (Edit Single)

**Edit Single → Inputs.** Live edit uses **`cmd=0x6F`** ([extended page](../misc/virus.md#live-edit-command-bytes)),
part **`00`**. Legacy **Input Mode** / **Input Select** on Page A (**CC 101** /
**102**) may apply when [MIDI Controller Page A](../misc/virus.md#midi-controller-page-a) =
**Controller Data**.

**Panel visibility**

| Control          | Visible when                                                     |
| ---------------- | ---------------------------------------------------------------- |
| **Atomizer**     | Always                                                           |
| **Input Mode**   | **Atomizer** = **Off** (`7E` = `00`)                             |
| **Input Select** | **Input Mode** = **Dynamic** or **Static** (`7C` = `01` or `02`) |

### Atomizer

**Live edit:** `cmd=0x6F`, param `0x7E`.

**Atomizer** is a **beat-synced instant looper**
on
external audio at the Virus inputs. Incoming audio passes **dry** to the outputs
until you trigger a **loop/buffer key**; a slice captured at that moment is
**looped** at the rate for the key you hold. While the key is down you hear only
the loop; on release you hear **dry** again. The source stream keeps running in
real time underneath — you are **replacing stretches of the input with looped
slices of itself**. Loop lengths run from about **½ note** (shortest named
division) down through **1/32** and smaller slices that can sound like pitched
tones.

The **Inputs → Atomizer** menu value selects the feature state / preset index on
the wire (not individual loop keys — those are played on the keyboard). Panel
labels **2**–**16** are stored **`02`–`10`**.

Enum: [Atomizer preset](../reference/parameter-options.md#atomizer-preset)
(`00`–`10`).

```text
F0 00 20 33 01 00 6F 00 7E 00 F7 # Atomizer Off
F0 00 20 33 01 00 6F 00 7E 01 F7 # Atomizer On
F0 00 20 33 01 00 6F 00 7E 10 F7 # Atomizer 16
```

### Input Mode

**Live edit:** `cmd=0x6F`, param `0x7C`.

Enum: [Input Mode](../reference/parameter-options.md#input-mode).

```text
F0 00 20 33 01 00 6F 00 7C 00 F7 # Input Mode Off
F0 00 20 33 01 00 6F 00 7C 01 F7 # Input Mode Dynamic
F0 00 20 33 01 00 6F 00 7C 02 F7 # Input Mode Static
```

### Input Select

**Live edit:** `cmd=0x6F`, param `0x7D`.

Enum: [Input Select](../reference/parameter-options.md#input-select).

```text
F0 00 20 33 01 00 6F 00 7D 00 F7 # Input Select Left
F0 00 20 33 01 00 6F 00 7D 01 F7 # Input Select L + R
F0 00 20 33 01 00 6F 00 7D 02 F7 # Input Select Right
```

---

## Global parameters

**Live edit:** `cmd=0x73`.

Device-wide settings — not Multi **`0x72`** or part sound **`0x6E`**.

The byte **`<device_id>`** (immediately before **`0x73`**) is the SysEx
**destination device ID**. The Virus only acts on the message when this
matches its configured **MIDI Device ID** (CONFIG).

At least **All Delays** (`0x1B`) is **transmitted by the Virus** when
changed on the front panel. Many other **`0x73`** globals are **RX only**
(host → synth); the panel does not emit SysEx when they are edited — see
[Knob Response](#knob-response) and [CONFIG → Inputs / USB (RX only)](#config--inputs--usb-rx-only).

## Summary

| Param ID | Parameter              | Value encoding                                                        |
| -------- | ---------------------- | --------------------------------------------------------------------- |
| `0x09`   | USB Audio Mode         | See [USB Audio Mode](#usb-audio-mode)                                 |
| `0x10`   | Edit mode / focus      | See [Edit mode 0x10](#edit-mode-0x10)                                 |
| `0x19`   | All EQs                | See [All EQs](#all-eqs)                                               |
| `0x1A`   | All Arpeggiators       | See [All Arpeggiators](#all-arpeggiators)                             |
| `0x1B`   | All Delays             | See [All Delays](#all-delays)                                         |
| `0x1C`   | All Reverbs            | See [All Reverbs](#all-reverbs)                                       |
| `0x1D`   | Input Characteristic   | See [Input Characteristic](#input-characteristic)                     |
| `0x1F`   | Input Sensitivity      | See [Input Sensitivity](#input-sensitivity)                           |
| `0x28`   | Navigation             | See [Navigation](#navigation) — **`73 40`** scope byte                |
| `0x29`   | Value Wrapping         | See [Value Wrapping](#value-wrapping)                                 |
| `0x2B`   | Input Source           | See [Input Source](#input-source)                                     |
| `0x32`   | BPM Brightness         | See [BPM Brightness](#bpm-brightness)                                 |
| `0x33`   | LED Lux                | See [LED Lux](#led-lux)                                               |
| `0x35`   | Random PG — Scope      | See [Randomize Scope](#randomize-scope)                               |
| `0x36`   | Random PG — Strength   | See [Randomize Strength](#randomize-strength)                         |
| `0x55`   | Global Program Change  | See [Global Program Change](#global-program-change)                   |
| `0x57`   | Global MIDI Volume RX  | See [Global MIDI Volume RX](#global-midi-volume-rx)                   |
| `0x5A`   | Input Direct Thru      | See [Input Direct Thru](#input-direct-thru)                           |
| `0x5B`   | Input Boost            | See [Input Boost](#input-boost)                                       |
| `0x5D`   | MIDI Device ID         | See [MIDI Device ID](#midi-device-id)                                 |
| `0x5E`   | MIDI Controller Page A | See [MIDI Controller Page A](../misc/virus.md#midi-controller-page-a) |
| `0x5F`   | MIDI Controller Page B | See [MIDI Controller Page B](../misc/virus.md#midi-controller-page-b) |
| `0x60`   | Global ARP Note Send   | See [Global ARP Note Send](#global-arp-note-send)                     |
| `0x6A`   | MIDI Clock             | See [MIDI Clock](#midi-clock)                                         |
| `0x75`   | Knob Response          | See [Knob Response](#knob-response)                                   |
| `0x76`   | Memory Protect         | See [Memory Protect](#memory-protect)                                 |
| `0x7A`   | Play mode              | See [Play mode](#play-mode)                                           |
| `0x7C`   | Global MIDI Channel    | See [Global MIDI Channel](#global-midi-channel)                       |
| `0x7D`   | LED Mode               | See [LED Mode](#led-mode)                                             |
| `0x7E`   | LCD Contrast           | See [LCD Contrast](#lcd-contrast)                                     |

## Parameters

### Edit mode 0x10

**Live edit:** `cmd=0x73`, param `0x10` — **synth → host only** (not host → synth).

**Not** a sound parameter. The Virus sends **`cmd=0x73`**, param **`0x10`**
when the **front-panel mode** or **multi program selection** changes. The
byte after **`0x73`** mirrors live-edit **scope** (`0x00` vs **`0x40`**
Single buffer) used on **`0x70`** / **`0x72`** / **`0x6E`**.

| Message (hex body)   | Observed when                                                                                         |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| `… 73 00 10 00`      | Selecting multis from **Multi bank** (e.g. #31, then **#32 INIT MULTI**) — sent **twice** on one load |
| `… 73 40 10 00`      | Pressing **SINGLE** (leave Multi-focused UI for Single edit)                                          |
| `F0 F7` only (empty) | **MULTI+SINGLE** (Sequencer) and some **MULTI** presses — no data bytes                               |

```text
F0 00 20 33 01 00 73 00 10 00 F7 # Multi / multi-bank context
F0 00 20 33 01 00 73 40 10 00 F7 # Single-buffer scope 0x40
```

For **host → synth** mode selection, use [Play mode (`0x7A`)](#play-mode)
instead.

### Play mode

**Live edit:** `cmd=0x73`, param `0x7A`.

**EDIT CONFIG → System → Play mode** — **Single**, **Sequencer** (**MULTI+SINGLE**),
or **Multi**. Host sends **`cmd=0x73`**, param **`0x7A`**, value below.

**Not** the same param byte under other commands — e.g. **FILTERS SELECT**
uses **`71`/`7A`**, Filter Common **Pan Spread** uses **`6E`/`7A`**.

| `<value>` | Mode       | Panel label        |
| --------- | ---------- | ------------------ |
| `00`      | Single     | **SINGLE**         |
| `01`      | Sequencer  | **MULTI+SINGLE**   |
| `02`      | Multi      | **MULTI**          |

```text
F0 00 20 33 01 00 73 00 7A 00 F7 # Single
F0 00 20 33 01 00 73 00 7A 01 F7 # Sequencer (MULTI+SINGLE)
F0 00 20 33 01 00 73 00 7A 02 F7 # Multi
```

Panel mode changes may also emit **`73 … 10 …`** — see
[Edit mode `0x10`](#edit-mode-0x10) (synth → host).

### All EQs

**Live edit:** `cmd=0x73`, param `0x19`.

**EDIT CONFIG → System → All EQs** — global EQ bypass on/off.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 19 00 F7

# Enabled
F0 00 20 33 01 00 73 00 19 01 F7
```

### All Arpeggiators

**Live edit:** `cmd=0x73`, param `0x1A`.

**EDIT CONFIG → System → All Arpeggiators** — global arpeggiator bypass on/off.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 1A 00 F7

# Enabled
F0 00 20 33 01 00 73 00 1A 01 F7
```

### All Delays

**Live edit:** `cmd=0x73`, param `0x1B`.

**EDIT CONFIG → System → All Delays** — global delay bypass on/off. The Virus
may transmit this message (**synth → host**) when the setting is changed on the
front panel.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 1B 00 F7

# Enabled
F0 00 20 33 01 00 73 00 1B 01 F7
```

### All Reverbs

**Live edit:** `cmd=0x73`, param `0x1C`.

**EDIT CONFIG → System → All Reverbs** — global reverb bypass on/off.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 1C 00 F7

# Enabled
F0 00 20 33 01 00 73 00 1C 01 F7
```

### Navigation

**Live edit:** `cmd=0x73`, param `0x28`.

**EDIT CONFIG → System → Navigation** — how the front panel steps through
parameter pages (**By Page** vs **By Parameter**).

Unlike most globals in this doc, the byte after **`0x73`** is **`0x40`**
(not **`0x00`**) — same **scope** prefix as [Edit mode `0x10`](#edit-mode-0x10):

```text
F0 00 20 33 01 <device_id> 73 40 28 <value> F7
```

| Value | Panel            |
| ----- | ---------------- |
| `00`  | **By Page**      |
| `01`  | **By Parameter** |

```text
F0 00 20 33 01 00 73 40 28 00 F7 # By Page
F0 00 20 33 01 00 73 40 28 01 F7 # By Parameter
```

### Value Wrapping

**Live edit:** `cmd=0x73`, param `0x29`.

**EDIT CONFIG → System → Value Wrapping** — whether encoder/knob values
**wrap** at min/max or **stop** at the limit.

Standard global layout: **`73 00 29 <value>`**.

| Value | Panel   |
| ----- | ------- |
| `00`  | **Off** |
| `01`  | **On**  |

```text
F0 00 20 33 01 00 73 00 29 00 F7 # Off
F0 00 20 33 01 00 73 00 29 01 F7 # On
```

### BPM Brightness

**Live edit:** `cmd=0x73`, param `0x32`.

**EDIT CONFIG → System → BPM Brightness** — BPM display brightness (**0%**–**100%**).
Same encoding as [LED Lux](#led-lux): direct 7-bit `0x00`–`0x7F`,

```text
stored = min(0x7F, round(percent × 128 / 100))
```

| LCD    | `<value>` |
| ------ | --------- |
| 0%     | `00`      |
| 0.8%   | `01`      |
| 1.6%   | `02`      |
| 64.1%  | `52`      |
| 98.4%  | `7E`      |
| 100.0% | `7F`      |

```text
F0 00 20 33 01 00 73 00 32 00 F7 # 0%
F0 00 20 33 01 00 73 00 32 01 F7 # 0.8%
F0 00 20 33 01 00 73 00 32 02 F7 # 1.6%
F0 00 20 33 01 00 73 00 32 52 F7 # 64.1%
F0 00 20 33 01 00 73 00 32 7E F7 # 98.4%
F0 00 20 33 01 00 73 00 32 7F F7 # 100%
```

### LED Lux

**Live edit:** `cmd=0x73`, param `0x33`.

Front-panel **LED** brightness (**0%**–**100%**). Direct 7-bit value
`0x00`–`0x7F`:

```text
stored = min(0x7F, round(percent × 128 / 100))
```

LCD **`100.0%`** = **`0x7F`**. Examples:

| LCD    | `<value>` |
| ------ | --------- |
| 0%     | `00`      |
| 21.1%  | `1B`      |
| 24.2%  | `1F`      |
| 71.9%  | `5C`      |
| 100.0% | `7F`      |

```text
F0 00 20 33 01 00 73 00 33 00 F7 # 0%
F0 00 20 33 01 00 73 00 33 1B F7 # 21.1%
F0 00 20 33 01 00 73 00 33 1F F7 # 24.2%
F0 00 20 33 01 00 73 00 33 5C F7 # 71.9%
F0 00 20 33 01 00 73 00 33 7F F7 # 100%
```

### Randomize Scope

**Live edit:** `cmd=0x73`, param `0x35`.

**EDIT CONFIG → Random PG → Scope**. How much of the program is affected when
randomizing. **0.0..100.0 %** — same 7-bit encoding as
[BPM Brightness](#bpm-brightness) (`00` = 0%, `7F` = 100.0%).

| LCD    | `<value>` |
| ------ | --------- |
| 0.0%   | `00`      |
| 50.0%  | `40`      |
| 100.0% | `7F`      |

```text
F0 00 20 33 01 00 73 00 35 00 F7 # 0 %
F0 00 20 33 01 00 73 00 35 40 F7 # 50.0 %
F0 00 20 33 01 00 73 00 35 7F F7 # 100.0 %
```

### Randomize Strength

**Live edit:** `cmd=0x73`, param `0x36`.

**EDIT CONFIG → Random PG → Strength**. Randomization intensity.
**0.0..100.0 %** — same encoding as [Scope](#randomize-scope).

| LCD    | `<value>` |
| ------ | --------- |
| 0.0%   | `00`      |
| 50.0%  | `40`      |
| 100.0% | `7F`      |

```text
F0 00 20 33 01 00 73 00 36 00 F7 # 0 %
F0 00 20 33 01 00 73 00 36 40 F7 # 50.0 %
F0 00 20 33 01 00 73 00 36 7F F7 # 100.0 %
```

### Global Program Change

**Live edit:** `cmd=0x73`, param `0x55`.

**EDIT CONFIG → MIDI → Program Change** — global Program Change receive.
Distinct from per-part **Program Change** in Edit Multi (packed flag at `0xF8 + part` in Multi Dump).

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 55 00 F7

# Enabled
F0 00 20 33 01 00 73 00 55 01 F7
```

### Global MIDI Volume RX

**Live edit:** `cmd=0x73`, param `0x57`.

**EDIT CONFIG → MIDI → MIDI Volume** (global CC#7 receive). **`cmd=0x73`**, part
**`00`**. **Host → synth only.**
**Not** in **Single Dump**. Distinct from per-part **Volume RX** in Edit Multi
(packed flag at `0xF8 + part` in Multi Dump).

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
F0 00 20 33 01 00 73 00 57 00 F7 # Disabled
F0 00 20 33 01 00 73 00 57 01 F7 # Enabled
```

### MIDI Device ID

**Live edit:** `cmd=0x73`, param `0x5D`.

**EDIT CONFIG → MIDI → MIDI Device ID** (**1–16**, or **Omni**).

The synth **accepts** `73 00 5D …` when the envelope **`<device_id>`** matches CONFIG.

| UI ID | `<device_id>` | `<value>` | Full message                                    |
| ----- | ------------- | --------- | ----------------------------------------------- |
| 1     | `00`          | `00`      | `F0 … 01 00 73 00 5D 00 F7`                     |
| 3     | `01`          | `01`      | `F0 … 01 01 73 00 5D 01 F7`                     |

**`<value>`** appears zero-based (`UI − 1` for IDs 1 and 3).

```text
# Device ID 1 (destination device 1, value 1)
F0 00 20 33 01 00 73 00 5D 00 F7

# Device ID 3 (destination device 3, value 3)
F0 00 20 33 01 01 73 00 5D 01 F7
```

When sending manually, set **both** the envelope **`<device_id>`** and
**`<value>`** to match the target Virus CONFIG setting.

**MIDI Controller Page A / B:** [Paging](../misc/virus.md#paging).

### Global ARP Note Send

**Live edit:** `cmd=0x73`, param `0x60`.

**EDIT CONFIG → MIDI → ARP Note Send** — whether the arpeggiator sends **MIDI note** data.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 60 00 F7

# Enabled
F0 00 20 33 01 00 73 00 60 01 F7
```

### MIDI Clock

**Live edit:** `cmd=0x73`, param `0x6A`.

**EDIT CONFIG → Audio Clock → MIDI Clock** — internal vs external sync.

| Value | Mode (LCD)                               |
| ----- | ---------------------------------------- |
| `00`  | Internal sync                            |
| `01`  | Sync to External                         |

```text
# Internal
F0 00 20 33 01 00 73 00 6A 00 F7

# External
F0 00 20 33 01 00 73 00 6A 01 F7
```

### Knob Response

**Live edit:** `cmd=0x73`, param `0x75`.

**EDIT CONFIG → Knob Behavior → Response** — how front-panel encoders respond
when a parameter is changed (**Off**, **Jump**, **Snap**, **Rel**). **Host → synth only.**

```text
F0 00 20 33 01 <device_id> 73 00 75 <value> F7
```

| Value | Panel    |
| ----- | -------- |
| `00`  | **Off**  |
| `01`  | **Jump** |
| `02`  | **Snap** |
| `03`  | **Rel**  |

```text
F0 00 20 33 01 00 73 00 75 00 F7 # Off
F0 00 20 33 01 00 73 00 75 01 F7 # Jump
F0 00 20 33 01 00 73 00 75 02 F7 # Snap
F0 00 20 33 01 00 73 00 75 03 F7 # Rel
```

<a id="config-inputs--usb-rx-only"></a>

### CONFIG → Inputs / USB (RX only)

**EDIT CONFIG → Inputs / USB** (and related input level menus). All use
**`cmd=0x73`**, part **`00`**. **Host → synth only.** **Not** in **Single Dump**.

Param bytes are **not global** across `cmd` — e.g. **`0x5B`** here is **Input
Boost**, not Edit Single **Patch Volume** (`70`/`5B`).

#### USB Audio Mode

**Live edit:** `cmd=0x73`, param `0x09`.

**EDIT CONFIG → USB Audio Mode** (output/input routing preset).

| LCD           | `<value>` |
| ------------- | --------- |
| 2 outs / 0 in | `00`      |
| 3 outs / 0 in | `01`      |
| 3 outs / 1 in | `02`      |

```text
F0 00 20 33 01 00 73 00 09 00 F7 # 2 outs / 0 in
F0 00 20 33 01 00 73 00 09 01 F7 # 3 outs / 0 in
F0 00 20 33 01 00 73 00 09 02 F7 # 3 outs / 1 in
```

#### Input Direct Thru

**Live edit:** `cmd=0x73`, param `0x5A`.

**EDIT CONFIG → Input Direct Thru**. Direct **0–127** (`stored = lcd`).

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 73 00 5A 00 F7 # 0
F0 00 20 33 01 00 73 00 5A 7F F7 # 127
```

#### Input Sensitivity

**Live edit:** `cmd=0x73`, param `0x1F`.

**EDIT CONFIG → Input Sensitivity** (analog input level preset). **`stored =
index`**.

| LCD       | `<value>` |
| --------- | --------- |
| +16 dBv   | `00`      |
| +5 dBv    | `01`      |
| −8 dBv    | `02`      |
| −16 dBv   | `03`      |

```text
F0 00 20 33 01 00 73 00 1F 00 F7 # +16 dBv
F0 00 20 33 01 00 73 00 1F 01 F7 # +5 dBv
F0 00 20 33 01 00 73 00 1F 02 F7 # −8 dBv
F0 00 20 33 01 00 73 00 1F 03 F7 # −16 dBv
```

**Not** Edit FX **Input Follower → Sensitivity** (`70`/`38` → dump **`0x040`**).

#### Input Boost

**Live edit:** `cmd=0x73`, param `0x5B`.

**EDIT CONFIG → Input Boost**. **`Off`**, then **`1`–`127`** → `stored = lcd`
(`00` = Off).

```text
F0 00 20 33 01 00 73 00 5B 00 F7 # Off
F0 00 20 33 01 00 73 00 5B 01 F7 # 1
F0 00 20 33 01 00 73 00 5B 7F F7 # 127
```

**Not** Edit Single **Patch Volume** (`70`/`5B` → dump **`0x063`**).

#### Input Source

**Live edit:** `cmd=0x73`, param `0x2B`.

**EDIT CONFIG → Input Source**.

| LCD     | `<value>` |
| ------- | --------- |
| Analog  | `00`      |
| S/PDIF  | `01`      |

```text
F0 00 20 33 01 00 73 00 2B 00 F7 # Analog
F0 00 20 33 01 00 73 00 2B 01 F7 # S/PDIF
```

#### Input Characteristic

**Live edit:** `cmd=0x73`, param `0x1D`.

**EDIT CONFIG → Input Characteristic** (analog input EQ curve).

| LCD    | `<value>` |
| ------ | --------- |
| Linear | `00`      |
| Phono  | `01`      |

```text
F0 00 20 33 01 00 73 00 1D 00 F7 # Linear
F0 00 20 33 01 00 73 00 1D 01 F7 # Phono
```

**Not** Edit FX **Character** intensity (`70`/`15` → dump **`0x01D`**) — same
param **hex** on a different **`cmd`**.

### Memory Protect

**Live edit:** `cmd=0x73`, param `0x76`.

**EDIT CONFIG → System → Memory Protect** — prevents overwriting stored programs when
enabled.

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 76 00 F7

# Enabled
F0 00 20 33 01 00 73 00 76 01 F7
```

### Global MIDI Channel

**Live edit:** `cmd=0x73`, param `0x7C`.

**EDIT CONFIG → MIDI → Global Channel** (Global MIDI Channel). **Host → synth only.**

Zero-based channel index (same convention as per-part MIDI channel in
Multi Dump at `0x49 + (part−1)`).

| LCD channel | `<value>` |
| ----------- | --------- |
| 1           | `00`      |
| 9           | `08`      |

```text
# Global MIDI Channel 1
F0 00 20 33 01 00 73 00 7C 00 F7

# Global MIDI Channel 9
F0 00 20 33 01 00 73 00 7C 08 F7
```

### LED Mode

**Live edit:** `cmd=0x73`, param `0x7D`.

**EDIT CONFIG → System → LED Mode** — front-panel **LED** meter/display mode.

| Value | Mode (LCD) |
| ----- | ---------- |
| `00`  | Lfo        |
| `01`  | Ext Inputs |
| `02`  | Auto       |
| `03`  | Output1    |
| `04`  | Output2    |
| `05`  | Output3    |
| `06`  | ---        |

```text
F0 00 20 33 01 00 73 00 7D 00 F7 # Lfo
F0 00 20 33 01 00 73 00 7D 01 F7 # Ext Inputs
F0 00 20 33 01 00 73 00 7D 02 F7 # Auto
F0 00 20 33 01 00 73 00 7D 03 F7 # Output1
F0 00 20 33 01 00 73 00 7D 04 F7 # Output2
F0 00 20 33 01 00 73 00 7D 05 F7 # Output3
F0 00 20 33 01 00 73 00 7D 06 F7 # ---
```

### LCD Contrast

**Live edit:** `cmd=0x73`, param `0x7E`.

**EDIT CONFIG → System → LCD Contrast** — **LCD** contrast (**0%**–**100%**). Same encoding as
[BPM Brightness](#bpm-brightness) / [LED Lux](#led-lux): direct
7-bit `0x00`–`0x7F`,

```text
stored = min(0x7F, round(percent × 128 / 100))
```

| LCD    | `<value>` |
| ------ | --------- |
| 0.0%   | `00`      |
| 31.3%  | `28`      |
| 50.0%  | `40`      |
| 98.4%  | `7E`      |
| 100.0% | `7F`      |

```text
F0 00 20 33 01 00 73 00 7E 00 F7 # 0%
F0 00 20 33 01 00 73 00 7E 28 F7 # 31.3%
F0 00 20 33 01 00 73 00 7E 40 F7 # 50%
F0 00 20 33 01 00 73 00 7E 7E F7 # 98.4%
F0 00 20 33 01 00 73 00 7E 7F F7 # 100%
```
