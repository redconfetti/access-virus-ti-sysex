# Access Virus (TI mk2)

General notes about Access Virus TI mk2 architecture

Note: Currently applies only to Access Virus TI mk2 desktop (not keyboard/Polar)

## Banks and programs

The TI mk2 provides **four RAM banks** (A–D). Each bank holds **128 Single programs**.

| Bank  | Role     |
| ----- | -------- |
| RAM A | User RAM |
| RAM B | User RAM |
| RAM C | User RAM |
| RAM D | User RAM |

There are also **26 ROM banks** (ROM A through ROM Z), each with **128 factory Singles**.

In **reference** Multi programs, each part stores a **bank index** and
**program number** pointing at one of these Singles. The encoding is
documented in [multis.md](multis.md#part-bank-index-0x29--part).

## SysEx dump types

The Virus can export or stream several kinds of MIDI SysEx data:

| #   | Name                | Description                                                          | Project interest                                 |
| --- | ------------------- | -------------------------------------------------------------------- | ------------------------------------------------ |
| 1   | **Single Buffer**   | One Single in the temporary edit buffer                              | Secondary — relates to arrangement exports       |
| 2   | **Single Bank**     | All 128 programs in a RAM bank (A–D)                                 | Secondary                                        |
| 3   | **Controller Dump** | One Single as a sequence of parameter changes (CC or SysEx)          | Secondary                                        |
| 4   | **Arrangement**     | Current Multi (or sequencer) buffer: **multi settings + 16 Singles** | Important — full performance snapshot            |
| 5   | **Multi Bank**      | All programs in the Multi bank (128 slots)                           | Important — slot 1–16 embedded, 17–128 reference |
| 6   | **Remote Patches**  | Remote control templates                                             | Out of scope                                     |

**Arrangement** exports are often what you get when dumping the **Multi
edit buffer** from the panel: one `DUMP_MULTI` (267 bytes) plus sixteen
`DUMP_SINGLE` messages (524 bytes each). **Reference-style** transfers
send only `DUMP_MULTI` when the host requests a stored reference multi.

Message-level layouts:

- Multi: [multis.md](multis.md)
- Single: [single.md](single.md)
- Live multi edits (not full dumps): [multis.md#live-edit](multis.md#live-edit)

## Multi bank (TI series)

The Virus TI has **one Multi bank** with **128 Multi program slots**.

| Slots      | Type            | Contents                                                    |
| ---------- | --------------- | ----------------------------------------------------------- |
| **1–16**   | Embedded multi  | Multi parameters **plus** full Single data for all 16 parts |
| **17–128** | Reference multi | Multi parameters **plus** bank/program pointer per part     |

From OS **1.1** onward, slots 17–127 (documentation sometimes says
17–127 vs 17–128) add **reference-style** multis so older Multi
behavior (pointers only) coexists with TI embedded multis.

Whether the panel always dumps the **edit buffer** (arrangement-style)
vs a **stored** slot (reference-only payload) depends on export path
and tool — see capture notes in
[multis.md](multis.md#capture-baseline).
