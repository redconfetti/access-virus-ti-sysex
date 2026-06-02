# Single Live Edit

Single-related SysEx notes for Virus TI mk2.

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7   # multi / common (some params)
F0 00 20 33 01 00 71 <part> <param> <value> F7   # common (some params)
F0 00 20 33 01 00 6E <part> <param> <value> F7   # part single edit buffer
```

Param IDs are **not global** — the same hex ID can mean different settings
under different `cmd` bytes (e.g. **`0x73` / `0x19`** = All EQs global,
**`0x71` / `0x19`** = Smooth Mode).

## Common (Edit Single)

Per-part **Common** page settings (AURA). Not stored in **`DUMP_MULTI`**
(hardware-tested for Bend Up/Down — see [multis-live-edit.md](multis-live-edit.md)).

### Smooth Mode (`0x19`, `cmd=0x71`)

Arpeggiator / note **Smooth Mode** (Edit Single → Common).

| Value | Mode              | Confirmed |
| ----- | ----------------- | --------- |
| `00`  | Off               | ✓ (AURA 26.05.17 cannot set Off — [aura-notes.md](aura-notes.md)) |
| `01`  | On                | ✓         |
| `02`  | Auto              | ✓         |
| `03`  | Note              | ✓         |
| `04`  | Quantise 1/64     | ✓         |
| `05`  | Quantise 1/32     | ✓         |
| `06`  | Quantise 1/16     | inferred  |
| `07`  | Quantise 1/8      | inferred  |
| `08`  | Quantise 1/4      | inferred  |
| `09`  | Quantise 1/2      | ✓         |
| `0A`  | Quantise 3/64     | ✓         |
| `0B`  | Quantise 3/32     | inferred  |
| `0C`  | Quantise 3/16     | inferred  |
| `0D`  | Quantise 3/8      | inferred  |
| `0E`  | Quantise 1/24     | inferred  |
| `0F`  | Quantise 1/12     | inferred  |
| `10`  | Quantise 1/6      | inferred  |
| `11`  | Quantise 1/3      | inferred  |
| `12`  | Quantise 2/3      | inferred  |
| `13`  | Quantise 3/4      | inferred  |
| `14`  | Quantise 1/1      | inferred  |

```text
F0 00 20 33 01 00 71 00 19 00 F7   # Off
F0 00 20 33 01 00 71 00 19 01 F7   # On
F0 00 20 33 01 00 71 00 19 02 F7   # Auto
F0 00 20 33 01 00 71 00 19 03 F7   # Note
F0 00 20 33 01 00 71 00 19 04 F7   # Quantise 1/64
F0 00 20 33 01 00 71 00 19 05 F7   # Quantise 1/32
F0 00 20 33 01 00 71 00 19 09 F7   # Quantise 1/2
F0 00 20 33 01 00 71 00 19 0A F7   # Quantise 3/64
```

### Bender Scale (`0x1C` / `0x1D`)

**Pitch bender curve** (Edit Single → Common → Bender Scale).

| Mode         | Message | Confirmed |
| ------------ | ------- | --------- |
| Linear       | `F0 … 72 00 1D 00 F7` | ✓ |
| Exponential  | `F0 … 71 00 1C 01 F7` | ✓ |

Uses **mixed commands** (`0x72` for Linear / param **`0x1D`**, `0x71` for
Exponential / param **`0x1C`**). Re-verify Exponential on hardware if a
single param ID is expected.

### Bend Up / Bend Down (`0x1A` / `0x1B`, `cmd=0x71`)

Pitch bend **range** limits — documented in
[multis-live-edit.md — Bend Up / Bend Down](multis-live-edit.md#bend-up-0x1a-cmd0x71).
Same Edit Single **Common** context; not in **`DUMP_MULTI`**.

### Patch Volume (CC 91)

**Edit Single → Common → Patch Volume** — **MIDI CC 91 only** (no SysEx).
See [control-change.md — Patch Volume](control-change.md#patch-volume-cc-91).
Distinct from Multi **Part Level** (`0x99 + part` / live `0x27`).

## Live Edit

### Reverb Send (`cmd=0x6E`)

`cmd=0x6E` is used while editing a **part’s sound** (part/single edit
buffer), not while storing a full Multi program.
Reverb Send is **not** in the 267-byte `DUMP_MULTI`.

| Param ID | Field       | Notes                 |
| -------- | ----------- | --------------------- |
| `0x02`   | Reverb Send | See value table below |

| Item           | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6E <part> 02 <value> F7`                  |
| Scope          | Part edit / single edit buffer (not stored in `DUMP_MULTI`)  |
| Value range    | Direct byte `0..127`                                         |
| Key points     | `0` = Off, `96` (`0x60`) = unity, `127` (`0x7F`) = max send  |
| Status         | Mapping confirmed for Reverb Send on TI mk2                  |

| Value | Hex  | Display        |
| ----- | ---- | -------------- |
| 0     | `00` | Off            |
| 1     | `01` | −46.2 dB       |
| 2     | `02` | −40.2 dB       |
| 10    | `0A` | −26.2 dB       |
| 20    | `14` | −20.6 dB       |
| 30    | `1E` | −16.6 dB       |
| 40    | `28` | −14.0 dB       |
| 41    | `29` | −13.75 dB      |
| 45    | `2D` | −12.75 dB      |
| 54    | `36` | −10.5 dB       |
| 57    | `39` | −9.75 dB       |
| 90    | `5A` | −1.5 dB        |
| 91    | `5B` | −1.25 dB       |
| 92    | `5C` | −1.0 dB        |
| 93    | `5D` | −0.75 dB       |
| 94    | `5E` | −0.5 dB        |
| 95    | `5F` | −0.25 dB       |
| 96    | `60` | 0/0 dB (unity) |
| 97    | `61` | 0/−0.3 dB      |
| 98    | `62` | 0/−0.6 dB      |
| 99    | `63` | 0/−0.9 dB      |
| 100   | `64` | 0/−1.2 dB      |
| 108   | `6C` | 0/−4.1 dB      |
| 109   | `6D` | 0/−4.5 dB      |
| 110   | `6E` | 0/−5.0 dB      |
| 111   | `6F` | 0/−5.5 dB      |
| 112   | `70` | 0/−6.0 dB      |
| 114   | `72` | 0/−7.2 dB      |
| 115   | `73` | 0/−7.8 dB      |
| 116   | `74` | 0/−8.5 dB      |
| 117   | `75` | 0/−9.3 dB      |
| 118   | `76` | 0/−10.1 dB     |
| 119   | `77` | 0/−11.0 dB     |
| 120   | `78` | 0/−12.0 dB     |
| 121   | `79` | 0/−13.2 dB     |
| 122   | `7A` | 0/−14.5 dB     |
| 123   | `7B` | 0/−16.1 dB     |
| 124   | `7C` | 0/−18.1 dB     |
| 125   | `7D` | 0/−20.6 dB     |
| 126   | `7E` | 0/−24.0 dB     |
| 127   | `7F` | effect (max)   |

Unlisted values are piecewise / non-linear. Approximations:
**`41`–`95`** ≈ **`−0.25 × (96 − value)`** dB; **`1`–`40`** steeper;
**`97`–`126`** larger steps toward max.

### Related: AURA `DUMP_SINGLE` on part enable

When a part is disabled then re-enabled in AURA, a **524-byte**
`cmd=0x10` (`DUMP_SINGLE`) loads that part’s single into the edit
buffer. Multi context details are documented in
[multis-dump.md](multis-dump.md#aura-behavior-part-enable-sends-dump_single).
