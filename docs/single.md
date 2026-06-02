# Single Presets

Single-related SysEx notes for Virus TI mk2.

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
| ----: | ---- | -------------- |
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
[multis.md](multis.md#aura-behavior-part-enable-sends-dump_single).

## Single Dump

- **Transport**: One MIDI SysEx message per Single.
- **Total length**: 524 bytes including `F0` and `F7`.
- **Manufacturer / model header**:
  - Byte 0: `F0` – SysEx start
  - Bytes 1–3: `00 20 33` – Access manufacturer + product family
  - Bytes 4–7: `01 00 10 00` – Message group and command bytes for a Single dump

The remaining 516 bytes (offsets 0x04–0x20F) form the Single payload plus
trailing metadata and a checksum byte immediately before `F7`.

## High‑level regions (from `-INIT-` baseline)

Using offsets in hexadecimal (0x00 is the `F0` byte):

- **0x00–0x0B – Fixed header**
  - `f0 00 20 33 01 00 10 00 7f 0c 00 00`
  - Interpreted as: SysEx start, manufacturer/product, message group, command,
    and a small set of header fields (device / bank / slot not yet mapped).
- **0x0C–~0xEF – Parameter payload**
  - Dense, non‑ASCII data, assumed to contain:
    - Oscillator, mixer, filter, envelope, LFO and matrix parameters
    - FX / EQ / reverb / chorus / global edit‑menu parameters
  - Exact field boundaries within this block are not yet mapped, but this block
    is where most sound‑shaping values live.
- **~0xF8–0x103 – Patch name and nearby globals**
  - Contains the ASCII patch name `-INIT-` padded with spaces:
    - The ASCII sequence `2d 49 4e 49 54 2d 20 20 20`
      (`-INIT-` padded with spaces)
      appears near offset 0xFA.
  - Surrounding bytes likely hold category and other global Single attributes.
- **0x204–0x20D – Trailer metadata + checksum**
  - The last 8 bytes of the baseline dump are:
    - `7f 40 00 01 00 00 44 f7`
  - `F7` is the SysEx terminator; the preceding byte `0x44` appears to be a
    checksum or validation byte; algorithm not yet known (simple 7‑bit sum of
    the body does **not** match `0x44` on the `-INIT-` baseline).

## Known / unknowns at this stage

- **Known**
  - Single dumps are **fixed‑size 524‑byte** SysEx messages.
  - All Singles share a common header `f0 00 20 33 01 00 10 00` indicating
    Access Virus Single‑dump messages.
  - The **patch name** appears as an ASCII sequence near offset 0xFA, padded to
    a fixed length with spaces.
  - The final byte before `F7` behaves like a **checksum byte**.
- **Unknown (to be refined with more examples)**
  - Exact mapping from offsets to GUI parameters (oscillators, filters,
    matrix, FX, etc.).
  - The precise meaning of the header bytes at offsets 0x08–0x0B (device ID,
    bank, slot, flags, or OS version).
  - The checksum algorithm used to produce the `0x44` value on the baseline.

Future work: compare additional Single dumps (small, targeted parameter
changes) and record byte deltas here.
