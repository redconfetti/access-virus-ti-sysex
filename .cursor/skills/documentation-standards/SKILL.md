---
name: documentation-standards
description: >-
 Documents Access Virus TI SysEx in this repo: reference/parameter-options.md for enums,
 live-edit by panel section, SysEx examples per parameter. Use when adding or
 editing docs/live-edit, docs/dumps, or parameter option tables.
disable-model-invocation: true
---

# Documentation standards (Access Virus TI SysEx)

Apply when writing or restructuring documentation in this repository.

## File roles

| File / area                                                  | Role                                                                          |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| [docs/reference/parameter-options.md](../../docs/reference/parameter-options.md) | **All** option/value lookup tables (enums, panel visibility, LCD curves)      |
| [Documentation](../../README.md#documentation)            | Live SysEx per **panel section** — `cmd` / `param` / encoding + **examples**  |
| [Documentation](../../README.md#documentation)                    | Single Dump / Multi Dump layout and parameter **inventory** (offsets TBD) |
| [README.md](../../README.md)                         | Tools, ports, first `sendmidi` message                                        |
| [docs/getting-started.md](../../docs/getting-started.md)     | SysEx primer (`cmd`, requests vs live edit)                                   |

**Do not** put enum option tables in live-edit files — link to
`reference/parameter-options.md#anchor` instead.

## Virus TI logical sections

Organize live-edit and dump inventory rows to match the synth’s menus:

| Section                                                       | Live-edit doc                                         | Dump inventory (`single.md`)                                       |
| ------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| **Config**                                                    | [global.md](../../docs/live-edit/global.md) | Global / Patch Utility — Config                                    |
| **Single** (Common, Soft Knobs, Unison, Env 3/4, Velocity, …) | [single.md](../../docs/live-edit/single/single.md) | Common, Soft Knobs, …                                              |
| **Multi**                                                     | [multis.md](../../docs/live-edit/multis.md)   | (multi map in [multi.md](../../docs/dumps/multi.md)) |
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
2. **Live edit** — `cmd`, `param`, value encoding (formula or enum link).
3. **SysEx examples** — fenced `text` block with full lines (include `F0`/`F7`
 in docs for readability; note `sendmidi` omits them). See template below.
4. **Confirmed** — Hardware TX / panel / capture when known; otherwise mark
 **TBD**.
5. **Enums** — link to [parameter-options.md](../../docs/reference/parameter-options.md);
 table lives there, not duplicated.

Example SysEx block (Distortion Mix):

```text
F0 00 20 33 01 00 6E 00 48 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 48 40 F7 # 50.0 %
F0 00 20 33 01 00 6E 00 48 7F F7 # 100.0 %
```

### Parameter block template

```markdown
### Control name

**Live edit:** `cmd=0x..`, param `0x..`.

**Panel → Submenu → Control**. One-line encoding summary.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 <cmd> <part> <param> <value> F7` |
| Panel range    | …                                                   |
| Confirmed      | Hardware TX (…)                                     |

\`\`\`text
F0 00 20 33 01 00 … F7 # comment
\`\`\`
```

Use clean heading text only (no `{#…}` custom anchors, no `cmd`/param in the
title). Wire bytes live on the **Live edit:** line under the heading. Duplicate
titles within one file get `-1`, `-2`, … suffixes in auto-generated slugs.

## parameter-options.md rules

- One section per enum or panel-visibility family.
- Tables: index or wire `<value>`, option label, confirmation column when known.
- Use descriptive heading text for stable auto-generated anchor slugs.
- Panel visibility tables (which controls appear per mode) belong **here**, not
 in live-edit prose.

## Dump map rules

- [single.md](../../docs/dumps/single.md): worksheet columns **Control**,
 **SubCategory**, **Dump offset**, **Live edit** (link to live-edit anchor).
- Fill **Dump offset** only when correlated from captures — do not guess.

## Hardware mapping

When confirming against hardware, use
[hardware-mapping-workflow](../hardware-mapping-workflow/SKILL.md) — not
ad-hoc capture steps in random doc files.

## Style

- [markdownlint](https://github.com/DavidAnson/markdownlint) — project
 `.markdownlint.json` (`line_length: 120`, aligned tables). **Do not edit
 `.markdownlint.json`** unless the user asks and approves — fix markdown
 content instead.
- Prefer links over pasting large tables twice.
