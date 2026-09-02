# Controller Dump Request (`0x37`)

Part of [Documentation](../../../README.md#documentation). **Controller Dump Request** (`0x37`).

Unlike **Single Dump** (`0x10`), a controller dump is a **stream of many
short SysEx messages** (live-edit / CC-style parameter updates) that together
describe the current state of one part’s Single edit buffer. Useful for finding
**`cmd`/`param` pairs** missing from [live-edit docs](../../../README.md#documentation) or
[single.md](single.md#single-parameter-map).

## Contents

- [Request](#request)
  - [`<part>`](#part)
- [Reply (overview)](#reply-overview)
- [Why the disassembly is consistent with a streamed reply](#why-the-disassembly-is-consistent-with-a-streamed-reply)
  - [How the end of the stream is detected — and why the host doesn't see it](#how-the-end-of-the-stream-is-detected--and-why-the-host-doesnt-see-it)
- [Related](#related)

---

## Request

```text
F0 00 20 33 01 <device> 37 00 <part> F7
```

| Byte     | Value                   | Meaning                                                                 |
| -------- | ----------------------- | ----------------------------------------------------------------------- |
| `37`     | Controller Dump Request | Fixed                                                                   |
| `00`     | Subcommand              | Fixed in captures                                                       |
| `<part>` | Part / buffer selector  | Same as [Single Request](bank.md#single-request) edit-buffer slots      |

### `<part>`

| `<part>`          | Target                                 |
| ----------------- | -------------------------------------- |
| **`0x00`–`0x0F`** | Multi **Part 1–16** Single edit buffer |
| **`0x40`**        | **Single mode** Single edit buffer     |

```bash
# Multi Part 1 — all parameters as SysEx stream
sendmidi dev "<MIDI port>" hex syx \
  00 20 33 01 00 0x37 0x00 0x00

# Single mode edit buffer
sendmidi dev "<MIDI port>" hex syx \
  00 20 33 01 00 0x37 0x00 0x40

receivemidi dev "<MIDI port>" syx
```

## Reply (overview)

- **Many messages**, not one bulk dump.
- Expected content: **Page A / B / part-buffer** live edits — see
  [Paging](../misc/virus.md#live-edit-command-bytes) (`0x70`, `0x71`, `0x6E`, …).

## Why the disassembly is consistent with a streamed reply

From disassembling the TI2's SysEx dispatcher on **5.1.7.00**. This section is background for the
behaviour described above, not a correction to it.

`0x37`'s handler **never assembles a dump**. It walks the selected part's edit buffer and, for each
step, writes the two **DSP HDI08 host mailboxes**, which are mapped into the 8051's external data
space (XDATA) at `0x0000` and `0x0100`. It then runs the DSP response pump, which enqueues what the
DSPs return into the **parameter ring** at XDATA `0x0D00`. That ring is the same structure the
inbound live-edit commands (`0x6E`–`0x74`) write into.

That control flow is **consistent with** the reply being the DSPs' current parameter state leaving
through the ordinary parameter-change path rather than the bulk-dump path — which would explain why
`0x37` alone among the requests answers in many short messages. The HDI08 traffic itself was not
observed, so this is read from the code, not measured on the wire.

### How the end of the stream is detected — and why the host doesn't see it

After sending, the 8051 enters a receive loop reading 3-byte triples back from the DSPs. The loop
**treats two byte patterns as exit conditions**, both keyed on `0xF4` in the first byte:

| Triple        | Effect on the loop |
| ------------- | ------------------ |
| `F4 F4 F4`    | exit               |
| `F4 <any> F7` | exit               |

In this exchange `0xF4` prefixes the special triples: the same routine *opens* it by sending
`F4 75 55` before the walk begins. Whether the DSPs actually emit the two exit patterns was not
observed — the disassembly shows only that the 8051 stops when it sees them.

**The exit path returns before reaching the routine that forwards a triple onward.** Every triple
that is not one of those two patterns goes through that forwarding routine; the two exit patterns do
not. So whatever ends the exchange internally, **this handler forwards nothing to mark it.**

Practical consequence for a host: **do not wait for a terminating message.** There is no bulk
completion message, and no end marker arrives from this path. Use an idle gap after the last
live-edit message, or count the parameters you expect for the requested part.

This establishes only that this handler emits no terminator. It does not rule out markers
elsewhere.

**Scope:** TI2 running **5.1.7.00**. Addresses are specific to that build and the behaviour is
untested on other models and versions.

## Related

| Message                            | What you get                               |
| ---------------------------------- | ------------------------------------------ |
| **`0x30`** Single Request          | One **524-byte** Single Dump snapshot      |
| **`0x37`** Controller Dump Request | **Parameter-by-parameter** SysEx stream    |
| **`0x72`/`0x20`/`0x21`** live edit | Bank/program metadata only (no full state) |

Request command table: [bank.md](bank.md#controller-dump-request).
