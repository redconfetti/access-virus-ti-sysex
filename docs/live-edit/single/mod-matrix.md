# Modulation Matrix

Edit Single — **Modulation Matrix** — **six slots**. Each slot has **one**
**Source** and **three** **Destination** / **Amount** pairs (modulation routes).

Part of [Documentation](../../../README.md#documentation). Source and destination enums:
[Mod Matrix Sources](../../reference/parameter-options.md#mod-matrix-sources),
[Mod Matrix Destinations](../../reference/parameter-options.md#mod-matrix-destinations).
Amount encoding: [Mod Matrix Amount](../../reference/parameter-options.md#mod-matrix-amount).
Dump worksheet: [single.md — Modulation Matrix](../../dumps/single.md#modulation-matrix).
All **42** Source / Destination / Amount cells confirmed in **Single Dump**
(`30 00 40` / `<part>=0x40`).

Paging: [virus.md](../../misc/virus.md#part-byte). **`cmd`** and **param** depend on **slot** and **row** — there is
no single global **`41`** / **`42`** pair for all slots.

## Slot layout

Each of the **six** matrix slots on the panel:

```text
Slot N
├── Source          (one menu — shared by all three routes below)
├── Destination 1   + Amount 1
├── Destination 2   + Amount 2
└── Destination 3   + Amount 3
```

There is **no** per-row Source — only **Destination** and **Amount** repeat
three times.

## Per-slot `cmd` / param map

Full enum sweeps on all six slots; all **42** cells verified on Single edit
buffer **`30 00 40`**.

| Slot | Source | Dest 1 | Amt 1 | Dest 2 | Amt 2 | Dest 3 | Amt 3 |
| ----- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| **1** | `71`/`40` | `71`/`41` | `71`/`42` | `6E`/`5A` | `6E`/`5B` | `6E`/`5C` | `6E`/`5D` |
| **2** | `71`/`43` | `71`/`44` | `71`/`45` | `71`/`46` | `71`/`47` | `6E`/`5E` | `6E`/`5F` |
| **3** | `71`/`48` | `71`/`49` | `71`/`4A` | `71`/`4B` | `71`/`4C` | `71`/`4D` | `71`/`4E` |
| **4** | `71`/`67` | `71`/`68` | `71`/`69` | `6E`/`60` | `6E`/`61` | `6E`/`62` | `6E`/`63` |
| **5** | `71`/`6A` | `71`/`6B` | `71`/`6C` | `6E`/`64` | `6E`/`65` | `6E`/`66` | `6E`/`67` |
| **6** | `71`/`6D` | `71`/`6E` | `71`/`6F` | `6E`/`68` | `6E`/`69` | `6E`/`6A` | `6E`/`6B` |

**Layout notes:**

- **Slots 1–3** pack into Page B **`40`–`4E`** (Slot 3 uses **`71`** for all
  three rows). **Slots 4–6** use Page B **`67`–`6F`** for Source + row 1 only.
- **Rows 2–3** use **`6E`** for slots **1**, **2** (row 3 only), **4**–**6** —
  not for Slot **3** (all rows stay on **`71`**).
- **`<value>`** namespaces are unchanged: source enum; destination = [LFO Assign
  Target](../../reference/parameter-options.md#assign-target) wire map; amount bipolar
  offset.

### Page B byte reuse

Several matrix params share Page B bytes with other EDIT pages when those pages
are active — decode by **panel context** (selected slot / row), not param alone:

- **Slot 2** **`43`–`47`** — same bytes as **LFO 1** settings (Rate, Shape, …).
- **Slot 3** **`48`–`49`** — same bytes as **LFO 1** Key Follow / Trigger Phase.

## Examples

```text
# Slot 1 — Source LFO 1 bipolar
F0 00 20 33 01 00 71 40 40 15 F7
# Slot 1 row 1 — Filter 1 Cutoff, +0
F0 00 20 33 01 00 71 40 41 18 F7
F0 00 20 33 01 00 71 40 42 40 F7
# Slot 1 row 2 — same destination namespace on 6E
F0 00 20 33 01 00 6E 40 5A 18 F7
F0 00 20 33 01 00 6E 40 5B 40 F7

# Slot 2 row 2 — Filter 1 Env Amount, −64 (spot-check ✓)
F0 00 20 33 01 00 71 40 46 1C F7
F0 00 20 33 01 00 71 40 47 00 F7

# Slot 3 row 2 — Osc 2 Wave Select, −17 (spot-check ✓; all rows on 71)
F0 00 20 33 01 00 71 40 4B 0D F7
F0 00 20 33 01 00 71 40 4C 2F F7

# Slot 6 row 1 — Distortion Mix, −39 (spot-check ✓)
F0 00 20 33 01 00 71 40 6E 7F F7
F0 00 20 33 01 00 71 40 6F 19 F7
```

### Source

**`<value>`** wire map: [Mod Matrix Sources](../../reference/parameter-options.md#mod-matrix-sources)
(not the table **Index** column). Param **`0x40`** is **Slot 1** only — see table
above for slots **2**–**6**.

### Destination

**`<value>`** wire map: same namespace as [LFO 1 Assign Target](../../reference/parameter-options.md#assign-target)
(**`4F/xx`** = **`41/xx`** = **`5A/xx`**, etc., for the same target on the
matching slot/row param). Panel label **Filterbank Frequency** uses wire **`60`**.

### Amount

Bipolar **−64..+63** → `stored = ui + 64` (**`00`** = −64, **`40`** = +0,
**`7F`** = +63). Same family as [LFO Contour](../../reference/parameter-options.md#contour-1).

| `<value>` | LCD |
| --------- | --- |
| `00` | −64 |
| `19` | −39 |
| `2F` | −17 |
| `40` | +0 |
| `7F` | +63 |
