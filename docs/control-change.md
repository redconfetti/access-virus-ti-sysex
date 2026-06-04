# MIDI Control Change

MIDI **CC** parameters on the **part MIDI channel** (Multi / Edit Single).
Observed from the **Virus hardware panel** (and MIDI CC when Page A =
**Controller Data**).
These are **not** Access SysEx.

Whether a CC is stored in **`DUMP_MULTI`** / **`DUMP_SINGLE`** is noted per
parameter. Panel live edit uses **MIDI CC** when globals **MIDI Controller
Page A / B** are set to **Controller Data**; set both to **SysEx** for Access
SysEx on wire during mapping sessions — see
[global-live-edit.md](global-live-edit.md#midi-controller-page-a-0x5e).

## Summary

| CC  | Scope         | Parameter             | Transport   | `DUMP_MULTI` | Menu path            |
| --- | ------------- | --------------------- | ----------- | ------------ | -------------------- |
| 10  | Part-specific | Panorama              | CC or SysEx | Unverified   | Edit Single → Common |
| 34  | Part-specific | Sub Oscillator Volume | CC or SysEx | Unverified   | Sub Oscillator menu  |
| 91  | Part-specific | Patch Volume          | CC or SysEx | **No**       | Edit Single → Common |
| 93  | Part-specific | Patch Transpose       | **CC only** | Unverified   | Edit Single → Common |
| 94  | Part-specific | Key Mode              | **CC only** | Unverified   | Edit Single → Common |

## Parameters

### Sub Oscillator Volume (CC 34)

**Oscillators → Sub Oscillator → Volume**. When global **MIDI Controller Page
A** = **Controller Data**, live edit uses **MIDI CC 34** on the part channel.
When Page A = **SysEx**, the same parameter is **`70` / `0x22`** — see
[Sub Oscillator Volume](single-live-edit.md#sub-oscillator-volume-0x22-cmd0x70--cc-34).

| Field         | Status                          |
| ------------- | ------------------------------- |
| Scope         | Part-specific                   |
| Channel       | Part MIDI channel (CC path)     |
| SysEx         | **`F0 … 70 <part> 22 <val> F7`** (Page A = SysEx) |
| `DUMP_SINGLE` | **Likely yes** (offset TBD)     |
| Value range   | **0**–**127** (`stored = lcd`)  |

**Sub Oscillator Shape** (CC **35** / SysEx **`70` / `0x23`**): Square **`00`**,
Triangle **`01`** only — [Sub Oscillator Shape](single-live-edit.md#sub-oscillator-shape-0x23-cmd0x70--cc-35).

### Patch Transpose (CC 93)

**Edit Single → Common → Transpose** (Patch Transpose). With **Page A = SysEx**,
**`cmd=0x70` `param=0x5D`** (**−64..+63** → `ui+64`) — see
[Transpose](single-live-edit.md#transpose--patch-transpose-0x5d-cmd0x70--cc-93).
With **Controller Data**, **CC 93** only. Distinct from Edit Multi **Transpose**
(SysEx `0x72` / `0x25`, dump `0x79 + part`).
Page **A** param **93** in [waf80.md](waf80.md).

| Field          | Status                         |
| -------------- | ------------------------------ |
| Scope          | Part-specific (single patch)   |
| Channel        | Part MIDI channel              |
| SysEx          | **None on live edit**          |
| `DUMP_SINGLE`  | Unverified                     |
| Value encoding | Bipolar **`stored = ui + 64`** |
| Confirmed      | UI **+1** → CC **65** (`0x41`) |

### Panorama (CC 10)

**Edit Single → Common → Panorama**. With **Page A = Controller Data**, the
panel sends **CC 10**. With **Page A = SysEx**, live edit is **`cmd=0x70`**
**`param=0x0A`** — see
[Panorama](single-live-edit.md#panorama-0x0a-cmd0x70--cc-10).

### Patch Volume (CC 91)

**Edit Single → Common → Patch Volume**. With **Page A = Controller Data**,
the panel sends **CC 91**. With **Page A = SysEx**, live edit is
**`cmd=0x70` `param=0x5B`** (**0..127** direct) — see
[Patch Volume](single-live-edit.md#patch-volume-0x5b-cmd0x70--cc-91).

Distinct from Edit Multi **Volume** (`0x99 + part` in `DUMP_MULTI`, live
`0x72` / `0x27`). Host UI label “Part Level”: [aura-notes.md](aura-notes.md).

| Field        | Status                         |
| ------------ | ------------------------------ |
| Scope        | Part-specific                  |
| Channel      | Part MIDI channel              |
| SysEx        | **`70`/`5B`** when Page A SysEx |
| `DUMP_MULTI` | **No**                         |
| Value range  | **0..127** (`stored = lcd`)    |

### Key Mode (CC 94)

**Key Mode** — Page **A** param **94** (`0x5E`). Full enum confirmed via
**CC 94** and **`cmd=0x70`** / `0x5E` on the Virus panel (Page A = SysEx).

| CC / value | Mode   |
| ---------- | ------ |
| `0`        | Poly   |
| `1`        | Mono 1 |
| `2`        | Mono 2 |
| `3`        | Mono 3 |
| `4`        | Mono 4 |
| `5`        | Hold   |

| Transport | When                         | Message                                                                                                  |
| --------- | ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| **CC 94** | Page A = **Controller Data** | On part MIDI channel                                                                                     |
| **SysEx** | Page A = **SysEx**           | `F0 … 70 <part> 5E <value> F7` — [single-live-edit.md](single-live-edit.md#key-mode-0x5e-cmd0x70--cc-94) |

Virus **MONO** button: **on** restores the last selected **Mono 1..4** value;
**off** switches to **Poly** (`0`) and may send companion `6E` / `0x7A`
state first (see single-live-edit doc).
