# Single Dump

Single-related SysEx dump notes for Virus TI mk2.

Live-edit notes (`cmd=0x6E`, `cmd=0x10`) are in
[single-live-edit.md](single-live-edit.md).

## Dump Format

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
