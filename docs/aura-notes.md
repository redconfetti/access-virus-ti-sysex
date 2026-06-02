# AURA Plugin Notes

**Version used for captures in this repo:** **26.05.17** (Virus TI mk2 desktop).

## Discovered Bugs

Issues observed when using the AURA Plugin (**26.05.17**) with a Virus TI mk2.
Live SysEx (`cmd=0x72` / `0x6E`) often works even when the
**267-byte `DUMP_MULTI`** does not reflect the change.

### Parameters not persisted in multi dump

| Parameter          | Live SysEx                      | Multi dump (`DUMP_MULTI`)          | Notes                                                                           |
| ------------------ | ------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------- |
| Part Transpose     | Works (`0x72` / `0x25`)         | Not saved from **AURA export**     | Virus hardware dump: `0x79 + part`, `stored = ui + 64` — map via Virus panel    |
| Part Output        | Works (`0x72` / `0x29`)         | Not saved from AURA                | Change on Virus front panel, then dump                                          |
| Low Key / High Key | Works (`0x72` / `0x23`, `0x24`) | Not saved from AURA                | Use Virus + dump to map (`0x59`, `0x69`)                                        |
| Volume RX          | Works (`0x72` / `0x49`)         | Only via `0xF9` `+2` if RX left on | AURA turns RX off when Init Vol → `0`; use Virus to capture RX without Init Vol |

## UI naming (AURA)

| AURA label     | Edit Multi / synth parameter                                                            |
| -------------- | --------------------------------------------------------------------------------------- |
| **Part Level** | Multi **Volume** (`0x99 + part`, live `0x27`) on Edit Multi page |
| **Patch Volume** | Edit Single → Common; **CC 91 only** — see [control-change.md](control-change.md) |

AURA may display the **stored** byte value (e.g. `100` = `0x64`)
while the Virus panel shows **bipolar** UI (e.g. `+36` where `0x64`
= `36 + 64`).

## UI coupling (AURA)

| Behavior                    | Notes                                                      |
| --------------------------- | ---------------------------------------------------------- |
| Init Volume → **Off** (`0`) | AURA also sets **Volume RX** to **Disabled** automatically |
| Smooth Mode → **Off**       | AURA **26.05.17** cannot send Off; hardware accepts `71 00 19 00` |

When capturing Init Volume, note **Volume RX** on the panel after
setting Init Volume — do not assume RX stayed enabled.

## Workaround for dump mapping

When AURA does not persist a field into the 267-byte export:

1. Load multi in AURA as usual.
2. Change the parameter on the **Virus hardware** (or confirm via
   live SysEx that the synth received the edit).
3. Request / capture **`DUMP_MULTI`** (`cmd=0x11`, 267 bytes) from the Virus.

Note: dumps taken from the Virus panel may differ in header/slot
bytes (e.g. `0x08` slot) from AURA reference exports — diff against
a baseline captured the same way when possible.
