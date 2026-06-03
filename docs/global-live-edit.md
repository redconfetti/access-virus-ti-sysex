# Global Live Edit (`cmd=0x73`)

Device-wide settings on the Virus TI. These use **`cmd=0x73`**, not Multi edit
**`cmd=0x72`**. Whether any of them appear in **`DUMP_MULTI`** is **not
confirmed** for most parameters.

Host-specific capture notes (AURA plugin): [aura-notes.md](aura-notes.md).

```text
F0 00 20 33 01 <device_id> 73 00 <param> <value> F7
```

The byte **`<device_id>`** (immediately before **`0x73`**) is the SysEx
**destination device ID**. The Virus only acts on the message when this
matches its configured **MIDI Device ID** (CONFIG). Captures in this doc
use **`00`** (device 1) unless noted.

At least **All Delays** (`0x1B`) is **transmitted by the Virus** when
changed on the front panel. Other globals may need re-verification on the
panel where **Hardware TX** is still blank below.

## Summary

| Param ID | Parameter              | Value encoding                                             | `DUMP_MULTI` | Hardware TX |
| -------- | ---------------------- | ---------------------------------------------------------- | ------------ | ----------- |
| `0x10`   | Edit mode / focus      | See [Edit mode 0x10](#edit-mode-0x10-tentative)            | Unverified   | Yes (panel) |
| `0x19`   | All EQs                | See [All EQs](#all-eqs-0x19)                               | Unverified   | —           |
| `0x1A`   | All Arpeggiators       | See [All Arpeggiators](#all-arpeggiators-0x1a)             | Unverified   | —           |
| `0x1B`   | All Delays             | See [All Delays](#all-delays-0x1b)                         | Unverified   | Yes         |
| `0x1C`   | All Reverbs            | See [All Reverbs](#all-reverbs-0x1c)                       | Unverified   | —           |
| `0x32`   | BPM Brightness         | See [BPM Brightness](#bpm-brightness-0x32)                 | Unverified   | —           |
| `0x33`   | LED Lux                | See [LED Lux](#led-lux-0x33)                               | Unverified   | —           |
| `0x55`   | Global Program Change  | See [Global Program Change](#global-program-change-0x55)   | Unverified   | —           |
| `0x57`   | Global MIDI Volume RX  | See [Global MIDI Volume RX](#global-midi-volume-rx-0x57)   | Unverified   | —           |
| `0x5D`   | MIDI Device ID         | See [MIDI Device ID](#midi-device-id-0x5d)                 | Unverified   | —           |
| `0x5E`   | MIDI Controller Page A | See [MIDI Controller Page A](#midi-controller-page-a-0x5e) | Unverified   | —           |
| `0x5F`   | MIDI Controller Page B | See [MIDI Controller Page B](#midi-controller-page-b-0x5f) | Unverified   | —           |
| `0x60`   | Global ARP Note Send   | See [Global ARP Note Send](#global-arp-note-send-0x60)     | Unverified   | —           |
| `0x6A`   | MIDI Clock             | See [MIDI Clock](#midi-clock-0x6a)                         | Unverified   | —           |
| `0x76`   | Memory Protect         | See [Memory Protect](#memory-protect-0x76)                 | Unverified   | —           |
| `0x7C`   | Global MIDI Channel    | Zero-based (`00` = ch 1 … `0F` = ch 16)                    | Unverified   | —           |
| `0x7D`   | LED Mode               | See [LED Mode](#led-mode-0x7d)                             | Unverified   | —           |
| `0x7E`   | LCD Contrast           | See [LCD Contrast](#lcd-contrast-0x7e)                     | Unverified   | —           |

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
F0 00 20 33 01 00 73 00 10 00 F7   # Multi / multi-bank context (tentative)
F0 00 20 33 01 00 73 40 10 00 F7   # Single-buffer scope 0x40 (tentative)
```

**Not confirmed:** exact meaning of value **`0x00`**; whether **`0x10`**
is “enter Multi mode” or a broader **edit focus** indicator. Sequencer
transitions did **not** repeat the `73 … 10` message.

### All EQs (`0x19`)

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

### All Arpeggiators (`0x1A`)

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

### All Delays (`0x1B`)

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

### All Reverbs (`0x1C`)

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

### BPM Brightness (`0x32`)

**BPM** display brightness (**0%**–**100%**). Same encoding as
[LED Lux](#led-lux-0x33): direct 7-bit `0x00`–`0x7F`,

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
F0 00 20 33 01 00 73 00 32 00 F7   # 0%
F0 00 20 33 01 00 73 00 32 01 F7   # 0.8%
F0 00 20 33 01 00 73 00 32 02 F7   # 1.6%
F0 00 20 33 01 00 73 00 32 52 F7   # 64.1%
F0 00 20 33 01 00 73 00 32 7E F7   # 98.4%
F0 00 20 33 01 00 73 00 32 7F F7   # 100%
```

### LED Lux (`0x33`)

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
F0 00 20 33 01 00 73 00 33 00 F7   # 0%
F0 00 20 33 01 00 73 00 33 1B F7   # 21.1%
F0 00 20 33 01 00 73 00 33 1F F7   # 24.2%
F0 00 20 33 01 00 73 00 33 5C F7   # 71.9%
F0 00 20 33 01 00 73 00 33 7F F7   # 100%
```

### Global Program Change (`0x55`)

Global **Program Change** receive. Distinct from per-part **Program Change**
in Edit Multi (packed flag at `0xF8 + part` in `DUMP_MULTI`; CONFIG global
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

### Global MIDI Volume RX (`0x57`)

Global receive **MIDI Volume** (CC#7). Distinct from per-part **Volume RX**
in Edit Multi (packed flag at `0xF8 + part` in `DUMP_MULTI`).

| Value | Setting  |
| ----- | -------- |
| `00`  | Disabled |
| `01`  | Enabled  |

```text
# Disabled
F0 00 20 33 01 00 73 00 57 00 F7

# Enabled
F0 00 20 33 01 00 73 00 57 01 F7
```

### MIDI Device ID (`0x5D`)

CONFIG **MIDI Device ID** (**1–16**, or **Omni**). Not yet confirmed from
**Virus front panel** edits (the SysEx **`<device_id>`** byte must match
the unit’s configured ID). First captures were from a host plugin — see
[aura-notes.md](aura-notes.md).

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

### MIDI Controller Page A (`0x5E`)

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

### MIDI Controller Page B (`0x5F`)

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

### Global ARP Note Send (`0x60`)

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

### MIDI Clock (`0x6A`)

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

### Memory Protect (`0x76`)

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

### Global MIDI Channel (`0x7C`)

Zero-based channel index (same convention as per-part MIDI channel in
`DUMP_MULTI` at `0x49 + (part−1)`).

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

### LED Mode (`0x7D`)

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
F0 00 20 33 01 00 73 00 7D 00 F7   # Lfo
F0 00 20 33 01 00 73 00 7D 01 F7   # Ext Inputs
F0 00 20 33 01 00 73 00 7D 02 F7   # Auto
F0 00 20 33 01 00 73 00 7D 03 F7   # Output1
F0 00 20 33 01 00 73 00 7D 04 F7   # Output2
F0 00 20 33 01 00 73 00 7D 05 F7   # Output3
F0 00 20 33 01 00 73 00 7D 06 F7   # ---
```

### LCD Contrast (`0x7E`)

**LCD** contrast (**0%**–**100%**). Same encoding as
[BPM Brightness](#bpm-brightness-0x32) / [LED Lux](#led-lux-0x33): direct
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
F0 00 20 33 01 00 73 00 7E 00 F7   # 0%
F0 00 20 33 01 00 73 00 7E 28 F7   # 31.3%
F0 00 20 33 01 00 73 00 7E 40 F7   # 50%
F0 00 20 33 01 00 73 00 7E 7E F7   # 98.4%
F0 00 20 33 01 00 73 00 7E 7F F7   # 100%
```

## Correlation with `DUMP_MULTI` (planned)

To test whether globals are stored in the multi payload:

1. Load a known multi (e.g. INIT MULTI).
2. Change one global via **`0x73`** and confirm on the Virus LCD.
3. Request **`DUMP_MULTI`** (edit buffer or stored slot).
4. Diff against baseline; check unmapped regions in
   [multis-dump.md — Unmapped payload](multis-dump.md#unmapped-payload):
   `0x19..0x28`, `0xB9..0xC7`, `0xE8..0xF7`.

**Keyboard to MIDI** (Edit Multi global, live `0x72` / `0x40`) is a separate
one-bit field; if stored in a multi dump it would most likely be a single
`00`/`01` byte in one of the zero blocks above.
