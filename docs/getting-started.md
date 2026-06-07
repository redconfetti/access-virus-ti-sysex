# Getting started

Access Virus SysEx is standard MIDI: one message per `F0 … F7` frame. The
docs use the same byte layout you see in a MIDI monitor or in `sendmidi hex
syx` (without the `F0`/`F7` wrappers — sendmidi adds those).

Prerequisites: [Setup](setup.md) (`sendmidi`, port choice, first messages).

## One message, byte by byte

```text
F0 00 20 33 01 00 <cmd> <payload> F7
│ └─ Access ─┘ │ │ │ │
│ fam dev command + data |
start (TI) ID end
```

| Bytes       | Role                                                                |
| ----------- | ------------------------------------------------------------------- |
| `F0` / `F7` | SysEx start / end (omit when using `sendmidi hex syx`)              |
| `00 20 33`  | Access Music manufacturer ID                                        |
| `01`        | Family (TI series)                                                  |
| `00`        | Device ID (`00`–`0F` = unit 1–16; match your synth)                 |
| **`<cmd>`** | **What kind of message this is** (see below)                        |
| *rest*      | Depends on command: bank/slot, parameter bytes, or a full dump body |

Placeholders like `<part>`, `<param>`, and `<value>` are **one byte each** in
the real message (shown as hex). Example — change one live parameter:

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7
```

`sendmidi` (no `F0`/`F7`):

```bash
sendmidi dev "Virus TI USB Plugin I/O" hex syx 00 20 33 01 00 72 00 4a 00
#                                                             │  │  │  └── value (0 = Off)
#                                                             │  │  └─────── param 0x4A
#                                                             │  └──────────── part 0 = Part 1
#                                                             └──────────────── cmd 0x72
```

## What `cmd=0x71` (and similar) means

In the docs, **`cmd=0x71`** means: the **command byte** at that position in
the SysEx is **`71` hexadecimal** (decimal 113). It tells the synth how to
interpret the bytes that follow — **not** a MIDI note or a UI percentage by
itself.

Rough groups:

| Command byte                  | Typical role                                                | Example                                                                                      |
| ----------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **`0x30`–`0x37`**             | **Requests** — ask the synth to **send** data back          | `0x30` = request one Single; `0x34` = request arrangement (Multi + 16 Singles)               |
| **`0x10`**, **`0x11`**        | **Dumps** — synth **replies** with a stored snapshot        | `0x10` = `DUMP_SINGLE` (524 bytes on TI); `0x11` = `DUMP_MULTI` (267 bytes)                  |
| **`0x70`–`0x73`**, **`0x6E`** | **Live edit** — change **one** parameter now (no full dump) | `0x71` = edit a Single “Page B” parameter; `0x72` = Multi/common; `0x6E` = part sound buffer |

So **`cmd=0x71`** in [live-edit](live-edit/README.md) is **live
parameter edit** on Page B (`0x71`; e.g. Smooth Mode `param 0x19`), not
“dump single” and not “dump arrangement”. **`cmd=0x10`** is the opposite
direction: a **full Single program** coming back from a request or save.

Request and dump commands: [bank.md](dumps/bank.md),
[arrangements.md](dumps/arrangements.md#request_multi-byte-table).

## What `0x23`-style values mean

**`0x` prefix = one byte written in hexadecimal** (0–255). On the wire,
MIDI SysEx data bytes are almost always **7-bit** (`00`–`7F` = 0–127).

The same notation is used for **different roles** — context tells you which:

| In docs                                | Meaning                                                         | Example                          |
| -------------------------------------- | --------------------------------------------------------------- | -------------------------------- |
| **`cmd=0x72`**                         | Command byte in the **message header**                          | Live Multi edit                  |
| **`param 0x4A`** / **`0x72` / `0x4A`** | **Parameter index** in a live-edit message                      | Hold Pedal enable                |
| **`<value> 00`**                       | **Parameter value** in a live-edit message                      | Off / 0% / minimum               |
| **`0x29`**, **`0x0D..0x16`**           | **Offset** inside a **dump** (byte index from start of `F0`)    | “Part bank lives at byte `0x29`” |
| **`bank 01`**, **`slot 40`**           | **Address** bytes in requests/dump headers (which program slot) | RAM A program 0 → `01` `00`      |

**Offsets** (`0x29`, `0x209`, …) are **positions in the 524- or 267-byte
dump file**, not separate MIDI messages. **Live-edit** lines like
`71 00 19 00` are **not** offsets — they are **param** and **value** bytes
right after `cmd` and `part`.

Some parameters use **encoded** values (not “what you see on the LCD”):

- Direct **`0`–`127`** (e.g. Reverb Send)
- **Bipolar**: `stored = ui + 64` (UI −64 → byte `00`)
- **Tempo**: `stored = bpm − 63`

The parameter map tables mark **Live edit** as command + param (e.g.
`71` / `0x19`) and **Dump offset** as a hex position when known.

## Implementer notes {#implementer-notes}

**Scope:** This repo documents **SysEx** — message bytes, confirmed
encodings, and hardware TX/RX where tested. It does **not** specify full panel
layout, menu flow, or LED behaviour except where needed to interpret a byte.

For **host software** or **AI agents** building against this spec:

**Parameter IDs are not global.** The same **`param`** byte means different
controls under different **`cmd`** bytes. Example: **`70`/`13`** = Oscillator 1
wave; **`6E`/`13`** = Filter Bank Type.

**Context-dependent reuse.** One **`cmd`/`param`** pair can change encoding with
another setting. Example: decode **`70`/`6A`** and **`70`/`6B`** using
**`70`/`67`** (Chorus Type); decode **`70`/`77`** using [Delay
Type](../parameter-options.md#delay-type).

**Prefer confirmed tables over inference.** Rows marked **TBD** or “dump only”
were not verified on TI mk2 hardware; do not assume names match panel text.

## Requests vs dumps vs live edits

```text
# Request: “send me the edit-buffer Multi” (you receive DUMP_MULTI 0x11)
F0 00 20 33 01 00 31 00 7f F7

# Request: “send arrangement” → DUMP_MULTI + 16 × DUMP_SINGLE
F0 00 20 33 01 00 34 00 F7

# Reply fragment: start of a Single dump (cmd 0x10, bank 00, slot = part 1)
F0 00 20 33 01 00 10 00 00 … F7

# Live edit: set one parameter (no full program transfer)
F0 00 20 33 01 00 71 00 19 00 F7
```

**Single mode “load program”:** there is no short SysEx “load bank/slot by
reference” — use **MIDI Program Change**, or **`0x30` + full `0x10` upload**
for editor/backup workflows. See
[bank.md — Single mode program recall](dumps/bank.md#single-mode-program-recall).

Not everything is SysEx: some controls use **MIDI CC** only (e.g. Patch
Volume = CC 91). See [control-change.md](control-change.md).

## Where to go next

| You want…                                    | Start here                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------- |
| Build an editor / agent against this spec    | [Implementer notes](#implementer-notes) · [live-edit](live-edit/README.md)      |
| Request/dump command list                    | [dumps/bank.md](dumps/bank.md) · [dumps/arrangements.md](dumps/arrangements.md) |
| Live edit (by panel menu)                    | [live-edit/README.md](live-edit/README.md)                                      |
| Dumps (single / multi / banks)               | [dumps/README.md](dumps/README.md)                                              |
| Banks, arrangement, architecture             | [virus.md](virus.md)                                                            |
| OsTIrus (TI2 firmware in a DAW, no hardware) | [ostirus.md](ostirus.md)                                                        |

Full topic index: [README — Documentation](../README.md#documentation).
Doc standards: `.cursor/skills/documentation-standards/SKILL.md`.
