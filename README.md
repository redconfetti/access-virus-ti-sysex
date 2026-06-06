# Access Virus SysEx

Reverse engineered **Access Virus TI mk2** SysEx specifications with assistance
from Cursor AI. The same messages apply in principle to
**[OsTIrus](docs/ostirus.md)**
(TI/TI2/Snow firmware emulation in a DAW) — no hardware required for MIDI/SysEx
control, only a suitable host port.

- **[Setup](docs/setup.md)** — `sendmidi` / `receivemidi`, ports, first SysEx
- **[Getting started](docs/getting-started.md)** — message layout, `cmd` bytes,
  requests vs dumps vs live edit

## Documentation {#documentation}

| Topic                                   | Document                                                         |
| --------------------------------------- | ---------------------------------------------------------------- |
| Setup (`sendmidi`, ports)               | [docs/setup.md](docs/setup.md)                                   |
| Getting started (SysEx primer)          | [docs/getting-started.md](docs/getting-started.md)               |
| Hardware testing (index)                | [docs/testing.md](docs/testing.md)                               |
| General notes about Virus architecture  | [docs/virus.md](docs/virus.md)                                   |
| Live edit — CONFIG / global (`0x73`)    | [docs/live-edit/edit-config.md](docs/live-edit/edit-config.md)   |
| Live edit — Edit Single                 | [docs/live-edit/edit-single.md](docs/live-edit/edit-single.md)   |
| Live edit — Oscillators / Filters / FX  | [docs/live-edit/](docs/live-edit/README.md)                      |
| Live edit — Edit Multi (`0x72`)         | [docs/live-edit/edit-multi.md](docs/live-edit/edit-multi.md)     |
| Dump — Single (`DUMP_SINGLE`)           | [docs/dumps/single.md](docs/dumps/single.md)                     |
| Dump — Multis & arrangements            | [docs/dumps/arrangements.md](docs/dumps/arrangements.md)         |
| Dump — Banks & requests                 | [docs/dumps/bank.md](docs/dumps/bank.md)                         |
| MIDI Control Change (CC)                | [docs/control-change.md](docs/control-change.md)                 |
| WAF80 SysEx reference (1999, classic)   | [docs/waf80.md](docs/waf80.md)                                   |
| Parameter options (enums, panel tables) | [docs/parameter-options.md](docs/parameter-options.md)           |
| OsTIrus (DSP56300 TI/TI2 emulation)     | [docs/ostirus.md](docs/ostirus.md)                               |
