# Parameter options

Full Virus TI parameter value tables, providing complete wire maps and panel
option lists, used as reference for documented SysEx parameters.

Contents: **shared wire encodings** (reused formulas and full value tables) and
**panel option enums** (named menu choices). For panel enums, **Index** is the
zero-based list position; for most **`stored = index`** (exceptions:
[Soft Knob Destinations](#soft-knob-destinations), [Soft Knob Names](#soft-knob-names)
use per-row **`<value>`**).

From a live-edit parameter section, link **below** the range summary and SysEx
examples:

```markdown
Full wire map: [Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40)
Panel enum: [Arpeggiator Mode](#arpeggiator-mode)
```

## Value encodings

Shared wire formats reused across many parameters. **Live-edit docs** describe
range and exceptions, show min/center/max SysEx examples, then link here for the
**full** value table.

### Bipolar centered (±64 @ 0x40)

Signed UI **−64..+63** with **+0** at wire **`0x40`**. The most common bipolar
encoding on the Virus TI.

```text
stored = ui + 64
ui     = stored − 64
```

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| −63 | `01`      |
| −62 | `02`      |
| −61 | `03`      |
| −60 | `04`      |
| −59 | `05`      |
| −58 | `06`      |
| −57 | `07`      |
| −56 | `08`      |
| −55 | `09`      |
| −54 | `0A`      |
| −53 | `0B`      |
| −52 | `0C`      |
| −51 | `0D`      |
| −50 | `0E`      |
| −49 | `0F`      |
| −48 | `10`      |
| −47 | `11`      |
| −46 | `12`      |
| −45 | `13`      |
| −44 | `14`      |
| −43 | `15`      |
| −42 | `16`      |
| −41 | `17`      |
| −40 | `18`      |
| −39 | `19`      |
| −38 | `1A`      |
| −37 | `1B`      |
| −36 | `1C`      |
| −35 | `1D`      |
| −34 | `1E`      |
| −33 | `1F`      |
| −32 | `20`      |
| −31 | `21`      |
| −30 | `22`      |
| −29 | `23`      |
| −28 | `24`      |
| −27 | `25`      |
| −26 | `26`      |
| −25 | `27`      |
| −24 | `28`      |
| −23 | `29`      |
| −22 | `2A`      |
| −21 | `2B`      |
| −20 | `2C`      |
| −19 | `2D`      |
| −18 | `2E`      |
| −17 | `2F`      |
| −16 | `30`      |
| −15 | `31`      |
| −14 | `32`      |
| −13 | `33`      |
| −12 | `34`      |
| −11 | `35`      |
| −10 | `36`      |
| −9  | `37`      |
| −8  | `38`      |
| −7  | `39`      |
| −6  | `3A`      |
| −5  | `3B`      |
| −4  | `3C`      |
| −3  | `3D`      |
| −2  | `3E`      |
| −1  | `3F`      |
| +0  | `40`      |
| +1  | `41`      |
| +2  | `42`      |
| +3  | `43`      |
| +4  | `44`      |
| +5  | `45`      |
| +6  | `46`      |
| +7  | `47`      |
| +8  | `48`      |
| +9  | `49`      |
| +10 | `4A`      |
| +11 | `4B`      |
| +12 | `4C`      |
| +13 | `4D`      |
| +14 | `4E`      |
| +15 | `4F`      |
| +16 | `50`      |
| +17 | `51`      |
| +18 | `52`      |
| +19 | `53`      |
| +20 | `54`      |
| +21 | `55`      |
| +22 | `56`      |
| +23 | `57`      |
| +24 | `58`      |
| +25 | `59`      |
| +26 | `5A`      |
| +27 | `5B`      |
| +28 | `5C`      |
| +29 | `5D`      |
| +30 | `5E`      |
| +31 | `5F`      |
| +32 | `60`      |
| +33 | `61`      |
| +34 | `62`      |
| +35 | `63`      |
| +36 | `64`      |
| +37 | `65`      |
| +38 | `66`      |
| +39 | `67`      |
| +40 | `68`      |
| +41 | `69`      |
| +42 | `6A`      |
| +43 | `6B`      |
| +44 | `6C`      |
| +45 | `6D`      |
| +46 | `6E`      |
| +47 | `6F`      |
| +48 | `70`      |
| +49 | `71`      |
| +50 | `72`      |
| +51 | `73`      |
| +52 | `74`      |
| +53 | `75`      |
| +54 | `76`      |
| +55 | `77`      |
| +56 | `78`      |
| +57 | `79`      |
| +58 | `7A`      |
| +59 | `7B`      |
| +60 | `7C`      |
| +61 | `7D`      |
| +62 | `7E`      |
| +63 | `7F`      |

**Used by** (non-exhaustive): Edit Single **Transpose** (`70`/`5D`), **Detune**
in Multi Dump (`72`/`26`), **Bend Up/Down**, Mod Matrix **Amount**, Filter
**Offset** / **Keyfollow** / **Balance**, LFO **Contour**, Delay/Reverb
**Coloration**, Filter Bank **Frequency** / **Stereo Phase**, and many other
**`stored = ui + 64`** controls. Panel label units vary (semitones, cents, %,
etc.) — the wire map is the same unless a parameter doc notes an exception.

### Edit Multi live balance (−63..+64 @ 0x40)

**Live-edit wire only** for Edit Multi **Transpose** (`72`/`25`) and **Volume**
(`72`/`27`). UI **−63..+64** with **+1** at wire **`0x40`** (not **+0**). Multi
Dump storage for **Transpose** uses [Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40)
with a narrower UI range (−48..+48 semitones) — see
[multi.md](../dumps/multi.md#transpose).

```text
stored = ui + 63
ui     = stored − 63
```

| UI (live) | `<value>` |
| --------- | --------- |
| −63       | `00`      |
| −62       | `01`      |
| −61       | `02`      |
| −60       | `03`      |
| −59       | `04`      |
| −58       | `05`      |
| −57       | `06`      |
| −56       | `07`      |
| −55       | `08`      |
| −54       | `09`      |
| −53       | `0A`      |
| −52       | `0B`      |
| −51       | `0C`      |
| −50       | `0D`      |
| −49       | `0E`      |
| −48       | `0F`      |
| −47       | `10`      |
| −46       | `11`      |
| −45       | `12`      |
| −44       | `13`      |
| −43       | `14`      |
| −42       | `15`      |
| −41       | `16`      |
| −40       | `17`      |
| −39       | `18`      |
| −38       | `19`      |
| −37       | `1A`      |
| −36       | `1B`      |
| −35       | `1C`      |
| −34       | `1D`      |
| −33       | `1E`      |
| −32       | `1F`      |
| −31       | `20`      |
| −30       | `21`      |
| −29       | `22`      |
| −28       | `23`      |
| −27       | `24`      |
| −26       | `25`      |
| −25       | `26`      |
| −24       | `27`      |
| −23       | `28`      |
| −22       | `29`      |
| −21       | `2A`      |
| −20       | `2B`      |
| −19       | `2C`      |
| −18       | `2D`      |
| −17       | `2E`      |
| −16       | `2F`      |
| −15       | `30`      |
| −14       | `31`      |
| −13       | `32`      |
| −12       | `33`      |
| −11       | `34`      |
| −10       | `35`      |
| −9        | `36`      |
| −8        | `37`      |
| −7        | `38`      |
| −6        | `39`      |
| −5        | `3A`      |
| −4        | `3B`      |
| −3        | `3C`      |
| −2        | `3D`      |
| −1        | `3E`      |
| +0        | `3F`      |
| +1        | `40`      |
| +2        | `41`      |
| +3        | `42`      |
| +4        | `43`      |
| +5        | `44`      |
| +6        | `45`      |
| +7        | `46`      |
| +8        | `47`      |
| +9        | `48`      |
| +10       | `49`      |
| +11       | `4A`      |
| +12       | `4B`      |
| +13       | `4C`      |
| +14       | `4D`      |
| +15       | `4E`      |
| +16       | `4F`      |
| +17       | `50`      |
| +18       | `51`      |
| +19       | `52`      |
| +20       | `53`      |
| +21       | `54`      |
| +22       | `55`      |
| +23       | `56`      |
| +24       | `57`      |
| +25       | `58`      |
| +26       | `59`      |
| +27       | `5A`      |
| +28       | `5B`      |
| +29       | `5C`      |
| +30       | `5D`      |
| +31       | `5E`      |
| +32       | `5F`      |
| +33       | `60`      |
| +34       | `61`      |
| +35       | `62`      |
| +36       | `63`      |
| +37       | `64`      |
| +38       | `65`      |
| +39       | `66`      |
| +40       | `67`      |
| +41       | `68`      |
| +42       | `69`      |
| +43       | `6A`      |
| +44       | `6B`      |
| +45       | `6C`      |
| +46       | `6D`      |
| +47       | `6E`      |
| +48       | `6F`      |
| +49       | `70`      |
| +50       | `71`      |
| +51       | `72`      |
| +52       | `73`      |
| +53       | `74`      |
| +54       | `75`      |
| +55       | `76`      |
| +56       | `77`      |
| +57       | `78`      |
| +58       | `79`      |
| +59       | `7A`      |
| +60       | `7B`      |
| +61       | `7C`      |
| +62       | `7D`      |
| +63       | `7E`      |
| +64       | `7F`      |

### Bipolar centered narrow (−48..+48 @ 0x40)

Subset of [Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40): UI
**−48..+48** with **+0** at wire **`0x40`**. Valid wire bytes **`0x10`..`0x70`**
only — values outside that range use the same formula but are not reachable on
the panel for controls with this range (oscillator **Semitone**, Multi Dump
**Transpose**, etc.).

```text
stored = ui + 64
ui     = stored − 64
```

| UI  | `<value>` |
| --- | --------- |
| −48 | `10`      |
| −47 | `11`      |
| −46 | `12`      |
| −45 | `13`      |
| −44 | `14`      |
| −43 | `15`      |
| −42 | `16`      |
| −41 | `17`      |
| −40 | `18`      |
| −39 | `19`      |
| −38 | `1A`      |
| −37 | `1B`      |
| −36 | `1C`      |
| −35 | `1D`      |
| −34 | `1E`      |
| −33 | `1F`      |
| −32 | `20`      |
| −31 | `21`      |
| −30 | `22`      |
| −29 | `23`      |
| −28 | `24`      |
| −27 | `25`      |
| −26 | `26`      |
| −25 | `27`      |
| −24 | `28`      |
| −23 | `29`      |
| −22 | `2A`      |
| −21 | `2B`      |
| −20 | `2C`      |
| −19 | `2D`      |
| −18 | `2E`      |
| −17 | `2F`      |
| −16 | `30`      |
| −15 | `31`      |
| −14 | `32`      |
| −13 | `33`      |
| −12 | `34`      |
| −11 | `35`      |
| −10 | `36`      |
| −9  | `37`      |
| −8  | `38`      |
| −7  | `39`      |
| −6  | `3A`      |
| −5  | `3B`      |
| −4  | `3C`      |
| −3  | `3D`      |
| −2  | `3E`      |
| −1  | `3F`      |
| +0  | `40`      |
| +1  | `41`      |
| +2  | `42`      |
| +3  | `43`      |
| +4  | `44`      |
| +5  | `45`      |
| +6  | `46`      |
| +7  | `47`      |
| +8  | `48`      |
| +9  | `49`      |
| +10 | `4A`      |
| +11 | `4B`      |
| +12 | `4C`      |
| +13 | `4D`      |
| +14 | `4E`      |
| +15 | `4F`      |
| +16 | `50`      |
| +17 | `51`      |
| +18 | `52`      |
| +19 | `53`      |
| +20 | `54`      |
| +21 | `55`      |
| +22 | `56`      |
| +23 | `57`      |
| +24 | `58`      |
| +25 | `59`      |
| +26 | `5A`      |
| +27 | `5B`      |
| +28 | `5C`      |
| +29 | `5D`      |
| +30 | `5E`      |
| +31 | `5F`      |
| +32 | `60`      |
| +33 | `61`      |
| +34 | `62`      |
| +35 | `63`      |
| +36 | `64`      |
| +37 | `65`      |
| +38 | `66`      |
| +39 | `67`      |
| +40 | `68`      |
| +41 | `69`      |
| +42 | `6A`      |
| +43 | `6B`      |
| +44 | `6C`      |
| +45 | `6D`      |
| +46 | `6E`      |
| +47 | `6F`      |
| +48 | `70`      |

### Key Follow with Norm label

Same wire map as [Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40)
(**`stored = ui + 64`**). The panel names UI **+32** as **Norm** (wire **`0x60`**)
— a fixed scale tick, not the mathematical center (**+0** @ **`0x40`**).

| UI   | Panel label | `<value>` |
| ---- | ----------- | --------- |
| −64  | −64         | `00`      |
| +0   | 0           | `40`      |
| +32  | **Norm**    | `60`      |
| +63  | +63         | `7F`      |

Full wire map: [Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40).

### Note index (C1..G9)

Direct chromatic note index for Edit Multi **Low Key** / **High Key** and
similar controls. **`stored = index`** (wire byte **`0x00`..`0x7F`**); **`00`** =
**C1**, **`7F`** = **G9**.

| Note | `<value>` |
| ---- | --------- |
| C1   | `00`      |
| C#1  | `01`      |
| D1   | `02`      |
| D#1  | `03`      |
| E1   | `04`      |
| F1   | `05`      |
| F#1  | `06`      |
| G1   | `07`      |
| G#1  | `08`      |
| A1   | `09`      |
| A#1  | `0A`      |
| B1   | `0B`      |
| C2   | `0C`      |
| C#2  | `0D`      |
| D2   | `0E`      |
| D#2  | `0F`      |
| E2   | `10`      |
| F2   | `11`      |
| F#2  | `12`      |
| G2   | `13`      |
| G#2  | `14`      |
| A2   | `15`      |
| A#2  | `16`      |
| B2   | `17`      |
| C3   | `18`      |
| C#3  | `19`      |
| D3   | `1A`      |
| D#3  | `1B`      |
| E3   | `1C`      |
| F3   | `1D`      |
| F#3  | `1E`      |
| G3   | `1F`      |
| G#3  | `20`      |
| A3   | `21`      |
| A#3  | `22`      |
| B3   | `23`      |
| C4   | `24`      |
| C#4  | `25`      |
| D4   | `26`      |
| D#4  | `27`      |
| E4   | `28`      |
| F4   | `29`      |
| F#4  | `2A`      |
| G4   | `2B`      |
| G#4  | `2C`      |
| A4   | `2D`      |
| A#4  | `2E`      |
| B4   | `2F`      |
| C5   | `30`      |
| C#5  | `31`      |
| D5   | `32`      |
| D#5  | `33`      |
| E5   | `34`      |
| F5   | `35`      |
| F#5  | `36`      |
| G5   | `37`      |
| G#5  | `38`      |
| A5   | `39`      |
| A#5  | `3A`      |
| B5   | `3B`      |
| C6   | `3C`      |
| C#6  | `3D`      |
| D6   | `3E`      |
| D#6  | `3F`      |
| E6   | `40`      |
| F6   | `41`      |
| F#6  | `42`      |
| G6   | `43`      |
| G#6  | `44`      |
| A6   | `45`      |
| A#6  | `46`      |
| B6   | `47`      |
| C7   | `48`      |
| C#7  | `49`      |
| D7   | `4A`      |
| D#7  | `4B`      |
| E7   | `4C`      |
| F7   | `4D`      |
| F#7  | `4E`      |
| G7   | `4F`      |
| G#7  | `50`      |
| A7   | `51`      |
| A#7  | `52`      |
| B7   | `53`      |
| C8   | `54`      |
| C#8  | `55`      |
| D8   | `56`      |
| D#8  | `57`      |
| E8   | `58`      |
| F8   | `59`      |
| F#8  | `5A`      |
| G8   | `5B`      |
| G#8  | `5C`      |
| A8   | `5D`      |
| A#8  | `5E`      |
| B8   | `5F`      |
| C9   | `60`      |
| C#9  | `61`      |
| D9   | `62`      |
| D#9  | `63`      |
| E9   | `64`      |
| F9   | `65`      |
| F#9  | `66`      |
| G9   | `67`      |
| G#9  | `68`      |
| A9   | `69`      |
| A#9  | `6A`      |
| B9   | `6B`      |
| C10  | `6C`      |
| C#10 | `6D`      |
| D10  | `6E`      |
| D#10 | `6F`      |
| E10  | `70`      |
| F10  | `71`      |
| F#10 | `72`      |
| G10  | `73`      |
| G#10 | `74`      |
| A10  | `75`      |
| A#10 | `76`      |
| B10  | `77`      |
| C11  | `78`      |
| C#11 | `79`      |
| D11  | `7A`      |
| D#11 | `7B`      |
| E11  | `7C`      |
| F11  | `7D`      |
| F#11 | `7E`      |
| G11  | `7F`      |

### Note index (C-1..G9)

Direct chromatic note index from **C-1** through **G9**. Filter **Key Follow
Base** (`71`/`21`), and other semitone-index controls.

| Note | `<value>` |
| ---- | --------- |
| C-1  | `00`      |
| C#-1 | `01`      |
| D-1  | `02`      |
| D#-1 | `03`      |
| E-1  | `04`      |
| F-1  | `05`      |
| F#-1 | `06`      |
| G-1  | `07`      |
| G#-1 | `08`      |
| A-1  | `09`      |
| A#-1 | `0A`      |
| B-1  | `0B`      |
| C0   | `0C`      |
| C#0  | `0D`      |
| D0   | `0E`      |
| D#0  | `0F`      |
| E0   | `10`      |
| F0   | `11`      |
| F#0  | `12`      |
| G0   | `13`      |
| G#0  | `14`      |
| A0   | `15`      |
| A#0  | `16`      |
| B0   | `17`      |
| C1   | `18`      |
| C#1  | `19`      |
| D1   | `1A`      |
| D#1  | `1B`      |
| E1   | `1C`      |
| F1   | `1D`      |
| F#1  | `1E`      |
| G1   | `1F`      |
| G#1  | `20`      |
| A1   | `21`      |
| A#1  | `22`      |
| B1   | `23`      |
| C2   | `24`      |
| C#2  | `25`      |
| D2   | `26`      |
| D#2  | `27`      |
| E2   | `28`      |
| F2   | `29`      |
| F#2  | `2A`      |
| G2   | `2B`      |
| G#2  | `2C`      |
| A2   | `2D`      |
| A#2  | `2E`      |
| B2   | `2F`      |
| C3   | `30`      |
| C#3  | `31`      |
| D3   | `32`      |
| D#3  | `33`      |
| E3   | `34`      |
| F3   | `35`      |
| F#3  | `36`      |
| G3   | `37`      |
| G#3  | `38`      |
| A3   | `39`      |
| A#3  | `3A`      |
| B3   | `3B`      |
| C4   | `3C`      |
| C#4  | `3D`      |
| D4   | `3E`      |
| D#4  | `3F`      |
| E4   | `40`      |
| F4   | `41`      |
| F#4  | `42`      |
| G4   | `43`      |
| G#4  | `44`      |
| A4   | `45`      |
| A#4  | `46`      |
| B4   | `47`      |
| C5   | `48`      |
| C#5  | `49`      |
| D5   | `4A`      |
| D#5  | `4B`      |
| E5   | `4C`      |
| F5   | `4D`      |
| F#5  | `4E`      |
| G5   | `4F`      |
| G#5  | `50`      |
| A5   | `51`      |
| A#5  | `52`      |
| B5   | `53`      |
| C6   | `54`      |
| C#6  | `55`      |
| D6   | `56`      |
| D#6  | `57`      |
| E6   | `58`      |
| F6   | `59`      |
| F#6  | `5A`      |
| G6   | `5B`      |
| G#6  | `5C`      |
| A6   | `5D`      |
| A#6  | `5E`      |
| B6   | `5F`      |
| C7   | `60`      |
| C#7  | `61`      |
| D7   | `62`      |
| D#7  | `63`      |
| E7   | `64`      |
| F7   | `65`      |
| F#7  | `66`      |
| G7   | `67`      |
| G#7  | `68`      |
| A7   | `69`      |
| A#7  | `6A`      |
| B7   | `6B`      |
| C8   | `6C`      |
| C#8  | `6D`      |
| D8   | `6E`      |
| D#8  | `6F`      |
| E8   | `70`      |
| F8   | `71`      |
| F#8  | `72`      |
| G8   | `73`      |
| G#8  | `74`      |
| A8   | `75`      |
| A#8  | `76`      |
| B8   | `77`      |
| C9   | `78`      |
| C#9  | `79`      |
| D9   | `7A`      |
| D#9  | `7B`      |
| E9   | `7C`      |
| F9   | `7D`      |
| F#9  | `7E`      |
| G9   | `7F`      |

---

## Secondary output routing

**Off** plus **Out 1 L** … **USB 3 R**. **`00`** = Off; otherwise
**primary routing index + 1** (see [Output routing
(primary)](../live-edit/multis.md#output-routing-enum)).

Analog **Out 1**–**Out 3**: **`00`–`09`**; USB outs through **`12`**.

| Index | `<value>` | Option    |
| ----- | --------- | --------- |
| 0     | `00`      | Off       |
| 1     | `01`      | Out 1 L   |
| 2     | `02`      | Out 1 L+R |
| 3     | `03`      | Out 1 R   |
| 4     | `04`      | Out 2 L   |
| 5     | `05`      | Out 2 L+R |
| 6     | `06`      | Out 2 R   |
| 7     | `07`      | Out 3 L   |
| 8     | `08`      | Out 3 L+R |
| 9     | `09`      | Out 3 R   |
| 10    | `0A`      | USB 1 L   |
| 11    | `0B`      | USB 1 L+R |
| 12    | `0C`      | USB 1 R   |
| 13    | `0D`      | USB 2 L   |
| 14    | `0E`      | USB 2 L+R |
| 15    | `0F`      | USB 2 R   |
| 16    | `10`      | USB 3 L   |
| 17    | `11`      | USB 3 L+R |
| 18    | `12`      | USB 3 R   |

---

## Input Mode

3 options (`00`–`02`).

| Index | `<value>` | Option  |
| ----- | --------- | ------- |
| 0     | `00`      | Off     |
| 1     | `01`      | Dynamic |
| 2     | `02`      | Static  |

---

## Input Select

3 options (`00`–`02`). Panel visible when [Input Mode](#input-mode) is
**Dynamic** or **Static**.

| Index | `<value>` | Option |
| ----- | --------- | ------ |
| 0     | `00`      | Left   |
| 1     | `01`      | L + R  |
| 2     | `02`      | Right  |

---

## Atomizer preset

**Inputs → Atomizer** menu index (not loop trigger keys). **Off** / **On** /
panel **2**–**16** → **`02`–`10`**.

| Index | `<value>` | Option |
| ----- | --------- | ------ |
| 0     | `00`      | Off    |
| 1     | `01`      | On     |
| 2     | `02`      | 2      |
| 3     | `03`      | 3      |
| 4     | `04`      | 4      |
| 5     | `05`      | 5      |
| 6     | `06`      | 6      |
| 7     | `07`      | 7      |
| 8     | `08`      | 8      |
| 9     | `09`      | 9      |
| 10    | `0A`      | 10     |
| 11    | `0B`      | 11     |
| 12    | `0C`      | 12     |
| 13    | `0D`      | 13     |
| 14    | `0E`      | 14     |
| 15    | `0F`      | 15     |
| 16    | `10`      | 16     |

---

## Bender Scale

**Edit Single → Common → Bender Scale** (`71` / `0x1C`). **`stored = index`**.

| Index | `<value>` | Option      |
| ----- | --------- | ----------- |
| 0     | `00`      | Linear      |
| 1     | `01`      | Exponential |

---

## Arpeggiator Mode

**EDIT ARP → Mode** (`71` / `0x0F`). **`stored = index`**. lists modes **`00`–`06`**; **Arp>Matrix** at **`07`**.

| Index | `<value>` | Option     |
| ----- | --------- | ---------- |
| 0     | `00`      | Off        |
| 1     | `01`      | Up         |
| 2     | `02`      | Down       |
| 3     | `03`      | Up&Down    |
| 4     | `04`      | As Played  |
| 5     | `05`      | Random     |
| 6     | `06`      | Chord      |
| 7     | `07`      | Arp>Matrix |

---

## Arpeggiator panel visibility

**EDIT ARP**. **Mode** is always on the panel.

### Mode = Off (`00`)

**Mode** only — **Pattern**, **Octaves**, and all other **EDIT ARP** rows are
**hidden**.

### Mode = Down (`02`)

**Mode** and **Hold** only — no **Pattern**, **Octaves**, **Resolution**,
**Note Length**, or **Swing Factor**.

### Full settings — **Up** (`01`), **Up&Down** (`03`), **As Played** (`04`)

**Random** (`05`), **Chord** (`06`)

**Pattern**, **Octaves**, **Resolution**, **Note Length**, **Swing Factor**, and
**Hold** — same wire maps on all five modes (hardware TX confirmed).
User-pattern editor — [Arpeggiator Loop Length](#arpeggiator-loop-length)
(`6E`/`7F`; dump **`0x189`**); per-step data on **`6F`** / dump
**`0x18A`…`0x1E9`** — [Arpeggiator step triplet](#arpeggiator-step-triplet).

### Mode = **Arp>Matrix** (`07`)

**Pattern** and **Resolution** only — no **Octaves**, **Note Length**, **Swing
Factor**, or **Hold** (same wire maps as full settings modes for the two visible
rows).

---

## Arpeggiator Pattern

**EDIT ARP → Pattern** (`71` / `0x02`). **`stored = <value>`** (wire byte).
Hidden when **Mode** = **Off** or **Down**.
Visible on full settings modes and **Arp>Matrix**.

| `<value>` | LCD label |
| --------- | --------- |
| `00`      | User      |
| `01`      | 2         |
| `02`      | 3         |
| …         | …         |
| `3F`      | 64        |

Preset patterns **2**–**64**: **`stored = pattern_number − 1`** (LCD shows the
decimal pattern index). **User** is always **`00`**.

```text
F0 00 20 33 01 00 71 00 02 00 F7 # User
F0 00 20 33 01 00 71 00 02 01 F7 # 2
F0 00 20 33 01 00 71 00 02 3F F7 # 64
```

---

## Arpeggiator Octaves

**EDIT ARP → Octaves**.
**`stored = octaves − 1`** (**`00`–`03`** → LCD **1**–**4**). Full settings
modes only — hidden when **Mode** = **Off**, **Down**, or **Arp>Matrix**.

| Octaves | `<value>` |
| ------- | --------- |
| 1       | `00`      |
| 2       | `01`      |
| 3       | `02`      |
| 4       | `03`      |

```text
F0 00 20 33 01 00 71 00 03 00 F7 # 1 octave
F0 00 20 33 01 00 71 00 03 03 F7 # 4 octaves
```

---

## Arpeggiator Resolution

**EDIT ARP → Resolution**.
**`stored = <value>`** (wire byte). **No Off** row — slowest option is
**1/128** (`01`). Same division **names** as [Delay Clock](#delay-clock) /
[LFO Clock](#lfo-clock) but a **different** wire map
(finer grid through **1/128** / **3/128**; stops at **1/2**, no **2/3** /
**3/4**). Hidden when **Mode** = **Off** or **Down**. Also on **Arp>Matrix**
(with **Pattern** only).

Panel menu order (slow → fast):

| `<value>` | Option |
| --------- | ------ |
| `01`      | 1/128  |
| `02`      | 1/64   |
| `0B`      | 1/48   |
| `07`      | 3/128  |
| `03`      | 1/32   |
| `0C`      | 1/24   |
| `08`      | 3/64   |
| `04`      | 1/16   |
| `0D`      | 1/12   |
| `09`      | 3/32   |
| `05`      | 1/8    |
| `0E`      | 1/6    |
| `0A`      | 3/16   |
| `06`      | 1/4    |
| `0F`      | 1/3    |
| `10`      | 3/8    |
| `11`      | 1/2    |

```text
F0 00 20 33 01 00 71 00 11 01 F7 # 1/128
F0 00 20 33 01 00 71 00 11 11 F7 # 1/2
```

---

## Arpeggiator Note Length (LCD)

**EDIT ARP → Note Length** (`71` / `0x05`). Bipolar **`stored = ui + 64`**
(**`00`–`7F`**). LCD **−100.0..+100.0 %** with **+0.0 %** at **`40`**. Full
settings modes only — hidden when **Mode** = **Off**, **Down**, or **Arp>Matrix**.

| UI       | `<value>` |
| -------- | --------- |
| −100.0 % | `00`      |
| +0.0 %   | `40`      |
| +100.0 % | `7F`      |

```text
F0 00 20 33 01 00 71 00 05 00 F7 # −100.0 %
F0 00 20 33 01 00 71 00 05 40 F7 # +0.0 %
F0 00 20 33 01 00 71 00 05 7F F7 # +100.0 %
```

---

## Arpeggiator Swing Factor (LCD)

**EDIT ARP → Swing Factor** (`71` / `0x06`). **`00`** = **Off**. **`01`–`7F`**
= swing amount. Most detents show **XX.X %** on the LCD (**50.2 %** at **`01`**
through **75.0 %** at **`7F`**). Five wire values instead show **16-note swing
shorthand** (**16B** … **16F**) — not a percentage readout.
Full settings modes only — hidden when **Mode** = **Off**, **Down**, or
**Arp>Matrix**.

Intermediate detents step the wire byte **+1**; LCD **%** is **not** linear in
**`stored`**.

### Percent anchors

| `<value>` | LCD    |
| --------- | ------ |
| `01`      | 50.2 % |
| `41`      | 62.8 % |
| `43`      | 63.2 % |
| `7E`      | 74.8 % |
| `7F`      | 75.0 % |

### 16-note swing shorthand (not **%**)

| `<value>` | LCD |
| --------- | --- |
| `15`      | 16B |
| `29`      | 16C |
| `42`      | 16D |
| `57`      | 16E |
| `6B`      | 16F |

```text
F0 00 20 33 01 00 71 00 06 00 F7 # Off
F0 00 20 33 01 00 71 00 06 01 F7 # 50.2 %
F0 00 20 33 01 00 71 00 06 15 F7 # 16B
F0 00 20 33 01 00 71 00 06 29 F7 # 16C
F0 00 20 33 01 00 71 00 06 42 F7 # 16D
F0 00 20 33 01 00 71 00 06 57 F7 # 16E
F0 00 20 33 01 00 71 00 06 6B F7 # 16F
F0 00 20 33 01 00 71 00 06 7E F7 # 74.8 %
F0 00 20 33 01 00 71 00 06 7F F7 # 75.0 %
```

---

## Arpeggiator Hold

**EDIT ARP → Hold**. **`00`** = **Off**, **`01`** = **On**. Hidden when
**Mode** = **Off** or **Arp>Matrix**. On **Down**, **Hold** is the only setting
besides **Mode**; on full settings modes, **Hold** is the last row of the
settings block.

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | On     |

```text
F0 00 20 33 01 00 71 40 04 00 F7 # Off (Single edit buffer; part 40)
F0 00 20 33 01 00 71 40 04 01 F7 # On
```

---

## Arpeggiator Loop Length

User arpeggiator pattern **loop length** — **1**–**32** steps (max pattern length
). Live edit: **`cmd=0x6E`**, param **`0x7F`** (part buffer — not Page
B **`71`**). **`stored = steps − 1`** (**`00`–`1F`**). **Single Dump**
offset **`0x189`** ( **`-INIT-`** baseline).

| Steps | `<value>` |
| ----- | --------- |
| 1     | `00`      |
| 2     | `01`      |
| 16    | `0F`      |
| 32    | `1F`      |

```text
F0 00 20 33 01 00 6E 00 7F 00 F7 # 1 step
F0 00 20 33 01 00 6E 00 7F 01 F7 # 2 steps
F0 00 20 33 01 00 6E 00 7F 0F F7 # 16 steps
F0 00 20 33 01 00 6E 00 7F 1F F7 # 32 steps
```

**Not** [Oscillators SELECT](../live-edit/single/oscillators.md#select-717f) — same
param byte **`7F`**, different **`cmd`** (`6E` vs `71`).

---

## Arpeggiator step triplet

User-pattern **steps 1**–**32** each use **three** consecutive **`cmd=0x6F`**
params (stride **+3** per step). Base param **`(step − 1) × 3`**. Same layout
in **Single Dump** at **`0x18A + (step − 1) × 3`** ( **`-INIT-`** baseline).

| Offset | Control       | Param (step *n*)         | Encoding                                           |
| ------ | ------------- | ------------------------ | -------------------------------------------------- |
| +0     | Step Length   | **`(n − 1) × 3`**        | **−100..+100 %** — [map](#arpeggiator-step-length) |
| +1     | Step Velocity | **`0x01 + (n − 1) × 3`** | **`0`–`127`** direct                               |
| +2     | Step Enable   | **`0x02 + (n − 1) × 3`** | **`00`** off · **`01`** on                         |

Step **1** → **`00`/`01`/`02`**; step **32** → **`5D`/`5E`/`5F`**.

**Not** Edit Single **Inputs** (`6F`/`7C`–`7E` on the same **`cmd`**).

---

## Arpeggiator Step Length

User-pattern **step length** — steps **1**–**32**. Live edit:
**`cmd=0x6F`**, param **`(step − 1) × 3`**. Standard Virus bipolar **%**
encoding: **`stored = ui + 64`** (**`00`–`7F`**), **−100.0..+100.0 %** with
**+0.0 %** at **`40`** — same family as [Arpeggiator Note
Length](#arpeggiator-note-length-lcd) and other **−100.0..+100.0 %** LCD
controls. Param stride confirmed for step **32** (`5D`); steps **1**–**31** use
the same **`(step − 1) × 3`** formula as [Step Velocity](#arpeggiator-step-velocity).

| UI       | `<value>` |
| -------- | --------- |
| −100.0 % | `00`      |
| +0.0 %   | `40`      |
| +100.0 % | `7F`      |

```text
F0 00 20 33 01 00 6F 00 5D 00 F7 # Step 32 length −100.0 %
F0 00 20 33 01 00 6F 00 5D 40 F7 # Step 32 length +0.0 %
F0 00 20 33 01 00 6F 00 5D 7F F7 # Step 32 length +100.0 %
```

See [Arpeggiator step triplet](#arpeggiator-step-triplet).

---

## Arpeggiator Step Velocity

User-pattern **step velocity** — steps **1**–**32**. Live edit:
**`cmd=0x6F`**, param **`0x01 + (step − 1) × 3`**, **`stored = lcd`** (**`00`–`7F`**
→ **0**–**127**).
buffer read in host software).

| Step | `<param>` |
| ---- | --------- |
| 1    | `01`      |
| 2    | `04`      |
| …    | +3/step   |
| 32   | `5E`      |

```text
F0 00 20 33 01 00 6F 00 01 00 F7 # Step 1 velocity 0
F0 00 20 33 01 00 6F 00 01 7F F7 # Step 1 velocity 127
F0 00 20 33 01 00 6F 00 04 00 F7 # Step 2 velocity 0
F0 00 20 33 01 00 6F 00 04 7F F7 # Step 2 velocity 127
F0 00 20 33 01 00 6F 00 5E 00 F7 # Step 32 velocity 0
F0 00 20 33 01 00 6F 00 5E 7F F7 # Step 32 velocity 127
```

See [Arpeggiator step triplet](#arpeggiator-step-triplet).

---

## Arpeggiator Step Enable

User-pattern **step on/off** — steps **1**–**32**. Live edit:
**`cmd=0x6F`**, param **`0x02 + (step − 1) × 3`**, **`00`** = off, **`01`** = on.

| Step | `<param>` | Off      | On       |
| ---- | --------- | -------- | -------- |
| 1    | `02`      | `…02 00` | `…02 01` |
| 2    | `05`      | ✓        | ✓        |
| …    | +3/step   | `00`     | `01`     |
| 32   | `5F`      | ✓        | ✓        |

```text
F0 00 20 33 01 00 6F 00 02 00 F7 # Step 1 off
F0 00 20 33 01 00 6F 00 02 01 F7 # Step 1 on
F0 00 20 33 01 00 6F 00 5F 00 F7 # Step 32 off
F0 00 20 33 01 00 6F 00 5F 01 F7 # Step 32 on
```

See [Arpeggiator step triplet](#arpeggiator-step-triplet).

---

## Delay Type

**Edit FX → Delay → Type**. **`stored = index`**.

| Index | `<value>` | Option       |
| ----- | --------- | ------------ |
| 0     | `00`      | Classic      |
| 1     | `01`      | Tape Clocked |
| 2     | `02`      | Tape Free    |
| 3     | `03`      | Tape Doppler |

---

## Delay panel visibility

**Edit FX → Delay**. Panel-confirmed. **Type** is always available.

### Send = Off (`00`)

For every **Type**, when **Send** = **Off** (`00` in [Delay Send](#delay-send-lcd)),
the panel shows only **Type**, **Send**, and **Feedback**. No
**Delay Time** / **Time**, **Mode**, **Clock**, **Coloration**, LFO rows, or
other
tape/classic rows.

| Control      | Visible | Notes                                                                                         |
| ------------ | ------- | --------------------------------------------------------------------------------------------- |
| **Type**     | Yes     | [Delay Type](#delay-type) — always available                                                  |
| **Send**     | Yes     | [Delay Send (LCD)](#delay-send-lcd)                                                           |
| **Feedback** | Yes     | [Delay Feedback](#delay-feedback) — **Classic** **0.0..100.0 %**; **Tape** **0.0..200.0 %**   |

Set **Send** to any value **other than Off** to reveal the type-specific
controls
below (**Type**, **Send**, and **Feedback** stay available).

### Type = Classic (`00`) — Send not Off

| Control                   | Visible                                     | Panel range / notes                                                                                       |
| ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Send                      | Yes                                         | [Delay Send (LCD)](#delay-send-lcd)                                                                       |
| Feedback                  | Yes                                         | [Delay Feedback](#delay-feedback) — **Classic** **0..100 %** / **Tape** **0..200 %** on **`73`**          |
| Mode                      | Yes                                         | [Delay Mode](#delay-mode) — **`01`–`16`**                                                                 |
| Coloration                | Yes                                         | [Delay Coloration](#delay-coloration) — **−64..+63**                                                      |
| LFO (Rate / Depth / Wave) | Yes                                         | [Delay LFO](#delay-lfo) — same panel page                                                                 |
| Clock                     | Simple Delay / Ping Pong … only             | [Delay Clock](#delay-clock) — **`00`–`10`**; **`00`** = **Off**                                           |
| Delay Time                | Simple/Ping Pong + **Clock** = **Off** only | [Delay Time (ms)](#delay-time-ms) — **not** on **Pattern** (`06`–`16`; **Pattern 5+5**)                   |

When **Clock** is a tempo division (**not** **Off**), **Delay Time** is
**hidden**
(synced delay). When **Clock** = **Off** (`00`), **Delay Time** replaces it on
the
panel.

**Pattern …** modes (`06`–`16`): no **Clock**, no **Delay Time** / **Time** on
the
on **Pattern 5+5**. **Coloration** and LFO rows stay visible —
see
[Delay Mode](#delay-mode).

### Type = Tape Clocked (`01`) — Send not Off

| Control     | Visible | Notes                                                          |
| ----------- | ------- | -------------------------------------------------------------- |
| Send        | Yes     | [Delay Send (LCD)](#delay-send-lcd) — same curve all **Types** |
| Feedback    | Yes     | [Delay Feedback](#delay-feedback) — **0.0..200.0 %**           |
| Left Clock  | Yes     | [Delay Tape Left Clock](#delay-tape-left-clock)                |
| Right Clock | Yes     | [Delay Tape Right Clock](#delay-tape-right-clock)              |
| Frequency   | Yes     | [Tape Frequency](#delay-tape-frequency)                        |
| Bandwidth   | Yes     | [Tape Bandwidth](#delay-tape-bandwidth)                        |
| Modulation  | Yes     | [Tape Modulation](#delay-tape-modulation)                      |

No **Mode**, **Clock**, **Coloration**, **Rate**, **Depth**, **LFO Wave**,
**Time**,
or **Ratio**.

### Type = Tape Free (`02`) or Tape Doppler (`03`) — Send not Off

| Control    | Visible | Panel range (Free = Doppler)                                                                     |
| ---------- | ------- | ------------------------------------------------------------------------------------------------ |
| Send       | Yes     | [Delay Send (LCD)](#delay-send-lcd) — **Off**, −46.2 dB … **0/−24.0 dB**, **Effect** (`00`–`7F`) |
| Feedback   | Yes     | [Delay Feedback](#delay-feedback) — **0.0..200.0 %**                                             |
| Time       | Yes     | [Delay Time (ms)](#delay-time-ms) — panel **Time** = Classic **Delay Time**; **0.0..693.6 ms**   |
| Ratio      | Yes     | [Delay Tape Ratio](#delay-tape-ratio) — **1/4** … **4/1** (`00`–`06`)                            |
| Frequency  | Yes     | [Tape Frequency](#delay-tape-frequency) — **`0`–`127`**                                          |
| Bandwidth  | Yes     | [Tape Bandwidth](#delay-tape-bandwidth) — **`0`–`127`**                                          |
| Modulation | Yes     | [Tape Modulation](#delay-tape-modulation) — **0.0..100.0 %**                                     |

Same panel set and ranges for **Tape Free** (`02`) and **Tape Doppler** (`03`).
All seven type-specific rows above (`6E`/`0A`/`03`).
No **Left Clock** / **Right Clock** (Tape Clocked only). No Classic rows.

---

## Delay Tape Left Clock

**Edit FX → Delay → Left Clock** (**Type** = Tape Clocked, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0D`**. **`stored = <value>`** (wire byte).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/32   |
| `01`      | 1/16   |
| `02`      | 2/16   |
| `03`      | 3/16   |
| `04`      | 4/16   |
| `05`      | 5/16   |

---

## Delay Tape Right Clock

**Edit FX → Delay → Right Clock** (**Type** = Tape Clocked, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0E`**. Same options as
[Left Clock](#delay-tape-left-clock).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/32   |
| `01`      | 1/16   |
| `02`      | 2/16   |
| `03`      | 3/16   |
| `04`      | 4/16   |
| `05`      | 5/16   |

---

## Delay Tape Frequency

**Edit FX → Delay → Frequency** (**Tape Clocked**, **Tape Free**, **Tape
Doppler**
— not Classic). **No** **Time** / **Ratio** on Tape Clocked.
Live edit: **`cmd=0x70`**, param **`0x77`** (Page **A#119**). **`stored = lcd`**
(**`0`–`127`**). Panel **0..127** on **Tape Doppler** (`03`). Same param byte as
[Delay Coloration](#delay-coloration) on **Classic** (**`stored = ui + 64`**).

---

## Delay Tape Bandwidth

**Edit FX → Delay → Bandwidth** (all three **Tape** types when **Send** ≠ Off).
Live edit:
**`cmd=0x6E`**, param **`0x11`**. **`stored = lcd`** (**`0`–`127`**). Panel
**0..127**
on **Tape Doppler** (`03`).

---

## Delay Tape Modulation

**Edit FX → Delay → Modulation** (all three **Tape** types when **Send** ≠ Off).
Live edit:
**`cmd=0x70`**, param **`0x75`** (same param byte as Classic delay
[Delay Feedback](../live-edit/single/effects.md#delay-feedback); tape
**Feedback** uses **`73`** instead).

**0.0..100.0 %**:

```text
stored = round(pct × 127 / 100)
```

**`00`** = 0 %, **`7F`** = 100.0 %. Panel **0.0..100.0 %** on **Tape Doppler**
(`03`).

---

## Delay Time (ms)

One control, two panel labels: **Delay Time** (**Classic**) and **Time** (**Tape
Free** / **Tape Doppler**). Same live edit, scale, and wire map.

Live edit: **`cmd=0x70`**, param **`0x72`** (Page **A#114**). Panel **0.0..693.6
ms**
(one decimal on LCD). **`stored = lcd`** (direct byte **`00`–`7F`**). Hardware
TX
confirmed (**Tape Free** `6E`/`0A`/`02`, **Time** sweep `70`/`72`
**`00`–`7F`**).

| Context                          | Panel label    | When visible                                                                                                                                      |
| -------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Classic**                      | **Delay Time** | **Send** ≠ Off, **Mode** = Simple Delay or Ping Pong … (`01`–`05`), **[Clock](#delay-clock) = Off** (`00`); **hidden** on **Pattern** (`06`–`16`) |
| **Tape Free** / **Tape Doppler** | **Time**       | **Send** ≠ Off (no **Clock** row)                                                                                                                 |

Approximate scale:

```text
lcd_ms ≈ stored × 693.6 / 127 # round display to 0.1 ms
```

| `<value>` | dec | LCD (ms) |
| --------- | --- | -------- |
| `00`      | 0   | 0.0      |
| `20`      | 32  | 174.8    |
| `28`      | 40  | 218.5    |
| `40`      | 64  | 349.5    |
| `50`      | 80  | 436.9    |
| `60`      | 96  | 524.3    |
| `64`      | 100 | 546.1    |
| `70`      | 112 | 611.7    |
| `7F`      | 127 | 693.6    |

Wire **`40`** is hex (**decimal 64**), not decimal 40.

---

## Delay Tape Ratio

**Edit FX → Delay → Ratio** (**Tape Free** or **Tape Doppler**, **Send** ≠ Off).
Live edit: **`cmd=0x6E`**, param **`0x0C`**. **`stored = <value>`** (wire byte).

| `<value>` | Option |
| --------- | ------ |
| `00`      | 1/4    |
| `01`      | 2/4    |
| `02`      | 3/4    |
| `03`      | 4/4    |
| `04`      | 4/3    |
| `05`      | 4/2    |
| `06`      | 4/1    |

Same seven options on **Tape Doppler** (`03`). Panel-confirmed (`6E`/`0C`
stepped).

---

## Delay Feedback

**Edit FX → Delay → Feedback** (visible when **Send** = Off with **Type** and
**Send**;
also when **Send** ≠ Off with type-specific rows). Live edit:
**`cmd=0x70`**, param **`0x73`** (Page **A#115**).
Same wire byte; **encoding depends on Type**:

| **Type**             | Panel range      | Encoding                          |
| -------------------- | ---------------- | --------------------------------- |
| **Classic** (`00`)   | **0.0..100.0 %** | `stored = round(pct × 127 / 100)` |
| **Tape** (`01`–`03`) | **0.0..200.0 %** | `stored = round(pct × 127 / 200)` |

### Classic (`00`)

| LCD     | `<value>` |
| ------- | --------- |
| 0.0 %   | `00`      |
| 100.0 % | `7F`      |

### Tape (`01`–`03`)

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 100.0 % | `40`      |
| 200.0 % | `7F`      |

See [effects.md — Delay
Feedback](../live-edit/single/effects.md#delay-feedback).

---

## Delay Mode

**Edit FX → Delay → Mode** (**Type** = Classic, **Send** ≠ Off). Live edit:
**`cmd=0x70`**, param **`0x70`** (Page **A#112**). **`stored = <value>`** (wire
byte;
first option is **`01`**, not **`00`**).
stepped; full enum **`01`–`16`**). Not **Type** (`6E`/`0A`).

**Do not confuse** with [Delay LFO Rate](#delay-lfo-rate) (**`70`/`74`**, not
**`0x70`**).

### Simple Delay and Ping Pong (`01`–`05`)

Show **Clock** (and **Delay Time** when **Clock** = Off), **Coloration**,
**Rate**,
**Depth**, **LFO Wave**.

| `<value>` | Option        |
| --------- | ------------- |
| `01`      | Simple Delay  |
| `02`      | Ping Pong 2:1 |
| `03`      | Ping Pong 4:3 |
| `04`      | Ping Pong 4:1 |
| `05`      | Ping Pong 8:7 |

### Pattern (`06`–`16`)

No **Clock** row; no **Delay Time** / **Time** control on the panel (confirmed
**Pattern 5+5**). **Coloration** + LFO rows remain. Live-edit TX confirmed for
**Feedback** (`73`) and **Coloration** (`77`) on **Pattern 5+5** (`16`).

| `<value>` | Option      |
| --------- | ----------- |
| `06`      | Pattern 1+1 |
| `07`      | Pattern 2+1 |
| `08`      | Pattern 3+1 |
| `09`      | Pattern 4+1 |
| `0A`      | Pattern 5+1 |
| `0B`      | Pattern 2+3 |
| `0C`      | Pattern 2+5 |
| `0D`      | Pattern 3+2 |
| `0E`      | Pattern 3+3 |
| `0F`      | Pattern 3+4 |
| `10`      | Pattern 3+5 |
| `11`      | Pattern 4+3 |
| `12`      | Pattern 4+5 |
| `13`      | Pattern 5+2 |
| `14`      | Pattern 5+3 |
| `15`      | Pattern 5+4 |
| `16`      | Pattern 5+5 |

**Simple Delay** / **Ping Pong …**: **Clock** + **Delay Time** when **Clock** =
**Off** — [Delay Clock](#delay-clock), [Delay Time (ms)](#delay-time-ms).

---

## Delay Coloration

**Edit FX → Delay → Coloration** (**Type** = Classic, **Send** ≠ Off). Panel
**−64..+63** (signed UI). Full wire map:
[Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40).

Live edit: **`cmd=0x70`**, param **`0x77`** (Page **A#119**). (**`00`–`7F`–`00`**).
Mod-matrix **Delay Coloration** id **`0x54`** ≠ live-edit param byte (same
pattern as **Delay Rate** `0x1E` vs **`0x74`**).

On **Tape** types, **`77`** is [Tape Frequency](#delay-tape-frequency)
(**`0`–`127`**,
`stored = lcd`) — same wire byte, different **Type** context.

---

## Delay Clock

**Edit FX → Delay → Clock** ( **Type** = Classic, **Send** ≠ Off, **Mode** =
Simple Delay or Ping Pong …).
Live edit: **`F0 … 71 00 14 <value> F7`**. **`stored =
<value>`**
(wire byte). Table order = **panel menu** (slow → fast). Distinct from Common
**Smooth Mode** (`71`/`19`); same division labels as
[Control Smooth Mode / clock quantize](#control-smooth-mode--clock-quantize)
quantize rows but **different** wire map.

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | 1/64   |
| `02`      | 1/32   |
| `0B`      | 1/24   |
| `07`      | 3/64   |
| `03`      | 1/16   |
| `0C`      | 1/12   |
| `08`      | 3/32   |
| `04`      | 1/8    |
| `0D`      | 1/6    |
| `09`      | 3/16   |
| `05`      | 1/4    |
| `0E`      | 1/3    |
| `0A`      | 3/8    |
| `06`      | 1/2    |
| `0F`      | 2/3    |
| `10`      | 3/4    |

Valid wire values **`00`–`10`** only (every byte in that range is used; no
gaps).
**`11`**, **`12`** probed via SysEx → **ignored**. **`13`–`7F`** not in menu.

**Panel visibility:** **`00` Off** shows [Delay Time (ms)](#delay-time-ms)
(**0.0..693.6 ms**). Any synced division **hides** **Delay Time** (tempo-locked
delay length).

See also [LFO Clock](#lfo-clock) — same **`00`–`10`** grid, plus **`11`–`15`**
(whole-note multiples through **16/1**).

---

## LFO Clock

**EDIT LFO → LFO *n* → Clock** (panel **Clock**; **Clock**).
Live edit: **`cmd=0x71`**, **`stored = <value>`** (wire byte).

**Panel knob:** minimum (**all the way down**) = **Off** (`00`); each step up =
**1/64**, **1/32**, … through **16/1** (`15`). **Off** is the first row on the
**Clock** control (same idea as [Delay Clock](#delay-clock) **Off** + **Delay Time**).

Synced divisions **`01`–`15`** run **slow → fast** on the panel (same grid as
[Delay Clock](#delay-clock) for **`01`–`10`**, plus **`11`–`15`** whole-note
multiples).

| LFO   | Page B | Param      |
| ----- | ------ | ---------- |
| LFO 1 | #18    | **`0x12`** |
| LFO 2 | #19    | **`0x13`** |
| LFO 3 | #21    | **`0x15`** |

```text
F0 00 20 33 01 00 71 40 12 00 F7 # LFO 1 Off
F0 00 20 33 01 00 71 40 12 05 F7 # LFO 1 1/4
F0 00 20 33 01 00 71 40 12 15 F7 # LFO 1 16/1
F0 00 20 33 01 00 71 40 13 00 F7 # LFO 2 Off
F0 00 20 33 01 00 71 40 13 05 F7 # LFO 2 1/4
F0 00 20 33 01 00 71 40 13 15 F7 # LFO 2 16/1
F0 00 20 33 01 00 71 40 15 00 F7 # LFO 3 Off
F0 00 20 33 01 00 71 40 15 05 F7 # LFO 3 1/4
F0 00 20 33 01 00 71 40 15 15 F7 # LFO 3 16/1
F0 00 20 33 01 00 71 00 12 <value> F7 # LFO 1 Clock (Multi Part 1)
```

**`<value>`** table — all three LFO **Clock** params (**`12`**, **`13`**, **`15`**):

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | 1/64   |
| `02`      | 1/32   |
| `0B`      | 1/24   |
| `07`      | 3/64   |
| `03`      | 1/16   |
| `0C`      | 1/12   |
| `08`      | 3/32   |
| `04`      | 1/8    |
| `0D`      | 1/6    |
| `09`      | 3/16   |
| `05`      | 1/4    |
| `0E`      | 1/3    |
| `0A`      | 3/8    |
| `06`      | 1/2    |
| `0F`      | 2/3    |
| `10`      | 3/4    |
| `11`      | 1/1    |
| `12`      | 2/1    |
| `13`      | 4/1    |
| `14`      | 8/1    |
| `15`      | 16/1   |

Valid wire values **`00`–`15`** (**22** menu rows). Distinct from
[Arpeggiator Resolution](#arpeggiator-resolution) (`71`/`11`) and [Delay
Clock](#delay-clock) (stops at **`10`**).

**Panel visibility:** **`00` Off** (knob minimum) shows [LFO Rate](#lfo-rate)
(**`0`–`127`**, free-running). Any synced division **`01`–`15`** **hides**
**Rate** (tempo-locked LFO speed).

---

## LFO live edit routing

**EDIT LFO → LFO *n*** settings share the same **value** encodings
([Rate](#lfo-rate), [Shape](#lfo-shape), [LFO settings](#lfo-settings)). Live
edit **`cmd` / `param`** depend on which LFO is being edited:

| Control           | LFO 1            | LFO 2            | LFO 3       |
| ----------------- | ---------------- | ---------------- | ----------- |
| **Clock**         | `71` / `12`      | `71` / `13`      | `71` / `15` |
| **Rate**          | `71` / `43`      | `70` / `4F`      | `71` / `07` |
| **Shape**         | `71` / `44`      | `70` / `50`      | `71` / `08` |
| **Envelope Mode** | `71` / `45`      | `70` / `51`      | —           |
| **Mode**          | `71` / `46`      | `70` / `52`      | `71` / `09` |
| **Contour**       | `71` / `47`      | `70` / `53`      | —           |
| **Key Follow**    | `71` / `48`      | `70` / `54`      | `71` / `0A` |
| **Trigger Phase** | `71` / `49`      | `70` / `55`      | —           |
| **Depth (×5)**    | `70` / `4A`–`4E` | `70` / `56`–`5A` | —           |
| **Assign Target** | `71` / `4F`      | `71` / `51`      | `71` / `0B` |
| **Amount**        | `71` / `50`      | `71` / `52`      | `71` / `0C` |
| **Fade In**       | —                | —                | `71` / `0D` |

**Routing rules:**

- **Clock** — always **`cmd=0x71`** (Page B). Params **`0x12`** (LFO 1),
  **`0x13`** (LFO 2), **`0x15`** (LFO 3). Byte **`0x14`** is not an LFO clock
  param.
- **LFO 1** — all settings on **`cmd=0x71`**, seven-param block **`0x43`–`0x49`**
  (Rate → Shape → Envelope Mode → Mode → Contour → Key Follow → Trigger Phase).
- **LFO 2** — settings on **`cmd=0x70`** (Page A), same seven-param order,
  block **`0x4F`–`0x55`**.
- **LFO 1 Destination** — depths on **`cmd=0x70`** **`4A`–`4E`**; **Assign Target**
  **`71`/`4F`**, **Amount** **`71`/`50`** — [LFO 1 Destination](#lfo-1-destination).
- **LFO 2 Destination** — depths on **`cmd=0x70`** **`56`–`5A`**; **Assign Target**
  **`71`/`51`**, **Amount** **`71`/`52`** — [LFO 2 Destination](#lfo-2-destination).
  Assign **`<value>`** bytes match LFO 1.
- **LFO 3** — compact panel on **`cmd=0x71`**: **Rate** **`0x07`**, **Shape**
  **`0x08`**, **Mode** **`0x09`**, **Key Follow** **`0x0A`**, **Clock**
  **`0x15`**. Sub-menu **LFO 3 Destination**: **Assign Target** **`0x0B`**,
  **Amount** **`0x0C`**, **Fade In** **`0x0D`** — [LFO 3 Destination](#lfo-3-destination).

```text
# LFO 2 — minimum settings (hardware TX)
F0 00 20 33 01 00 71 40 13 00 F7 # Clock Off
F0 00 20 33 01 00 70 40 4F 00 F7 # Rate 0
F0 00 20 33 01 00 70 40 50 00 F7 # Shape Sine
F0 00 20 33 01 00 70 40 51 00 F7 # Envelope Mode Off
F0 00 20 33 01 00 70 40 52 00 F7 # Mode Poly
F0 00 20 33 01 00 70 40 53 00 F7 # Contour −64
F0 00 20 33 01 00 70 40 54 00 F7 # Key Follow Off
F0 00 20 33 01 00 70 40 55 00 F7 # Trigger Phase Off

# LFO 3 — minimum settings (hardware TX)
F0 00 20 33 01 00 71 40 15 00 F7 # Clock Off
F0 00 20 33 01 00 71 40 07 00 F7 # Rate 0
F0 00 20 33 01 00 71 40 08 00 F7 # Shape Sine
F0 00 20 33 01 00 71 40 09 00 F7 # Mode Poly
F0 00 20 33 01 00 71 40 0A 00 F7 # Key Follow Off

# LFO 3 Destination (hardware TX)
F0 00 20 33 01 00 71 40 0B 00 F7 # Assign Target Osc 1 Pitch
F0 00 20 33 01 00 71 40 0C 00 F7 # Amount 0 %
F0 00 20 33 01 00 71 40 0D 00 F7 # Fade In 0
```

---

## LFO Rate

**EDIT LFO → LFO *n* → Rate** — visible only when [Clock](#lfo-clock) =
**Off**. **`stored = lcd`** (**`0`–`127`** → **`00`–`7F`**). Same direct
encoding as [Delay LFO Rate](#delay-lfo-rate). Routing:
[LFO live edit routing](#lfo-live-edit-routing).

| LFO   | `cmd`      | Param      |
| ----- | ---------- | ---------- |
| LFO 1 | **`0x71`** | **`0x43`** |
| LFO 2 | **`0x70`** | **`0x4F`** |
| LFO 3 | **`0x71`** | **`0x07`** |

```text
F0 00 20 33 01 00 71 40 43 <value> F7 # LFO 1 Rate (Clock Off)
F0 00 20 33 01 00 70 40 4F <value> F7 # LFO 2 Rate (Clock Off)
F0 00 20 33 01 00 71 40 07 <value> F7 # LFO 3 Rate (Clock Off)
```

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

---

## LFO Shape

**EDIT LFO → LFO *n* → Shape** (**Shape**).
**`stored = <value>`** (wire byte). **68** panel choices **`00`–`43`**. Routing:
[LFO live edit routing](#lfo-live-edit-routing).

| LFO   | `cmd`      | Param      |
| ----- | ---------- | ---------- |
| LFO 1 | **`0x71`** | **`0x44`** |
| LFO 2 | **`0x70`** | **`0x50`** |
| LFO 3 | **`0x71`** | **`0x08`** |

```text
F0 00 20 33 01 00 71 40 44 <value> F7 # LFO 1 Shape
F0 00 20 33 01 00 70 40 50 <value> F7 # LFO 2 Shape
F0 00 20 33 01 00 71 40 08 <value> F7 # LFO 3 Shape
```

### Basic shapes (`00`–`05`)

Same labels and wire bytes as [Delay LFO Wave](#delay-lfo-wave):

| `<value>` | Option   |
| --------- | -------- |
| `00`      | Sine     |
| `01`      | Triangle |
| `02`      | Sawtooth |
| `03`      | Square   |
| `04`      | S&H      |
| `05`      | S&G      |

### Spectral waves (`06`–`43`)

**Wave 3** … **Wave 64** — same LCD names as Oscillator **Wave Select**
(`70`/`13`, `70`/`18` at **`02`–`3F`**) and the wave block of Osc 3
**Mode/Wave** (`71`/`29` at **`06`–`43`**):

```text
wave_number = stored − 3        # Wave 3 → 06, Wave 64 → 43
stored      = wave_number + 3   # for wave_number 3..64
```

Contiguous run — no gaps between **Wave 3** and **Wave 64**. Spot-checked:

| `<value>` | Option  |
| --------- | ------- |
| `06`      | Wave 3  |
| `0E`      | Wave 11 |
| `16`      | Wave 19 |
| `23`      | Wave 32 |
| `43`      | Wave 64 |

Equivalently: LFO **`06`–`43`** = Osc **Wave Select** **`02`–`3F`** + **`04`**
offset.

---

## LFO settings

**EDIT LFO → LFO *n*** — settings besides [Clock](#lfo-clock) and
[Shape](#lfo-shape). **`stored = <value>`** (wire byte). **`cmd` / `param`** per
[LFO live edit routing](#lfo-live-edit-routing). Value encodings below apply to
**LFO 1 and LFO 2** (and to LFO 3 where the control exists).

| Control       | LFO 1     | LFO 2     | LFO 3     |
| ------------- | --------- | --------- | --------- |
| Rate          | `71`/`43` | `70`/`4F` | `71`/`07` |
| Envelope Mode | `71`/`45` | `70`/`51` | —         |
| Mode          | `71`/`46` | `70`/`52` | `71`/`09` |
| Contour       | `71`/`47` | `70`/`53` | —         |
| Key Follow    | `71`/`48` | `70`/`54` | `71`/`0A` |
| Trigger Phase | `71`/`49` | `70`/`55` | —         |

```text
F0 00 20 33 01 00 71 40 43 <value> F7 # LFO 1 Rate (Clock Off)
F0 00 20 33 01 00 71 40 45 <value> F7 # LFO 1 Envelope Mode
F0 00 20 33 01 00 71 40 46 <value> F7 # LFO 1 Mode
F0 00 20 33 01 00 71 40 47 <value> F7 # LFO 1 Contour
F0 00 20 33 01 00 71 40 48 <value> F7 # LFO 1 Key Follow
F0 00 20 33 01 00 71 40 49 <value> F7 # LFO 1 Trigger Phase
F0 00 20 33 01 00 71 40 07 <value> F7 # LFO 3 Rate (Clock Off)
F0 00 20 33 01 00 71 40 09 <value> F7 # LFO 3 Mode
F0 00 20 33 01 00 71 40 0A <value> F7 # LFO 3 Key Follow
```

### Contour

**Live edit:** `cmd=0x71`/`0x70`, param `0x47` (LFO 1 / LFO 2).

**Waveform Contour** — bipolar **−64..+63**:
[Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40).

### Mode (`0x46` / LFO 3 `0x09`)

| `<value>` | Option |
| --------- | ------ |
| `00`      | Poly   |
| `01`      | Mono   |

### Envelope Mode

**Live edit:** `cmd=0x71`/`0x70`, param `0x45` (LFO 1 / LFO 2).

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | On     |

Same **`00`/`01`** pattern as [Arpeggiator Hold](#arpeggiator-hold).

### Trigger Phase

**Live edit:** `cmd=0x71`/`0x70`, param `0x49` (LFO 1 / LFO 2).

| `<value>` | Option          |
| --------- | --------------- |
| `00`      | Off             |
| `01`–`7F` | **1** … **127** |

```text
phase = stored            # for stored 01h..7Fh
stored = phase            # panel 1..127
```

### Key Follow (`0x48` / LFO 3 `0x0A`)

**`00`** = **Off**. **`01`–`7F`** = **0.8..100.0 %** (LCD shows one decimal):

```text
pct = 0.8 + (stored − 1) × 99.2 / 126     # stored 01h..7Fh
stored = round((pct − 0.8) × 126 / 99.2 + 1)
```

| `<value>` | LCD     |
| --------- | ------- |
| `00`      | Off     |
| `01`      | 0.8 %   |
| `7F`      | 100.0 % |

---

## LFO 1 Destination

**EDIT LFO → LFO 1 → LFO 1 Destination** (modulation depth sub-menu). Worksheet
**LFO Modulation 1** rows map here. **Osc 1+2 Pitch** is a **linked panel
control** — one knob sends the same depth to **`70`/`4A`** and **`70`/`4B`**
(Osc 1 Pitch / Osc 2 Pitch); no separate wire param.

### Modulation depth

**Live edit:** `cmd=0x70`.

Bipolar **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64`
(**`00`** = −100.0 %, **`40`** = +0.0 %, **`7F`** = +100.0 %). Same family as
[Edit Single Panorama](#edit-single--panorama-lcd).

| Panel control | Param      |
| ------------- | ---------- |
| Osc 1 Pitch   | **`0x4A`** |
| Osc 2 Pitch   | **`0x4B`** |
| Pulse Width   | **`0x4C`** |
| Resonance     | **`0x4D`** |
| Filter Gain   | **`0x4E`** |

```text
F0 00 20 33 01 00 70 40 4A 00 F7 # Osc 1 Pitch −100.0 %
F0 00 20 33 01 00 70 40 4A 40 F7 # Osc 1 Pitch +0.0 %
F0 00 20 33 01 00 70 40 4A 7F F7 # Osc 1 Pitch +100.0 %
F0 00 20 33 01 00 70 40 4B 43 F7 # Osc 2 Pitch +4.7 % (linked knob example)
```

### Assign Target

**Live edit:** `cmd=0x71`, param `0x4F`.

**Assign Target** menu. **`00`** = **Off**. Other rows share the **Mod Matrix
Destinations** name set ([Mod Matrix Destinations](#mod-matrix-destinations));
wire **`<value>`** bytes are a separate namespace (not the mod-matrix table
index). Full enum confirmed (**121** destinations + **Off**), matching
[Mod Matrix Destinations](#mod-matrix-destinations) by name. Same **`<value>`**
bytes on [LFO 2 Assign Target](#assign-target-1) (**`71`/`51`**). Unused wire
bytes: **`49`**, **`4A`**, **`58`**, **`6B`**, **`70`**, **`77`**.

**Filterbank Frequency (`60`):** Mod matrix and LFO Assign Target wire **`60`**
→ [Filter Bank → Frequency](../live-edit/single/effects.md#filter-bank) (**`6E`/`15`**).
Modulation confirmed across **Ring Modulator**, **Frequency Shifter**, **Vowel
Filter**, **Comb Filter**, **Pole XFade**, and **VariSlope** types. LFO menu LCD
still shows **FreqShifter Frequency** — treat as **Filterbank Frequency** (mislabel).

| `<value>` | Panel label                                         |
| --------- | --------------------------------------------------- |
| `00`      | Off                                                 |
| `01`      | Patch Volume                                        |
| `02`      | Osc 1 Interpolation                                 |
| `03`      | Panorama                                            |
| `04`      | Transpose                                           |
| `05`      | Portamento                                          |
| `06`      | Osc 1 Shape/Index                                   |
| `07`      | Osc 1 Pulse Width                                   |
| `08`      | Osc 1 Wave Select                                   |
| `09`      | Osc 1 Pitch                                         |
| `0A`      | Slot 6 Amount 3                                     |
| `0B`      | Osc 2 Shape/Index                                   |
| `0C`      | Osc 2 Pulse Width                                   |
| `0D`      | Osc 2 Wave Select                                   |
| `0E`      | Osc 2 Pitch                                         |
| `0F`      | Osc 2 Detune                                        |
| `10`      | Osc 2 FM Amount                                     |
| `11`      | Filter Env > Osc 2 Pitch                            |
| `12`      | Filter Env > FM/Sync                                |
| `13`      | Osc 2 Interpolation                                 |
| `14`      | Oscillator Balance                                  |
| `15`      | Sub Osc Volume                                      |
| `16`      | Oscillator Volume                                   |
| `17`      | Noise Volume                                        |
| `18`      | Filter 1 Cutoff                                     |
| `19`      | Filter 2 Cutoff                                     |
| `1A`      | Filter 1 Resonance                                  |
| `1B`      | Filter 2 Resonance                                  |
| `1C`      | Filter 1 Env Amount                                 |
| `1D`      | Filter 2 Env Amount                                 |
| `1E`      | Slot 5 Amount 2                                     |
| `1F`      | Slot 5 Amount 3                                     |
| `20`      | Filter Balance                                      |
| `21`      | Filter Env Attack                                   |
| `22`      | Filter Env Decay                                    |
| `23`      | Filter Env Sustain                                  |
| `24`      | Filter Env Slope                                    |
| `25`      | Filter Env Release                                  |
| `26`      | Amp Env Attack                                      |
| `27`      | Amp Env Decay                                       |
| `28`      | Amp Env Sustain                                     |
| `29`      | Amp Env Slope                                       |
| `2A`      | Amp Env Release                                     |
| `2B`      | LFO 1 Rate                                          |
| `2C`      | LFO 1 Contour                                       |
| `2D`      | LFO 1 > Osc 1 Pitch                                 |
| `2E`      | LFO 1 > Osc 2 Pitch                                 |
| `2F`      | LFO 1 > Pulse Width                                 |
| `30`      | LFO 1 > Resonance                                   |
| `31`      | LFO 1 > Filter Gain                                 |
| `32`      | LFO 2 Rate                                          |
| `33`      | LFO 2 Contour                                       |
| `34`      | LFO 2 > Shape                                       |
| `35`      | LFO 2 > FM Amount                                   |
| `36`      | LFO 2 > Cutoff 1                                    |
| `37`      | LFO 2 > Cutoff 2                                    |
| `38`      | LFO 2 > Panorama                                    |
| `39`      | LFO 3 Rate                                          |
| `3A`      | LFO 3 > Assign Amount                               |
| `3B`      | Unison Detune                                       |
| `3C`      | Pan Spread                                          |
| `3D`      | Unison LFO Phase                                    |
| `3E`      | Chorus Mix                                          |
| `3F`      | Chorus Mod Rate                                     |
| `40`      | Chorus Mod Depth                                    |
| `41`      | Chorus Delay                                        |
| `42`      | Chorus Feedback                                     |
| `43`      | Delay Send                                          |
| `44`      | Delay Time                                          |
| `45`      | Delay Feedback                                      |
| `46`      | Delay Mod Rate                                      |
| `47`      | Delay Mod Depth                                     |
| `48`      | Reverb Send                                         |
| `4B`      | Slot 6 Amount 2                                     |
| `4C`      | Slot 4 Amount 2                                     |
| `4D`      | Slot 4 Amount 3                                     |
| `4E`      | Filterbank Resonance                                |
| `4F`      | Filterbank Poles                                    |
| `50`      | Slot 2 Amount 3                                     |
| `51`      | Filterbank Slope                                    |
| `52`      | Slot 1 Amount 1                                     |
| `53`      | Slot 2 Amount 1                                     |
| `54`      | Slot 2 Amount 2                                     |
| `55`      | Slot 3 Amount 1                                     |
| `56`      | Slot 3 Amount 2                                     |
| `57`      | Slot 3 Amount 3                                     |
| `59`      | Punch Intensity                                     |
| `5A`      | Ring Modulator                                      |
| `5B`      | Noise Color                                         |
| `5C`      | Delay Coloration                                    |
| `5D`      | Slot 1 Amount 2                                     |
| `5E`      | Slot 1 Amount 3                                     |
| `5F`      | Distortion Intensity                                |
| `60`      | Filterbank Frequency *(LCD: FreqShifter Frequency)* |
| `61`      | Osc 3 Volume                                        |
| `62`      | Osc 3 Pitch                                         |
| `63`      | Osc 3 Detune                                        |
| `64`      | LFO 1 > Assign Amount                               |
| `65`      | LFO 2 > Assign Amount                               |
| `66`      | Phaser Mix                                          |
| `67`      | Phaser Mod Rate                                     |
| `68`      | Phaser Mod Depth                                    |
| `69`      | Phaser Frequency                                    |
| `6A`      | Phaser Feedback                                     |
| `6C`      | Reverb Time                                         |
| `6D`      | Reverb Dampening                                    |
| `6E`      | Reverb Coloration                                   |
| `6F`      | Reverb PreDelay                                     |
| `71`      | Surround Balance                                    |
| `72`      | Arp Note Length                                     |
| `73`      | Arp Swing Factor                                    |
| `74`      | Arp Pattern                                         |
| `75`      | EQ Mid Gain                                         |
| `76`      | EQ Mid Frequency                                    |
| `78`      | Slot 4 Amount 1                                     |
| `79`      | Slot 5 Amount 1                                     |
| `7A`      | Slot 6 Amount 1                                     |
| `7B`      | Osc 1 F-Shift                                       |
| `7C`      | Osc 2 F-Shift                                       |
| `7D`      | Osc 1 F-Spread                                      |
| `7E`      | Osc 2 F-Spread                                      |
| `7F`      | Distortion Mix                                      |

```text
F0 00 20 33 01 00 71 40 4F 00 F7 # Off
F0 00 20 33 01 00 71 40 4F 26 F7 # Amp Env Attack
F0 00 20 33 01 00 71 40 4F 43 F7 # Delay Send
```

### Amount

**Live edit:** `cmd=0x71`, param `0x50`.

Active when **Assign Target** ≠ **Off**. Bipolar **−100.0..+100.0 %** (same
encoding as depth rows above — **not** the unipolar map used for [LFO 3
Amount](#amount)).

| `<value>` | LCD      |
| --------- | -------- |
| `00`      | −100.0 % |
| `40`      | +0.0 %   |
| `7F`      | +100.0 % |

```text
F0 00 20 33 01 00 71 40 50 00 F7 # −100.0 %
F0 00 20 33 01 00 71 40 50 40 F7 # +0.0 %
F0 00 20 33 01 00 71 40 50 7F F7 # +100.0 %
```

---

## LFO 2 Destination

**EDIT LFO → LFO 2 → LFO 2 Destination** (modulation depth sub-menu). Worksheet
**LFO Modulation 2** rows map here. **Cutoff 1+2** is a **linked panel control**
— one knob sends the same depth to **`70`/`58`** and **`70`/`59`** (Cutoff 1 /
Cutoff 2); no separate wire param.

### Modulation depth

**Live edit:** `cmd=0x70`.

Bipolar **−100.0..+100.0 %** — same encoding as [LFO 1 Destination](#lfo-1-destination)
depth rows.

| Panel control | Param      |
| ------------- | ---------- |
| Shape 1+2     | **`0x56`** |
| FM Amount     | **`0x57`** |
| Cutoff 1      | **`0x58`** |
| Cutoff 2      | **`0x59`** |
| Panorama      | **`0x5A`** |

```text
F0 00 20 33 01 00 70 40 56 00 F7 # Shape 1+2 −100.0 %
F0 00 20 33 01 00 70 40 58 40 F7 # Cutoff 1 +0.0 %
F0 00 20 33 01 00 70 40 59 53 F7 # Cutoff 2 +29.7 % (linked knob example)
F0 00 20 33 01 00 70 40 5A 7F F7 # Panorama +100.0 %
```

### Assign Target

**Live edit:** `cmd=0x71`, param `0x51`.

**Assign Target** menu — same **`<value>`** namespace as [LFO 1 Assign
Target](#assign-target) (full enum table there). confirms matching bytes (**`51`/`xx`** = **`4F`/`xx`**).

```text
F0 00 20 33 01 00 71 40 51 00 F7 # Off
F0 00 20 33 01 00 71 40 51 26 F7 # Amp Env Attack
F0 00 20 33 01 00 71 40 51 43 F7 # Delay Send
```

### Amount

**Live edit:** `cmd=0x71`, param `0x52`.

Active when **Assign Target** ≠ **Off**. Bipolar **−100.0..+100.0 %** (same as
[LFO 1 Amount](#lfo-1-destination)).

| `<value>` | LCD      |
| --------- | -------- |
| `00`      | −100.0 % |
| `40`      | +0.0 %   |
| `7F`      | +100.0 % |

```text
F0 00 20 33 01 00 71 40 52 00 F7 # −100.0 %
F0 00 20 33 01 00 71 40 52 40 F7 # +0.0 %
F0 00 20 33 01 00 71 40 52 7F F7 # +100.0 %
```

---

## LFO 3 Destination

**EDIT LFO → LFO 3 → LFO 3 Destination** (destination sub-menu). Live edit:
**`cmd=0x71`**, **`stored = <value>`**. Worksheet rows **User Destination** /
**User Destination Amount** / **Fade In Time** map to panel **Assign Target** /
**Amount** / **Fade In**.

| Control       | Param      |
| ------------- | ---------- |
| Assign Target | **`0x0B`** |
| Amount        | **`0x0C`** |
| Fade In       | **`0x0D`** |

```text
F0 00 20 33 01 00 71 40 0B <value> F7 # Assign Target
F0 00 20 33 01 00 71 40 0C <value> F7 # Amount
F0 00 20 33 01 00 71 40 0D <value> F7 # Fade In
```

### Assign Target

**Live edit:** `cmd=0x71`, param `0x0B`.

| `<value>` | Option              |
| --------- | ------------------- |
| `00`      | Osc 1 Pitch         |
| `01`      | Osc 1+2 Pitch       |
| `02`      | Osc 2 Pitch         |
| `03`      | Osc 1 Pulse Width   |
| `04`      | Osc 1+2 Pulse Width |
| `05`      | Osc 2 Pulse Width   |
| `06`      | Sync Phase          |

### Amount

**Live edit:** `cmd=0x71`, param `0x0C`.

**0.0..100.0 %** — same unipolar encoding as [Delay LFO Depth](#delay-lfo-depth):

```text
stored = round(pct × 127 / 100)     # 0 % → 00, 100.0 % → 7F
pct    = stored × 100 / 127
```

| `<value>` | LCD     |
| --------- | ------- |
| `00`      | 0 %     |
| `7F`      | 100.0 % |

### Fade In

**Live edit:** `cmd=0x71`, param `0x0D`.

**`0`–`127`** → `stored = lcd` (**`00`–`7F`**). Panel label **Fade In**
(**Fade In Time**).

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

---

## Delay LFO

**Edit FX → Delay** — **Rate**, **Depth**, and **LFO Wave** share one panel page
(delay **LFO modulation** of the effect). Visible on **Classic** when **Send** ≠
Off
(and on **Pattern …** modes with **Coloration**; no **Clock** / **Delay Time**).
Not on **Tape** types (those use **Frequency** / **Bandwidth** / **Modulation**
instead).

| Control      | Live edit                         | Range                          |
| ------------ | --------------------------------- | ------------------------------ |
| **Rate**     | [`70`/`74`](#delay-lfo-rate)      | **`0`–`127`** (`stored = lcd`) |
| **Depth**    | [`70`/`75`](#delay-lfo-depth)     | **0.0..100.0 %**               |
| **LFO Wave** | [`70`/`76`](#delay-lfo-wave)      | enum **`00`–`05`**             |

---

## Delay LFO Rate

**Edit FX → Delay → Rate** (part of [Delay LFO](#delay-lfo)). Live edit:
**`cmd=0x70`**, param
**`0x74`** (Page **A#116**). **`stored = lcd`** (**`0`–`127`**).
(sweep **`00`–`7F`**; **Rate** `0` → **`00`**). Not **`0x70`** ([Delay
Mode](#delay-mode)).
Mod-matrix **Delay Rate** id **`0x1E`** ≠ live-edit param byte.

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

---

## Delay LFO Depth

**Edit FX → Delay → Depth** (part of [Delay LFO](#delay-lfo); **Classic** only
on this
LFO page). Live edit: **`cmd=0x70`**, param **`0x75`** (Page **A#117**). Panel
**0.0..100.0 %**.

```text
stored = round(pct × 127 / 100)
```

| LCD     | `<value>` |
| ------- | --------- |
| 0.0 %   | `00`      |
| 100.0 % | `7F`      |

On **Tape** types, **`75`** is [Tape Modulation](#delay-tape-modulation) (same
wire
byte, different **Type** context). **`73`** is [Delay
Feedback](#delay-feedback).

---

## Delay LFO Wave

**Edit FX → Delay → LFO Wave** (part of [Delay LFO](#delay-lfo)). Live edit:
**`cmd=0x70`**, param **`0x76`**
(Page **A#118**). **`stored = <value>`** (wire byte).

| `<value>` | Option   | Notes                                             |
| --------- | -------- | ------------------------------------------------- |
| `00`      | Sine     |                                                   |
| `01`      | Triangle |                                                   |
| `02`      | Sawtooth |                                                   |
| `03`      | Square   |                                                   |
| `04`      | S&H      | **Sample and Hold**                               |
| `05`      | S&G      | **Sample and Glide** — S&H through a slew limiter |

---

## Delay Send (LCD)

**Edit FX → Delay → Send** (all **Types**).
**`stored = index`** (`00`–`7F`). Live edit: **`cmd=0x70`**, param **`0x71`**
(Page **A#113**). Same LCD map as [Reverb Send](#reverb-send-lcd) (**`6E`/`02`**).
Panel-confirmed (see table). Rows **`19`–`1D`**,
**`1F`–`27`**, **`29`–`3F`** are
**amplitude-interpolated**.

| Region                  | Rule                                                                |
| ----------------------- | ------------------------------------------------------------------- |
| `00`                    | **Off**                                                             |
| `01`–`40`               | Piecewise attenuation — see table                                   |
| `41`–`95` (`29`–`5F`)   | **`−0.25 × (96 − index)`** dB; wholes show **`.0`** (**`−9.0 dB`**) |
| `96`–`103` (`60`–`67`)  | **`0/−0.3 × (index − 96)`** dB                                      |
| `104`–`107` (`68`–`6B`) | Increasing steps — see table                                        |
| `108`–`126` (`6C`–`7E`) | **`0/−X dB`** headroom                                              |
| `127` (`7F`)            | **Effect** (max send)                                               |

| Index | `<value>` | LCD        |     |
| ----- | --------- | ---------- | --- |
| 0     | `00`      | Off        |     |
| 1     | `01`      | −46.2 dB   | ✓   |
| 2     | `02`      | −40.2 dB   | ✓   |
| 3     | `03`      | −36.6 dB   | ✓   |
| 4     | `04`      | −34.1 dB   | ✓   |
| 5     | `05`      | −32.2 dB   | ✓   |
| 6     | `06`      | −30.6 dB   | ✓   |
| 7     | `07`      | −29.3 dB   | ✓   |
| 8     | `08`      | −28.1 dB   | ✓   |
| 9     | `09`      | −27.1 dB   | ✓   |
| 10    | `0A`      | −26.2 dB   | ✓   |
| 11    | `0B`      | −25.4 dB   | ✓   |
| 12    | `0C`      | −24.6 dB   | ✓   |
| 13    | `0D`      | −23.9 dB   | ✓   |
| 14    | `0E`      | −23.3 dB   | ✓   |
| 15    | `0F`      | −22.7 dB   | ✓   |
| 16    | `10`      | −22.1 dB   | ✓   |
| 17    | `11`      | −21.6 dB   | ✓   |
| 18    | `12`      | −21.1 dB   | ✓   |
| 19    | `13`      | −20.6 dB   | ✓   |
| 20    | `14`      | −20.6 dB   | ✓   |
| 21    | `15`      | −19.7 dB   | ✓   |
| 22    | `16`      | −19.3 dB   | ✓   |
| 23    | `17`      | −18.9 dB   | ✓   |
| 24    | `18`      | −18.6 dB   | ✓   |
| 25    | `19`      | −18.2 dB   | ≈   |
| 26    | `1A`      | −17.8 dB   | ≈   |
| 27    | `1B`      | −17.5 dB   | ≈   |
| 28    | `1C`      | −17.2 dB   | ≈   |
| 29    | `1D`      | −16.9 dB   | ≈   |
| 30    | `1E`      | −16.6 dB   | ✓   |
| 31    | `1F`      | −16.3 dB   | ≈   |
| 32    | `20`      | −16.0 dB   | ≈   |
| 33    | `21`      | −15.7 dB   | ≈   |
| 34    | `22`      | −15.5 dB   | ≈   |
| 35    | `23`      | −15.2 dB   | ≈   |
| 36    | `24`      | −14.9 dB   | ≈   |
| 37    | `25`      | −14.7 dB   | ≈   |
| 38    | `26`      | −14.5 dB   | ≈   |
| 39    | `27`      | −14.2 dB   | ≈   |
| 40    | `28`      | −14.0 dB   | ✓   |
| 41    | `29`      | −13.75 dB  | ✓   |
| 42    | `2A`      | −13.5 dB   | ✓   |
| 43    | `2B`      | −13.25 dB  | ✓   |
| 44    | `2C`      | −13.0 dB   | ✓   |
| 45    | `2D`      | −12.75 dB  | ✓   |
| 46    | `2E`      | −12.5 dB   | ✓   |
| 47    | `2F`      | −12.25 dB  | ✓   |
| 48    | `30`      | −12.0 dB   | ✓   |
| 49    | `31`      | −11.75 dB  | ✓   |
| 50    | `32`      | −11.5 dB   | ✓   |
| 51    | `33`      | −11.25 dB  | ✓   |
| 52    | `34`      | −11.0 dB   | ✓   |
| 53    | `35`      | −10.75 dB  | ✓   |
| 54    | `36`      | −10.5 dB   | ✓   |
| 55    | `37`      | −10.25 dB  | ✓   |
| 56    | `38`      | −10.0 dB   | ✓   |
| 57    | `39`      | −9.75 dB   | ✓   |
| 58    | `3A`      | −9.5 dB    | ✓   |
| 59    | `3B`      | −9.25 dB   | ✓   |
| 60    | `3C`      | −9.0 dB    | ✓   |
| 61    | `3D`      | −8.75 dB   | ✓   |
| 62    | `3E`      | −8.5 dB    | ✓   |
| 63    | `3F`      | −8.25 dB   | ✓   |
| 64    | `40`      | −8.0 dB    | ✓   |
| 65    | `41`      | −7.75 dB   | ✓   |
| 66    | `42`      | −7.5 dB    | ✓   |
| 67    | `43`      | −7.25 dB   | ✓   |
| 68    | `44`      | −7.0 dB    | ✓   |
| 69    | `45`      | −6.75 dB   | ✓   |
| 70    | `46`      | −6.5 dB    | ✓   |
| 71    | `47`      | −6.25 dB   | ✓   |
| 72    | `48`      | −6.0 dB    | ✓   |
| 73    | `49`      | −5.75 dB   | ✓   |
| 74    | `4A`      | −5.5 dB    | ✓   |
| 75    | `4B`      | −5.25 dB   | ✓   |
| 76    | `4C`      | −5.0 dB    | ✓   |
| 77    | `4D`      | −4.75 dB   | ✓   |
| 78    | `4E`      | −4.5 dB    | ✓   |
| 79    | `4F`      | −4.25 dB   | ✓   |
| 80    | `50`      | −4.0 dB    | ✓   |
| 81    | `51`      | −3.75 dB   | ✓   |
| 82    | `52`      | −3.5 dB    | ✓   |
| 83    | `53`      | −3.25 dB   | ✓   |
| 84    | `54`      | −3.0 dB    | ✓   |
| 85    | `55`      | −2.75 dB   | ✓   |
| 86    | `56`      | −2.5 dB    | ✓   |
| 87    | `57`      | −2.25 dB   | ✓   |
| 88    | `58`      | −2.0 dB    | ✓   |
| 89    | `59`      | −1.75 dB   | ✓   |
| 90    | `5A`      | −1.5 dB    | ✓   |
| 91    | `5B`      | −1.25 dB   | ✓   |
| 92    | `5C`      | −1.0 dB    | ✓   |
| 93    | `5D`      | −0.75 dB   | ✓   |
| 94    | `5E`      | −0.5 dB    | ✓   |
| 95    | `5F`      | −0.25 dB   | ✓   |
| 96    | `60`      | 0/0 dB     | ✓   |
| 97    | `61`      | 0/−0.3 dB  | ✓   |
| 98    | `62`      | 0/−0.6 dB  | ✓   |
| 99    | `63`      | 0/−0.9 dB  | ✓   |
| 100   | `64`      | 0/−1.2 dB  | ✓   |
| 101   | `65`      | 0/−1.5 dB  | ✓   |
| 102   | `66`      | 0/−1.8 dB  | ✓   |
| 103   | `67`      | 0/−2.1 dB  | ✓   |
| 104   | `68`      | 0/−2.5 dB  | ✓   |
| 105   | `69`      | 0/−2.9 dB  | ✓   |
| 106   | `6A`      | 0/−3.3 dB  | ✓   |
| 107   | `6B`      | 0/−3.7 dB  | ✓   |
| 108   | `6C`      | 0/−4.1 dB  | ✓   |
| 109   | `6D`      | 0/−4.5 dB  | ✓   |
| 110   | `6E`      | 0/−5.0 dB  | ✓   |
| 111   | `6F`      | 0/−5.5 dB  | ✓   |
| 112   | `70`      | 0/−6.0 dB  | ✓   |
| 113   | `71`      | 0/−6.6 dB  | ✓   |
| 114   | `72`      | 0/−7.2 dB  | ✓   |
| 115   | `73`      | 0/−7.8 dB  | ✓   |
| 116   | `74`      | 0/−8.5 dB  | ✓   |
| 117   | `75`      | 0/−9.3 dB  | ✓   |
| 118   | `76`      | 0/−10.1 dB | ✓   |
| 119   | `77`      | 0/−11.0 dB | ✓   |
| 120   | `78`      | 0/−12.0 dB | ✓   |
| 121   | `79`      | 0/−13.2 dB | ✓   |
| 122   | `7A`      | 0/−14.5 dB | ✓   |
| 123   | `7B`      | 0/−16.1 dB | ✓   |
| 124   | `7C`      | 0/−18.1 dB | ✓   |
| 125   | `7D`      | 0/−20.6 dB | ✓   |
| 126   | `7E`      | 0/−24.0 dB | ✓   |
| 127   | `7F`      | Effect     | ✓   |

**`60`–`67`:** **`0/−0.3 × (index − 96)`** dB. **`68`–`6B`:** larger steps
(**`68`** **`−2.5`**, then **`−0.4`** through **`6A`**, **`6B`** **`−3.7`**).
**`6C`–`7E`:** headroom ladder. **`7F`** = **Effect**.

---

## Reverb Mode

**Edit FX → Reverb → Mode**. Part-sound buffer (**`6E`**, not Page A). Live
edit:
**`cmd=0x6E`**, param **`0x01`**. **`stored = <value>`** (wire byte). Hardware
TX
confirmed (**`01`–`03`** stepped; **`00`** Off). First active algorithm is
**`01`**
(not **`00`**), same pattern as [Delay Mode](#delay-mode).

| `<value>` | Option     | Meaning                                          |
| --------- | ---------- | ------------------------------------------------ |
| `00`      | Off        | No reverb; other rows **hidden**                 |
| `01`      | Reverb     | Standard reverb + [Predelay](#reverb-predelay)   |
| `02`      | Feedback 1 | Feedback in predelay line → multiple tails       |
| `03`      | Feedback 2 | Like Feedback 1; first tail **immediate**        |

---

## Reverb Type

**Edit FX → Reverb → Type** — room / early-reflection character (**Ambience** …
**Hall**). Visible when **Mode** is **Reverb** or **Feedback 1/2** (not **Mode**
**Off**). Changing **Type** does not hide other rows. Live edit: **`cmd=0x6E`**,
param **`0x03`**. **`stored = <value>`** (wire byte).

```text
F0 00 20 33 01 00 6E 00 03 00 F7 # Ambience (Part 1)
```

| `<value>` | Option     |
| --------- | ---------- |
| `00`      | Ambience   |
| `01`      | Small Room |
| `02`      | Large Room |
| `03`      | Hall       |

---

## Reverb panel visibility

**Edit FX → Reverb**. Panel visibility follows [Delay panel visibility](#delay-panel-visibility).

### Mode = Off (`00`)

**Mode** and **[Send](#reverb-send-lcd)** only — algorithm rows **hidden**.

### Send = Off (`00` on Send control)

When **Mode** is **Reverb** or **Feedback 1/2**, **Send** = **Off** does **not**
hide **Type**, **Clock**, **Time**, **Damping**, **Coloration**, or **Predelay**
(on panel). Unlike **Delay**, where **Send** = **Off** leaves only
**Type**, **Send**, and **Feedback**.

### Mode = Reverb (`01`), Feedback 1 (`02`), or Feedback 2 (`03`)

Shared rows for all three **Modes** (on panel). **Feedback 2** shows
the
**same** controls as **Feedback 1** (only the algorithm differs — first tail
**immediate** on **Feedback 2**).

| Control        | Visible                  | Notes                                                                            |
| -------------- | ------------------------ | -------------------------------------------------------------------------------- |
| **Mode**       | Yes                      | [Reverb Mode](#reverb-mode)                                                      |
| **Send**       | Yes                      | [Reverb Send (LCD)](#reverb-send-lcd)                                            |
| **Type**       | Yes                      | [Reverb Type](#reverb-type) — room **Type** does not hide other rows             |
| **Clock**      | Yes                      | [Reverb Clock](#reverb-clock)                                                    |
| **Time**       | Yes                      | [Reverb Time](#reverb-time) — **0..127**                                         |
| **Damping**    | Yes                      | [Reverb Damping](#reverb-damping) — **0.0..100.0 %**                             |
| **Coloration** | Yes                      | [Reverb Coloration](#reverb-coloration) — **−64..+63**                           |
| **Predelay**   | **Clock** = **Off** only | [Reverb Predelay](#reverb-predelay) — **0.0..500.0 ms**                          |
| **Feedback**   | **Feedback 1/2 only**    | [Reverb Feedback](#reverb-feedback) — **0..127**; **not** on **Reverb** (`01`)   |

When **Clock** is a tempo division (**not** **Off**), **Predelay** is
**hidden**.
When **Clock** = **Off**, **Predelay** is on the panel.

**Signal path:** delay → reverb in series (dry + delay → reverb input) — TI
reference.

---

## Reverb Clock

**Edit FX → Reverb → Clock**. Synchronizes **[Predelay](#reverb-predelay)** to
the
tempo grid. Live edit: **`cmd=0x6E`**, param **`0x08`**. **`stored = <value>`**
(wire byte). **Same wire map** as [Delay Clock](#delay-clock) (`71`/`14` on Page **B**);
Reverb
uses the **part buffer** (`6E`) instead.

| `<value>` | Option           |
| --------- | ---------------- |
| `00`      | Off ✓ (capture)  |
| `01`      | 1/64 ✓ (capture) |
| `02`      | 1/32             |
| `0B`      | 1/24             |
| `07`      | 3/64             |
| `03`      | 1/16             |
| `0C`      | 1/12             |
| `08`      | 3/32             |
| `04`      | 1/8              |
| `0D`      | 1/6              |
| `09`      | 3/16             |
| `05`      | 1/4              |
| `0E`      | 1/3              |
| `0A`      | 3/8              |
| `06`      | 1/2              |
| `0F`      | 2/3              |
| `10`      | 3/4 ✓ (capture)  |

Valid wire values **`00`–`10`** (same as Delay Clock). **`11`–`7F`** not in
menu.

```text
F0 00 20 33 01 00 6E 00 08 00 F7 # Off
F0 00 20 33 01 00 6E 00 08 10 F7 # 3/4
```

---

## Reverb Time

**Edit FX → Reverb → Time**. Tail
length **0..127** on the panel. Live edit: **`cmd=0x6E`**, param **`0x04`**.
**`stored = lcd`** (direct wire byte).
**`00`–`7F`**).
Mod-matrix **Reverb Time** id **`0x1C`** ≠ live-edit param byte.

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 6E 00 04 00 F7 # 0
F0 00 20 33 01 00 6E 00 04 44 F7 # 68 (panel anchor)
F0 00 20 33 01 00 6E 00 04 7F F7 # 127
```

---

## Reverb Damping

**Edit FX → Reverb → Damping**. Panel **0.0..100.0 %**.
Live edit: **`cmd=0x6E`**, param **`0x05`**.

```text
stored = round(pct × 127 / 100)
```

Mod-matrix **Reverb Dampening** id
**`0x65`** ≠ live-edit param byte.

| LCD     | `<value>` |
| ------- | --------- |
| 0.0 %   | `00`      |
| 15.6 %  | `14`      |
| 100.0 % | `7F`      |

```text
F0 00 20 33 01 00 6E 00 05 00 F7 # 0.0 %
F0 00 20 33 01 00 6E 00 05 7F F7 # 100.0 %
```

---

## Reverb Coloration

**Edit FX → Reverb → Coloration**. Post-EQ **−64..+63**.
Live edit: **`cmd=0x6E`**, param **`0x06`**.

```text
stored = ui + 64
ui = stored − 64
```

Mod-matrix
**Reverb
Coloration** id **`0x66`** ≠ live-edit param byte (Delay
[Coloration](#delay-coloration) uses **`70`/`77`** on Classic).

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| +0  | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 6E 00 06 00 F7 # −64
F0 00 20 33 01 00 6E 00 06 40 F7 # +0
F0 00 20 33 01 00 6E 00 06 7F F7 # +63
```

---

## Reverb Predelay

**Edit FX → Reverb → Predelay**. **0.0..500.0 ms** on the panel when
**[Clock](#reverb-clock)** = **Off** (**300.4 ms** max
—
mk2 panel reaches **500.0 ms**). Also used as the repeat period for **Feedback
1/2**. Live edit: **`cmd=0x6E`**, param **`0x07`**. **`stored = lcd`** (wire
byte
**`00`–`5C`** only — **`5D`–`7F`** not used).

```text
lcd_ms ≈ stored × 500.0 / 92 # 92 = 0x5C (panel max wire)
```

0** → **500.0** ms; max wire **`5C`**).

| LCD (ms) | `<value>` |
| -------- | --------- |
| 0.0      | `00`      |
| 174.8    | `20`      |
| 349.5    | `40`      |
| 500.0    | `5C`      |

```text
F0 00 20 33 01 00 6E 00 07 00 F7 # 0.0 ms
F0 00 20 33 01 00 6E 00 07 20 F7 # 174.8 ms
F0 00 20 33 01 00 6E 00 07 40 F7 # 349.5 ms
F0 00 20 33 01 00 6E 00 07 5C F7 # 500.0 ms
```

---

## Reverb Feedback

**Edit FX → Reverb → Feedback**. **0..127** on the panel. Visible only when
**Mode** = **Feedback 1** (`02`) or **Feedback 2** (`03`) — same panel on both.
Live edit: **`cmd=0x6E`**, param **`0x09`**. **`stored = lcd`** (direct wire
byte
**`00`–`7F`**). Mod-matrix **Reverb Feedback** id **`0x67`** ≠ live-edit param byte.

| LCD | `<value>` |
| --- | --------- |
| 0   | `00`      |
| 127 | `7F`      |

```text
F0 00 20 33 01 00 6E 00 09 00 F7 # 0
F0 00 20 33 01 00 6E 00 09 7F F7 # 127
```

---

## Reverb Send (LCD)

**Edit FX → Reverb → Send**. Live edit **`cmd=0x6E`**, param **`0x02`** — see
[effects.md](../live-edit/single/effects.md#reverb-send).

**Same LCD ↔ wire map as [Delay Send](#delay-send-lcd)** — **`stored = index`**
(`00`–`7F`), direct wire byte. Only the live-edit address differs (**`6E`/`02`**
vs Delay **`70`/`71`**).

Panel-confirmed (Reverb path, **`02`/value** captures):

| `<value>` | LCD        |     |
| --------- | ---------- | --- |
| `00`      | Off        | ✓   |
| `01`      | −46.2 dB   | ✓   |
| `02`      | −40.2 dB   | ✓   |
| `03`      | −36.6 dB   | ✓   |
| `3A`      | −9.5 dB    | ✓   |
| `3D`      | −8.75 dB   | ✓   |
| `3E`      | −8.5 dB    | ✓   |
| `3F`      | −8.25 dB   | ✓   |
| `40`      | −8.0 dB    | ✓   |
| `41`      | −7.75 dB   | ✓   |
| `50`      | −4.0 dB    | ✓   |
| `5F`      | −0.25 dB   | ✓   |
| `60`      | 0/0 dB     | ✓   |
| `61`      | 0/−0.3 dB  | ✓   |
| `62`      | 0/−0.6 dB  | ✓   |
| `63`      | 0/−0.9 dB  | ✓   |
| `64`      | 0/−1.2 dB  | ✓   |
| `70`      | 0/−6.0 dB  | ✓   |
| `7A`      | 0/−14.5 dB | ✓   |
| `7E`      | 0/−24.0 dB | ✓   |
| `7F`      | Effect     | ✓   |

Full index table and region rules: [Delay Send (LCD)](#delay-send-lcd).

---

## EQ Low Frequency

**Edit FX → Low EQ → Frequency (Hz)**. Page **B#45** = **`0x2D`**. Live edit
**`cmd=0x71`**, param **`0x2D`** — see
[effects.md](../live-edit/single/effects.md#eq-low-frequency).

Log-spaced **32..458 Hz** (**`stored` ≠ Hz**). Panel shows integer **Hz**.
Adjacent wire bytes often share the same LCD label (duplicate detents).

Approximate fit between endpoints (interior steps use LCD rounding):

```text
freq_hz ≈ 32 × (458 / 32)^(stored / 127)
```

| `<value>` | LCD (Hz) |     | `<value>` | LCD (Hz) |     |
| --------- | -------- | --- | --------- | -------- | --- |
| `00`      | 32       | ✓   | `01`      | 32       | ✓   |
| `02`      | 33       | ✓   | `03`      | 33       | ✓   |
| `04`      | 35       | ✓   | `05`      | 35       | ✓   |
| `06`      | 36       | ✓   | `07`      | 36       | ✓   |
| `08`      | 38       | ✓   | `09`      | 38       | ✓   |
| `0A`      | 40       | ✓   | `0B`      | 40       | ✓   |
| `0C`      | 41       | ✓   | `0D`      | 41       | ✓   |
| `0E`      | 43       | ✓   | `0F`      | 43       | ✓   |
| `10`      | 45       | ✓   | `11`      | 45       | ✓   |
| `12`      | 47       | ✓   | `13`      | 47       | ✓   |
| `14`      | 49       | ✓   |           |          |     |
| `79`      | 404      | ✓   | `7A`      | 421      | ✓   |
| `7B`      | 421      | ✓   | `7C`      | 439      | ✓   |
| `7D`      | 439      | ✓   | `7E`      | 458      | ✓   |
| `7F`      | 458      | ✓   |           |          |     |

**Not** Page A **Filter 2 Envelope Amount** (`70`/`2D`).

---

## EQ Low Gain

**Edit FX → Low EQ → Gain**. Page **B#95** = **`0x5F`**. Live edit
**`cmd=0x71`**, param **`0x5F`** — see
[effects.md](../live-edit/single/effects.md#eq-low-gain).

Symmetric dB range with **Off** (0 dB) at wire center **`40`**:

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

Approximate mapping: **`gain_db ≈ (stored − 64) × 16 / 63`** (64 = **`0x40`**).

**Not** [Reverb Send](reverb-send-lcd) index **`0x5F`** (−0.25 dB row). **Not**
Page A **Filter 2 Envelope Amount** (`70`/`2D`).

---

## EQ Mid Frequency

**Edit FX → Mid EQ → Frequency (Hz)**. Page **B#93** = **`0x5D`**. Live edit
**`cmd=0x71`**, param **`0x5D`** — see
[effects.md](../live-edit/single/effects.md#eq-mid-frequency).

Log-spaced **19 Hz..24.0 kHz** (**`stored` ≠ Hz**). Below **`~0x70`**, panel
shows **Hz** (integer). From **`0x70`** upward, panel shows **kHz** (one decimal).

Approximate fit (interior steps use LCD rounding):

```text
freq_hz ≈ 19 × (24000 / 19)^(stored / 127)
```

| `<value>` | LCD  | Unit |     |
| --------- | ---- | ---- | --- |
| `00`      | 19   | Hz   | ✓   |
| `01`      | 20   | Hz   | ✓   |
| `10`      | 48   | Hz   | ✓   |
| `20`      | 118  | Hz   | ✓   |
| `30`      | 288  | Hz   | ✓   |
| `40`      | 707  | Hz   | ✓   |
| `50`      | 1731 | Hz   | ✓   |
| `60`      | 4238 | Hz   | ✓   |
| `6F`      | 9810 | Hz   | ✓   |
| `70`      | 10.3 | kHz  | ✓   |
| `71`      | 11.6 | kHz  | ✓   |
| `72`      | 12.2 | kHz  | ✓   |
| `73`      | 12.9 | kHz  | ✓   |
| `74`      | 13.7 | kHz  | ✓   |
| `75`      | 14.5 | kHz  | ✓   |
| `76`      | 15.3 | kHz  | ✓   |
| `77`      | 16.2 | kHz  | ✓   |
| `78`      | 17.1 | kHz  | ✓   |
| `7C`      | 21.4 | kHz  | ✓   |
| `7F`      | 24.0 | kHz  | ✓   |

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid
Frequency**
(wire **`71`** in **`71`/`3E`**, not param **`5D`**).

---

## EQ Mid Gain

**Edit FX → Mid EQ → Gain**. Page **B#92** = **`0x5C`**. Live edit
**`cmd=0x71`**, param **`0x5C`** — see
[effects.md](../live-edit/single/effects.md#eq-mid-gain).

Same symmetric dB encoding as [EQ Low Gain](#eq-low-gain) (**`40`** = Off):

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid Gain**
(wire **`70`** in **`71`/`3E`**, not param **`5C`**).

---

## EQ Mid Q-Factor

**Edit FX → Mid EQ → Q-Factor**. Page **B#94** = **`0x5E`**. Live edit
**`cmd=0x71`**, param **`0x5E`** — see
[effects.md](../live-edit/single/effects.md#eq-mid-q-factor).

Log-spaced **Q** between endpoints **`00`** = **0.28** and **`7F`** = **15.4**.
Panel shows **one decimal**. Approximate fit (interior steps use LCD rounding):

```text
Q ≈ 0.28 × (15.4 / 0.28)^(stored / 127)
```

| `<value>` | LCD (Q) |     |
| --------- | ------- | --- |
| `00`      | 0.28    | ✓   |
| `10`      | 0.45    | ✓   |
| `20`      | 0.71    | ✓   |
| `40`      | 1.58    | ✓   |
| `50`      | 2.82    | ✓   |
| `60`      | 5.01    | ✓   |
| `70`      | 8.91    | ✓   |
| `7E`      | 14.9    | ✓   |
| `7F`      | 15.4    | ✓   |

**Not** [Soft Knob Destinations](#soft-knob-destinations) row **EQ Mid
Q-Factor**
(wire **`72`** in **`71`/`3E`**, not param **`5E`**).

---

## EQ High Frequency

**Edit FX → High EQ → Frequency (Hz)**. Page **B#46** = **`0x2E`**. Live edit
**`cmd=0x71`**, param **`0x2E`** — see
[effects.md](../live-edit/single/effects.md#eq-high-frequency).

Log-spaced **1831 Hz..24.0 kHz** (**`stored` ≠ Hz**). Panel shows integer **Hz**
through most of the range; maximum **`7F`** shows **24.0 kHz**. Adjacent wire
bytes often share the same LCD label (duplicate detents).

Approximate fit between endpoints (interior steps use LCD rounding):

```text
freq_hz ≈ 1831 × (24000 / 1831)^(stored / 127)
```

| `<value>` | LCD (Hz) |     | `<value>` | LCD (Hz) |     |
| --------- | -------- | --- | --------- | -------- | --- |
| `00`      | 1831     | ✓   | `0C`      | 2355     | ✓   |
| `0D`      | 2355     | ✓   | `0E`      | 2456     | ✓   |
| `1F`      | 3436     | ✓   | `3B`      | 6183     | ✓   |
| `3C`      | 6448     | ✓   | `3D`      | 6448     | ✓   |
| `3E`      | 6724     | ✓   | `3F`      | 6724     | ✓   |
| `40`      | 7012     | ✓   | `7F`      | 24.0 kHz | ✓   |

**Not** Page A **Filter 1 Keyfollow** (`70`/`2E`).

---

## EQ High Gain

**Edit FX → High EQ → Gain**. Page **B#96** = **`0x60`**. Live edit
**`cmd=0x71`**, param **`0x60`** — see
[effects.md](../live-edit/single/effects.md#eq-high-gain).

Same symmetric dB encoding as [EQ Low Gain](#eq-low-gain) (**`40`** = Off):

| `<value>` | LCD    | Notes  |
| --------- | ------ | ------ |
| `00`      | −16 dB | min ✓  |
| `40`      | Off    | 0 dB ✓ |
| `7F`      | +16 dB | max ✓  |

---

## Oscillators SELECT

**OSCILLATORS** section — front-panel **SELECT** cycles **Oscillator 1** /
**Oscillator 2** / **Oscillator 3**. Live edit **`cmd=0x71`**, param **`0x7F`**
(Page B). **`stored = index`**.

| Index | `<value>` | Panel focus  |
| ----- | --------- | ------------ |
| 0     | `00`      | Oscillator 1 |
| 1     | `01`      | Oscillator 2 |
| 2     | `02`      | Oscillator 3 |

See [oscillators.md — SELECT](../live-edit/single/oscillators.md#select-717f).

Same **`71`/`7F`** wire as [Oscillator Section
Volume](../live-edit/single/oscillators.md#oscillator-section-volume)
— **SELECT** = index **`00`–`02`**; **Mixer volume** = bipolar
**`stored = ui + 64`**.

---

## Filters SELECT

**FILTERS** section — **SELECT** toggles **Filter 1** / **Filter 2** (press
both together for **Filter 1 + Filter 2**). Live edit **`cmd=0x71`**, param
**`0x7A`**. **`stored = index`**.

| Index | `<value>` | Panel focus         |
| ----- | --------- | ------------------- |
| 0     | `00`      | Filter 1            |
| 1     | `01`      | Filter 2            |
| 2     | `02`      | Filter 1 + Filter 2 |

See [filters.md — SELECT](../live-edit/single/filters.md#filters-select).

**Not** [Pan Spread](../live-edit/single/filters.md#pan-spread)
(`6E`/`7A` — same param byte, different **`cmd`**).

When [Vocoder Mode](vocoder-mode) ≠ **Off**, the **FILTERS** section is
unavailable — LCD shows **`Vocoder active. Filters are disabled`**. **Spread** and
**Q-Factor** reuse [Filter 1 Keyfollow](../live-edit/single/filters.md#filter-1-keyfollow)
/ [Filter 1 Resonance](../live-edit/single/filters.md#filter-1-resonance)
storage (**`70`/`2E`**, **`70`/`2A`**).

---

## EFFECTS SELECT group 1

Live edit **`cmd=0x6E`**, param **`0x75`** — see
[effects.md — SELECT](../live-edit/single/effects.md#select-6e75-6e76).
**`stored = index`**.

| Index | `<value>` | Label   |
| ----- | --------- | ------- |
| 0     | `00`      | Delay   |
| 1     | `01`      | Reverb  |
| 2     | `02`      | Low EQ  |
| 3     | `03`      | Mid EQ  |
| 4     | `04`      | High EQ |

Sets which **EFFECTS** section focus target the physical panel uses. Parameter
values are the live-edit bytes in [effects.md](../live-edit/single/effects.md) — not
documented here as knob routing.

---

## EFFECTS SELECT group 2

**EFFECTS** section — second **SELECT** group. Live edit **`cmd=0x6E`**, param
**`0x76`** — see
[effects.md — SELECT](../live-edit/single/effects.md#select-6e75-6e76).
**`stored = index`**.

| Index | `<value>` | Label      |
| ----- | --------- | ---------- |
| 0     | `00`      | Distortion |
| 1     | `01`      | Character  |
| 2     | `02`      | Chorus     |
| 3     | `03`      | Phaser     |
| 4     | `04`      | Others     |

Sets which **EFFECTS** section focus target the physical panel uses. Parameter
values are the live-edit bytes in [effects.md](../live-edit/single/effects.md) — not
documented here as knob routing.

**Others (`04`)** — **EDIT FX** then sub-menu (panel order):

1. **Filter Bank**
2. **Vocoder**
3. **Input Follower**

Stepping **Filter Bank** ↔ **Vocoder** ↔ **Input Follower** does **not** transmit
SysEx — LCD / menu navigation only. Effect focus remains **`6E`/`76`/`04`**
([EFFECTS focus group 2](#effects-select-group-2)). **Filter Bank → Type** uses
**`6E`/`13`** — [Filter Bank Type](#filter-bank-type). **Vocoder** /
**Input Follower** — see [Vocoder Mode](#vocoder-mode) / [Input Follower Input
Select](#input-follower-input-select).

**Not** [Delay LFO Wave](#delay-lfo-wave) (`70`/`76`). **Not** global Memory
Protect
(`73`/`76`).

---

## Character Type

**EDIT FX → Character → Type**. Live edit **`cmd=0x6E`**, param **`0x1A`** (part
single buffer) — see
[effects.md — Character Type](../live-edit/single/effects.md#character-type).
**`stored = <value>`** (dense **`00`–`08`**).
step-through after **`6E`/`76`/`01`** focus).

| `<value>` | Option          |
| --------- | --------------- |
| `00`      | Analog Boost    |
| `01`      | Vintage 1       |
| `02`      | Vintage 2       |
| `03`      | Vintage 3       |
| `04`      | Pad Opener      |
| `05`      | Lead Enhancer   |
| `06`      | Bass Enhancer   |
| `07`      | Stereo Widener  |
| `08`      | Speaker Cabinet |

Panel rows per **Type**: [Character panel
visibility](#character-panel-visibility).

---

## Character panel visibility

**EDIT FX → Character**. Which controls appear depends on [Character
Type](#character-type). Live-edit **`cmd`/`param`** per row — see
[effects.md — Character](../live-edit/single/effects.md#character).

### Analog Boost (`00`)

| Control       | Visible | `cmd`/`param` | Notes                                                                |
| ------------- | ------- | ------------- | -------------------------------------------------------------------- |
| **Type**      | Yes     | `6E`/`1A`     | [Character Type](#character-type)                                    |
| **Intensity** | Yes     | `70`/`15`     | [Character Intensity (LCD)](#character-intensity-lcd) — **`00`** Off |
| **Frequency** | Yes     | `70`/`21`     | **`0`–`127`** direct                                                 |

### Preset types (`01`–`06`)

**Vintage 1**, **Vintage 2**, **Vintage 3**, **Pad Opener**, **Lead Enhancer**,
**Bass Enhancer** . Selecting one of these types
applies a fixed character preset; there are **no** further **EDIT FX** menu
rows — only [`6E`/`1A`](#character-type) SysEx when changing **Type**. Dump: only
**`0x123`** changes (`stored = type index **`00`–`06`**).

| Control  | Visible | Notes                               |
| -------- | ------- | ----------------------------------- |
| **Type** | Yes     | [`6E`/`1A`](#character-type) only   |

### Stereo Widener (`07`) / Speaker Cabinet (`08`)

**Stereo Widener** and **Speaker Cabinet** share the same **EDIT FX** rows and
live-edit **`cmd`/`param`** IDs (panel- and capture-confirmed).

| Control       | Visible | `cmd`/`param` | Notes                                                                |
| ------------- | ------- | ------------- | -------------------------------------------------------------------- |
| **Type**      | Yes     | `6E`/`1A`     | [Character Type](#character-type)                                    |
| **Intensity** | Yes     | `71`/`61`     | [Character Intensity (LCD)](#character-intensity-lcd) — **`00`** Off |
| **Frequency** | Yes     | `71`/`62`     | **`0`–`127`** direct                                                 |

---

## Character Intensity (LCD)

**EDIT FX → Character → Intensity** when [Type](#character-type) = **Analog
Boost** (`00`), **Stereo Widener** (`07`), or **Speaker Cabinet** (`08`). Same
LCD curve on all three; live-edit **`cmd`/`param`** is **type-dependent** — see
[effects.md — Character Intensity](../live-edit/single/effects.md#character-intensity--analog-boost).

| Type                             | `cmd`/`param` |
| -------------------------------- | ------------- |
| Analog Boost                     | `70`/`15`     |
| Stereo Widener / Speaker Cabinet | `71`/`61`     |

Modulation destination **Analog Boost Int** (soft-knob wire **`55`**) — name
predates **Character** menu label; applies to **Analog Boost** intensity wire.

**`stored = wire byte`** (`00`–`7F`). **`00`** = **Off**; **`01`–`7F`** show
panel **%** (one decimal). Confirmed anchors; interior steps follow
**`pct ≈ stored × 100 / 127`** (LCD rounding).

| `<value>` | LCD     |     |
| --------- | ------- | --- |
| `00`      | Off     | ✓   |
| `01`      | 0.8 %   | ✓   |
| `02`      | 1.6 %   | ✓   |
| `03`      | 2.3 %   | ✓   |
| `40`      | 50.4 %  | ≈   |
| `7F`      | 100.0 % | ✓   |

---

## Chorus Type

**EDIT FX → Chorus → Type**. Live edit **`cmd=0x70`**, param **`0x67`** (Page
A) — see [effects.md — Chorus Type](../live-edit/single/effects.md#chorus-type).

| `<value>` | Option         |
| --------- | -------------- |
| `01`      | Classic        |
| `02`      | Vintage        |
| `03`      | Hyper Chorus   |
| `04`      | Air Chorus     |
| `05`      | Vibrato        |
| `06`      | Rotary Speaker |

---

## Chorus panel visibility

**EDIT FX → Chorus**. Rows depend on [Chorus Type](#chorus-type) — see
[effects.md — Chorus](../live-edit/single/effects.md#chorus).

### Classic (`01`)

| Control      | Visible | `cmd`/`param` | Notes                                                            |
| ------------ | ------- | ------------- | ---------------------------------------------------------------- |
| **Type**     | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)                                      |
| **Rate**     | Yes     | `70`/`6A`     | **`0`–`127`** direct                                             |
| **Depth**    | Yes     | `70`/`6B`     | **0.0..100.0 %**                                                 |
| **Feedback** | Yes     | `70`/`6D`     | **−100.0..+100.0 %** — **`stored = round(pct × 64 / 100) + 64`** |
| **Delay**    | Yes     | `70`/`6C`     | **`0`–`127`** direct                                             |
| **Mix**      | Yes     | `70`/`69`     | **`00`** Off; **`01`–`7F`** wet level (**1..127**)               |
| **LFO Wave** | Yes     | `70`/`6E`     | [Chorus LFO Wave](#chorus-lfo-wave)                              |

### Vintage (`02`)

| Control    | Visible | `cmd`/`param` | Notes                                   |
| ---------- | ------- | ------------- | --------------------------------------- |
| **Type**   | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)             |
| **Rate**   | Yes     | `70`/`6A`     | **`0`–`127`** — same byte as Classic    |
| **Depth**  | Yes     | `70`/`6B`     | **0.0..100.0 %** — same byte as Classic |
| **Mix**    | Yes     | `70`/`68`     | **`0`–`127`** direct                    |
| **X-Over** | Yes     | `70`/`6F`     | **`0`–`127`** direct                    |

### Hyper Chorus (`03`)

| Control    | Visible | `cmd`/`param` | Notes                                                                             |
| ---------- | ------- | ------------- | --------------------------------------------------------------------------------- |
| **Type**   | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)                                                       |
| **Depth**  | Yes     | `70`/`6B`     | **0.0..100.0 %**                                                                  |
| **Amount** | Yes     | `70`/`6C`     | **1.00..3.00** — [Chorus Amount (LCD)](#chorus-amount-lcd); not Classic **Delay** |
| **Mix**    | Yes     | `70`/`68`     | **`0`–`127`** direct                                                              |
| **X-Over** | Yes     | `70`/`6F`     | **`0`–`127`** direct                                                              |

### Air Chorus (`04`)

| Control    | Visible | `cmd`/`param` | Notes                         |
| ---------- | ------- | ------------- | ----------------------------- |
| **Type**   | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)   |
| **Depth**  | Yes     | `70`/`6B`     | **0.0..100.0 %**              |
| **X-Over** | Yes     | `70`/`6F`     | **`0`–`127`** direct          |

### Vibrato (`05`)

| Control    | Visible | `cmd`/`param` | Notes                                    |
| ---------- | ------- | ------------- | ---------------------------------------- |
| **Type**   | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)              |
| **Rate**   | Yes     | `70`/`6A`     | **`0`–`127`** direct                     |
| **Depth**  | Yes     | `70`/`6B`     | **`0`–`127`** direct — not Classic **%** |
| **X-Over** | Yes     | `70`/`6F`     | **`0`–`127`** direct                     |

### Rotary Speaker (`06`)

| Control              | Visible | `cmd`/`param` | Notes                                                                                                             |
| -------------------- | ------- | ------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Type**             | Yes     | `70`/`67`     | [Chorus Type](#chorus-type)                                                                                       |
| **Speed**            | Yes     | `70`/`6A`     | [Chorus Rotary Speed](#chorus-rotary-speed)                                                                       |
| **Distance**         | Yes     | `70`/`6B`     | [Chorus Rotary Distance (LCD)](#chorus-rotary-distance-lcd)                                                       |
| **Mix**              | Yes     | `70`/`68`     | **`0`–`127`** — [Vintage / Hyper / Rotary Mix](../live-edit/single/effects.md#chorus-mix--vintage--hyper--rotary) |
| **Mic Angle**        | Yes     | `70`/`6C`     | [Chorus Rotary Mic Angle (LCD)](#chorus-rotary-mic-angle-lcd)                                                     |
| **Low/High Balance** | Yes     | `70`/`6D`     | [Chorus Rotary Low/High Balance (LCD)](#chorus-rotary-lowhigh-balance-lcd)                                        |

---

## Chorus Rotary Speed

**EDIT FX → Chorus → Speed** when [Type](#chorus-type) = **Rotary Speaker**
(`06`). Live edit **`cmd=0x70`**, param **`0x6A`** — same byte as **Rate** on
other types.

| `<value>` | LCD  |     |
| --------- | ---- | --- |
| `00`      | Slow | ✓   |
| `7F`      | Fast | ✓   |

Interior positions: wire index **`01`–`7E`** (no discrete
enum).

---

## Chorus Rotary Distance (LCD)

**EDIT FX → Chorus → Distance** when [Type](#chorus-type) = **Rotary Speaker**
(`06`). Live edit **`cmd=0x70`**, param **`0x6B`** — same byte as **Depth** on
other types.

**`stored = wire byte`** (`00`–`7F`). Panel shows **one decimal** (**cm**).

| `<value>` | LCD     |     |
| --------- | ------- | --- |
| `00`      | 4.0 cm  | ✓   |
| `10`      | 6.0 cm  | ✓   |
| `29`      | 9.1 cm  | ✓   |
| `40`      | 12.0 cm | ✓   |
| `5A`      | 17.5 cm | ✓   |
| `7F`      | 30.0 cm | ✓   |

Init patch default **6.0 cm** @ wire **`10`**.

---

## Chorus Rotary Mic Angle (LCD)

**EDIT FX → Chorus → Mic Angle** when [Type](#chorus-type) = **Rotary Speaker**
(`06`). Live edit **`cmd=0x70`**, param **`0x6C`** — same byte as **Delay**
(Classic) and **Amount** (Hyper); decode with **`70`/`67`**.

Bipolar **degrees**. Center **`40`** = **+0°**; endpoints **`00`** = **−180°**,
**`7F`** = **+180°**.

```text
ui_deg = (stored − 64) × 180 / 64
stored = round(deg × 64 / 180) + 64
```

| `<value>` | LCD   |     |
| --------- | ----- | --- |
| `00`      | −180° | ✓   |
| `40`      | +0°   | ✓   |
| `7F`      | +180° | ✓   |

---

## Chorus Rotary Low/High Balance (LCD)

**EDIT FX → Chorus → LowHigh Bal** when [Type](#chorus-type) = **Rotary
Speaker** (`06`). Live edit **`cmd=0x70`**, param **`0x6D`** — same byte as
**Feedback** (Classic); decode with **`70`/`67`**.

Bipolar **percent** (one decimal). Same encoding as [Classic Chorus
Feedback](../live-edit/single/effects.md#chorus-feedback) — **`40`** =
**+0.0 %**.

```text
stored = round(pct × 64 / 100) + 64
pct = (stored − 64) × 100 / 64
```

| `<value>` | LCD      |     |
| --------- | -------- | --- |
| `00`      | −100.0 % | ✓   |
| `40`      | +0.0 %   | ✓   |
| `7F`      | +100.0 % | ✓   |

---

## Chorus Amount (LCD)

**EDIT FX → Chorus → Amount** when [Type](#chorus-type) = **Hyper Chorus** (`03`).
On **Rotary Speaker** (`06`), the same param byte is **Mic Angle** — see
[Chorus Rotary Mic Angle (LCD)](#chorus-rotary-mic-angle-lcd). Live edit
**`cmd=0x70`**, param **`0x6C`** (Page A). **Not** [Classic
Delay](../live-edit/single/effects.md#chorus-delay--classic) on the same param
byte.

**`stored = wire byte`** (`00`–`7F`). Panel shows **two decimal places**:

```text
amount = 1.00 + stored × (2.00 / 127)
```

| `<value>` | LCD   |     |
| --------- | ----- | --- |
| `00`      | 1.00  | ✓   |
| `40`      | ≈2.00 | ≈   |
| `7F`      | 3.00  | ✓   |

---

## Chorus LFO Wave

**EDIT FX → Chorus → LFO Wave** (**Classic**). Live edit **`cmd=0x70`**, param
**`0x6E`** (Page A). Same wire map as [Delay LFO Wave](#delay-lfo-wave)
(**`00`–`05`**).

| `<value>` | Option   |
| --------- | -------- |
| `00`      | Sine     |
| `01`      | Triangle |
| `02`      | Sawtooth |
| `03`      | Square   |
| `04`      | S&H      |
| `05`      | S&G      |

**Not** EFFECTS focus group 2 (`6E`/`76`). **Not** [Delay LFO Wave](#delay-lfo-wave)
param (**`76`** on **`70`**).

---

## Phaser panel visibility

**EDIT FX → Phaser**. Live edit **`cmd=0x71`** (Page **B**) — see
[effects.md — Phaser](../live-edit/single/effects.md#phaser).

**Mix** = **`00`** (**Off**): **Mix** only. **Mix** ≥ **`01`**: full row set below
.

| Control       | Visible (Mix = Off) | Visible (Mix ≥ `01`) | `cmd`/`param` | Notes                                                                                                     |
| ------------- | ------------------- | -------------------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| **Mix**       | Yes                 | Yes                  | `71`/`55`     | [Phaser Mix (LCD)](#phaser-mix-lcd)                                                                       |
| **Frequency** | No                  | Yes                  | `71`/`58`     | **`0`–`127`** direct                                                                                      |
| **Feedback**  | No                  | Yes                  | `71`/`59`     | **−100.0..+100.0 %** — same as [Chorus Feedback](../live-edit/single/effects.md#chorus-feedback)          |
| **Mod Rate**  | No                  | Yes                  | `71`/`56`     | **`0`–`127`** direct                                                                                      |
| **Mod Depth** | No                  | Yes                  | `71`/`57`     | **`0`–`127`** direct                                                                                      |
| **Stages**    | No                  | Yes                  | `71`/`54`     | [Phaser Stages](#phaser-stages)                                                                           |
| **Spread**    | No                  | Yes                  | `71`/`5A`     | **`0`–`127`** direct                                                                                      |

---

## Phaser Mix (LCD)

**EDIT FX → Phaser → Mix**. Live edit **`cmd=0x71`**, param **`0x55`** (Page
**B**). Modulation destination **Phaser Mix** (soft-knob wire **`5E`** — different
byte).

**`stored = wire byte`** (`00`–`7F`). **`00`** = **Off**; **`01`–`7F`** show
panel level **1..127** (LCD numeric).

| `<value>` | LCD |     |
| --------- | --- | --- |
| `00`      | Off | ✓   |
| `01`      | 1   | ✓   |
| `40`      | 64  | ✓   |
| `7F`      | 127 | ✓   |

---

## Phaser Stages

**EDIT FX → Phaser → Stages** (when [Mix](#phaser-mix-lcd) ≠ **Off**). Live edit
**`cmd=0x71`**, param **`0x54`**. **`stored = <value>`** (dense **`00`–`05`**).

| `<value>` | Option   |
| --------- | -------- |
| `00`      | 1 Stage  |
| `01`      | 2 Stages |
| `02`      | 3 Stages |
| `03`      | 4 Stages |
| `04`      | 5 Stages |
| `05`      | 6 Stages |

Panel-confirmed (step **`00`–`05`** after **Mix** ≠ **Off**).

---

## Others Type

**EDIT FX → Others** sub-pages (after **EFFECTS** group **2** =
**Others** — [`6E`/`76`/`04`](#effects-select-group-2)). Panel order:

| Menu order | Option             | SysEx on page change | Notes                                                          |
| ---------- | ------------------ | -------------------- | -------------------------------------------------------------- |
| 1          | **Filter Bank**    | **No**               | [Filter Bank Type](#filter-bank-type) — **`6E`/`13`**          |
| 2          | **Vocoder**        | **No**               | [Vocoder Mode](#vocoder-mode) — **`71`/`27`**                  |
| 3          | **Input Follower** | **No**               | [Input Select](#input-follower-input-select) — **`71`/`26`**   |

Paging among **Filter Bank**, **Vocoder**, and **Input Follower** sends **no**
live-edit SysEx. Parameter edits (e.g. **Filter Bank → Type**) do.

---

## Others panel visibility

**EDIT FX → Others**. Top-level sub-pages — [Others Type](#others-type) (no
SysEx when paging). Parameter rows per sub-page:

| Sub-page           | Panel-confirmed | Live edit                                                           |
| ------------------ | --------------- | ------------------------------------------------------------------- |
| **Filter Bank**    |                 | [Filter Bank panel visibility](#filter-bank-panel-visibility)       |
| **Vocoder**        |                 | [Vocoder panel visibility](#vocoder-panel-visibility)               |
| **Input Follower** |                 | [Input Follower panel visibility](#input-follower-panel-visibility) |

---

## Input Follower Input Select

**EDIT FX → Others → Input Follower → Input Select**. Live edit **`cmd=0x71`**,
param **`0x26`** (Single edit buffer **`<part>=0x40`**). **`stored = <value>`**
(dense **`00`–`03`**).

| `<value>` | Option |
| --------- | ------ |
| `00`      | Off    |
| `01`      | In L   |
| `02`      | In L+R |
| `03`      | In R   |

Panel rows per **Input Select**: [Input Follower panel
visibility](#input-follower-panel-visibility).

**Not** [Ring Modulator Volume](../live-edit/single/oscillators.md#ring-modulator-volume)
(`70`/`26`). **Not** Edit Multi **Detune** (`72`/`26`).

---

## Input Follower panel visibility

**EDIT FX → Others → Input Follower**. Rows depend on [Input
Select](#input-follower-input-select). **Input Select** = **`71`/`26`**; other
rows = **`70`** — see [effects.md — Input Follower](../live-edit/single/effects.md#input-follower).

| Control          | Off (`00`) | In L / In L+R / In R (`01`–`03`) |
| ---------------- | ---------- | -------------------------------- |
| **Input Select** | Yes        | Yes                              |
| **Attack**       | No         | Yes                              |
| **Release**      | No         | Yes                              |
| **Sensitivity**  | No         | Yes                              |

Active modes (`01`–`03`) share the same encodings:

| Control         | `cmd`/`param` | Encoding                                                                |
| --------------- | ------------- | ----------------------------------------------------------------------- |
| **Attack**      | `70`/`36`     | **0..127** → `stored = lcd`                                             |
| **Release**     | `70`/`3A`     | **0..127** → `stored = lcd`                                             |
| **Sensitivity** | `70`/`38`     | **0.0..100.0 %** — [Sensitivity (LCD)](#input-follower-sensitivity-lcd) |

Same **`param`** bytes as [Vocoder](#vocoder-panel-visibility) on **`70`**
(**`36`** = Carrier Attack, **`3A`** = Bands) — decode by **EDIT FX** sub-page.

---

## Input Follower Sensitivity (LCD)

**EDIT FX → Others → Input Follower → Sensitivity** when [Input
Select](#input-follower-input-select) ≠ **Off**. Live edit **`cmd=0x70`**, param
**`0x38`**. **`stored = round(pct × 127 / 100)`** — **`00`** = **0 %**,
**`7F`** = **100.0 %** (endpoints).

| LCD     | `<value>` |
| ------- | --------- |
| 0 %     | `00`      |
| 100.0 % | `7F`      |

See [effects.md — Input Follower Attack / Release /
Sensitivity](../live-edit/single/effects.md#input-follower).

---

## Filter Bank Type

**EDIT FX → Others → Filter Bank → Type**. Live edit **`cmd=0x6E`**, param
**`0x13`** (part single buffer — same **`cmd`** as [Character
Type](#character-type), different **`param`**). **`stored = <value>`** (dense
**`00`–`0B`**).
focus).

| `<value>` | Option            |
| --------- | ----------------- |
| `00`      | Off               |
| `01`      | Ring Modulator    |
| `02`      | Frequency Shifter |
| `03`      | Vowel Filter      |
| `04`      | Comb Filter       |
| `05`      | 1 Pole XFade      |
| `06`      | 2 Pole XFade      |
| `07`      | 4 Pole XFade      |
| `08`      | 6 Pole XFade      |
| `09`      | LP VariSlope      |
| `0A`      | HP VariSlope      |
| `0B`      | BP VariSlope      |

Panel rows per **Type**: [Filter Bank panel
visibility](#filter-bank-panel-visibility). Parameter map groups some pole-XFade
and VariSlope variants — see [single.md](../dumps/single.md).

**Not** Oscillator 1 wave select (`70`/`13`).

---

## Filter Bank panel visibility

**EDIT FX → Others → Filter Bank**. Rows depend on [Filter Bank
Type](#filter-bank-type) — see [effects.md — Filter
Bank](../live-edit/single/effects.md#filter-bank). Live edit **`cmd=0x6E`** on all rows
below (part single buffer).

| Control          | Always | `6E`/`13` = Off | Ring Mod (`01`) | Freq Shifter (`02`) | Vowel (`03`) |
| ---------------- | ------ | --------------- | --------------- | ------------------- | ------------ |
| **Type**         | Yes    | Yes             | Yes             | Yes                 | Yes          |
| **Mix**          | —      | No              | Yes             | Yes                 | Yes          |
| **Frequency**    | —      | No              | Yes             | Yes                 | Yes          |
| **Resonance**    | —      | No              | No              | No                  | Yes          |
| **Stereo Phase** | —      | No              | Yes             | Yes                 | Yes          |
| **Shape L**      | —      | No              | No              | Yes                 | No           |
| **Shape R**      | —      | No              | No              | Yes                 | No           |

### Ring Modulator (`01`)

| Control          | `cmd`/`param` | Encoding                                              |
| ---------------- | ------------- | ----------------------------------------------------- |
| **Mix**          | `6E`/`14`     | [Filter Bank Mix (LCD)](#filter-bank-mix-lcd)         |
| **Frequency**    | `6E`/`15`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**) |
| **Stereo Phase** | `6E`/`16`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**) |

### Frequency Shifter (`02`)

| Control          | `cmd`/`param` | Encoding                                                     |
| ---------------- | ------------- | ------------------------------------------------------------ |
| **Mix**          | `6E`/`14`     | [Filter Bank Mix (LCD)](#filter-bank-mix-lcd)                |
| **Frequency**    | `6E`/`15`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**)        |
| **Stereo Phase** | `6E`/`16`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**)        |
| **Shape L**      | `6E`/`17`     | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64` |
| **Shape R**      | `6E`/`18`     | **−100.0..+100.0 %** → `stored = round(pct × 64 / 100) + 64` |

### Vowel Filter (`03`)

| Control          | `cmd`/`param` | Encoding                                                      |
| ---------------- | ------------- | ------------------------------------------------------------- |
| **Mix**          | `6E`/`14`     | [Filter Bank Mix (LCD)](#filter-bank-mix-lcd)                 |
| **Frequency**    | `6E`/`15`     | [Filter Bank Vowel Frequency](#filter-bank-vowel-frequency)   |
| **Resonance**    | `6E`/`19`     | [Filter Bank Resonance (LCD)](#filter-bank-resonance-lcd)     |
| **Stereo Phase** | `6E`/`16`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**)         |

### Comb Filter (`04`)

| Control          | `cmd`/`param` | Encoding                                                    |
| ---------------- | ------------- | ----------------------------------------------------------- |
| **Mix**          | `6E`/`14`     | [Filter Bank Mix (LCD)](#filter-bank-mix-lcd)               |
| **Frequency**    | `6E`/`15`     | [Filter Bank Comb Frequency](#filter-bank-comb-frequency)   |
| **Resonance**    | `6E`/`19`     | [Filter Bank Resonance (LCD)](#filter-bank-resonance-lcd)   |
| **Stereo Phase** | `6E`/`16`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**)       |

### Pole XFade (`05`–`08`)

**1 / 2 / 4 / 6 Pole XFade** — same row set and encodings.

| Control         | `cmd`/`param` | Encoding                                                          |
| --------------- | ------------- | ----------------------------------------------------------------- |
| **Frequency**   | `6E`/`15`     | [Filter Bank Frequency (direct)](#filter-bank-frequency-direct)   |
| **Resonance**   | `6E`/`19`     | [Filter Bank Resonance (LCD)](#filter-bank-resonance-lcd)         |
| **Filter Type** | `6E`/`17`     | [Filter Bank XFade Filter Type](#filter-bank-xfade-filter-type)   |

### VariSlope (`09`–`0B`)

**LP / HP / BP VariSlope** — same row set and encodings.

| Control       | `cmd`/`param` | Encoding                                                              |
| ------------- | ------------- | --------------------------------------------------------------------- |
| **Frequency** | `6E`/`15`     | [Filter Bank Frequency (direct)](#filter-bank-frequency-direct)       |
| **Resonance** | `6E`/`19`     | [Filter Bank Resonance (LCD)](#filter-bank-resonance-lcd)             |
| **Poles**     | `6E`/`17`     | [Filter Bank VariSlope Poles (LCD)](#filter-bank-varislope-poles-lcd) |
| **Slope**     | `6E`/`18`     | [Filter Bank VariSlope Slope](#filter-bank-varislope-slope)           |

**`6E`/`15`–`19`** decoding depends on [Filter Bank Type](#filter-bank-type) —
see sections above.

---

## Filter Bank Mix (LCD)

**EDIT FX → Others → Filter Bank → Mix** when [Type](#filter-bank-type) =
**Ring Modulator** (`01`), **Frequency Shifter** (`02`), **Vowel Filter** (`03`),
or **Comb Filter** (`04`). Live edit **`cmd=0x6E`**, param **`0x14`**.

Same **%** curve as [Character Intensity (LCD)](#character-intensity-lcd):
**`00`** = **Off**; **`01`–`7F`** → panel **%** ( **`01`** = **0.8 %** …
**`7F`** = **100.0 %** ).

| `<value>` | LCD     |     |
| --------- | ------- | --- |
| `00`      | Off     | ✓   |
| `01`      | 0.8 %   | ✓   |
| `02`      | 1.6 %   | ✓   |
| `7F`      | 100.0 % | ✓   |

**Not** Character **Intensity** (`70`/`15` or `71`/`61`).

---

## Filter Bank Vowel Frequency

**EDIT FX → Others → Filter Bank → Frequency** when [Type](#filter-bank-type) =
**Vowel Filter** (`03`). Live edit **`cmd=0x6E`**, param **`0x15`**.

On other filter-bank types, **`6E`/`15`** uses a different map — see [Comb
Frequency](#filter-bank-comb-frequency), [Frequency (direct)](#filter-bank-frequency-direct),
bipolar **Frequency** (Ring Mod / Freq Shifter).

**Percentage:** **`stored = wire byte`** (`00`–`7F`). Panel **0.0..100.0 %** —
**`00`** = **0 %**, **`40`** = **50.0 %**, **`7F`** = **100.0 %**
(`pct ≈ stored × 100 / 127`).

**Vowel glyph** (shown beside **%** on panel; dense **`00`–`7F`** sweep):

| `<value>` | Glyph | `<value>` | Glyph | `<value>` | Glyph  | `<value>` | Glyph  |
| --------- | ----- | --------- | ----- | --------- | ------ | --------- | ------ |
| `00`      | `<u>` | `20`      | `<a>` | `40`      | `<i>`  | `60`      | `<ö>`  |
| `01`–`05` | `<u`  | `21`–`25` | `<a`  | `41`–`45` | `<i`   | `61`–`65` | `<ö`   |
| `06`–`0A` | `>o`  | `26`–`2A` | `>ä`  | `46`–`4A` | `>iü`  | `66`–`6A` | `>öe`  |
| `0B`      | `<o>` | `2B`      | `<ä>` | `4B`      | `<iü>` | `6B`      | `<öe>` |
| `0C`–`0F` | `<o`  | `2C`–`2F` | `<ä`  | `4C`–`4F` | `<iü`  | `6C`–`6F` | `<öe`  |
| `10`–`14` | `>ā`  | `30`–`34` | `>e`  | `50`–`54` | `>ü`   | `70`–`74` | `>o`   |
| `15`      | `<ā>` | `35`      | `<e>` | `55`      | `<ü>`  | `75`      | `<o>`  |
| `16`–`1A` | `<ā`  | `36`–`3A` | `<e`  | `56`–`5A` | `<ü`   | `76`–`7A` | `<o`   |
| `1B`–`1F` | `>a`  | `3B`–`3F` | `>i`  | `5B`–`5F` | `>ö`   | `7B`–`7E` | `>u`   |
|           |       |           |       |           |        | `7F`      | `<u>`  |

---

## Filter Bank Resonance (LCD)

**EDIT FX → Others → Filter Bank → Resonance** when [Type](#filter-bank-type) =
**Vowel Filter** (`03`), **Comb Filter** (`04`), **Pole XFade** (`05`–`08`), or
**VariSlope** (`09`–`0B`). Live edit **`cmd=0x6E`**, param **`0x19`**.

**`stored = wire byte`** (`00`–`7F`). Panel **0.0..100.0 %** — **`00`** = **0 %**,
**`40`** = **50.0 %**, **`7F`** = **100.0 %** (`pct ≈ stored × 100 / 127`).

| `<value>` | LCD     |     |
| --------- | ------- | --- |
| `00`      | 0 %     | ✓   |
| `40`      | 50.0 %  | ✓   |
| `7F`      | 100.0 % | ✓   |

---

## Filter Bank Comb Frequency

**EDIT FX → Others → Filter Bank → Frequency** when [Type](#filter-bank-type) =
**Comb Filter** (`04`). Live edit **`cmd=0x6E`**, param **`0x15`**.

**`stored = semitone index`** from **C0** — chromatic **`+1`** per step.
**`00`–`60`** (**97** steps): **`00`** = **C0** … **`5F`** = **B7**, **`60`** =
**C8**. Panel stops at **C8** — wire **`61`–`7F`** not reachable on panel.

| `<value>` | LCD |     |
| --------- | --- | --- |
| `00`      | C0  | ✓   |
| `01`      | C#0 | ✓   |
| `02`      | D0  | ✓   |
| `5F`      | B7  | ✓   |
| `60`      | C8  | ✓   |

---

## Filter Bank Frequency (direct)

**EDIT FX → Others → Filter Bank → Frequency** when [Type](#filter-bank-type) =
**Pole XFade** (`05`–`08`) or **VariSlope** (`09`–`0B`). Live edit
**`cmd=0x6E`**, param **`0x15`**.

**`stored = wire byte`** — panel **`0`–`127`** (`stored = value`).

| `<value>` | LCD |     |
| --------- | --- | --- |
| `00`      | 0   | ✓   |
| `40`      | 64  | ✓   |
| `7F`      | 127 | ✓   |

---

## Filter Bank XFade Filter Type

**EDIT FX → Others → Filter Bank → Filter Type** when [Type](#filter-bank-type) =
**Pole XFade** (`05`–`08`). Live edit **`cmd=0x6E`**, param **`0x17`**. Same
byte as **Shape L** on Frequency Shifter — decode using **`13`**.

| `<value>` | LCD           | Notes                           |
| --------- | ------------- | ------------------------------- |
| `00`      | Low Pass      | ✓                               |
| `01`–`7E` | **1**–**126** | Numeric panel labels (dense)    |
| `40`      | Band Pass     | ✓ — wire **`40`**, not **`65`** |
| `7F`      | High Pass     | ✓                               |

---

## Filter Bank VariSlope Poles (LCD)

**EDIT FX → Others → Filter Bank → Poles** when [Type](#filter-bank-type) =
**VariSlope** (`09`–`0B`). Live edit **`cmd=0x6E`**, param **`0x17`**.

**`stored = wire byte`** (`00`–`7F`). Panel **2.00..6.00** (two decimals) —
**`poles ≈ 2 + stored × 4 / 127`**.

| `<value>` | LCD  |     |
| --------- | ---- | --- |
| `00`      | 2.00 | ✓   |
| `40`      | 4.00 | ✓   |
| `7F`      | 6.00 | ✓   |

---

## Filter Bank VariSlope Slope

**EDIT FX → Others → Filter Bank → Slope** when [Type](#filter-bank-type) =
**VariSlope** (`09`–`0B`). Live edit **`cmd=0x6E`**, param **`0x18`**. Same
byte as **Shape R** on Frequency Shifter — decode using **`13`**.

**`stored = wire byte`** — panel **`0`–`127`**.

| `<value>` | LCD |     |
| --------- | --- | --- |
| `00`      | 0   | ✓   |
| `40`      | 64  | ✓   |
| `7F`      | 127 | ✓   |

---

## Vocoder Mode

**EDIT FX → Others → Vocoder → Mode**. Live edit **`cmd=0x71`** (Page B),
param **`0x27`**. **`stored = <value>`** (dense
**`00`–`06`**). **`00`** (**Off**): no further **EDIT FX** rows.

| `<value>` | Option     |
| --------- | ---------- |
| `00`      | Off        |
| `01`      | Oscillator |
| `02`      | Osc Hold   |
| `03`      | Noise      |
| `04`      | In L       |
| `05`      | In L+R     |
| `06`      | In R       |

Panel rows per **Mode**: [Vocoder panel
visibility](#vocoder-panel-visibility).

**Not** Noise **Color** (`70`/`27`).

---

## Vocoder panel visibility

**EDIT FX → Others → Vocoder**. Rows depend on [Vocoder Mode](#vocoder-mode).
**Mode** = **`71`/`27`**; all other rows = **`70`** (**Spread** **`2F`**, **Q**
**`2B`**) — see [effects.md — Vocoder](../live-edit/single/effects.md#vocoder).

| Control              | Off (`00`) | Modes `01`–`06` |
| -------------------- | ---------- | --------------- |
| **Mode**             | Yes        | Yes             |
| **Spread**           | No         | Yes             |
| **Q-Factor**         | No         | Yes             |
| **Center Freq**      | No         | Yes             |
| **Balance**          | No         | Yes             |
| **Mod Offset**       | No         | Yes             |
| **Carrier Attack**   | No         | Yes             |
| **Carrier Release**  | No         | Yes             |
| **Spectral Balance** | No         | Yes             |
| **Bands**            | No         | Yes             |

### Active modes (`01`–`06`)

**Oscillator**, **Osc Hold**, **Noise**, **In L**, **In L+R**, **In R** — same
row set and encodings.

| Control              | `cmd`/`param` | Encoding                                                                                                                                                            |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Spread**           | `70`/`2F`     | **−64..+63** → `stored = ui + 64` — dump **`0x037`**                                                                                                                |
| **Q-Factor**         | `70`/`2B`     | **`0`–`127`** direct — dump **`0x033`**                                                                                                                             |
| **Center Freq**      | `70`/`28`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**) — dump **`0x030`**                                                                                            |
| **Balance**          | `70`/`30`     | **`0`–`127`** direct — dump **`0x038`**                                                                                                                             |
| **Mod Offset**       | `70`/`29`     | **−64..+63** → `stored = ui + 64` (**`40`** = **+0**) — dump **`0x031`**                                                                                            |
| **Carrier Attack**   | `70`/`36`     | **`0`–`127`** direct — dump **`0x03E`** — `F0 … 70 40 36 00 F7` = **0**                                                                                             |
| **Carrier Release**  | `70`/`37`     | **`0`–`127`** direct — dump **`0x03F`** — `F0 … 70 40 37 7F F7` = **127**                                                                                           |
| **Spectral Balance** | `70`/`39`     | **`0`–`127`** direct — dump **`0x041`** — `F0 … 70 40 39 00 F7` = **0**                                                                                             |
| **Bands**            | `70`/`3A`     | [Vocoder Bands](#vocoder-bands) — dump **`0x042`** — `F0 … 70 40 3A 00 F7` = **01**                                                                                 |

---

## Vocoder Bands

**EDIT FX → Others → Vocoder → Bands** when [Mode](#vocoder-mode) =
**Oscillator** (`01`) through **In R** (`06`). Live edit **`cmd=0x70`**, param
**`0x3A`**. **`stored = index`** (**`00`–`1F`**) → panel **`01`–`32`**
(**`bands = stored + 1`**). Single edit buffer: **`F0 … 70 40 3A 00 F7`** → **01**
bands.

| `<value>` | Bands |     |
| --------- | ----- | --- |
| `00`      | 01    | ✓   |
| `01`      | 02    | ✓   |
| `1F`      | 32    | ✓   |

---

## Distortion Type

**Edit FX → Distortion → Type**. Live edit **`cmd=0x71`**, param **`0x64`**
(Page **B#100**) — see
[effects.md](../live-edit/single/effects.md#distortion-type).
**`stored = <value>`** (wire byte; **not** a dense `00`–`19` index).

| `<value>` | Option            |
| --------- | ----------------- |
| `00`      | Off               |
| `0C`      | Wide              |
| `01`      | Light             |
| `02`      | Soft              |
| `03`      | Medium            |
| `04`      | Hard              |
| `05`      | Digital           |
| `06`      | Wave Shaper       |
| `07`      | Rectifier         |
| `13`      | Bit Reducer       |
| `12`      | Rate Reducer      |
| `0D`      | Soft Bounce       |
| `0E`      | Hard Bounce       |
| `0F`      | Sine Fold         |
| `10`      | Triangle Fold     |
| `11`      | Sawtooth Fold     |
| `0A`      | Low Pass          |
| `0B`      | High Pass         |
| `08`      | Bit Reducer Old   |
| `09`      | Rate Reducer Old  |
| `14`      | Mint Overdrive    |
| `15`      | Curry Overdrive   |
| `16`      | Saffron Overdrive |
| `17`      | Onion Overdrive   |
| `18`      | Pepper Overdrive  |
| `19`      | Chili Overdrive   |

Panel rows per **Type**: [Distortion panel
visibility](#distortion-panel-visibility).

**Not** global multi **Part Enable** (`72`/`48`).

---

## Distortion panel visibility

**Edit FX → Distortion**. **Type** is always on the panel.

### Type = Off (`00`)

| Control    | Visible |
| ---------- | ------- |
| **Type**   | Yes     |
| All others | No      |

### Standard types — same four percent rows

**Type** wire values sharing **Mix**, **Intensity**, **Treble Boost**, **High
Cut**
(all **0.0..100.0 %**). Panel-confirmed:

| `<value>` | Type          |
| --------- | ------------- |
| `0C`      | Wide          |
| `01`      | Light         |
| `02`      | Soft          |
| `03`      | Medium        |
| `04`      | Hard          |
| `05`      | Digital       |
| `06`      | Wave Shaper   |
| `07`      | Rectifier     |
| `0D`      | Soft Bounce   |
| `0E`      | Hard Bounce   |
| `0F`      | Sine Fold     |
| `10`      | Triangle Fold |
| `11`      | Sawtooth Fold |

0..100.0 %** |
| **Intensity**    | Yes | `71`/`65` | **0.0..100.0 %** |
| **Treble Boost** | Yes | `6E`/`46` | **0.0..100.0 %** |
| **High Cut**     | Yes | `6E`/`47` | **0.0..100.0 %** |

Percent params: `stored = round(pct × 127 / 100)` — endpoints **`00`** = 0 %,
**`7F`** = 100.0 %.

| UI      | `<value>` | Param                                                                           | Notes                                                     |
| ------- | --------- | ------------------------------------------------------------------------------- | --------------------------------------------------------- |
| 0.0 %   | `00`      | Mix / Intensity / Treble / High Cut                                             | ✓                                                         |
| 56.3 %  | `48`      | **Mix** (`6E`/`48`)                                                             | ✓ (**Wide**; matches `round(pct × 127 / 100)`)            |
| 78.9 %  | `65`      | **Intensity** (`71`/`65`)                                                       | ✓ (**Wide**; naive round → **`64`**, panel uses **`65`**) |
| 50.0 %  | `40`      | **Treble Boost** (`6E`/`46`), **High Cut** (`6E`/`47`), **Quality** (`6E`/`49`) | ✓ (`round(50 × 127 / 100)` = **`0x40`**)                  |
| 100.0 % | `7F`      | standard % rows + **Quality**                                                   | ✓                                                         |

### Reducer types — Mix, Intensity, Quality

**Type** = **Rate Reducer** (`12`) or **Bit Reducer** (`13`). Same three rows;
Live edit **`6E`/`49`** for **Quality**.

| Control       | Visible | Live edit | Range                                 |
| ------------- | ------- | --------- | ------------------------------------- |
| **Type**      | Yes     | `71`/`64` | [Distortion Type](#distortion-type)   |
| **Mix**       | Yes     | `6E`/`48` | **0.0..100.0 %**                      |
| **Intensity** | Yes     | `71`/`65` | **0.0..100.0 %**                      |
| **Quality**   | Yes     | `6E`/`49` | **0.0..100.0 %**                      |

No **Treble Boost** / **High Cut** (capture: no **`46`/`47`** after **`64 12`**
/
**`64 13`**).

### Minimal types — Mix and Intensity only

**Type** wire values with only **Mix** and **Intensity** (both **0.0..100.0
%**).
Panel-confirmed:

| `<value>` | Type             |
| --------- | ---------------- |
| `0A`      | Low Pass         |
| `0B`      | High Pass        |
| `08`      | Bit Reducer Old  |
| `09`      | Rate Reducer Old |

0..100.0 %** |
| **Intensity** | Yes | `71`/`65` | **0.0..100.0 %** |

Percent encoding: same as [standard
types](#standard-types--same-four-percent-rows) (**Mix** /
**Intensity** calibration anchors apply).

### Overdrive types — Drive, Mix, High Cut

**Type** wire values with **Drive**, **Mix**, and **High Cut** (all **0.0..100.0
%**).
Panel label **Drive** uses the same live-edit byte as **Intensity** (`71`/`65`).

| `<value>` | Type              | **Tone** |
| --------- | ----------------- | -------- |
| `15`      | Curry Overdrive   | No       |
| `19`      | Chili Overdrive   | No       |
| `14`      | Mint Overdrive    | Yes      |
| `16`      | Saffron Overdrive | Yes      |
| `17`      | Onion Overdrive   | Yes      |
| `18`      | Pepper Overdrive  | Yes      |

| Control      | Visible              | Live edit | Range                                 |
| ------------ | -------------------- | --------- | ------------------------------------- |
| **Type**     | Yes                  | `71`/`64` | [Distortion Type](#distortion-type)   |
| **Drive**    | Yes                  | `71`/`65` | **0.0..100.0 %**                      |
| **Tone**     | Types with Tone only | `6E`/`4A` | **−100.0..+100.0 %**; **`40`** = +0 % |
| **Mix**      | Yes                  | `6E`/`48` | **0.0..100.0 %**                      |
| **High Cut** | Yes                  | `6E`/`47` | **0.0..100.0 %**                      |

**Drive** / **Mix** / **High Cut**: `stored = round(pct × 127 / 100)` — same as
standard
**Mix** row (**50.0 %** → **`40`** on **High Cut**).

**Tone** (when shown): capture on **`14`**/**`16`**/**`17`**/**`18`** —
**`6E`/`4A`**
sweep; **`00`** = −100.0 %, **`40`** = +0 %, **`7F`** = +100.0
%.
No **`4A`** after **`64 15`** / **`64 19`** (Curry / Chili). No
**`46`**/**`49`** on
overdrive types.

No **Intensity** / **Treble Boost** labels on the panel (byte **`65`** is
**Drive** here).

All **Distortion Type** wire values **`00`–`19`** panel-mapped (this
pass).

---

## Patch name categories

**Edit Single → Categories → Name Cat 1** / **Name Cat 2** (same list on both).
Virus TI **Search by Category** / browser filter names; **`stored = index`**.

23 options (`0`–`22`).

| Index | `<value>` | Option       |
| ----- | --------- | ------------ |
| 0     | `00`      | Off          |
| 1     | `01`      | Acid         |
| 2     | `02`      | Arpeggiator  |
| 3     | `03`      | Atomizer     |
| 4     | `04`      | Bass         |
| 5     | `05`      | Classic      |
| 6     | `06`      | Decay        |
| 7     | `07`      | Digital      |
| 8     | `08`      | Drums        |
| 9     | `09`      | EFX          |
| 10    | `0A`      | FM           |
| 11    | `0B`      | Input        |
| 12    | `0C`      | Lead         |
| 13    | `0D`      | Organ        |
| 14    | `0E`      | Pad          |
| 15    | `0F`      | Percussion   |
| 16    | `10`      | Piano        |
| 17    | `11`      | Pluck        |
| 18    | `12`      | String       |
| 19    | `13`      | Vocoder      |
| 20    | `14`      | Favourites 1 |
| 21    | `15`      | Favourites 2 |
| 22    | `16`      | Favourites 3 |

---

## Soft Knob Destinations

Soft Knob 1/2/3 **Function As…** — panel menu order (**128** names).
**`<value>`** is the SysEx destination byte (not the table index).
Capture: **`cmd=0x71`** — **Function As…** Knob 1 **`3E`**,
Knob 2 **`3F`** (**B#63** *Definable2 Single*), Knob 3 **`40`**.
Indices **59** / **61** use LCD names **Freq Shifter Mix** / **FreqShifter
Frequency**.

| Index | `<value>` | Option                             |
| ----- | --------- | ---------------------------------- |
| 0     | `00`      | Off                                |
| 1     | `40`      | Aftertouch                         |
| 2     | `55`      | Analog Boost Int                   |
| 3     | `56`      | Analog Boost Tune                  |
| 4     | `6F`      | Arp Hold                           |
| 5     | `69`      | Arp Mode                           |
| 6     | `6C`      | Arp Note Length                    |
| 7     | `6E`      | Arp Octaves                        |
| 8     | `6A`      | Arp Pattern                        |
| 9     | `6B`      | Arp Resolution                     |
| 10    | `6D`      | Arp Swing                          |
| 11    | `48`      | Assign 1 Amount 1                  |
| 12    | `49`      | Assign 2 Amount 1                  |
| 13    | `4A`      | Assign 2 Amount 2                  |
| 14    | `4B`      | Assign 3 Amount 1                  |
| 15    | `4C`      | Assign 3 Amount 2                  |
| 16    | `4D`      | Assign 3 Amount 3                  |
| 17    | `73`      | Assign 4 Amount 1                  |
| 18    | `74`      | Assign 5 Amount 1                  |
| 19    | `75`      | Assign 6 Amount 1                  |
| 20    | `06`      | Balance                            |
| 21    | `3E`      | Bend Up                            |
| 22    | `3F`      | Bend Down                          |
| 23    | `02`      | Breath                             |
| 24    | `0F`      | Channel Volume                     |
| 25    | `19`      | Chorus Delay                       |
| 26    | `18`      | Chorus Depth                       |
| 27    | `1A`      | Chorus Feedback                    |
| 28    | `16`      | Chorus Mix                         |
| 29    | `17`      | Chorus Rate                        |
| 30    | `4E`      | Clock Tempo                        |
| 31    | `03`      | Control 03                         |
| 32    | `07`      | Control 09                         |
| 33    | `09`      | Control 12                         |
| 34    | `0A`      | Control 13                         |
| 35    | `0B`      | Control 14                         |
| 36    | `0C`      | Control 15                         |
| 37    | `0D`      | Control 16                         |
| 38    | `05`      | Data Entry                         |
| 39    | `54`      | Delay Coloration                   |
| 40    | `1F`      | Delay Depth                        |
| 41    | `1D`      | Delay Feedback                     |
| 42    | `1E`      | Delay Rate                         |
| 43    | `1C`      | Delay Time                         |
| 44    | `57`      | Distortion Intensity               |
| 45    | `71`      | EQ Mid Frequency                   |
| 46    | `70`      | EQ Mid Gain                        |
| 47    | `72`      | EQ Mid Q-Factor                    |
| 48    | `1B`      | Effect Send (Delay)                |
| 49    | `76`      | Effect Send (Reverb)               |
| 50    | `08`      | Expression                         |
| 51    | `27`      | Filter Env > FM Amount             |
| 52    | `26`      | Filter Env > Osc 2 Pitch           |
| 53    | `2C`      | Filter 1 Env Amount                |
| 54    | `2E`      | Filter 1 Key Follow                |
| 55    | `2A`      | Filter 1 Resonance                 |
| 56    | `2D`      | Filter 2 Env Amount                |
| 57    | `2F`      | Filter 2 Key Follow                |
| 58    | `2B`      | Filter 2 Resonance                 |
| 59    | `7F`      | Freq Shifter Mix *(LCD name)*      |
| 60    | `04`      | Foot Pedal                         |
| 61    | `58`      | FreqShifter Frequency *(LCD name)* |
| 62    | `4F`      | Input Thru                         |
| 63    | `30`      | LFO 1 Contour                      |
| 64    | `5C`      | LFO 1 > Assign Amount              |
| 65    | `35`      | LFO 1 > Filter Gain                |
| 66    | `31`      | LFO 1 > Osc 1                      |
| 67    | `32`      | LFO 1 > Osc 2                      |
| 68    | `33`      | LFO 1 > Pulse Width                |
| 69    | `34`      | LFO 1 > Resonance                  |
| 70    | `36`      | LFO 2 Contour                      |
| 71    | `5D`      | LFO 2 > Assign Amount              |
| 72    | `39`      | LFO 2 > Cutoff 1                   |
| 73    | `3A`      | LFO 2 > Cutoff 2                   |
| 74    | `38`      | LFO 2 > FM Amount                  |
| 75    | `3B`      | LFO 2 > Panorama                   |
| 76    | `37`      | LFO 2 > Shape                      |
| 77    | `3C`      | LFO 3 Rate                         |
| 78    | `3D`      | LFO 3 > Assign Amount              |
| 79    | `01`      | Modulation Wheel                   |
| 80    | `53`      | Noise Color                        |
| 81    | `29`      | Noise Volume                       |
| 82    | `50`      | Osc Initial Phase                  |
| 83    | `79`      | Osc 1 F-Shift                      |
| 84    | `7B`      | Osc 1 F-Spread                     |
| 85    | `7D`      | Osc 1 Interpolation                |
| 86    | `23`      | Osc 1 Key Follow                   |
| 87    | `77`      | Osc 1 Local Detune                 |
| 88    | `22`      | Osc 1 Pitch                        |
| 89    | `21`      | Osc 1 Pulse Width                  |
| 90    | `20`      | Osc 1 Wave Select                  |
| 91    | `7A`      | Osc 2 F-Shift                      |
| 92    | `7C`      | Osc 2 F-Spread                     |
| 93    | `7E`      | Osc 2 Interpolation                |
| 94    | `28`      | Osc 2 Key Follow                   |
| 95    | `78`      | Osc 2 Local Detune                 |
| 96    | `25`      | Osc 2 Pulse Width                  |
| 97    | `24`      | Osc 2 Wave Select                  |
| 98    | `5B`      | Osc 3 Detune                       |
| 99    | `5A`      | Osc 3 Pitch                        |
| 100   | `59`      | Osc 3 Volume                       |
| 101   | `10`      | Panorama                           |
| 102   | `0E`      | Patch Volume                       |
| 103   | `60`      | Phaser Depth                       |
| 104   | `62`      | Phaser Feedback                    |
| 105   | `61`      | Phaser Frequency                   |
| 106   | `5E`      | Phaser Mix                         |
| 107   | `5F`      | Phaser Rate                        |
| 108   | `63`      | Phaser Spread                      |
| 109   | `12`      | Portamento                         |
| 110   | `51`      | Punch Intensity                    |
| 111   | `66`      | Reverb Coloration                  |
| 112   | `65`      | Reverb Dampening                   |
| 113   | `64`      | Reverb Decay                       |
| 114   | `67`      | Reverb Feedback                    |
| 115   | `52`      | Ring Modulator                     |
| 116   | `68`      | Surround Balance                   |
| 117   | `11`      | Transpose                          |
| 118   | `13`      | Unison Detune                      |
| 119   | `15`      | Unison LFO Phase                   |
| 120   | `14`      | Unison Spread                      |
| 121   | `41`      | Velo > FM Amount                   |
| 122   | `42`      | Velo > Filt 1 Env Amount           |
| 123   | `43`      | Velo > Filt 2 Env Amount           |
| 124   | `47`      | Velo > Panorama                    |
| 125   | `44`      | Velo > Resonance 1                 |
| 126   | `45`      | Velo > Resonance 2                 |
| 127   | `46`      | Velo > Volume                      |

---

## Soft Knob Names

Soft Knob 1/2/3 **Name** LCD label — **`71`/`33`**, **`34`**, **`35`**.

88 panel options. **Index** is the **alphabetical** menu order on the Virus
(e.g.
**>Para** … **Width**); **`<value>`** is the firmware wire byte — **not**
alphabetical and **not** the index (e.g. **Soften** `39`, **Speaker** `57`,
**Speed** `3A`, **Width** `47`).

Panel **Name** appears when **Function As…** ≠ Off.

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | >Para         |
| 1     | `01`      | +3rds         |
| 2     | `02`      | +4ths         |
| 3     | `03`      | +5ths         |
| 4     | `04`      | +7ths         |
| 5     | `05`      | +Octave       |
| 6     | `06`      | Access        |
| 7     | `07`      | ArpMode       |
| 8     | `08`      | ArpOct        |
| 9     | `09`      | Attack        |
| 10    | `0A`      | Balance       |
| 11    | `0B`      | Bite          |
| 12    | `0C`      | Bush          |
| 13    | `0D`      | Chorus        |
| 14    | `0E`      | Comb          |
| 15    | `0F`      | Cutoff        |
| 16    | `10`      | Decay         |
| 17    | `11`      | Delay         |
| 18    | `12`      | Depth         |
| 19    | `13`      | Destroy       |
| 20    | `14`      | Detune        |
| 21    | `15`      | Disolve       |
| 22    | `16`      | Distort       |
| 23    | `17`      | Dive          |
| 24    | `18`      | Effects       |
| 25    | `19`      | Elevate       |
| 26    | `1A`      | Energy        |
| 27    | `1B`      | EqHigh        |
| 28    | `1C`      | EqLow         |
| 29    | `1D`      | EqMid         |
| 30    | `1E`      | FM            |
| 31    | `1F`      | Fast          |
| 32    | `20`      | Fear          |
| 33    | `21`      | Filter        |
| 34    | `22`      | Flanger       |
| 35    | `23`      | Fuzz          |
| 36    | `24`      | F-Shift       |
| 37    | `25`      | F-Spread      |
| 38    | `26`      | Glide         |
| 39    | `27`      | Hold          |
| 40    | `28`      | Hype          |
| 41    | `29`      | Infect        |
| 42    | `2A`      | Interpolation |
| 43    | `2B`      | Length        |
| 44    | `2C`      | Mix           |
| 45    | `2D`      | Modulate      |
| 46    | `2E`      | Morph         |
| 47    | `2F`      | Muscle        |
| 48    | `30`      | Mutate        |
| 49    | `31`      | Noise         |
| 50    | `32`      | Open          |
| 51    | `33`      | Orbit         |
| 52    | `34`      | PWM           |
| 53    | `35`      | Pan           |
| 54    | `36`      | Party!        |
| 55    | `37`      | Phaser        |
| 56    | `38`      | Phatter       |
| 57    | `39`      | Pitch         |
| 58    | `3A`      | Pulsate       |
| 59    | `3B`      | Punch         |
| 60    | `3C`      | Push          |
| 61    | `3D`      | Rate          |
| 62    | `3E`      | Release       |
| 63    | `3F`      | Reso          |
| 64    | `40`      | Reverb        |
| 65    | `41`      | RingMod       |
| 66    | `42`      | Sack          |
| 67    | `43`      | Scream        |
| 68    | `44`      | Shape         |
| 69    | `45`      | Sharpen       |
| 70    | `46`      | Slow          |
| 71    | `39`      | Soften        |
| 72    | `57`      | Speaker       |
| 73    | `3A`      | Speed         |
| 74    | `4A`      | SubOsc        |
| 75    | `4B`      | Sustain       |
| 76    | `4C`      | Sweep         |
| 77    | `4D`      | Swing         |
| 78    | `4E`      | Tempo         |
| 79    | `4F`      | Thinner       |
| 80    | `50`      | Tone          |
| 81    | `51`      | Tremolo       |
| 82    | `52`      | Vibrato       |
| 83    | `53`      | Vowel         |
| 84    | `54`      | WahWah        |
| 85    | `55`      | Warmth        |
| 86    | `56`      | Warp          |
| 87    | `47`      | Width         |

## Mod Matrix Sources

Mod Matrix slot **Source**. **One** source per slot (three destination routes
share it). Live edit **`cmd=0x71`**; param **per slot** (**`0x40`**, **`0x43`**,
**`0x48`**, **`0x67`**, **`0x6A`**, **`0x6D`**) —
[mod-matrix.md](../live-edit/single/mod-matrix.md). **`<value>`** is the
SysEx wire byte (not the **Index** column).

40 options — full wire map confirmed (Slot 1 sweep):

| `<value>` | Option           | Index |
| --------- | ---------------- | ----- |
| `00`      | Off              | 0     |
| `01`      | Pitch Bend       | 1     |
| `02`      | Channel Pressure | 2     |
| `03`      | Mod Wheel        | 3     |
| `04`      | Breath           | 4     |
| `05`      | Controller 3     | 5     |
| `06`      | Foot Pedal       | 6     |
| `07`      | Data Entry       | 7     |
| `08`      | Balance          | 8     |
| `09`      | Controller 9     | 9     |
| `0A`      | Expression       | 10    |
| `0B`      | Controller 12    | 11    |
| `0C`      | Controller 13    | 12    |
| `0D`      | Controller 14    | 13    |
| `0E`      | Controller 15    | 14    |
| `0F`      | Controller 16    | 15    |
| `10`      | Hold Pedal       | 16    |
| `11`      | Portamento Sw    | 17    |
| `12`      | Sost Pedal       | 18    |
| `13`      | Amp Envelope     | 19    |
| `14`      | Filter Envelope  | 20    |
| `15`      | LFO 1 bipolar    | 23    |
| `16`      | LFO 2 bipolar    | 25    |
| `17`      | LFO 3 bipolar    | 27    |
| `18`      | Velocity On      | 29    |
| `19`      | Velocity Off     | 30    |
| `1A`      | Key Follow       | 31    |
| `1B`      | Random           | 32    |
| `1C`      | Arp Input        | 33    |
| `1D`      | LFO 1 unipolar   | 24    |
| `1E`      | LFO 2 unipolar   | 26    |
| `1F`      | LFO 3 unipolar   | 28    |
| `20`      | 1% Constant      | 38    |
| `21`      | 10% Constant     | 39    |
| `22`      | AnaKey1 Fine     | 34    |
| `23`      | AnaKey 2 Fine    | 35    |
| `24`      | AnaKey1 Coarse   | 36    |
| `25`      | AnaKey2 Coarse   | 37    |
| `26`      | Envelope 3       | 21    |
| `27`      | Envelope 4       | 22    |

```text
F0 00 20 33 01 00 71 40 40 03 F7 # Mod Wheel
F0 00 20 33 01 00 71 40 40 15 F7 # LFO 1 bipolar
```

## Mod Matrix Amount

Mod Matrix **Amount**. **Three** amount fields per slot (one per destination
row). **`cmd`** / **param** vary by slot and row — full map in
[mod-matrix.md](../live-edit/single/mod-matrix.md). Full wire map:
[Bipolar centered (±64 @ 0x40)](#bipolar-centered-64--0x40).

## Mod Matrix Destinations

Mod Matrix slot **Destination**. **Three** destination fields per slot.
**`cmd`** / **param** vary by slot and row — full map in
[mod-matrix.md](../live-edit/single/mod-matrix.md). **`<value>`** wire bytes
match [LFO 1 Assign Target](#assign-target) (**`41/xx`** = **`4F/xx`**, etc.)
— full **121**-destination table there.

122 options (**Index** `0`–`121`). Wire **`<value>`** bytes for the same panel
names are in [LFO 1 Assign Target](#assign-target) (index ≠ wire byte).

| Index | Destination                                                         |
| ----- | ------------------------------------------------------------------- |
| 0     | Off                                                                 |
| 1     | Amp Env Attack                                                      |
| 2     | Amp Env Decay                                                       |
| 3     | Amp Env Slope                                                       |
| 4     | Amp Env Sustain                                                     |
| 5     | Amp Env Release                                                     |
| 6     | Arp Note Length                                                     |
| 7     | Arp Pattern                                                         |
| 8     | Arp Swing Factor                                                    |
| 9     | Chorus Delay                                                        |
| 10    | Chorus Feedback                                                     |
| 11    | Chorus Mix                                                          |
| 12    | Chorus Mod Depth                                                    |
| 13    | Chorus Mod Rate                                                     |
| 14    | Delay Coloration                                                    |
| 15    | Delay Feedback                                                      |
| 16    | Delay Mod Depth                                                     |
| 17    | Delay Mod Rate                                                      |
| 18    | Delay Send                                                          |
| 19    | Delay Time                                                          |
| 20    | Distortion Intensity                                                |
| 21    | Distortion Mix                                                      |
| 22    | EQ Mid Frequency                                                    |
| 23    | EQ Mid Gain                                                         |
| 24    | Filter Env > FM/Sync                                                |
| 25    | Filter Env > Osc 2 Pitch                                            |
| 26    | Filter Balance                                                      |
| 27    | Filter Env Attack                                                   |
| 28    | Filter Env Decay                                                    |
| 29    | Filter Env Slope                                                    |
| 30    | Filter Env Sustain                                                  |
| 31    | Filter Env Release                                                  |
| 32    | Filter 1 Cutoff                                                     |
| 33    | Filter 1 Env Amount                                                 |
| 34    | Filter 1 Resonance                                                  |
| 35    | Filter 2 Cutoff                                                     |
| 36    | Filter 2 Env Amount                                                 |
| 37    | Filter 2 Resonance                                                  |
| 38    | Filterbank Poles                                                    |
| 39    | Filterbank Resonance                                                |
| 40    | Filterbank Slope                                                    |
| 41    | Filterbank Frequency *(wire `60`; [Assign Target](#assign-target))* |
| 42    | LFO 1 > Assign Amount                                               |
| 43    | LFO 1 Contour                                                       |
| 44    | LFO 1 Rate                                                          |
| 45    | LFO 1 > Filter Gain                                                 |
| 46    | LFO 1 > Osc 1 Pitch                                                 |
| 47    | LFO 1 > Osc 2 Pitch                                                 |
| 48    | LFO 1 > Pulse Width                                                 |
| 49    | LFO 1 > Resonance                                                   |
| 50    | LFO 2 > Assign Amount                                               |
| 51    | LFO 2 Contour                                                       |
| 52    | LFO 2 Rate                                                          |
| 53    | LFO 2 > Cutoff 1                                                    |
| 54    | LFO 2 > Cutoff 2                                                    |
| 55    | LFO 2 > FM Amount                                                   |
| 56    | LFO 2 > Panorama                                                    |
| 57    | LFO 2 > Shape                                                       |
| 58    | LFO 3 > Assign Amount                                               |
| 59    | LFO 3 Rate                                                          |
| 60    | Noise Color                                                         |
| 61    | Noise Volume                                                        |
| 62    | Oscillator Balance                                                  |
| 63    | Oscillator Volume                                                   |
| 64    | Osc 1 F-Shift                                                       |
| 65    | Osc 1 F-Spread                                                      |
| 66    | Osc 1 Interpolation                                                 |
| 67    | Osc 1 Pitch                                                         |
| 68    | Osc 1 Pulse Width                                                   |
| 69    | Osc 1 Shape/Index                                                   |
| 70    | Osc 1 Wave Select                                                   |
| 71    | Osc 2 Detune                                                        |
| 72    | Osc 2 FM Amount                                                     |
| 73    | Osc 2 F-Shift                                                       |
| 74    | Osc 2 F-Spread                                                      |
| 75    | Osc 2 Interpolation                                                 |
| 76    | Osc 2 Pitch                                                         |
| 77    | Osc 2 Pulse Width                                                   |
| 78    | Osc 2 Shape/Index                                                   |
| 79    | Osc 2 Wave Select                                                   |
| 80    | Osc 3 Detune                                                        |
| 81    | Osc 3 Pitch                                                         |
| 82    | Osc 3 Volume                                                        |
| 83    | Sub Osc Volume                                                      |
| 84    | Pan Spread                                                          |
| 85    | Panorama                                                            |
| 86    | Patch Volume                                                        |
| 87    | Phaser Feedback                                                     |
| 88    | Phaser Frequency                                                    |
| 89    | Phaser Mix                                                          |
| 90    | Phaser Mod Depth                                                    |
| 91    | Phaser Mod Rate                                                     |
| 92    | Portamento                                                          |
| 93    | Punch Intensity                                                     |
| 94    | Reverb Send                                                         |
| 95    | Reverb Coloration                                                   |
| 96    | Reverb Dampening                                                    |
| 97    | Reverb Time                                                         |
| 98    | Reverb PreDelay                                                     |
| 99    | Ring Modulator                                                      |
| 100   | Slot 1 Amount 1                                                     |
| 101   | Slot 1 Amount 2                                                     |
| 102   | Slot 1 Amount 3                                                     |
| 103   | Slot 2 Amount 1                                                     |
| 104   | Slot 2 Amount 2                                                     |
| 105   | Slot 2 Amount 3                                                     |
| 106   | Slot 3 Amount 1                                                     |
| 107   | Slot 3 Amount 2                                                     |
| 108   | Slot 3 Amount 3                                                     |
| 109   | Slot 4 Amount 1                                                     |
| 110   | Slot 4 Amount 2                                                     |
| 111   | Slot 4 Amount 3                                                     |
| 112   | Slot 5 Amount 1                                                     |
| 113   | Slot 5 Amount 2                                                     |
| 114   | Slot 5 Amount 3                                                     |
| 115   | Slot 6 Amount 1                                                     |
| 116   | Slot 6 Amount 2                                                     |
| 117   | Slot 6 Amount 3                                                     |
| 118   | Surround Balance                                                    |
| 119   | Transpose                                                           |
| 120   | Unison Detune                                                       |
| 121   | Unison LFO Phase                                                    |

## Wavetable Names

Oscillator **Wavetable** wave select names (`cmd=0x70`, `param=0x13`,
**Mode `02`**).
**Wire** = index **`00`–`63`** for panel indices **0–99**. Order confirmed
.

100 options (`0`–`99`).

| Index | Option       |
| ----- | ------------ |
| 0     | Sine         |
| 1     | HarmncSweep  |
| 2     | Glass Sweep  |
| 3     | Draw Bars    |
| 4     | Clusters     |
| 5     | Insine Out   |
| 6     | Landing      |
| 7     | Liquid Metal |
| 8     | Opposition   |
| 9     | Overtunes 1  |
| 10    | Overtunes 2  |
| 11    | Scale Trix   |
| 12    | Sine Rider   |
| 13    | Sqr Series   |
| 14    | Upsine Down  |
| 15    | Thumbs Up    |
| 16    | Waterphone   |
| 17    | E-Chime      |
| 18    | Tinkabell    |
| 19    | Bellfizz     |
| 20    | Bellentine   |
| 21    | Robot Wars   |
| 22    | Alternator   |
| 23    | Finger Bass  |
| 24    | Fizzybar     |
| 25    | Flutes       |
| 26    | HP Love      |
| 27    | Majestix     |
| 28    | Hotch Potch  |
| 29    | Resynater    |
| 30    | Smooth Rough |
| 31    | Sawsalito    |
| 32    | Bells 1      |
| 33    | Bells 2      |
| 34    | SportReport  |
| 35    | Metal Guru   |
| 36    | Bat Cave     |
| 37    | Acetate      |
| 38    | Buzzbizz     |
| 39    | Buzzpartout  |
| 40    | Vanish       |
| 41    | Overbones    |
| 42    | Pulsechecker |
| 43    | Stratosfear  |
| 44    | Sooty Sweep  |
| 45    | Throaty      |
| 46    | Didgitalis   |
| 47    | Evil         |
| 48    | Chords       |
| 49    | FM Grit      |
| 50    | Bellsarnie   |
| 51    | Octavius     |
| 52    | Eat Pulse    |
| 53    | Sinzin       |
| 54    | Sine System  |
| 55    | Clip Sweep   |
| 56    | Roughage     |
| 57    | Waving       |
| 58    | Pling Saw    |
| 59    | E-Peas       |
| 60    | Bump Sweep   |
| 61    | Filter Sqr   |
| 62    | Fourmant     |
| 63    | Formantera   |
| 64    | Sundial 1    |
| 65    | Sundial 2    |
| 66    | Sundial 3    |
| 67    | Clipdial 1   |
| 68    | Clipdial 2   |
| 69    | Voxonix      |
| 70    | Solenoid     |
| 71    | KlingKlang   |
| 72    | Violator     |
| 73    | Potassium    |
| 74    | Pile Up      |
| 75    | Tincanali    |
| 76    | Sniper       |
| 77    | Squeezy      |
| 78    | Decomposer   |
| 79    | Morfants     |
| 80    | Pingvox      |
| 81    | Adenoids     |
| 82    | Nasal        |
| 83    | Partialism   |
| 84    | TableDance   |
| 85    | Cascade      |
| 86    | Prismism     |
| 87    | Friction     |
| 88    | Robotix      |
| 89    | Whizzfizz    |
| 90    | Spangly      |
| 91    | Fluxbin      |
| 92    | Fiboglide    |
| 93    | Fibonice     |
| 94    | Fibonasty    |
| 95    | Penetrator   |
| 96    | Blinder      |
| 97    | Element 5    |
| 98    | Bad Signs    |
| 99    | Domina7rix   |

## Control Smooth Mode / clock quantize

**Edit Single → Common → Smooth Mode** (`cmd=0x71`, `param=0x19`). **`stored =
index`**
(`00`–`14`). The **Quantise …** rows (`04`–`14`, hardware-confirmed) use the
same **clock division
labels** Access documents for **LFO 1/2/3 Clock**, [Delay Clock](#delay-clock),
and **Arpeggiator Resolution** on the panel
([Arpeggiator Resolution](#arpeggiator-resolution) uses a **different** wire map
on **`71`/`11`**).

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | Off           |
| 1     | `01`      | On            |
| 2     | `02`      | Auto          |
| 3     | `03`      | Note          |
| 4     | `04`      | Quantise 1/64 |
| 5     | `05`      | Quantise 1/32 |
| 6     | `06`      | Quantise 1/16 |
| 7     | `07`      | Quantise 1/8  |
| 8     | `08`      | Quantise 1/4  |
| 9     | `09`      | Quantise 1/2  |
| 10    | `0A`      | Quantise 3/64 |
| 11    | `0B`      | Quantise 3/32 |
| 12    | `0C`      | Quantise 3/16 |
| 13    | `0D`      | Quantise 3/8  |
| 14    | `0E`      | Quantise 1/24 |
| 15    | `0F`      | Quantise 1/12 |
| 16    | `10`      | Quantise 1/6  |
| 17    | `11`      | Quantise 1/3  |
| 18    | `12`      | Quantise 2/3  |
| 19    | `13`      | Quantise 3/4  |
| 20    | `14`      | Quantise 1/1  |

four-mode summary); the Virus TI panel exposes the full quantize grid above.

---

## Edit Single — Panorama (LCD)

**Edit Single → Common → Panorama** (`cmd=0x70`, `param=0x0A`).
Bipolar **`stored = ui + 64`** (`00` = full left, `40` = center, `7F` = full
right).
Panel readout is **not** linear in the wire byte; VALUE ± steps are mostly **1.5
%**
or **1.6 %** in the displayed value.

**Mirror rule** (hardware-confirmed **`41`–`7E`**): for right wire **`R`**, the
label
matches left wire **`0x80 − R`** with **`L<`** → **`% >R`**. Endpoints **`00`**
/
**`7F`** are both **100.0 %** (not mirrored).

| `<value>` | LCD        | `<value>` | LCD       |
| --------- | ---------- | --------- | --------- |
| `00`      | L< 100.0 % | `01`      | L< 98.4 % |
| `02`      | L< 96.9 %  | `03`      | L< 95.3 % |
| `04`      | L< 93.8 %  | `05`      | L< 92.2 % |
| `06`      | L< 90.6 %  | `07`      | L< 89.1 % |
| `08`      | L< 87.5 %  | `09`      | L< 85.9 % |
| `0A`      | L< 84.4 %  | `0B`      | L< 82.8 % |
| `0C`      | L< 81.3 %  | `0D`      | L< 79.7 % |
| `0E`      | L< 78.1 %  | `0F`      | L< 76.6 % |
| `10`      | L< 75.0 %  | `11`      | L< 73.4 % |
| `12`      | L< 71.9 %  | `13`      | L< 70.3 % |
| `14`      | L< 68.8 %  | `15`      | L< 67.2 % |
| `16`      | L< 65.6 %  | `17`      | L< 64.1 % |
| `18`      | L< 62.5 %  | `19`      | L< 60.9 % |
| `1A`      | L< 59.4 %  | `1B`      | L< 57.8 % |
| `1C`      | L< 56.3 %  | `1D`      | L< 54.7 % |
| `1E`      | L< 53.1 %  | `1F`      | L< 51.6 % |
| `20`      | L< 50.0 %  | `21`      | L< 48.4 % |
| `22`      | L< 46.9 %  | `23`      | L< 45.3 % |
| `24`      | L< 43.8 %  | `25`      | L< 42.2 % |
| `26`      | L< 40.6 %  | `27`      | L< 39.0 % |
| `28`      | L< 37.5 %  | `29`      | L< 35.9 % |
| `2A`      | L< 34.4 %  | `2B`      | L< 32.8 % |
| `2C`      | L< 31.3 %  | `2D`      | L< 29.7 % |
| `2E`      | L< 28.1 %  | `2F`      | L< 26.6 % |
| `30`      | L< 25.0 %  | `31`      | L< 23.4 % |
| `32`      | L< 21.9 %  | `33`      | L< 20.3 % |
| `34`      | L< 18.8 %  | `35`      | L< 17.2 % |
| `36`      | L< 15.6 %  | `37`      | L< 14.1 % |
| `38`      | L< 12.5 %  | `39`      | L< 10.9 % |
| `3A`      | L< 9.4 %   | `3B`      | L< 7.8 %  |
| `3C`      | L< 6.3 %   | `3D`      | L< 4.7 %  |
| `3E`      | L< 3.1 %   | `3F`      | L< 1.6 %  |
| `40`      | <0>        |           |           |

Right of center (`41`–`7F`):

| `<value>` | LCD        | `<value>` | LCD       |
| --------- | ---------- | --------- | --------- |
| `41`      | 1.6 % >R   | `42`      | 3.1 % >R  |
| `43`      | 4.7 % >R   | `44`      | 6.3 % >R  |
| `45`      | 7.8 % >R   | `46`      | 9.4 % >R  |
| `47`      | 10.9 % >R  | `48`      | 12.5 % >R |
| `49`      | 14.1 % >R  | `4A`      | 15.6 % >R |
| `4B`      | 17.2 % >R  | `4C`      | 18.8 % >R |
| `4D`      | 20.3 % >R  | `4E`      | 21.9 % >R |
| `4F`      | 23.4 % >R  | `50`      | 25.0 % >R |
| `51`      | 26.6 % >R  | `52`      | 28.1 % >R |
| `53`      | 29.7 % >R  | `54`      | 31.3 % >R |
| `55`      | 32.8 % >R  | `56`      | 34.4 % >R |
| `57`      | 35.9 % >R  | `58`      | 37.5 % >R |
| `59`      | 39.0 % >R  | `5A`      | 40.6 % >R |
| `5B`      | 42.2 % >R  | `5C`      | 43.8 % >R |
| `5D`      | 45.3 % >R  | `5E`      | 46.9 % >R |
| `5F`      | 48.4 % >R  | `60`      | 50.0 % >R |
| `61`      | 51.6 % >R  | `62`      | 53.1 % >R |
| `63`      | 54.7 % >R  | `64`      | 56.3 % >R |
| `65`      | 57.8 % >R  | `66`      | 59.4 % >R |
| `67`      | 60.9 % >R  | `68`      | 62.5 % >R |
| `69`      | 64.1 % >R  | `6A`      | 65.6 % >R |
| `6B`      | 67.2 % >R  | `6C`      | 68.8 % >R |
| `6D`      | 70.3 % >R  | `6E`      | 71.9 % >R |
| `6F`      | 73.4 % >R  | `70`      | 75.0 % >R |
| `71`      | 76.6 % >R  | `72`      | 78.1 % >R |
| `73`      | 79.7 % >R  | `74`      | 81.3 % >R |
| `75`      | 82.8 % >R  | `76`      | 84.4 % >R |
| `77`      | 85.9 % >R  | `78`      | 87.5 % >R |
| `79`      | 89.1 % >R  | `7A`      | 90.6 % >R |
| `7B`      | 92.2 % >R  | `7C`      | 93.8 % >R |
| `7D`      | 95.3 % >R  | `7E`      | 96.9 % >R |
| `7F`      | 100.0 % >R |           |           |

## Osc 1 Classic — Pulse Width (LCD)

**Wire:** `pct = 50 + stored × 50 / 127` — see
[oscillators.md — Pulse Width](../live-edit/single/oscillators.md#pulse-width-shape--sawtooth).
**LCD:** `round(pct + 0.4, 0.1)` in most of the range (partial map below; not
every
detent listed).

| `<value>` | LCD % | `<value>` | LCD % | `<value>` | LCD % |
| --------- | ----- | --------- | ----- | --------- | ----- |
| `00`      | 50.0  | `01`      | 50.4  | `02`      | 50.8  |
| `03`      | 51.2  | `04`      | 51.6  | `05`      | 52.0  |
| `06`      | 52.4  | `07`      | 52.7  | `08`      | 53.1  |
| `09`      | 53.5  | `0A`      | 53.9  | `0B`      | 54.3  |
| `0C`      | 54.7  | `0D`      | 55.1  | `0E`      | 55.5  |
| `0F`      | 55.9  | `10`      | 56.2  | `11`      | 56.7  |
| `12`      | 57.0  | `13`      | 57.5  | `14`      | 57.9  |
| `15`      | 58.7  | `16`      | 59.1  | `17`      | 59.4  |
| `18`      | 59.8  | `19`      | 60.2  | `1A`      | 60.6  |
| `1B`      | 61.0  | `1C`      | 61.4  | `1D`      | 61.8  |
| `1E`      | 62.2  | `1F`      | 63.0  | `20`      | 63.4  |
| `21`      | 63.8  | `22`      | 64.2  | `23`      | 64.2  |
| `24`      | 64.6  | `25`      | 65.0  | `26`      | 65.4  |
| `27`      | 65.7  | `28`      | 66.1  | `29`      | 66.5  |
| `2A`      | 66.9  | `2B`      | 67.3  | `2C`      | 67.7  |
| `2D`      | 68.1  | `2E`      | 68.5  | `2F`      | 68.9  |
| `30`      | 69.3  | `31`      | 69.7  | `32`      | 70.1  |
| `33`      | 70.5  | `34`      | 70.9  | `35`      | 71.3  |
| `36`      | 71.7  | `37`      | 72.0  | `38`      | 72.4  |
| `39`      | 72.8  | `3A`      | 73.2  | `3B`      | 73.6  |
| `3C`      | 74.0  | `3D`      | 74.4  | `3E`      | 74.8  |
| `3F`      | 75.2  | `40`      | 75.6  | `41`      | 76.0  |
| `42`      | 76.4  | `43`      | 76.8  | `44`      | 77.2  |
| `45`      | 77.6  | `46`      | 78.0  | `47`      | 78.3  |
| `48`      | 78.7  | `49`      | 79.1  | `4A`      | 79.5  |
| `4B`      | 79.9  | `4C`      | 80.3  | `4D`      | 80.7  |
| `4E`      | 81.1  | `4F`      | 81.5  | `50`      | 81.9  |
| `51`      | 82.3  | `52`      | 82.7  | `5A`      | 85.8  |
| `65`      | 90.2  | `6C`      | 92.9  | `6E`      | 93.7  |
| `79`      | 98.0  | `7A`      | 98.4  | `7D`      | 99.6  |
| `7F`      | 100   |           |       |           |       |

## Osc 1 Hypersaw — Density (LCD)

**Mode `01`**, `cmd=0x70`, `param=0x11`.
**Wire:** `internal = 1 + stored × 8 / 127`.
**LCD candidate:** `round(1 + (internal − 1) × (stored / 127), 0.1)` — see
[Osc 1 Hypersaw Density](../live-edit/single/oscillators.md#oscillator-1--hypersaw).
**128/128** wire → LCD entries (`00`–`7F`); duplicate labels on some detents.

| `<value>` | LCD | `<value>` | LCD | `<value>` | LCD |
| --------- | --- | --------- | --- | --------- | --- |
| `00`      | 1.0 | `01`      | 1.1 | `02`      | 1.1 |
| `03`      | 1.1 | `04`      | 1.2 | `05`      | 1.2 |
| `06`      | 1.2 | `07`      | 1.3 | `08`      | 1.3 |
| `09`      | 1.3 | `0A`      | 1.4 | `0B`      | 1.4 |
| `0C`      | 1.4 | `0D`      | 1.5 | `0E`      | 1.5 |
| `0F`      | 1.5 | `10`      | 1.6 | `11`      | 1.6 |
| `12`      | 1.6 | `13`      | 1.7 | `14`      | 1.7 |
| `15`      | 1.7 | `16`      | 1.7 | `17`      | 1.8 |
| `18`      | 1.8 | `19`      | 1.8 | `1A`      | 1.8 |
| `1B`      | 1.9 | `1C`      | 1.9 | `1D`      | 1.9 |
| `1E`      | 1.9 | `1F`      | 2.0 | `20`      | 2.0 |
| `21`      | 2.1 | `22`      | 2.1 | `23`      | 2.1 |
| `24`      | 2.2 | `25`      | 2.2 | `26`      | 2.2 |
| `27`      | 2.3 | `28`      | 2.3 | `29`      | 2.3 |
| `2A`      | 2.4 | `2B`      | 2.4 | `2C`      | 2.4 |
| `2D`      | 2.5 | `2E`      | 2.5 | `2F`      | 2.5 |
| `30`      | 2.6 | `31`      | 2.6 | `32`      | 2.6 |
| `33`      | 2.7 |           |     |           |     |
| `34`      | 2.7 | `35`      | 2.7 | `36`      | 2.7 |
| `37`      | 2.8 | `38`      | 2.8 | `39`      | 2.8 |
| `3A`      | 2.8 | `3B`      | 2.9 | `3C`      | 2.9 |
| `3D`      | 2.9 | `3E`      | 2.9 | `3F`      | 3.0 |
| `40`      | 3.0 | `41`      | 3.1 | `42`      | 3.2 |
| `43`      | 3.3 | `44`      | 3.4 | `45`      | 3.5 |
| `46`      | 3.5 | `47`      | 3.6 | `48`      | 3.6 |
| `49`      | 3.7 | `4A`      | 3.7 | `4B`      | 3.8 |
| `4C`      | 3.8 | `4D`      | 3.9 | `4E`      | 3.9 |
| `4F`      | 4.0 | `50`      | 4.0 | `51`      | 4.1 |
| `52`      | 4.2 | `53`      | 4.3 | `54`      | 4.4 |
| `55`      | 4.5 | `56`      | 4.5 | `57`      | 4.6 |
| `58`      | 4.6 | `59`      | 4.7 | `5A`      | 4.7 |
| `5B`      | 4.8 | `5C`      | 4.8 | `5D`      | 4.9 |
| `5E`      | 4.9 | `5F`      | 5.0 | `60`      | 5.0 |
| `61`      | 5.1 | `62`      | 5.3 | `63`      | 5.5 |
| `64`      | 5.7 |           |     |           |     |
| `65`      | 5.8 | `66`      | 5.9 | `67`      | 6.0 |
| `68`      | 6.0 | `69`      | 6.1 | `6A`      | 6.3 |
| `6B`      | 6.5 | `6C`      | 6.7 | `6D`      | 6.8 |
| `6E`      | 6.9 | `6F`      | 7.0 |           |     |
| `70`      | 7.0 | `71`      | 7.1 | `72`      | 7.3 |
| `73`      | 7.5 | `74`      | 7.7 | `75`      | 7.8 |
| `76`      | 7.9 | `77`      | 8.0 | `78`      | 8.0 |
| `79`      | 8.1 | `7A`      | 8.3 | `7B`      | 8.5 |
| `7C`      | 8.7 | `7D`      | 8.8 | `7E`      | 8.9 |
| `7F`      | 9.0 |           |     |           |     |
