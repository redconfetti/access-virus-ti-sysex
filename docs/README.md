# Documentation Index

Start with the root [README](../README.md) for notation, setup, and the
request / dump / live-edit mental model. This index groups the reference files
inside `docs/`.

## Start Here

| Need                                        | Document             |
| ------------------------------------------- | -------------------- |
| Banks, programs, slots, and mode behavior   | [virus.md](virus.md) |
| Classic 1999 SysEx map used as a hypothesis | [waf80.md](waf80.md) |

## Dump Formats

| Need                                                | Document                         |
| --------------------------------------------------- | -------------------------------- |
| `DUMP_MULTI`, `REQUEST_MULTI`, Multi offsets        | [multis-dump.md](multis-dump.md) |
| `DUMP_SINGLE`, arrangement export, Single inventory | [single-dump.md](single-dump.md) |

## Live Edits

| Need                                       | Document                                   |
| ------------------------------------------ | ------------------------------------------ |
| Multi edit parameters and dump correlation | [multis-live-edit.md](multis-live-edit.md) |
| Single / part sound live edits             | [single-live-edit.md](single-live-edit.md) |
| Device-wide `cmd=0x73` globals             | [global-live-edit.md](global-live-edit.md) |
| MIDI CC-only and CC-vs-SysEx routing       | [control-change.md](control-change.md)     |

## Reference Data

| Need                                       | Document                                               |
| ------------------------------------------ | ------------------------------------------------------ |
| Enumerated option labels and long UI lists | [parameter-option-lists.md](parameter-option-lists.md) |

## Testing And Host Notes

| Need                                                  | Document                       |
| ----------------------------------------------------- | ------------------------------ |
| Hardware capture, diffing, and confirmation workflow  | [testing.md](testing.md)       |
| AURA / Virus Control host behavior and export caveats | [aura-notes.md](aura-notes.md) |
