# Setup

Install [Homebrew](https://brew.sh/) MIDI helpers:

```bash
brew install sendmidi receivemidi
```

List ports:

```bash
sendmidi list
receivemidi list
```

Use **`Virus TI USB Plugin I/O`** for both directions when using the **Access
Virus TI plugin** with hardware. Use `Virus TI USB External I/O` only when
controlling the synth from a standalone keyboard rig, not through the plugin.

**[OsTIrus](ostirus.md)** users: route MIDI/SysEx from your DAW or a
virtual port into the plugin; port names are host-specific (`sendmidi list`).

Send SysEx with **`hex`** before **`syx`**, and **omit `F0`/`F7`** (sendmidi
adds them). Bare decimals are wrong (`20` → `0x14`); `0x20` parses as **0**:

```bash
# Part 1 Hold Pedal off (11 bytes on wire: F0 + 9 data + F7)
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 72 00 4a 00

# Listen for replies (e.g. DUMP_MULTI)
receivemidi dev "Virus TI USB Plugin I/O" dump
```

Message formats: [live-edit](live-edit/README.md),
[dumps](dumps/README.md). For agent/hardware test workflows see
[testing.md](testing.md).

Next: [Getting started](getting-started.md) — how to read the docs and SysEx
byte layout.
