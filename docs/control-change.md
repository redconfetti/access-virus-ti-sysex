# MIDI Control Change

MIDI **CC** parameters observed in the **AURA** plugin (**26.05.17**). These
are **not** Access SysEx — standard control-change messages on the **part MIDI
channel** (Multi mode).

Whether a CC is stored in **`DUMP_MULTI`** / **`DUMP_SINGLE`** is noted per
parameter. SysEx equivalents (if any) are documented in
[multis-live-edit.md](multis-live-edit.md) and
[multis-dump.md](multis-dump.md).

## Summary

| CC  | Scope         | Parameter     | Transport   | `DUMP_MULTI` | Menu (AURA)        |
| --- | ------------- | ------------- | ----------- | ------------ | ------------------ |
| 91  | Part-specific | Patch Volume  | **CC only** | **No**       | Edit Single → Common |
| 94  | Part-specific | Key Mode      | **CC only** | Unverified   | Edit Single → Common |

## Parameters

### Patch Volume (CC 91)

**Edit Single → Common → Patch Volume** (AURA **26.05.17**). Moving the
control sends **MIDI CC 91 only** — no Access SysEx observed on the wire.

Distinct from Edit Multi **Volume** / **Part Level** (`0x99 + part` in
`DUMP_MULTI`, live `0x72` / `0x27`; AURA label “Part Level” on the Multi
page).

| Field         | Status                          |
| ------------- | ------------------------------- |
| Scope         | Part-specific                   |
| Channel       | Part MIDI channel               |
| SysEx         | **None observed** (CC 91 only)  |
| `DUMP_MULTI`  | **No**                          |
| Value range   | Not yet captured                |

### Key Mode (CC 94)

**Edit Single → Common** (AURA). Observed as **MIDI CC 94** — no SysEx
capture yet.

| Field    | Status        |
| -------- | ------------- |
| Scope    | Part-specific |
| Channel  | Part MIDI channel |
| Value range | Not yet captured |
