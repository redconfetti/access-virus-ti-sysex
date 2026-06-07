# Dumps

Bulk SysEx — program files, banks, arrangements (**`DUMP_SINGLE`**,
**`DUMP_MULTI`**, requests).

| Document                                       | Contents                                                                                      |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [single.md](single.md)                         | **`DUMP_SINGLE`** format, [parameter map](single.md#single-parameter-map), arrangement export |
| [single-dump-upload.md](single-dump-upload.md) | **Single Dump** (`0x10`) upload — load into edit buffer from a captured dump                  |
| [arrangements.md](arrangements.md)             | **`DUMP_MULTI`**, embedded slots 1–16, Edit Multi dump map                                    |
| [bank.md](bank.md)                             | RAM A–D, ROM A–Z, request commands (`0x30`–`0x37`)                                            |
| [controller-dump.md](controller-dump.md)       | **Controller Dump Request** (`0x37`) — live-edit SysEx stream per part                        |

**Live edit** (per-knob SysEx while editing):
[live-edit/README.md](../live-edit/README.md)
