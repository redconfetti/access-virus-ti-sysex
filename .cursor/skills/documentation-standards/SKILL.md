---
name: documentation-standards
description: >-
 Documents Access Virus SysEx in this repo: what to retain, doc hierarchy,
 reference/parameter-options.md for enums, live-edit by panel section, SysEx
 examples per parameter. Use when adding or editing docs/live-edit, docs/dumps,
 or parameter option tables.
disable-model-invocation: true
---

# Documentation standards (Access Virus SysEx)

Apply when writing or restructuring documentation in this repository.

## Specification retention

Documentation should contain only:

1. **Confirmed SysEx commands or responses**

2. **Data dump SysEx and structure** — Single, Multi, Bank, Controller,
   Arrangement

3. **Enum tables** — parameter labels, options, hex values, offsets, and anything
   else needed to build supported SysEx messages

4. **Summary tables with SysEx examples** — fenced `text` blocks as templates or
   concrete examples:

   ```text
   F0 00 20 33 01 00 72 <part> <param> <value> F7 # multi / common (some params)
   F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B single (some params)
   F0 00 20 33 01 00 70 <part> <param> <value> F7 # Page A single (when global Page A = SysEx)
   F0 00 20 33 01 00 6E <part> <param> <value> F7 # part single edit buffer
   ```

   ```text
   F0 00 20 33 01 00 70 00 28 00 F7 # Cutoff 0 (landing)
   F0 00 20 33 01 00 70 00 28 7F F7 # Cutoff max (127 on wire)
   ```

5. **Conditional visibility** — which parameters apply when other options in the
   same group are chosen (Type, Mode, etc.)

## Organization

Docs follow this hierarchy. Link from [README.md](../../README.md) only — not
nested READMEs under `docs/`.

* [docs/live-edit/](../../docs/live-edit/)
  * [docs/live-edit/single/](../../docs/live-edit/single/)
    * [single.md](../../docs/live-edit/single/single.md) — Common, Unison,
      Envelope 3/4, Velocity Map, Soft Knobs, etc.
    * [oscillators.md](../../docs/live-edit/single/oscillators.md) — Osc 1–3,
      Sub-Osc, Mixer, Noise, Ring Modulator, FM, etc.
    * [filters.md](../../docs/live-edit/single/filters.md) — Filters, Filter
      Envelopes, Amp Envelope, etc.
    * [modulators.md](../../docs/live-edit/single/modulators.md) — LFO 1/2/3
    * [mod-matrix.md](../../docs/live-edit/single/mod-matrix.md) — Mod Matrix
      slots 1–6
    * [arpeggiator.md](../../docs/live-edit/single/arpeggiator.md)
    * [effects.md](../../docs/live-edit/single/effects.md)
  * [multis.md](../../docs/live-edit/multis.md) — Edit Multi SysEx
  * [global.md](../../docs/live-edit/global.md) — Global / CONFIG SysEx
* [docs/dumps/](../../docs/dumps/)
  * [single.md](../../docs/dumps/single.md) — Single Dump layout
  * [multi.md](../../docs/dumps/multi.md) — Multi Dump layout
  * [controller.md](../../docs/dumps/controller.md) — Controller Dump Request
  * [bank.md](../../docs/dumps/bank.md) — Bank / request commands
* [docs/reference/](../../docs/reference/)
  * [parameter-options.md](../../docs/reference/parameter-options.md) — Full
    value tables (link targets only — no index; link from live-edit/dump docs)
* [docs/misc/](../../docs/misc/)
  * [virus.md](../../docs/misc/virus.md) — Architecture (banks, dump types,
    modes, Paging)
  * [ostirus.md](../../docs/misc/ostirus.md)

Also: [getting-started.md](../../docs/getting-started.md) (testing and SysEx
primer) and [README.md](../../README.md) (documentation TOC).

## File roles

| File / area                                                                      | Role                                                                           |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [docs/reference/parameter-options.md](../../docs/reference/parameter-options.md) | **Link target** — full wire maps and panel enums (no TOC; reached via anchors) |
| [Documentation](../../README.md#documentation)                                   | Live SysEx per **panel section** — `cmd` / `param` / encoding + **examples**   |
| [Documentation](../../README.md#documentation)                                   | Single Dump / Multi Dump layout and parameter **inventory**                    |
| [README.md](../../README.md)                                                     | Documentation TOC                                                              |
| [docs/getting-started.md](../../docs/getting-started.md)                         | SysEx testing (`sendmidi`), primer (`cmd`, requests vs live edit)              |

**Do not** put enum option tables or shared value-encoding tables in live-edit
files — link to `reference/parameter-options.md#anchor` instead.

## Logical sections

Organize live-edit and dump inventory rows to match the synth’s menus:

| Section                                                       | Live-edit doc                                                | Dump inventory (`single.md`)                                       |
| ------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Config**                                                    | [global.md](../../docs/live-edit/global.md)                  | Global / Patch Utility — Config                                    |
| **Single** (Common, Soft Knobs, Unison, Env 3/4, Velocity, …) | [single.md](../../docs/live-edit/single/single.md)           | Common, Soft Knobs, …                                              |
| **Multi**                                                     | [multis.md](../../docs/live-edit/multis.md)                  | (multi map in [multi.md](../../docs/dumps/multi.md))               |
| **Oscillators**                                               | [oscillators.md](../../docs/live-edit/single/oscillators.md) | Oscillators                                                        |
| **Filters**                                                   | [filters.md](../../docs/live-edit/single/filters.md)         | Filters, Amplifier                                                 |
| **Effects**                                                   | [effects.md](../../docs/live-edit/single/effects.md)         | FX 1 / FX 2                                                        |
| **Modulators**                                                | [modulators.md](../../docs/live-edit/single/modulators.md)   | LFO                                                                |
| **Matrix**                                                    | [mod-matrix.md](../../docs/live-edit/single/mod-matrix.md)   | Modulation Matrix                                                  |
| **Arpeggiator**                                               | [arpeggiator.md](../../docs/live-edit/single/arpeggiator.md) | Arpeggiator                                                        |

Add new parameters under the correct section file — do not append unrelated
blocks to `effects.md` or `single.md`.

## Every parameter section must include

1. **Panel path** — e.g. `EDIT FX → Distortion → Mix`.
2. **Live edit** — `cmd`, `param`, and a **minimal** value summary (range
   formula, or endpoints / exceptions — not the full wire table).
3. **SysEx examples** — fenced `text` block; pick anchors that teach the
   encoding:
   * **Bipolar centered** — minimum, center, maximum (e.g. `00`, `40`, `7F`).
   * **Unipolar percent** — `00`, `40`, `7F` (0 %, 50 %, 100 %).
   * **Named exceptions** — include the special label (e.g. Key Follow **Norm**
     @ `60`) in addition to min/center/max when relevant.
   * **Note index** — lowest and highest note (e.g. C1 `00`, G9 `7F`).
4. **Full options link** — *after* the range summary and SysEx block, link to
   [parameter-options.md](../../docs/reference/parameter-options.md) for the
   complete value table or panel enum. The live-edit section should stand alone
   for basic SysEx generation; the reference doc resolves any remaining ambiguity.

Example (bipolar centered):

```text
F0 00 20 33 01 00 70 00 5D 00 F7 # −64
F0 00 20 33 01 00 70 00 5D 40 F7 # +0
F0 00 20 33 01 00 70 00 5D 7F F7 # +63
```

Full wire map: [Bipolar centered (±64 @ 0x40)](../../docs/reference/parameter-options.md#bipolar-centered-64--0x40).

### Parameter block template

```markdown
### Control name

**Live edit:** `cmd=0x..`, param `0x..`.

**Panel → Submenu → Control**. Range: **−64..+63** → `stored = ui + 64`.

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

\`\`\`text
F0 00 20 33 01 00 … 00 F7 # minimum
F0 00 20 33 01 00 … 40 F7 # center
F0 00 20 33 01 00 … 7F F7 # maximum
\`\`\`

Full wire map: [Bipolar centered (±64 @ 0x40)](../../docs/reference/parameter-options.md#bipolar-centered-64--0x40).
```

Use clean heading text only (no `{#…}` custom anchors, no `cmd`/param in the
title). Wire bytes live on the **Live edit:** line under the heading. Duplicate
titles within one file get `-1`, `-2`, … suffixes in auto-generated slugs.

## parameter-options.md rules

Two section kinds:

* **Value encodings** — shared formulas and **full** wire tables. Distinguish
  variants when they differ (e.g. bipolar **±64 @ 0x40** vs Edit Multi live
  **−63..+64**; Key Follow **Norm** @ `0x60`). Live-edit docs show range +
  min/center/max examples only; link here for every label and hex value.
* **Panel option enums** — named menu choices (Mode, Type, Pattern, …). Same
  split: live-edit shows range and representative examples; full enum table
  lives here.

Do **not** add a file-level index or TOC to `parameter-options.md` — other docs
link directly to section anchors.

For panel enums:

* One section per enum or panel-visibility family.
* Tables: index or wire `<value>`, option label, meaning.
* Use descriptive heading text for stable auto-generated anchor slugs.
* Panel visibility tables (which controls appear per mode) belong **here**, not
 in live-edit prose.

## Dump map rules

* [single.md](../../docs/dumps/single.md): inventory columns **Control**,
 **SubCategory**, **Dump offset**, **Live edit** (link to live-edit anchor).

## Hardware mapping

When confirming against hardware, use
[hardware-mapping-workflow](../hardware-mapping-workflow/SKILL.md) — not
ad-hoc capture steps in random doc files.

## Style

* [markdownlint](https://github.com/DavidAnson/markdownlint) — project
 `.markdownlint.json` (`line_length: 120`, aligned tables). **Do not edit
 `.markdownlint.json`** unless the user asks and approves — fix markdown
 content instead.
* Prefer links over pasting large tables twice.
