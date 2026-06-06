# Banks & storage

Part of [Dumps](README.md). RAM/ROM banks, **REQUEST** commands, store/load —
not per-parameter dump offsets.

Architecture: [virus.md](../virus.md).

## Request messages

All requests use header `F0 00 20 33 01 <device> … F7`.

| Cmd | Name | Body (after device) | Reply |
| --- | ---- | ------------------- | ----- |
| **`0x30`** | **Single Request** | `30 <bank> <slot>` | `DUMP_SINGLE` (`0x10`) — stored banks **`01`–`1E`** |
| **`0x10`** | **Single Dump** (upload) | Full 524-byte message | Writes edit buffer / RAM — [single-dump-upload.md](single-dump-upload.md) |
| **`0x31`** | **Multi Request** | `31 <bank> <slot> [checksum]` | `DUMP_MULTI` (`0x11`) — [arrangements.md](arrangements.md#request_multi-byte-table) |
| **`0x32`** | **Single Bank Request** | `32 <bank>` | **128 × `DUMP_SINGLE`** — banks **`01`–`1E`** (RAM + ROM) |
| **`0x33`** | Multi Bank Request | `33 <bank>` | Bulk Multi bank — **TBD** |
| **`0x34`** | **Arrangement Request** | `34 00` (TI) | `DUMP_MULTI` + 16 × `DUMP_SINGLE` — [single.md](single.md#arrangement-export-dump_single--16) |
| **`0x35`** | Global Request | `35` | Global data — **TBD** |
| **`0x36`** | Total Request | `36` | Full device snapshot — **TBD** |
| **`0x37`** | **Controller Dump Request** | `37 00 <part>` | SysEx parameter stream — [controller-dump.md](controller-dump.md) |

### Single Request (`0x30`) {#single-request-0x30}

Access documentation (and older Virus SysEx references) call this message
**SINGLE REQUEST** — same as **`cmd=0x30`** here.

```text
F0 00 20 33 01 <device> 30 <bank> <slot> F7
```

| `bank` | `slot` | Meaning |
| ------ | ------ | ------- |
| `00` | `00`–`0F` | Multi **Part 1–16** edit-buffer single |
| `00` | `40` | **Single mode** edit buffer |
| `01`–`04` | `00`–`7F` | RAM Single banks **A–D** (128 programs) |
| `05`–`1E` | `00`–`7F` | ROM Single banks **A–Z** (128 programs each) |

**Stored-bank byte** on **`0x30`** / **`0x32`**: **`request_bank = dump_index + 1`**
where **`dump_index`** is the sequential index in
[Part bank index](arrangements.md#part-bank-index) (RAM A = `0x00` … ROM Z =
`0x1D`). Edit-buffer requests use **`bank = 00`** instead — not this formula.

Live edit **`<part>`** for **`0x70`/`0x71`/`0x6E`**: Multi parts
**`0x00`–`0x0F`**; Single-mode buffer **`0x40`**. Edit Multi **Bank** /
**Program** (**`0x72`/`0x20`**, **`0x21`**) use Multi part index only. See
[Single dump — addressing](single.md#single-vs-multi-addressing).

```bash
# Single mode edit buffer
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 30 00 40

# Multi Part 1 edit-buffer single
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 30 00 00
```

### Single Bank Request (`0x32`) {#single-bank-request-0x32}

Classic Access docs: **SINGLE BANK REQUEST** — ask the synth to send **all 128**
Singles in one stored bank. TI mk2 reply: **128 × 524-byte** `DUMP_SINGLE`
(hardware-confirmed for **`32 01`** RAM A and **`32 1E`** ROM Z; stream
framing **TBD**).

```text
F0 00 20 33 01 <device> 32 <bank> F7
```

**`<bank>`** uses the same encoding as [Single Request](#single-request-0x30)
stored banks. Valid range on TI mk2: **`01`–`1E`** (30 banks = 4 RAM + 26 ROM).

| Request `bank` | Bank | Dump index | TI mk2 |
| --- | --- | --- | --- |
| `00` | — | — | **No reply** (edit-buffer scope on `0x30`, not a stored bank) |
| `01`–`04` | RAM A–D | `0x00`–`0x03` | **`32 01`** RAM A → 128 dumps ✓ |
| `05`–`1E` | ROM A–Z | `0x04`–`0x1D` | **`32 1E`** ROM Z → 128 dumps ✓ |
| **`1F`+** | — | — | **No reply** ✓ (no bank after ROM Z) |

ROM letter → request byte: **`0x05 + (letter − 'A')`** (A→`05` … Z→**`1E`**).
Example: **`32 0F`** = ROM **K**.

```bash
# Entire RAM A bank
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 0x32 0x01

# Entire ROM Z bank
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 0x32 0x1E

receivemidi dev "Virus TI USB Plugin I/O" syx
```

**Note:** AURA may still issue **128 × Single Request** (`0x30`) per slot instead
of **`0x32`** — both can be valid; bulk bank request avoids per-slot handshakes
when the host accepts a long SysEx stream.

### Controller Dump Request (`0x37`) {#controller-dump-request-0x37}

Classic **CONTROLLER DUMP REQUEST**. TI mk2: **`37 00 <part>`** → **many**
short SysEx replies (live-edit style), not one bulk message. **`<part>`**:
Multi **`0x00`–`0x0F`**, Single mode **`0x40`** (same as edit-buffer
[Single Request](#single-request-0x30)).

Full notes and mapping workflow: [controller-dump.md](controller-dump.md).

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 0x37 0x00 0x00
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 0x37 0x00 0x40
```

## RAM Single banks (A–D)

Four **RAM** banks (**A**–**D**), **128** programs each. Live edit uses the
**edit buffer**; stored programs use banks **`01`–`04`** in **Single Request**
(`0x30`).

## ROM Singles (A–Z)

**26** ROM banks, **128** programs each. Request bank bytes **`05`–`1E`**
(ROM A–Z); **`32 1E`** streams all 128 ROM Z singles; **`32 1F`** — no
response (upper bound confirmed on TI mk2). Same encoding on **`0x30`**. Flash
ROM excluded from [single map](single.md#single-parameter-map).

## Multi bank

[Arrangements & Multis](arrangements.md) — **128** slots; slots **1–16** embed
16× `DUMP_SINGLE`.

Per-slot **store** / **dump-to-buffer** byte maps: **TBD**.
