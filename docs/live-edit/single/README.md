# Single live edit

Guides in this folder document **Edit Single** SysEx — parameters on the
**OSCILLATORS**, **FILTERS**, **EDIT FX**, **EDIT ARP**, **EDIT LFO**, **Common**,
and related panels.

## Single edit buffer (default)

**All SysEx examples in these guides target the Single edit buffer** —
**`<part>` = `0x40`**.

That is the RAM holding the sound you edit in **Single** mode (or the sound
loaded into the Single edit slot). It is **not** the same memory as a Multi
part.

| Target             | Live-edit `<part>` |
| ------------------ | ------------------ |
| Multi Part 1–16    | **`0x00`–`0x0F`**  |
| Single edit buffer | **`0x40`**         |

See also [Paging — `<part>` byte](../../misc/virus.md#part--byte).

## Multi edit buffer parts

The **same** `cmd` / `param` / `value` messages work for **Multi** — change
only **`<part>`** to the zero-based part index (**`0x00`** = Part 1, **`0x01`**
= Part 2, … **`0x0F`** = Part 16).

### Example — Osc Volume

**Oscillators → EDIT → Common → Osc Volume** — Page A, param **`0x24`**. Bipolar
**−64..+63** → `stored = ui + 64` (wire **`40`** = LCD **`<0>`**).

```text
F0 00 20 33 01 00 70 <part> 24 <value> F7
```

```text
F0 00 20 33 01 00 70 00 24 40 F7 # Multi edit buffer — Part 1; Osc Volume "<0>"
F0 00 20 33 01 00 70 01 24 40 F7 # Multi edit buffer — Part 2; Osc Volume "<0>"
F0 00 20 33 01 00 70 0F 24 40 F7 # Multi edit buffer — Part 16; Osc Volume "<0>"
F0 00 20 33 01 00 70 40 24 40 F7 # Single edit buffer; Osc Volume "<0>"
```

If a command “does nothing”, check that **`<part>`** matches the buffer you are
editing: **`0x40`** for Single mode / Single edit buffer, **`0x00`–`0x0F`** for
the matching Multi part.

## Guides

| Doc                                         | Panel scope                                      |
| ------------------------------------------- | ------------------------------------------------ |
| [single.md](single.md)                      | Common, Envelope 3/4, Velocity Map, Soft Knobs   |
| [oscillators.md](oscillators.md)            | Osc 1–3, Noise, Ring Mod, Sub Osc, Unison, Punch |
| [filters.md](filters.md)                    | Filters, Filter/Amp envelopes, Saturation        |
| [modulators.md](modulators.md)              | LFO 1–3                                          |
| [mod-matrix.md](mod-matrix.md)              | Modulation Matrix slots 1–6                      |
| [arpeggiator.md](arpeggiator.md)            | EDIT ARP                                         |
| [effects.md](effects.md)                    | EDIT FX                                          |
