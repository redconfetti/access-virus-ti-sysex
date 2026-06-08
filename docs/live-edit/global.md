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

**Edit Single → Inputs.** TI mk2 live edit uses **`cmd=0x6F`** (extended page,
same family as part buffer **`0x6E`**), part **`00`**. Classic
**Input Mode** / **Input Select** on Page A (**CC 101** / **102** →
**`70`/`65`**
/ **`66`**); those CCs may still apply when **MIDI Controller Page A** =
**Controller Data** — not re-verified here.

**Panel visibility**

| Control          | Visible when                                                     |
| ---------------- | ---------------------------------------------------------------- |
| **Atomizer**     | Always                                                           |
| **Input Mode**   | **Atomizer** = **Off** (`7E` = `00`)                             |
| **Input Select** | **Input Mode** = **Dynamic** or **Static** (`7C` = `01` or `02`) |

### Atomizer

**Live edit:** `cmd=0x6F`, param `0x7E`.

TI manual (Atomizer tutorial): **Atomizer** is a **beat-synced instant looper**
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
labels **2**–**16** are stored **`02`–`10`**; exact musical length per index is
not yet correlated to SysEx here (see Atomizer manual for performance detail).

Enum: [Atomizer preset](../reference/parameter-options.md#atomizer-preset)
(`00`–`10`).

```text
F0 00 20 33 01 00 6F 00 7E 00 F7 # Atomizer Off
F0 00 20 33 01 00 6F 00 7E 01 F7 # Atomizer On
F0 00 20 33 01 00 6F 00 7E 10 F7 # Atomizer 16
```

### Input Mode

**Live edit:** `cmd=0x6F`, param `0x7C`.

Enum: [Input Mode](../reference/parameter-options.md#input-mode-1).

```text
F0 00 20 33 01 00 6F 00 7C 00 F7 # Input Mode Off
F0 00 20 33 01 00 6F 00 7C 01 F7 # Input Mode Dynamic
F0 00 20 33 01 00 6F 00 7C 02 F7 # Input Mode Static
```

### Input Select

**Live edit:** `cmd=0x6F`, param `0x7D`.

Enum: [Input Select](../reference/parameter-options.md#input-select-1).

```text
F0 00 20 33 01 00 6F 00 7D 00 F7 # Input Select Left
F0 00 20 33 01 00 6F 00 7D 01 F7 # Input Select L + R
F0 00 20 33 01 00 6F 00 7D 02 F7 # Input Select Right
```

---

## Global parameters

**Live edit:** `cmd=0x73`.

Device-wide settings — not Multi **`0x72`** or part sound **`0x6E`**. Whether
any appear in **Multi Dump** is **not confirmed** for most parameters.

The byte **`<device_id>`** (immediately before **`0x73`**) is the SysEx
**destination device ID**. The Virus only acts on the message when this
matches its configured **MIDI Device ID** (CONFIG). Captures in this doc
use **`00`** (device 1) unless noted.

At least **All Delays** (`0x1B`) is **transmitted by the Virus** when
changed on the front panel. Many other **`0x73`** globals are **RX only**
(host → synth); the panel does not emit SysEx when they are edited — see
[Knob Response](#knob-response) and [CONFIG → Inputs / USB (RX only)](#config-inputs--usb-rx-only).

## Summary

| Param ID | Parameter              | Value encoding                                              | Multi Dump | Hardware TX      |
| -------- | ---------------------- | ----------------------------------------------------------- | ------------ | ---------------- |
| `0x09`   | USB Audio Mode         | See [USB Audio Mode](#usb-audio-mode)                  | Unverified   | No; RX ✓         |
| `0x10`   | Edit mode / focus      | See [Edit mode 0x10](#edit-mode-0x10-tentative)             | Unverified   | Yes (panel)      |
| `0x19`   | All EQs                | See [All EQs](#all-eqs)                                | Unverified   | —                |
| `0x1A`   | All Arpeggiators       | See [All Arpeggiators](#all-arpeggiators)              | Unverified   | —                |
| `0x1B`   | All Delays             | See [All Delays](#all-delays)                          | Unverified   | Yes              |
| `0x1C`   | All Reverbs            | See [All Reverbs](#all-reverbs)                        | Unverified   | —                |
| `0x1D`   | Input Characteristic   | See [Input Characteristic](#input-characteristic)      | Unverified   | No; RX ✓         |
| `0x1F`   | Input Sensitivity      | See [Input Sensitivity](#input-sensitivity)            | Unverified   | No; RX ✓         |
| `0x28`   | Navigation             | See [Navigation](#navigation) — **`73 40`** scope byte | Unverified   | ✓                |
| `0x29`   | Value Wrapping         | See [Value Wrapping](#value-wrapping)                  | Unverified   | ✓                |
| `0x2B`   | Input Source           | See [Input Source](#input-source)                      | Unverified   | No; RX ✓         |
| `0x32`   | BPM Brightness         | See [BPM Brightness](#bpm-brightness)                  | Unverified   | —                |
| `0x33`   | LED Lux                | See [LED Lux](#led-lux)                                | Unverified   | —                |
| `0x35`   | Random PG — Scope      | See [Randomize Scope](#randomize-scope)                | Unverified   | ✓                |
| `0x36`   | Random PG — Strength   | See [Randomize Strength](#randomize-strength)          | Unverified   | ✓                |
| `0x55`   | Global Program Change  | See [Global Program Change](#global-program-change)    | Unverified   | —                |
| `0x57`   | Global MIDI Volume RX  | See [Global MIDI Volume RX](#global-midi-volume-rx)    | Unverified   | No; RX ✓         |
| `0x5A`   | Input Direct Thru      | See [Input Direct Thru](#input-direct-thru)            | Unverified   | No; RX ✓         |
| `0x5B`   | Input Boost            | See [Input Boost](#input-boost)                        | Unverified   | No; RX ✓         |
| `0x5D`   | MIDI Device ID         | See [MIDI Device ID](#midi-device-id)                  | Unverified   | No (panel)       |
| `0x5E`   | MIDI Controller Page A | See [MIDI Controller Page A](#midi-controller-page-a)  | Unverified   | —                |
| `0x5F`   | MIDI Controller Page B | See [MIDI Controller Page B](#midi-controller-page-b)  | Unverified   | —                |
| `0x60`   | Global ARP Note Send   | See [Global ARP Note Send](#global-arp-note-send)      | Unverified   | —                |
| `0x6A`   | MIDI Clock             | See [MIDI Clock](#midi-clock)                          | Unverified   | —                |
| `0x75`   | Knob Response          | See [Knob Response](#knob-response)                    | Unverified   | No (panel); RX ✓ |
| `0x76`   | Memory Protect         | See [Memory Protect](#memory-protect)                  | Unverified   | —                |
| `0x7A`   | Play mode              | See [Play mode](#play-mode)                            | Unverified   | —                |
| `0x7C`   | Global MIDI Channel    | See [Global MIDI Channel](#global-midi-channel)        | Unverified   | No (panel)       |
| `0x7D`   | LED Mode               | See [LED Mode](#led-mode)                              | Unverified   | —                |
| `0x7E`   | LCD Contrast           | See [LCD Contrast](#lcd-contrast)                      | Unverified   | —                |

## Parameters

### Edit mode 0x10 tentative

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
F0 00 20 33 01 00 73 00 10 00 F7 # Multi / multi-bank context (tentative)
F0 00 20 33 01 00 73 40 10 00 F7 # Single-buffer scope 0x40 (tentative)
```

**Not confirmed:** exact meaning of value **`0x00`**; whether **`0x10`**
is “enter Multi mode” or a broader **edit focus** indicator. Sequencer
transitions did **not** repeat the `73 … 10` message.

For **host → synth** mode selection, use [Play mode (`0x7A`)](#play-mode)
instead.

### Play mode

**Live edit:** param `0x7A`.

**Front-panel play/edit mode** — **Single**, **Sequencer** (**MULTI+SINGLE**),
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
[Edit mode `0x10`](#edit-mode-0x10-tentative) (synth → host, tentative).

### All EQs

**Live edit:** param `0x19`.

Global **All EQs** on/off.

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

**Live edit:** param `0x1A`.

Global **All Arpeggiators** on/off.

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

**Live edit:** param `0x1B`.

Global **All Delays** on/off. **Confirmed:** the Virus sends this message
on the USB interface when the setting is changed on the **front panel**
(same `cmd=0x73` format).

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

**Live edit:** param `0x1C`.

Global **All Reverbs** on/off.

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

**Live edit:** param `0x28`.

**EDIT CONFIG → System → Navigation** — how the front panel steps through
parameter pages (**By Page** vs **By Parameter**).

Unlike most globals in this doc, the byte after **`0x73`** is **`0x40`**
(not **`0x00`**) — same **scope** prefix as [Edit mode `0x10`](#edit-mode-0x10-tentative):

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

Confirmed on Virus TI mk2 (hardware TX + manual `sendmidi`).

### Value Wrapping

**Live edit:** param `0x29`.

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

Confirmed on Virus TI mk2 (hardware TX + manual `sendmidi`).

### BPM Brightness

**Live edit:** param `0x32`.

**BPM** display brightness (**0%**–**100%**). Same encoding as
[LED Lux](#led-lux): direct 7-bit `0x00`–`0x7F`,

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

**Live edit:** param `0x33`.

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

**Live edit:** param `0x35`.

**EDIT CONFIG → Random PG → Scope**. How much of the program is affected when
randomizing. **0.0..100.0 %** — same 7-bit encoding as
[BPM Brightness](#bpm-brightness) (`00` = 0%, `7F` = 100.0%).

```text
F0 00 20 33 01 00 73 00 35 00 F7 # 0 %
F0 00 20 33 01 00 73 00 35 7F F7 # 100.0 %
```

Confirmed on Virus TI mk2 (hardware TX + manual `sendmidi`).

### Randomize Strength

**Live edit:** param `0x36`.

**EDIT CONFIG → Random PG → Strength**. Randomization intensity.
**0.0..100.0 %** — same encoding as [Scope](#randomize-scope).

```text
F0 00 20 33 01 00 73 00 36 00 F7 # 0 %
F0 00 20 33 01 00 73 00 36 7F F7 # 100.0 %
```

Confirmed on Virus TI mk2 (hardware TX + manual `sendmidi`).

### Global Program Change

**Live edit:** param `0x55`.

Global **Program Change** receive. Distinct from per-part **Program Change**
in Edit Multi (packed flag at `0xF8 + part` in Multi Dump; CONFIG global
ignored for parts per TI manual).

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

**Live edit:** param `0x57`.

**EDIT CONFIG → MIDI → MIDI Volume** (global CC#7 receive). **`cmd=0x73`**, part
**`00`**. **Hardware TX:** **No** (RX only — host **`sendmidi`** confirmed).
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

**Live edit:** param `0x5D`.

**EDIT CONFIG → MIDI → MIDI Device ID** (**1–16**, or **Omni**).

**Hardware TX:** the Virus **does not** emit SysEx when this setting is
changed on the **front panel** (TI mk2 desktop, confirmed). Wire map below is
from manual **`sendmidi`** / host capture only — the synth
**accepts** `73 00 5D …` when the envelope **`<device_id>`** matches CONFIG.

| UI ID | `<device_id>` | `<value>` | Full message                                    |
| ----- | ------------- | --------- | ----------------------------------------------- |
| 1     | `00`          | `00`      | `F0 … 01 00 73 00 5D 00 F7`                     |
| 2     | *(TBD)*       | *(TBD)*   | Capture matched ID 1 in one session — re-verify |
| 3     | `01`          | `01`      | `F0 … 01 01 73 00 5D 01 F7`                     |

**`<value>`** appears zero-based (`UI − 1` for IDs 1 and 3). **Omni**
encoding not yet captured.

```text
# Device ID 1 (destination device 1, value 1)
F0 00 20 33 01 00 73 00 5D 00 F7

# Device ID 3 (destination device 3, value 3)
F0 00 20 33 01 01 73 00 5D 01 F7
```

When sending manually, set **both** the envelope **`<device_id>`** and
**`<value>`** to match the target Virus CONFIG setting.

### MIDI Controller Page A

**Live edit:** param `0x5E`.

Soft-knob **MIDI Controller** assignment, **Page A**.

| Value | Mode            |
| ----- | --------------- |
| `00`  | SysEx           |
| `01`  | Controller Data |

Additional values not yet captured.

```text
# SysEx
F0 00 20 33 01 00 73 00 5E 00 F7

# Controller Data
F0 00 20 33 01 00 73 00 5E 01 F7
```

### MIDI Controller Page B

**Live edit:** param `0x5F`.

Soft-knob **MIDI Controller** assignment, **Page B**.

| Value | Mode          |
| ----- | ------------- |
| `00`  | SysEx         |
| `01`  | Poly Pressure |

Additional values not yet captured.

```text
# SysEx
F0 00 20 33 01 00 73 00 5F 00 F7

# Poly Pressure
F0 00 20 33 01 00 73 00 5F 01 F7
```

### Global ARP Note Send

**Live edit:** param `0x60`.

Whether the arpeggiator sends **MIDI note** data.

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

**Live edit:** param `0x6A`.

| Value | Mode (LCD)                               |
| ----- | ---------------------------------------- |
| `00`  | Internal sync                            |
| `01`  | Sync to External                         |
| `02`  | *(third option — label TBD on hardware)* |

```text
# Internal
F0 00 20 33 01 00 73 00 6A 00 F7

# External
F0 00 20 33 01 00 73 00 6A 01 F7

# Third mode (value 02)
F0 00 20 33 01 00 73 00 6A 02 F7
```

### Knob Response

**Live edit:** param `0x75`.

**EDIT CONFIG → Knob Behavior → Response** — how front-panel encoders respond
when a parameter is changed (**Off**, **Jump**, **Snap**, **Rel**).

**Hardware TX:** **No** — the Virus does not emit SysEx when changed on the
panel (TI mk2 desktop, confirmed). **RX:** confirmed via manual
**`sendmidi`**.

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
**`cmd=0x73`**, part **`00`**. **Hardware TX:** **No** on TI mk2 desktop
(confirmed / user capture). **RX:** host **`sendmidi`** confirmed for the
examples below. **Not** in **Single Dump**.

Param bytes are **not global** across `cmd` — e.g. **`0x5B`** here is **Input
Boost**, not Edit Single **Patch Volume** (`70`/`5B`).

#### USB Audio Mode

**Live edit:** param `0x09`.

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

**Live edit:** param `0x5A`.

**EDIT CONFIG → Input Direct Thru**. **`0`–`127`** → `stored = lcd`.

```text
F0 00 20 33 01 00 73 00 5A 00 F7 # 0
F0 00 20 33 01 00 73 00 5A 7F F7 # 127
```

#### Input Sensitivity

**Live edit:** param `0x1F`.

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

**Live edit:** param `0x5B`.

**EDIT CONFIG → Input Boost**. **`Off`**, then **`1`–`127`** → `stored = lcd`
(`00` = Off).

```text
F0 00 20 33 01 00 73 00 5B 00 F7 # Off
F0 00 20 33 01 00 73 00 5B 01 F7 # 1
F0 00 20 33 01 00 73 00 5B 7F F7 # 127
```

**Not** Edit Single **Patch Volume** (`70`/`5B` → dump **`0x063`**).

#### Input Source

**Live edit:** param `0x2B`.

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

**Live edit:** param `0x1D`.

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

**Live edit:** param `0x76`.

**Memory Protect** on/off — prevents overwriting stored programs when
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

**Live edit:** param `0x7C`.

**EDIT CONFIG → MIDI → Global Channel** (Global MIDI Channel).

**Hardware TX:** the Virus **does not** emit SysEx when this setting is
changed on the **front panel** (TI mk2 desktop, confirmed). Examples below
are from manual **`sendmidi`** / host capture only; **RX** on the synth is assumed
but not fully swept.

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

**Live edit:** param `0x7D`.

Front-panel **LED** meter/display mode.

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

**Live edit:** param `0x7E`.

**LCD** contrast (**0%**–**100%**). Same encoding as
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

## Correlation with Multi Dump (planned)

To test whether globals are stored in the multi payload:

1. Load a known multi (e.g. INIT MULTI).
2. Change one global via **`0x73`** and confirm on the Virus LCD.
3. Request **Multi Dump** (edit buffer or stored slot).
4. Diff against baseline; check unmapped regions in
 [multi.md — Unmapped
 payload](../dumps/multi.md#unmapped-payload):
 `0x19..0x28`, `0xB9..0xC7`, `0xE8..0xF7`.

**Keyboard to MIDI** (Edit Multi global, live `0x72` / `0x40`) is a separate
one-bit field; if stored in a multi dump it would most likely be a single
`00`/`01` byte in one of the zero blocks above.
