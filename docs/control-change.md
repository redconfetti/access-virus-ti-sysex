# MIDI Control Change

MIDI **CC** parameters on the **part MIDI channel** (Multi / Edit Single).
Observed from **AURA** (**26.05.17**) and **Virus hardware panel** (Easy page).
These are **not** Access SysEx.

Whether a CC is stored in **`DUMP_MULTI`** / **`DUMP_SINGLE`** is noted per
parameter. Panel live edit uses **MIDI CC** when globals **MIDI Controller
Page A / B** are set to **Controller Data**; set both to **SysEx** for Access
SysEx on wire during mapping sessions — see
[global-live-edit.md](global-live-edit.md#midi-controller-page-a-0x5e).

## Summary

| CC  | Scope         | Parameter             | Transport   | `DUMP_MULTI` | Menu (AURA / VC)     |
| --- | ------------- | --------------------- | ----------- | ------------ | -------------------- |
| 34  | Part-specific | Sub Oscillator Volume | **CC only** | Unverified   | Easy / Quick Edit    |
| 91  | Part-specific | Patch Volume          | **CC only** | **No**       | Edit Single → Common |
| 93  | Part-specific | Patch Transpose       | **CC only** | Unverified   | Edit Single → Common |
| 94  | Part-specific | Key Mode              | **CC only** | Unverified   | Edit Single → Common |

## Parameters

### Sub Oscillator Volume (CC 34)

**Easy / Quick Edit → Sub Oscillator Volume**. Live edit from the Virus
panel uses **MIDI CC 34 only** — no Access SysEx on
**`Virus TI USB Plugin I/O`** (hardware-tested). Value may still be stored
in **`DUMP_SINGLE`** (byte offset not yet mapped). Page **A** param **34**
in [waf80.md](waf80.md).

| Field         | Status                                     |
| ------------- | ------------------------------------------ |
| Scope         | Part-specific                              |
| Channel       | Part MIDI channel                          |
| SysEx         | **None on live edit**                      |
| `DUMP_SINGLE` | **Likely yes** (offset TBD; no live SysEx) |
| Value range   | `0`–`127` (UI **0** → CC **0**)            |

### Patch Transpose (CC 93)

**Edit Single → Common → Patch Transpose** (AURA / VC). Live edit is
**MIDI CC 93** only — no Access SysEx (hardware-tested). Distinct from
Edit Multi **Transpose** (SysEx `0x72` / `0x25`, dump `0x79 + part`).
Page **A** param **93** in [waf80.md](waf80.md).

| Field          | Status                         |
| -------------- | ------------------------------ |
| Scope          | Part-specific (single patch)   |
| Channel        | Part MIDI channel              |
| SysEx          | **None on live edit**          |
| `DUMP_SINGLE`  | Unverified                     |
| Value encoding | Bipolar **`stored = ui + 64`** |
| Confirmed      | UI **+1** → CC **65** (`0x41`) |

### Patch Volume (CC 91)

**Edit Single → Common → Patch Volume** (AURA **26.05.17**). Moving the
control sends **MIDI CC 91 only** — no Access SysEx observed on the wire.

Distinct from Edit Multi **Volume** / **Part Level** (`0x99 + part` in
`DUMP_MULTI`, live `0x72` / `0x27`; AURA label “Part Level” on the Multi
page).

| Field        | Status                         |
| ------------ | ------------------------------ |
| Scope        | Part-specific                  |
| Channel      | Part MIDI channel              |
| SysEx        | **None observed** (CC 91 only) |
| `DUMP_MULTI` | **No**                         |
| Value range  | Not yet captured               |

### Key Mode (CC 94)

**Key Mode** — Page **A** param **94** (`0x5E`). Full enum confirmed via
AURA (CC) and Virus panel (SysEx with Page A = SysEx).

| CC / value | Mode   |
| ---------- | ------ |
| `0`        | Poly   |
| `1`        | Mono 1 |
| `2`        | Mono 2 |
| `3`        | Mono 3 |
| `4`        | Mono 4 |
| `5`        | Hold   |

| Transport | When                         | Message                                                                                              |
| --------- | ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| **CC 94** | Page A = **Controller Data** | On part MIDI channel                                                                                 |
| **SysEx** | Page A = **SysEx**           | `F0 … 70 40 5E <value> F7` — [single-live-edit.md](single-live-edit.md#key-mode-0x5e-cmd0x70--cc-94) |

Virus **MONO** button: **on** → SysEx value **`2`** (Mono 2); **off** → Poly
(`0`) plus an extra `6E` / `0x7A` message (see single-live-edit doc).
