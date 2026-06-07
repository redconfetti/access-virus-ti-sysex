# Unmapped and outstanding parameters

Living checklist of **gaps** in this repo — parameters or byte regions that are
**not yet** fully correlated, **intentionally absent** from a dump type, or
**not applicable** on TI mk2 hardware. Use this when asking “what’s left to map?”

**Worksheets (what *is* mapped):**

- Single sound data: [dumps/single.md — parameter map](dumps/single.md#single-parameter-map)
- Multi arrangement: [dumps/arrangements.md — Multi parameter map](dumps/arrangements.md#multi-parameter-map)
- Live edit by menu: [live-edit/README.md](live-edit/README.md)
- CONFIG / globals: [live-edit/edit-config.md](live-edit/edit-config.md)

Hardware workflow: [testing.md](testing.md) · skill
`hardware-mapping-workflow`.

---

## Summary

| Scope                                                | Status                                                                                                                         |
| -----                                                | ------                                                                                                                         |
| **Single sound editing** (`DUMP_SINGLE`, `30 00 40`) | **Essentially complete** for TI mk2 panel menus                                                                                |
| **Single patch editor blockers**                     | Surround **Output** (live edit only); **Single patch rename** (bytes in dump, no SysEx)                                        |
| **CONFIG / Global**                                  | Out of scope unless the panel emits SysEx — see [edit-config.md](live-edit/edit-config.md) for confirmed **`0x73`** wires only |

---

## Single sound parameters — mapped (done)

These sections have **live-edit SysEx** and **`DUMP_SINGLE`** dump offsets
(hardware-verified on `-INIT-`, Single edit buffer **`<part>=0x40`**, unless
noted):

| Section                                                                     | Doc                                                                                           |
| -------                                                                     | ---                                                                                           |
| Oscillators                                                                 | [oscillators.md](live-edit/oscillators.md)                                                    |
| Filters (+ velocity targets, env 3/4, amp env)                              | [filters.md](live-edit/filters.md)                                                            |
| LFO 1–3                                                                     | [modulators.md](live-edit/modulators.md)                                                      |
| Mod Matrix (6 slots)                                                        | [modulation-matrix.md](live-edit/modulation-matrix.md)                                        |
| Arpeggiator (+ user pattern)                                                | [arpeggiator.md](live-edit/arpeggiator.md)                                                    |
| Edit FX                                                                     | [effects.md](live-edit/effects.md)                                                            |
| Edit Single — Common, Unison, Env 3/4, Velocity Map, Categories, Soft Knobs | [edit-single.md](live-edit/edit-single.md)                                                    |
| Surround **Balance**                                                        | [edit-single.md — Surround](live-edit/edit-single.md#surround-edit-single) → dump **`0x0C2`** |
| Inputs (Mode / Select / Atomizer)                                           | [edit-config.md — Inputs](live-edit/edit-config.md#inputs-edit-single) → **`0x205`–`0x207`**  |

---

## Documented sound params — intentionally not in `DUMP_SINGLE`

| Parameter                  | Live edit                        | Notes                                                                                                              |
| ---------                  | ---------                        | -----                                                                                                              |
| Surround **Output**        | `73` / `0x2D`, **`<part>=0x40`** | [edit-single.md](live-edit/edit-single.md#surround-edit-single). Hardware-tested: **no** `30 00 40` payload change |
| Multi Tempo / Master Clock | `72` / `0x0F`                    | Global Multi tempo; in **`DUMP_MULTI`** only at **`0x18`**, not Single payload                                     |

**Note:** Bend Up / Down / Scale and Smooth Mode **are** stored in
**`DUMP_SINGLE`** at **`0x0A1`–`0x0A4`**. [edit-multi.md](live-edit/edit-multi.md)
correctly marks bends as **not in `DUMP_MULTI`** — that is Multi-specific, not
Single.

---

## In the dump, not fully mapped as editable parameters

| Item                                                        | Notes                                                                    |
| ----                                                        | -----                                                                    |
| **Single patch name** (ASCII ~**`0xFA`**)                   | Present in dump; **no live-edit SysEx** documented for renaming          |
| **Single name / metadata block** ~**`0xF8`–`0x103`**        | Name Cat 1/2 at **`0x103`/`0x104`**; surrounding bytes not fully decoded |
| **Header / trailer** **`0x09`–`0x0B`**, **`0x204`–`0x208`** | Structural; not tied to panel controls                                   |

| **Edit Multi** | Core part fields mapped; payload holes remain |

---

## CONFIG / Global (`cmd=0x73`)

**Out of scope** for Single sound mapping. This repo documents CONFIG only where
**hardware TX** or confirmed **`sendmidi`** captures exist — see
[edit-config.md](live-edit/edit-config.md). Panel-only globals (no SysEx on TI
mk2 desktop) are **not** listed here or in the parameter inventory.

**`DUMP_MULTI`** correlation for globals is **unverified** and low priority.

---

## Edit Multi — separate worksheet

**Mapped:** multi program name (**`0x0D`–`0x16`**, null **`0x17`** — panel rename,
no SysEx), bank, program, MIDI channel, key range, transpose, detune, volume,
init volume, output routing, panorama, packed flags (Enable, Hold, Priority,
Program Change, …). See [edit-multi.md](live-edit/edit-multi.md) and
[arrangements.md](dumps/arrangements.md).

### Documented; not in `DUMP_MULTI`

| Parameter         | Live edit                                               |
| ---------         | ---------                                               |
| Secondary Output  | `73` / `0x2D`                                           |
| Bend Up / Down    | `71` / `0x1A`, `0x1B` (in **`DUMP_SINGLE`**, not Multi) |
| Keyboard-related  | `72` / `0x40` (desktop; label TBD)                      |
| Keyboard to MIDI  | Global CONFIG — **no dump byte** on desktop module      |
| Direct Monitoring | VC-only; byte not found                                 |

### Unmapped Multi payload regions

From [arrangements.md — unmapped payload](dumps/arrangements.md#unmapped-payload):

| Offset range                 | Notes                                   |
| ------------                 | -----                                   |
| **`0xB9`–`0xC7`**            | All **`0x00`** in current captures      |
| **`0xE8`–`0xF7`**            | All **`0x00`** in current captures      |
| **`0x19`–`0x28`** (16 bytes) | Partially understood; not fully decoded |

---

## Not real TI mk2 gaps (safe to ignore)

Inventory / AURA leftovers — strikethrough / **N/A** rows in
[single.md — parameter map](dumps/single.md#single-parameter-map) (e.g. duplicate
osc/sync inventory labels, analog-mode toggle, Filter 2 cutoff).

**Enum spot-checks:** [parameter-options.md](parameter-options.md) documents
many lists with endpoint confirmation only (“not yet spot-checked”); wire bytes
are often mapped — full LCD sweeps are optional polish.

**Other TBD (protocol, not panel):**

- [controller-dump.md](dumps/controller-dump.md) — unmapped `cmd`/`param` pairs from `0x37` stream
- TI **store** path for RAM banks ([bank.md](dumps/bank.md))
- Multi Bank Request (`0x33`) reply format

---

## Worksheet inconsistencies (docs only)

Not missing hardware — tidy when touching those files:

| Issue                                                                               | Fix                                                    |
| -----                                                                               | ---                                                    |
| **Amplifier** Patch Volume / Panorama rows in [single.md](dumps/single.md)          | Duplicate of **Common** — use **`0x063`**, **`0x012`** |
| [filters.md](live-edit/filters.md) “Filters queue” link to [testing.md](testing.md) | Stale; filter velocity rows are mapped                 |

---

## Suggested next passes

1. **Single patch name block** — decode ~**`0xF8`–`0x103`**; find rename SysEx if it exists.
2. **Edit Multi holes** — probe **`0xB9`–`0xC7`**, **`0xE8`–`0xF7`** when a control is found that changes them.
3. **CONFIG `0x73`** — add to [edit-config.md](live-edit/edit-config.md) only when panel TX
   or host capture confirms a wire byte.

When a row is confirmed, move it into the appropriate live-edit or dump doc and
**remove or update** the matching section here.
