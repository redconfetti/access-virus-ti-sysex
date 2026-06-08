# Banks & storage

Part of [Documentation](../../../README.md#documentation). RAM/ROM banks, **REQUEST** commands, store/load —
not per-parameter dump offsets.

Architecture: [virus.md](../misc/virus.md).

## Request messages

All requests use header `F0 00 20 33 01 <device> … F7`.

| Cmd        | Name                        | Body (after device)           | Reply                                                                                         |
| ---------- | --------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------- |
| **`0x30`** | **Single Request**          | `30 <bank> <slot>`            | Single Dump (`0x10`) — stored banks **`01`–`1E`**                                             |
| **`0x10`** | **Single Dump** (upload)    | Full 524-byte message         | Writes edit buffer / RAM — [single.md — upload](single.md#single-dump-upload-0x10)            |
| **`0x31`** | **Multi Request**           | `31 <bank> <slot> [checksum]` | Multi Dump (`0x11`) — [multi.md](multi.md#request_multi-byte-table)                           |
| **`0x32`** | **Single Bank Request**     | `32 <bank>`                   | **128 × Single Dump** — banks **`01`–`1E`** (RAM + ROM)                                       |
| **`0x34`** | **Arrangement Request**     | `34 00` (TI)                  | Multi Dump + 16 × Single Dump — [single.md](single.md#arrangement-export-single-dump--16)     |
| **`0x37`** | **Controller Dump Request** | `37 00 <part>`                | SysEx parameter stream — [controller.md](controller.md)                                       |

### Single Request

**Request:** `cmd=0x30`.

**Single Request** — **`cmd=0x30`**.

```text
F0 00 20 33 01 <device> 30 <bank> <slot> F7
```

| `bank`    | `slot`    | Meaning                                      |
| --------- | --------- | -------------------------------------------- |
| `00`      | `00`–`0F` | Multi **Part 1–16** edit-buffer single       |
| `00`      | `40`      | **Single mode** edit buffer                  |
| `01`–`04` | `00`–`7F` | RAM Single banks **A–D** (128 programs)      |
| `05`–`1E` | `00`–`7F` | ROM Single banks **A–Z** (128 programs each) |

**Stored-bank byte** on **`0x30`** / **`0x32`**: **`request_bank = dump_index + 1`**
where **`dump_index`** is the sequential index in
[Part bank index](multi.md#part-bank-index) (RAM A = `0x00` … ROM Z =
`0x1D`). Edit-buffer requests use **`bank = 00`** instead — not this formula.

Live edit **`<part>`** for **`0x70`/`0x71`/`0x6E`**: see
[Paging](../misc/virus.md#part-byte) and
[single.md — Single vs Multi addressing](single.md#single-vs-multi-addressing).

```bash
# Single mode edit buffer
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 30 00 40

# Multi Part 1 edit-buffer single
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 30 00 00
```

### No “load program by slot” SysEx in Single mode

There is **no** short SysEx that means “load RAM bank *X* program *Y* into the
Single edit buffer” without transferring the full **524-byte** Single Dump
body. **`0x10`** upload always carries the entire program; a header-only
message like `F0 … 10 01 40 F7` has **no payload to parse** — see
[single.md — upload](single.md#single-dump-upload-0x10).

**Single mode program recall uses MIDI Program Change** (and Bank Select if
your setup maps banks that way) — the same mechanism as picking a slot on the
front panel. SysEx **`0x30`** is for **reading** a stored program into a dump
message (backup/editor workflow), not a one-byte “load” substitute for PC.

To copy a RAM slot into the edit buffer without Program Change, **Single
Request** (`0x30`) the slot, then **Single Dump** (`0x10`) upload with header
**`10 00 40`** (Single edit buffer) — full transfer, not a reference.

### Single Bank Request

**Request:** `cmd=0x32`.

**Single Bank Request** — ask the synth to send **all 128** Singles in one stored bank. Reply: **128 × 524-byte** Single Dump (confirmed for **`32 01`** RAM A and **`32 1E`** ROM Z).

```text
F0 00 20 33 01 <device> 32 <bank> F7
```

**`<bank>`** uses the same encoding as [Single Request](#single-request)
stored banks. Valid range: **`01`–`1E`** (30 banks = 4 RAM + 26 ROM).

| Request `bank` | Bank    | Dump index    | Result                                                        |
| -------------- | ------- | ------------- | ------------------------------------------------------------- |
| `00`           | —       | —             | **No reply** (edit-buffer scope on `0x30`, not a stored bank) |
| `01`–`04`      | RAM A–D | `0x00`–`0x03` | **`32 01`** RAM A → 128 dumps ✓                               |
| `05`–`1E`      | ROM A–Z | `0x04`–`0x1D` | **`32 1E`** ROM Z → 128 dumps ✓                               |
| **`1F`+**      | —       | —             | **No reply** ✓ (no bank after ROM Z)                          |

ROM letter → request byte: **`0x05 + (letter − 'A')`** (A→`05` … Z→**`1E`**).
Example: **`32 0F`** = ROM **K**.

```bash
# Entire RAM A bank
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 0x32 0x01

# Entire ROM Z bank
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 0x32 0x1E

receivemidi dev "<MIDI port>" syx
```

**Note:** Some hosts issue **128 × Single Request** (`0x30`) per slot instead of
**`0x32`** — both can be valid; bulk bank request avoids per-slot handshakes
when the host accepts a long SysEx stream.

### Controller Dump Request

**Request:** `cmd=0x37`.

**Controller Dump Request**. **`37 00 <part>`** → **many**
short SysEx replies (live-edit style), not one bulk message. **`<part>`**:
Multi **`0x00`–`0x0F`**, Single mode **`0x40`** (same as edit-buffer
[Single Request](#single-request)).

Full notes: [controller.md](controller.md).

```bash
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 0x37 0x00 0x00
sendmidi dev "<MIDI port>" hex syx 00 20 33 01 00 0x37 0x00 0x40
```

## RAM Single banks (A–D)

Four **RAM** banks (**A**–**D**), **128** programs each. Live edit uses the
**edit buffer**; stored programs use banks **`01`–`04`** in **Single Request**
(`0x30`).

## ROM Singles (A–Z)

**26** ROM banks, **128** programs each. Request bank bytes **`05`–`1E`**
(ROM A–Z); **`32 1E`** streams all 128 ROM Z singles; **`32 1F`** — no
response (upper bound confirmed). Same encoding on **`0x30`**. Flash
ROM excluded from [single map](single.md#single-parameter-map).

## Multi bank

[Arrangements & Multis](multi.md) — **128** slots; slots **1–16** embed
16× Single Dump.
