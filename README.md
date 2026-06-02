# Access Virus SysEx

Reverse engineered **Access Virus TI mk2** SysEx specifications with assistance
from Cursor AI.

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

Use **`Virus TI USB Plugin I/O`** for both directions (VST/plugin path). Use
`Virus TI USB External I/O` only when controlling the synth from a standalone
keyboard rig, not through the plugin.

Send SysEx with **`hex`** before **`syx`**, and **omit `F0`/`F7`** (sendmidi
adds them). Bare decimals are wrong (`20` → `0x14`); `0x20` parses as **0**:

```bash
# Part 1 Hold Pedal off (11 bytes on wire: F0 + 9 data + F7)
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 72 00 4a 00

# Listen for replies (e.g. DUMP_MULTI)
receivemidi dev "Virus TI USB Plugin I/O" dump
```

Message formats: [multis-live-edit.md](docs/multis-live-edit.md),
[multis-dump.md](docs/multis-dump.md). For agent/hardware test workflows see
[docs/testing.md](docs/testing.md).

## Documentation

| Topic                                  | Document                                             |
| -------------------------------------- | ---------------------------------------------------- |
| Hardware testing (`sendmidi`, etc.)    | [docs/testing.md](docs/testing.md)                   |
| General notes about Virus architecture | [docs/virus.md](docs/virus.md)                       |
| Single program dump (`DUMP_SINGLE`)    | [docs/single-dump.md](docs/single-dump.md)           |
| Multi program dump (`DUMP_MULTI`)      | [docs/multis-dump.md](docs/multis-dump.md)           |
| Multi Live Edit (`0x72`, …)            | [docs/multis-live-edit.md](docs/multis-live-edit.md) |
| Global Live Edit (`0x73`)              | [docs/global-live-edit.md](docs/global-live-edit.md) |
| Single Live Edit                       | [docs/single-live-edit.md](docs/single-live-edit.md) |
| AURA plugin notes                      | [docs/aura-notes.md](docs/aura-notes.md)             |
