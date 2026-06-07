# Single Dump upload (`0x10`)

Part of [Dumps](README.md). Classic Access docs call this **SINGLE DUMP**; the
TI mk2 reply/upload is **`DUMP_SINGLE`** — **524 bytes**, not 256 + checksum.

## Request vs dump

| Message            | Cmd    | Direction                        | Body                    |
| ------------------ | ------ | -------------------------------- | ----------------------- |
| **Single Request** | `0x30` | Host → synth (ask)               | `30 <bank> <slot>` only |
| **Single Dump**    | `0x10` | Synth → host or **host → synth** | Full program bytes      |

**Single Request** pulls a stored program or edit buffer over MIDI.

**Single Dump** **must include the entire program**. Header `bb` / `ss` name
the **destination** on upload, not “load from bank X slot Y by reference”:

```text
F0 00 20 33 01 <device> 10 <bank> <slot> <TI payload 0x09..0x208> <cs> F7
```

| `bank` (`0x07`) | `slot` (`0x08`) | Upload target                                         |
| --------------- | --------------- | ----------------------------------------------------- |
| `00`            | `00`–`0F`       | Multi **Part 1–16** edit buffer                       |
| `00`            | `40`            | **Single mode** edit buffer                           |
| `01`–`04`       | `00`–`7F`       | **Store** to RAM A–D (classic; TI store path **TBD**) |

A short message like `F0 … 10 01 40 F7` (no payload) will **not** load RAM A
program 64 — there is nothing to parse.

**Why no “load slot” SysEx in Single mode:** program recall is already **MIDI
Program Change** (plus bank select as configured). The synth does not need a
parallel one-message SysEx loader; hosts that want a stored patch should send
**PC**, or pull **`0x30`** + re-upload **`0x10`** when they need the full
524-byte body (editors, backup tools). See
[bank.md — Single mode program recall](bank.md#single-mode-program-recall).

## Load RAM A program 64 into Multi Part 1 (TI mk2)

Two steps — **Single Request**, then re-send a full **`0x10`** with the
destination header:

**1. Single Request** — read stored program:

```text
F0 00 20 33 01 00 30 01 40 F7
                      ^^  ^^ bank 01 = RAM A, slot 0x40 = program 64
```

**2. Single Dump** — re-send the **524-byte** reply with header **`10 00 00`**
(Part 1 edit buffer) and a recalculated checksum at **`0x209`**:

```text
F0 00 20 33 01 00 10 00 00 0C … 522 data bytes … cs F7
```

Checksum (TI mk2, confirmed):

```text
cs = (device + 0x10 + bank + slot + sum(bytes 0x09..0x208)) & 0x7F
```

Capture the **`0x30`** reply to a local file (see [setup — capture
scratch](../setup.md#local-capture-scratch)), retarget header bytes **`10 00
00`**, recalculate **`cs`**, then send the 522-byte body with **`sendmidi hex
syx`**.

See [Single dump format](single.md#dump-format), [Single Request](bank.md#single-request-0x30).
