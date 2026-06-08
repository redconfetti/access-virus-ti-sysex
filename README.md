# Access Virus SysEx

Reverse engineered **Access Virus TI mk2** SysEx specifications with assistance
from Cursor AI.

- [Getting started (SysEx primer)](docs/getting-started.md)
- [General notes about Virus architecture](docs/misc/virus.md)
- Live edit
  - Singles
    - [Live edit — Single](docs/live-edit/single/single.md)
    - [Live edit — Oscillators](docs/live-edit/single/oscillators.md)
    - [Live edit — Filters](docs/live-edit/single/filters.md)
    - [Live edit — Effects](docs/live-edit/single/effects.md)
    - [Live edit — Arpeggiator](docs/live-edit/single/arpeggiator.md)
    - [Live edit — Modulators (LFO)](docs/live-edit/single/modulators.md)
    - [Live edit — Modulation Matrix](docs/live-edit/single/mod-matrix.md)
  - [Live edit — Multis](docs/live-edit/multis.md)
  - [Live edit — Global](docs/live-edit/global.md)
- Dump
  - [Dump — Single](docs/dumps/single.md)
  - [Dump — Multis & arrangements](docs/dumps/multi.md)
  - [Dump — Banks & requests](docs/dumps/bank.md)
  - [Dump — Controller dump](docs/dumps/controller-dump.md)
- [Parameter options (enums, panel tables)](docs/reference/parameter-options.md)
- [OsTIrus (DSP56300 TI/TI2 emulation)](docs/misc/ostirus.md)

## Setup

Install [Homebrew](https://brew.sh/) MIDI helpers:

```bash
brew install sendmidi receivemidi
```

List ports:

```bash
sendmidi list
receivemidi list
```

Use the same port name for `sendmidi` and `receivemidi` (from the lists above).

Send SysEx with **`hex`** before **`syx`**, and **omit `F0`/`F7`** (sendmidi
adds them). Prefix data bytes with **`0x`** so values are not parsed as decimal
(e.g. `0x72` for cmd **`0x72`**, not `72` → `0x48`).

Request the edit-buffer Multi (Multi Dump):

```bash
sendmidi dev "<MIDI port>" hex syx \
  00 20 33 01 00 0x31 0x00 0x7f

receivemidi dev "<MIDI port>" dump
```
