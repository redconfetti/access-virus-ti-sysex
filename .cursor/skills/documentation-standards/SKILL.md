---
name: documentation-standards
description: >-
 Documents Access Virus TI SysEx in this repo: parameter-options.md for enums,
 live-edit by panel section, SysEx examples per parameter. Use when adding or
 editing docs/single-live-edit, docs/dumps, or parameter option tables.
disable-model-invocation: true
---

# Documentation standards (Access Virus TI SysEx)

Apply when writing or restructuring documentation in this repository.

## File roles

| File / area                                                  | Role                                                                          |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| [docs/parameter-options.md](../../docs/parameter-options.md) | **All** option/value lookup tables (enums, panel visibility, LCD curves)      |
| [docs/live-edit/](../../docs/live-edit/README.md)            | Live SysEx per **panel section** — `cmd` / `param` / encoding + **examples**  |
| [docs/dumps/](../../docs/dumps/README.md)                    | `DUMP_SINGLE` / `DUMP_MULTI` layout and parameter **inventory** (offsets TBD) |
| [docs/setup.md](../../docs/setup.md)                         | Tools, ports, first `sendmidi` message                                        |
| [docs/getting-started.md](../../docs/getting-started.md)     | SysEx primer (`cmd`, requests vs live edit)                                   |

**Do not** put enum option tables in live-edit files — link to
`parameter-options.md#anchor` instead.

## Virus TI logical sections

Organize live-edit and dump inventory rows to match the synth’s menus:

| Section                                                       | Live-edit doc                                         | Dump inventory (`single.md`)                                       |
| ------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| **Config**                                                    | [edit-config.md](../../docs/live-edit/edit-config.md) | Global / Patch Utility — Config                                    |
| **Single** (Common, Soft Knobs, Unison, Env 3/4, Velocity, …) | [edit-single.md](../../docs/live-edit/edit-single.md) | Common, Soft Knobs, …                                              |
| **Multi**                                                     | [edit-multi.md](../../docs/live-edit/edit-multi.md)   | (multi map in [arrangements.md](../../docs/dumps/arrangements.md)) |
| **Oscillators**                                               | [oscillators.md](../../docs/live-edit/oscillators.md) | Oscillators                                                        |
| **Filters**                                                   | [filters.md](../../docs/live-edit/filters.md)         | Filters, Amplifier                                                 |
| **Effects**                                                   | [effects.md](../../docs/live-edit/effects.md)         | FX 1 / FX 2                                                        |
| **Modulators**                                                | [modulators.md](../../docs/live-edit/modulators.md)   | LFO                                                                |
| **Matrix**                                                    | *TBD*                                                 | Modulation Matrix                                                  |
| **Arpeggiator**                                               | [arpeggiator.md](../../docs/live-edit/arpeggiator.md) | Arpeggiator                                                        |

Add new parameters under the correct section file — do not append unrelated
blocks to `effects.md` or `edit-single.md`.

## Every parameter section must include

1. **Panel path** — e.g. `EDIT FX → Distortion → Mix`.
2. **Live edit** — `cmd`, `param`, value encoding (formula or enum link).
3. **SysEx examples** — fenced `text` block with full lines (include `F0`/`F7`
 in docs for readability; note `sendmidi` omits them). See template below.
4. **Confirmed** — Hardware TX / panel / capture when known; otherwise mark
 **TBD**.
5. **Enums** — link to [parameter-options.md](../../docs/parameter-options.md);
 table lives there, not duplicated.

Example SysEx block (Distortion Mix):

```text
F0 00 20 33 01 00 6E 00 48 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 48 40 F7 # 50.0 %
F0 00 20 33 01 00 6E 00 48 7F F7 # 100.0 %
```

### Parameter block template

```markdown
### Control name (`cmd=0x..`, param `0x..`) {#anchor-id}

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

Use explicit `{#anchor-id}` when cross-linked from other files.

## parameter-options.md rules

- One section per enum or panel-visibility family.
- Tables: index or wire `<value>`, option label, confirmation column when known.
- Anchor headings for stable links from live-edit and dumps.
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
