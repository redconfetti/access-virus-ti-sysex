# Controller Dump Request (`0x37`)

Part of [Dumps](README.md). Classic Access docs: **CONTROLLER DUMP REQUEST**.

Unlike **`DUMP_SINGLE`** (`0x10`), a controller dump is a **stream of many
short SysEx messages** (live-edit / CC-style parameter updates) that together
describe the current state of one part’s Single edit buffer. Useful for finding
**`cmd`/`param` pairs** not yet mapped in [live-edit](../live-edit/README.md) or
[single.md](single.md#single-parameter-map).

## Request

```text
F0 00 20 33 01 <device> 37 00 <part> F7
```

| Byte     | Value                   | Meaning                                                                 |
| -------- | ----------------------- | ----------------------------------------------------------------------- |
| `37`     | Controller Dump Request | Fixed                                                                   |
| `00`     | Subcommand              | Fixed in TI mk2 captures (**TBD** if other values exist)                |
| `<part>` | Part / buffer selector  | Same as [Single Request](bank.md#single-request-0x30) edit-buffer slots |

### `<part>` (TI mk2, confirmed)

| `<part>`          | Target                                 |
| ----------------- | -------------------------------------- |
| **`0x00`–`0x0F`** | Multi **Part 1–16** Single edit buffer |
| **`0x40`**        | **Single mode** Single edit buffer     |

```bash
# Multi Part 1 — all parameters as SysEx stream
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x37 0x00 0x00

# Single mode edit buffer
sendmidi dev "Virus TI USB Plugin I/O" hex syx \
  00 20 33 01 00 0x37 0x00 0x40

receivemidi dev "Virus TI USB Plugin I/O" syx
```

## Reply (overview)

- **Many messages**, not one bulk dump.
- Expected content: **Page A / B / part-buffer** live edits (`0x70`, `0x71`,
  `0x6E`, …) and possibly MIDI **CC** — same family as panel/automation traffic.
- Exact message list, order, and completeness vs **`DUMP_SINGLE`** payload:
  **TBD** (capture + diff workflow).

## Mapping workflow (suggested)

1. Baseline: request controller dump for Part 1 (`37 00 00`) with a known
   **`-INIT-`** single loaded.
2. Change **one** panel control on the Virus.
3. Request controller dump again; diff the two streams for new/changed
   **`cmd`/`param`/`value`** triplets.
4. Cross-check winners against **`DUMP_SINGLE`** byte diffs when a dump offset
   is needed.

See [testing.md](../testing.md) and
`.cursor/skills/hardware-mapping-workflow/SKILL.md`.

## Related

| Message                            | What you get                               |
| ---------------------------------- | ------------------------------------------ |
| **`0x30`** Single Request          | One **524-byte** `DUMP_SINGLE` snapshot    |
| **`0x37`** Controller Dump Request | **Parameter-by-parameter** SysEx stream    |
| **`0x72`/`0x20`/`0x21`** live edit | Bank/program metadata only (no full state) |

Request command table: [bank.md](bank.md#controller-dump-request-0x37).
