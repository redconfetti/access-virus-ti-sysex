# Access Virus (TI mk2)

General notes about Access Virus TI mk2 architecture

Note: Currently applies only to Access Virus TI mk2 desktop (not keyboard/Polar)

## Banks and programs

The TI mk2 provides **four RAM banks** (A–D). Each bank holds **128 Single
programs**.

| Bank  | Role     |
| ----- | -------- |
| RAM A | User RAM |
| RAM B | User RAM |
| RAM C | User RAM |
| RAM D | User RAM |

There are also **26 ROM banks** (ROM A through ROM Z), each with **128 factory
Singles**.

In each Multi, every part stores a **bank index** and **program number**
pointing at a Single. The encoding is documented in
[multi.md](../dumps/multi.md#part-bank-index).

## SysEx dump types

The Virus can export or stream several kinds of MIDI SysEx data:

| #   | Name                | Description                                                          | Project interest                                                                            |
| --- | ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1   | **Single Buffer**   | One Single in the temporary edit buffer                              | Secondary — relates to arrangement exports                                                  |
| 2   | **Single Bank**     | All 128 programs in a RAM bank (A–D)                                 | **`0x32`** request, banks **`01`–`04`** — [bank.md](../dumps/bank.md#single-bank-request) |
| 3   | **Controller Dump** | One Single as a stream of live-edit SysEx (not Single Dump)        | **`0x37`** — [controller-dump.md](../dumps/controller-dump.md)                                 |
| 4   | **Arrangement**     | Current Multi (or sequencer) buffer: **multi settings + 16 Singles** | Important — full performance snapshot                                                       |
| 5   | **Multi Bank**      | All programs in the Multi bank (128 slots)                           | Important                                                                                   |
| 6   | **Remote Patches**  | Remote control templates                                             | Out of scope                                                                                |

**Multi bank export:** one **Multi Dump** (267 bytes) for every slot.
**Slots 1–16** also include **sixteen Single Dump** messages (524 bytes
each) — the full part sounds are stored with the multi. **Slots 17–128**
return the 267-byte multi settings only (bank/program pointers per part in
that header). The **edit buffer** (`REQUEST` bank `00` slot `7F`) uses the
same 267-byte block; it may be exported with sixteen singles like slots
1–16.

Message-level layouts:

- Multi dump: [multi.md](../dumps/multi.md)
- Single dump: [single.md](../dumps/single.md)
- Live multi edits (not full dumps):
[multis.md](../live-edit/multis.md)

## Multi bank (TI series)

See [multi.md — Embedded vs Reference
Multis](../dumps/multi.md#embedded-vs-reference-multis).

## Front-panel modes

The TI desktop exposes **Multi**, **Single**, and **Sequencer**
(**MULTI+SINGLE**) play/edit modes.

**Host → synth** — select mode with **`cmd=0x73`**, param **`0x7A`**:

| Mode      | SysEx body      |
| --------- | --------------- |
| Single    | `73 00 7A 00`   |
| Sequencer | `73 00 7A 01`   |
| Multi     | `73 00 7A 02`   |

See [Play mode (`0x7A`)](../live-edit/global.md#play-mode).

**Synth → host** (panel) may emit **`cmd=0x73`**, param **`0x10`**, or empty
`F0 F7` frames — see [Edit mode `0x10`](../live-edit/global.md#edit-mode-0x10-tentative).

| Panel action                 | Typical SysEx from Virus          |
| ---------------------------- | --------------------------------- |
| Select multi from bank       | `73 00 10 00` (often twice)       |
| Press **SINGLE**             | `73 40 10 00`                     |
| **MULTI+SINGLE** / Sequencer | Empty `F0 F7` frames (no payload) |

This is separate from **parameter edits** (e.g. Filter Cutoff uses
**`cmd=0x70`** while editing a Single on Part 1).
