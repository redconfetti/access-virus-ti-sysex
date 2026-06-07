# Hardware testing

Guide for verifying SysEx documentation against a **Virus TI mk2 desktop**.

**Agents:** use the project skill **`hardware-mapping-workflow`**
(`.cursor/skills/hardware-mapping-workflow/SKILL.md`) for the full
step-by-step workflow — `sendmidi` syntax, capture loop,
queue, dump diff, and when to stop.

**Batch rule:** during dump correlation, if **≥ 10** parameters return **NONE**
(no payload change), **stop** and report the failure list to the user for
corrective data before continuing or updating docs.

## Quick links

| Topic                         | Doc                                               |
| ----------------------------- | ------------------------------------------------- |
| Install, ports, first message | [setup.md](setup.md)                              |
| OsTIrus (no hardware)         | [ostirus.md](ostirus.md)                          |
| Live edit by menu             | [live-edit/README.md](live-edit/README.md)        |
| Dump maps                     | [dumps/README.md](dumps/README.md)                |
| Doc writing rules             | `.cursor/skills/documentation-standards/SKILL.md` |
| Parameter enums               | [parameter-options.md](parameter-options.md)      |

## Message types (reference)

| Purpose            | Cmd  | Length    | Doc                                                               |
| ------------------ | ---- | --------- | ----------------------------------------------------------------- |
| Live multi edit    | `72` | 11 bytes  | [edit-multi.md](live-edit/edit-multi.md)                          |
| Request multi dump | `31` | 11 bytes  | [arrangements.md](dumps/arrangements.md#request_multi-byte-table) |
| Multi dump reply   | `11` | 267 bytes | [arrangements.md](dumps/arrangements.md)                          |
