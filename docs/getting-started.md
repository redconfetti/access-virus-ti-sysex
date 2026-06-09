# Getting started

## Sending System Exclusive Messages

The best way to understand SysEx commands is to test them using [sendmidi][]
and [receivemidi][]. You can install them on a Mac using [Homebrew][].

```bash
brew install sendmidi receivemidi
```

[Homebrew]: https://brew.sh/
[sendmidi]: https://github.com/gbevin/SendMIDI
[receivemidi]: https://github.com/gbevin/ReceiveMIDI

To communicate with your synth, you'll need to list the ports to identify which
one to send commands to.

```bash
$ sendmidi list
Virus TI USB External I/O
Virus TI USB Plugin I/O
Behringer Swing MIDI Port
```

The Virus TI is not responsive to System Exclusive messages on the
"External I/O" interface, so make sure to target "Virus TI USB Plugin I/O" or
its equivalent for your Virus TI.

```bash
# Sets "Osc Volume" to "<0>" (before Saturation)
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 70 40 24 40
```

Use the same port name for `sendmidi` and `receivemidi` (from the lists above).

In the example above the full System Exclusive message is:

```text
F0 00 20 33 01 00 70 40 24 40 F7
```

All System Exclusive messages begin with `F0` and end with `F7`, so sendmidi
omits requiring them from the command, and adds them to the command for you.

### Receiving System Exclusive Data

Some commands request the Virus TI to return data, such as a dump.

To receive the data returned, open a terminal window and run the following:

```bash
receivemidi dev "Virus TI USB Plugin I/O" syx
```

Then in another terminal window, request the single edit-buffer dump:

```bash
# Request Single Edit Buffer dump
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 30 00 40
```

After you've run the command, the data should show in the other terminal:

```bash
$ receivemidi dev "Virus TI USB Plugin I/O" syx
system-exclusive hex 00 20 33 01 00 10 00 40 0C 01 00 7F 00 00 00 00 00 00 40 00 00 00 00 00 00 40 00 00 40 60 40 00 00 40 20 00 00 40 40 60 00 40 00 0040 00 00 40 7F 40 00 00 00 00 40 40 40 00 00 00 00 00 00 2E 00 40 7F 00 7F 7F 40 04 00 00 00 30 01 00 00 40 00 00 40 40 40 40 40 30 01 00 00 40 00 00 4040 40 40 40 64 00 40 00 00 00 00 30 7F 40 00 01 01 7F 00 45 10 7F 40 01 00 01 00 40 00 10 0C 01 40 00 00 00 00 00 00 00 00 40 00 00 00 00 40 00 5E 01 0000 01 00 00 00 00 39 04 00 00 00 00 00 00 00 01 42 3E 01 00 01 01 01 24 00 00 00 00 00 00 00 00 40 40 28 2B 55 40 40 40 40 00 00 00 40 40 40 40 7F 00 4040 40 00 03 3A 64 00 00 40 00 40 00 00 40 00 40 00 40 00 40 00 40 00 03 00 24 70 30 40 7F 00 40 47 33 40 40 28 20 00 00 00 00 03 00 40 03 00 40 03 00 4020 2D 49 4E 49 54 2D 20 20 20 02 00 00 00 00 15 17 00 01 00 02 44 14 40 01 00 00 00 00 03 04 02 00 00 00 00 00 7F 40 40 7F 7F 40 00 00 00 00 00 00 00 0000 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 00 00 7F 7F 40 00 00 00 00 00 14 46 00 40 4614 46 00 40 46 00 40 00 40 00 40 00 40 00 40 00 40 00 40 00 40 00 40 00 00 00 00 00 00 00 00 02 00 00 00 00 00 01 01 01 00 00 1F 40 64 01 40 64 00 40 6401 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 6400 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 40 64 01 40 64 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0000 00 00 00 00 00 00 00 00 00 01 30 7F 40 00 01 00 53 46 dec
```

## Message structure

### Live Edits

For parameter change messages, the format is typically:

```text
F0 00 20 33  01  00  70  40  24  40  F7
             │   │   │   │   │   └── Value (center / "<0>")
             │   │   │   │   └────── Param — Osc Volume (`0x24`)
             │   │   │   └────────── Buffer Index — Single edit buffer (`0x40`)
             │   │   └────────────── Command (`0x70`) / Page
             │   └────────────────── device ID — unit 1 (`0x00`)
             └────────────────────── family — TI series (`0x01`, fixed on TI)

F0 00 20 33 ff dd cc bb pp vv F7
```

Breaking it down:

```text
F0              Start SysEx
00 20 33        Access Music manufacturer ID
ff              Family (e.g. Virus TI)
dd              Device ID (00 is Device 1, 01 is Device 2, etc)
cc              Command
bb              Buffer Index
pp              Parameter
vv              Value
F7              End SysEx
```

That's 11 bytes total.

The Single Edit Buffer used in Single mode is usually addressed as `40`,
with the 16 Multi parts addressed as `00` through `0F`.

For example, the "Osc Volume" is referenced by Parameter (pp) as `24`. The value
range for this parameter is -64 (`00`) through +63 (`7F`), with the middle
value (`40`) setting the volume to "0".

```text
------------------------------------------------------------------------
F0 00 20 33 ff dd cc bb pp vv F7    # Reference Template
------------------------------------------------------------------------
F0 00 20 33 01 00 70 40 24 7F F7    # Single Edit Buffer; Osc Volume set to +63
------------------------------------------------------------------------
F0 00 20 33 01 00 70 00 24 00 F7    # Multi Edit Buffer; Part 1 - Set to -64
F0 00 20 33 01 00 70 01 24 40 F7    # Multi Edit Buffer; Part 2 - Set to 0
F0 00 20 33 01 00 70 02 24 66 F7    # Multi Edit Buffer; Part 3 - Set to +39
F0 00 20 33 01 00 70 03 24 40 F7    # Multi Edit Buffer; Part 4 - Set to 0
F0 00 20 33 01 00 70 04 24 00 F7    # Multi Edit Buffer; Part 5 - Set to -64
F0 00 20 33 01 00 70 05 24 6F F7    # Multi Edit Buffer; Part 6 - Set to +48
F0 00 20 33 01 00 70 06 24 40 F7    # Multi Edit Buffer; Part 7 - Set to 0
F0 00 20 33 01 00 70 07 24 00 F7    # Multi Edit Buffer; Part 8 - Set to -64
F0 00 20 33 01 00 70 08 24 40 F7    # Multi Edit Buffer; Part 9 - Set to 0
F0 00 20 33 01 00 70 09 24 00 F7    # Multi Edit Buffer; Part 10 - Set to -64
F0 00 20 33 01 00 70 0A 24 40 F7    # Multi Edit Buffer; Part 11 - Set to 0
F0 00 20 33 01 00 70 0B 24 77 F7    # Multi Edit Buffer; Part 12 - Set to +56
F0 00 20 33 01 00 70 0C 24 40 F7    # Multi Edit Buffer; Part 13 - Set to 0
F0 00 20 33 01 00 70 0D 24 40 F7    # Multi Edit Buffer; Part 14 - Set to 0
F0 00 20 33 01 00 70 0E 24 40 F7    # Multi Edit Buffer; Part 15 - Set to 0
F0 00 20 33 01 00 70 0F 24 40 F7    # Multi Edit Buffer; Part 16 - Set to 0
```

### Single Requests

Other commands, like global edits or single dump requests use a 10 byte
structure.

```text
F0              Start SysEx
00 20 33        Access Music manufacturer ID
ff              Family (e.g. Virus TI)
dd              Device ID (00 is Device 1, 01 is Device 2, etc)
cc              Command
bb              Bank
ss              Slot
F7              End SysEx
```

Here's an example request:

```text
F0 00 20 33 ff dd cc bb ss F7    # Reference Template
F0 00 20 33 01 00 30 00 40 F7    # Single Program Request (30);
                                 # Bank RAM-A (00); Slot 64 (40)
F0 00 20 33 01 00 30 06 01 F7    # Single Program Request (30);
                                 # Bank ROM-B (06); Slot 2 (01)
```

### Payload shapes

After `F0 00 20 33 01 00`, the rest of the message depends on **`<cmd>`**:

| Kind        | `<cmd>`                       | Shape after device ID                  |
| ----------- | ----------------------------- | -------------------------------------- |
| Live edit   | `0x70`–`0x72`, `0x6E`, `0x6F` | `<cmd> <buffer> <page> <index> <value>`|
| Global      | `0x73`                        | `73 00 <param> <value>`                |
| Request     | `0x30`–`0x37`                 | `<cmd>` + 1–3 bytes (bank/slot, …)     |
| Dump        | `0x10`, `0x11`                | `<cmd>` + large body (524 B or 267 B)  |

Examples (full frames):

```text
# Live edit — Single edit buffer, Page A, Osc Volume
F0 00 20 33 01 00 70 40 24 40 F7

# Request — Single edit-buffer dump (reply is cmd 0x10)
F0 00 20 33 01 00 30 00 40 F7

# Live edit — Multi Part 11, Bank → RAM A
F0 00 20 33 01 00 72 0A 20 00 F7
```

Dumps and requests: [bank.md](dumps/bank.md), [multi.md](dumps/multi.md).
Field-by-field Single map: [dumps/single.md](dumps/single.md).

## Address index

If you are starting with a specific System Exclusive message and want to
know what it does, feel free to use the
[address index](reference/address-index.md) reference guide.

## Parameter values

Wire values are often **not** the number on the LCD — common patterns include
direct **0–127**, **bipolar** (`stored = ui + 64`), and **tempo**
(`stored = bpm − 63`). Enumerated panel menus (Arp Mode, Delay Type, …) list
every **`stored`** byte in [parameter-options.md](reference/parameter-options.md).

Start with [Value encodings](reference/parameter-options.md#value-encodings) for
shared formulas. For **`cmd` / `param` / dump offset** notation, see
[Notation](reference/parameter-options.md#notation-cmd-param-dump-offset).
