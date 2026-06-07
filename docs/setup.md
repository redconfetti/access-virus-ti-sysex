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
adds them).

**Byte values:** use an **`0x` prefix on every data byte** you care about.
sendmidi’s parsing is easy to get wrong:

| You type | Often becomes       | You wanted                  |
| -------- | ------------------- | --------------------------- |
| `20`     | `0x14` (decimal 20) | param **`0x20`** (Bank)     |
| `21`     | `0x15` (decimal 21) | param **`0x21`** (Program)  |
| `40`     | `0x28` (decimal 40) | program **64** → **`0x40`** |
| `72`     | `0x48` (decimal 72) | cmd **`0x72`**              |

Example — Part 1 → RAM A, program **64**:

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x72 0x00 0x20 0x00

sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x72 0x00 0x21 0x40
```

Wire (check in a MIDI monitor):

```text
F0 00 20 33 01 00 72 00 20 00 F7
F0 00 20 33 01 00 72 00 21 40 F7
                              ^^ program 64, not decimal 40
```

Hold Pedal off (all bytes prefixed):

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x72 0x00 0x4a 0x00
```

Listen for replies (e.g. `DUMP_MULTI`):

```bash
receivemidi dev "Virus TI USB Plugin I/O" dump
```

Message formats: [live-edit](live-edit/README.md),
[dumps](dumps/README.md). For agent/hardware test workflows see
[testing.md](testing.md).

## Local capture scratch

`artifacts/captures/` is **gitignored** — a temporary place for MIDI monitor
logs, baseline dumps, and one-off helper scripts while mapping parameters.
**Do not commit** contents; fold results into `docs/` and delete or overwrite
local files when done.

Example (controller dump baseline, Single edit buffer):

```bash
mkdir -p artifacts/captures
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x37 0x00 0x40
receivemidi dev "Virus TI USB Plugin I/O" syx \
  > artifacts/captures/controller-dump.txt
```

See [controller-dump.md](dumps/controller-dump.md) for the diff workflow.

Next: [Getting started](getting-started.md) — how to read the docs and SysEx
byte layout.
