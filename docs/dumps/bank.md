# Banks & storage

Part of [Dumps](README.md). RAM/ROM banks, **REQUEST** commands, store/load —
not per-parameter dump offsets.

Architecture: [virus.md](../virus.md).

## RAM Single banks (A–D)

Four **RAM** banks (**A**–**D**), **128** programs each. Live edit uses the
**edit buffer**; stored programs use banks **`01`–`04`** in **Single Request**
(`0x30`) — [waf80.md — Single Request](../waf80.md#single-request-0x30).

| Request `bank` | Meaning                                                    |
| -------------- | ---------------------------------------------------------- |
| `00`           | Edit buffer — slot `40` (Single) or `00`–`0F` (Multi part) |
| `01`–`04`      | RAM A–D                                                    |

```text
F0 00 20 33 01 <device> 30 <bank> <slot> F7
```

**Single Bank Request** (`0x32`) — bulk one RAM bank (see waf80).

## ROM Singles (A–Z)

**26** ROM banks, **128** programs each. Factory ROM; request/dump **TBD** here
(Flash ROM excluded from [single map](single.md#single-parameter-map)).

## Multi bank

[Arrangements & Multis](arrangements.md) — **128** slots; slots **1–16** embed
16× `DUMP_SINGLE`.

## Commands

| Cmd             | Role              | Doc                                                         |
| --------------- | ----------------- | ----------------------------------------------------------- |
| `0x10`          | `DUMP_SINGLE`     | [single.md](single.md#dump-format)                          |
| `0x11`          | `DUMP_MULTI`      | [arrangements.md](arrangements.md)                          |
| `0x30`          | Single Request    | [waf80.md](../waf80.md#single-request-0x30)                 |
| `0x31`          | Multi Request     | [arrangements.md](arrangements.md#request_multi-byte-table) |
| `0x32` / `0x33` | Bank bulk request | [waf80.md](../waf80.md)                                     |

Per-slot **store** / **dump-to-buffer** byte maps: **TBD**.
