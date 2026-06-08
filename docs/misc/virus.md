# Access Virus

General notes about Access Virus architecture

Desktop module only (not keyboard/Polar).

## Banks and programs

The Virus provides **four RAM banks** (A–D). Each bank holds **128 Single
programs**.

| Bank | Role |
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

## Paging

Access Virus singles expose parameters through **paged** live-edit space. The
**`cmd`** byte in a live-edit message selects which page holds the **`param`**
byte — the same **`param`** value under a different **`cmd`** is usually a
**different** control.

### Live-edit command bytes

| `cmd` | Page / scope | Typical use |
| ----- | ---------------- | ----------- |
| **`0x70`** | **Page A** | Single sound — filters, oscillators, many Edit FX rows, LFO 2 settings |
| **`0x71`** | **Page B** | Single sound — Common, EDIT ARP, EDIT LFO 1/3, many Edit FX rows |
| **`0x6E`** | **Part buffer** | Single sound in a Multi part — ring mod, some FX, mod-matrix amounts |
| **`0x6F`** | **Extended page** | Unison, arpeggiator user-pattern steps, Edit Single → Inputs |
| **`0x72`** | **Multi / common** | Edit Multi part settings, some Edit Single fields (e.g. Multi Tempo) |
| **`0x73`** | **Global / CONFIG** | Device-wide settings — [global.md](../live-edit/global.md) |

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7 # Multi / common (some Single params)
F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B
F0 00 20 33 01 00 70 <part> <param> <value> F7 # Page A (when Page A = SysEx)
F0 00 20 33 01 00 6E <part> <param> <value> F7 # Part single edit buffer
F0 00 20 33 01 00 6F <part> <param> <value> F7 # Extended page
F0 00 20 33 01 00 73 00 <param> <value> F7 # Global / CONFIG
```

Placeholders **`<part>`**, **`<param>`**, **`<value>`** are one byte each.

### Page A vs Page B

Many Single parameters are split between **Page A** and **Page
B**. On the TI, live edits use **`cmd=0x70`** (Page A) or **`cmd=0x71`** (Page
B). Which page a panel control uses is fixed per parameter — see the panel
live-edit docs and [parameter-options.md](../reference/parameter-options.md).

Some controls also exist on **`0x6E`** (part sound buffer) or **`0x6F`**
(extended). **Edit FX** adds **`0x6E`/`75`** and **`0x6E`/`76`** **SELECT**
bytes for sub-page focus (Delay vs Reverb vs …) — not the same as Page A/B.

### Param IDs are not global

Always interpret **`param`** together with **`cmd`** (and often **`part`**).
Example: **`0x0F`** on **`0x71`** is arpeggiator **Mode**; on **`0x72`** it is
**Master Clock** tempo.

### `<part>` byte

The **`<part>`** byte names **which edit buffer** receives the change:

| Target | Live edit `<part>` | Single Request `30 00 …` | Single Dump `@0x08` |
| ------------------ | -------------------- | -------------------------- | --------------------- |
| Multi Part 1–16 | **`0x00`–`0x0F`** | **`00`–`0F`** | **`00`–`0F`** |
| Single edit buffer | **`0x40`** | **`40`** | **`0x40`** |

Multi Part 1 (**`<part>=00`**) and the Single edit buffer (**`<part>=40`**) are
**separate RAM**. The wire **`<part>`** must match the buffer you intend.

**Exception:** Edit Multi **Bank** / **Program** (**`cmd=0x72`**, params
**`0x20`** / **`0x21`**) always use the Multi part index (**`0x00`–`0x0F`**),
never **`0x40`**.

Dump/request alignment and worked examples:
[single.md — Single vs Multi addressing](../dumps/single.md#single-vs-multi-addressing).

### MIDI Controller Page A / B

CONFIG chooses whether front-panel knobs emit **Access SysEx** or **MIDI CC /
pressure** for the two soft-knob pages. Set both to **SysEx** when capturing or
testing live-edit bytes.

**MIDI Controller Page A** — **`cmd=0x73`**, param **`0x5E`**:

| Value | Mode |
| ----- | --------------- |
| `00` | SysEx |
| `01` | Controller Data |

```text
F0 00 20 33 01 00 73 00 5E 00 F7 # Page A → SysEx
F0 00 20 33 01 00 73 00 5E 01 F7 # Page A → Controller Data
```

When **Page A = Controller Data**, many Page A parameters send **MIDI CC**
instead of **`cmd=0x70`** SysEx (e.g. Filter Cutoff → CC, Transpose → CC 93).

**MIDI Controller Page B** — **`cmd=0x73`**, param **`0x5F`**:

| Value | Mode |
| ----- | ------------- |
| `00` | SysEx |
| `01` | Poly Pressure |

```text
F0 00 20 33 01 00 73 00 5F 00 F7 # Page B → SysEx
F0 00 20 33 01 00 73 00 5F 01 F7 # Page B → Poly Pressure
```

Full global parameter list: [global.md](../live-edit/global.md).

## SysEx dump types

The Virus can export or stream several kinds of MIDI SysEx data:

| # | Name | Description | Project interest |
| --- | ------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1 | **Single Buffer** | One Single in the temporary edit buffer | Secondary — relates to arrangement exports |
| 2 | **Single Bank** | All 128 programs in a RAM bank (A–D) | **`0x32`** request, banks **`01`–`04`** — [bank.md](../dumps/bank.md#single-bank-request) |
| 3 | **Controller Dump** | One Single as a stream of live-edit SysEx (not Single Dump) | **`0x37`** — [controller-dump.md](../dumps/controller-dump.md) |
| 4 | **Arrangement** | Current Multi (or sequencer) buffer: **multi settings + 16 Singles** | Important — full performance snapshot |
| 5 | **Multi Bank** | All programs in the Multi bank (128 slots) | Important |
| 6 | **Remote Patches** | Remote control templates | Out of scope |

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

## Multi bank

See [multi.md — Embedded vs Reference
Multis](../dumps/multi.md#embedded-vs-reference-multis).

## Front-panel modes

The front panel exposes **Multi**, **Single**, and **Sequencer**
(**MULTI+SINGLE**) play/edit modes.

**Host → synth** — select mode with **`cmd=0x73`**, param **`0x7A`**:

| Mode | SysEx body |
| --------- | --------------- |
| Single | `73 00 7A 00` |
| Sequencer | `73 00 7A 01` |
| Multi | `73 00 7A 02` |

See [Play mode (`0x7A`)](../live-edit/global.md#play-mode).

**Synth → host** (panel) may emit **`cmd=0x73`**, param **`0x10`**, or empty
`F0 F7` frames — see [Edit mode `0x10`](../live-edit/global.md#edit-mode-0x10).

| Panel action | Typical SysEx from Virus |
| ---------------------------- | --------------------------------- |
| Select multi from bank | `73 00 10 00` (often twice) |
| Press **SINGLE** | `73 40 10 00` |
| **MULTI+SINGLE** / Sequencer | Empty `F0 F7` frames (no payload) |

This is separate from **parameter edits** — see [Paging — live-edit command bytes](#live-edit-command-bytes) (e.g. Filter Cutoff uses **`cmd=0x70`**).
