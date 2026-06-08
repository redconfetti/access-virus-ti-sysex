# Access Virus SysEx

Reverse engineered **Access Virus TI mk2 desktop** SysEx specifications with
assistance from Cursor AI.

- [Getting started (SysEx primer)](docs/getting-started.md)
- [General notes about Virus architecture](docs/misc/virus.md)
- Live edit
  - Singles
    - [Single](docs/live-edit/single/single.md)
    - [Oscillators](docs/live-edit/single/oscillators.md)
    - [Filters](docs/live-edit/single/filters.md)
    - [Effects](docs/live-edit/single/effects.md)
    - [Arpeggiator](docs/live-edit/single/arpeggiator.md)
    - [Modulators / LFO](docs/live-edit/single/modulators.md)
    - [Modulation Matrix](docs/live-edit/single/mod-matrix.md)
  - [Multis](docs/live-edit/multis.md)
  - [Global](docs/live-edit/global.md)
- Dump
  - [Single](docs/dumps/single.md)
  - [Multis & arrangements](docs/dumps/multi.md)
  - [Banks & requests](docs/dumps/bank.md)
  - [Controller](docs/dumps/controller.md)
- [Parameter options (enums, panel tables)](docs/reference/parameter-options.md)
- [OsTIrus (DSP56300 TI/TI2 emulation)](docs/misc/ostirus.md)

## Testing

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
