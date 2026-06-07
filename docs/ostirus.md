# OsTIrus (software Virus TI / TI2)

[OsTIrus](https://theusualsuspects.io/downloads/ostirus) (The Usual Suspects /
[gearmulator](https://github.com/dsp56300/gearmulator)) is a **multi-platform
audio plugin** (VST3, AU, CLAP, LV2; also an FX variant) that **low-level
emulates the Freescale DSP56300** processors used in the Access Virus TI family.
It runs the **original Virus TI firmware ROM** and presents the **TI UI** —
so behavior is meant to track **hardware TI / TI2 / Snow**, not a reimplemented
synth.

You supply a **licensed firmware image** (the project cannot distribute ROMs).
Preset sizes for TI singles are **512 bytes** in the emulator docs; this
repository’s TI mk2 hardware work uses **`DUMP_SINGLE` 524-byte** SysEx
(includes header/checksum — see [single-dump.md](dumps/single.md)).

## Who this documentation is for

| User                                                   | MIDI path                                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Virus TI mk2 desktop** (primary capture source here) | `Virus TI USB Plugin I/O` or hardware USB — [testing.md](testing.md)                             |
| **Access Virus TI plugin** (legacy TI integration)     | `Virus TI USB Plugin I/O`                                                                        |
| **OsTIrus in a DAW** (no hardware required)            | Host MIDI → plugin instance on a **MIDI channel**; optional virtual port for `sendmidi` / agents |

If you only run OsTIrus, you can still use the same **Access SysEx** vocabulary
documented in this repo (`00 20 33 01 00` …): **live edit** (`70`, `71`, `6E`,
`72`, `73`), **requests** (`30`, `31`, `34`), **dumps** (`10`, `11`), plus
**notes and CC** on the part channel for performance.

Expected outcome: changing a parameter via SysEx in the DAW (or via
`sendmidi` into the port the host routes to OsTIrus) updates the emulated patch
and **audio output**, the same conceptual model as hardware live edit.

## Routing MIDI to OsTIrus

Typical DAW setup:

1. Insert **OsTIrus** on a track.
2. Set the track **MIDI input** to a keyboard bus or to a **virtual MIDI port**.
3. Send **note/CC** traffic on that channel for music; send **SysEx** on the
 same path (many hosts put SysEx on the same MIDI port as notes).

For agent / script testing (as with hardware):

```bash
sendmidi list # find the port your host exposes (name varies)
sendmidi dev "<your-port>" hex syx 00 20 33 01 00 70 00 28 40
```

Use **`hex syx`** and omit `F0`/`F7` — see [Setup](setup.md)
and [testing.md](testing.md).

**Port names are host-specific** (not `Virus TI USB Plugin I/O` unless you use
the legacy Access TI plugin). IAC Bus (macOS), loopMIDI (Windows), or the
DAW’s own virtual port are common.

## Relationship to this repository

| Topic                | Notes                                                                                                                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Protocol**         | Captures on **Virus TI mk2** target TI2-family SysEx; OsTIrus is intended to run **TI/TI2/Snow ROM** — treat mappings here as the working hypothesis until confirmed on your ROM + host.                 |
| **Verification**     | Prefer a MIDI monitor on the OsTIrus track while stepping one control; compare to [single-live-edit.md](docs/live-edit/edit-single.md) / [edit-multi.md](live-edit/edit-multi.md).                       |
| **Dumps & analysis** | Request/export singles and multis from OsTIrus (when the UI/ROM supports it), parse with the same dump docs — useful for **preset-pack analysis** and constrained randomization without owning hardware. |
| **Composition**      | Combine **MIDI sequences** (channel 1–16 per part) with **SysEx live edits** between notes — same pattern as hardware demos; only the port and host differ.                                              |

**OsTIrus-specific** dump/export differences are not fully inventoried here
yet; file an issue or capture if bytes diverge from
[arrangements.md](dumps/arrangements.md) / [single.md](dumps/single.md).

## Further reading

- [OsTIrus downloads](https://theusualsuspects.io/downloads/ostirus)
- [Gearmulator / DSP56300 emulation](https://github.com/dsp56300/gearmulator)
- [Virus architecture & banks](virus.md)
