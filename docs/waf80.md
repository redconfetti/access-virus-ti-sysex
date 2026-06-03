# WAF80 Virus SysEx Reference (1999)

Transcribed from [WAF80 — Access Virus SysEx](https://www.waf80.de/virus/sysex.html)
(Access Music documentation posted **3 September 1999**). The **Virus TI**
family is not identical to the 1999 Virus, but many message types and
parameter page layouts appear **backward compatible**. Use this as a
**starting map** only.

**TI rule:** If a control is **not on the TI panel** or behaves differently
(e.g. no Filter 2 Cutoff — only **Offset**), mark it **N/A** in the TI docs and
do not assume the classic row applies. Confirm on TI hardware (see
[single-dump.md](single-dump.md), [multis-dump.md](multis-dump.md),
[single-live-edit.md](single-live-edit.md)).

## Parameter pages

| Page | SysEx `cmd` (classic) | Size  | Role                                                         |
| ---- | --------------------- | ----- | ------------------------------------------------------------ |
| A    | **`0x70`**            | 128 B | Single “LowPage” — also **MIDI CC** when LowPage=Contr       |
| B    | **`0x71`**            | 128 B | Single “HiPage” — also **poly pressure** when HiPage=PolyPrs |
| C    | **`0x72`**            | 128 B | **Multi + Global** parameters                                |

A **Single program** = Page A + Page B (**256 bytes**).  
Page C holds Multi and Global settings (SysEx only in classic doc).

### SysEx parameter change (classic)

```text
F0 00 20 33 01 <device> 7x <part> <param> <value> F7
```

| Byte    | Meaning                                                                   |
| ------- | ------------------------------------------------------------------------- |
| `7x`    | **`0x70`** Page A, **`0x71`** Page B, **`0x72`** Page C                   |
| `part`  | **`0x00`–`0x0F`** Multi part 1–16; **`0x40`** Single buffer (Single mode) |
| `param` | Parameter index **0–127** on that page                                    |
| `value` | **0–127**                                                                 |

Non-part-sensitive params ignore `part` (any value may be sent).

### Confirmed on Virus TI mk2 desktop

Promoted to project docs (trimmed from this file). Confirm here only when
regressing hardware:

| Topic                                             | Document                                                                     |
| ------------------------------------------------- | ---------------------------------------------------------------------------- |
| Multi live `0x72`, `DUMP_MULTI` offsets           | [multis-live-edit.md](multis-live-edit.md), [multis-dump.md](multis-dump.md) |
| Single Common `0x71` / `0x70`, part buffer `0x6E` | [single-live-edit.md](single-live-edit.md)                                   |
| Globals `0x73`                                    | [global-live-edit.md](global-live-edit.md)                                   |
| CC 91 / 93 / 94                                   | [control-change.md](control-change.md)                                       |
| `REQUEST_MULTI`, `REQUEST_ARRANGEMENT`            | [multis-dump.md](multis-dump.md), [single-dump.md](single-dump.md)           |

TI also uses **`cmd=0x73`** (globals) and **`cmd=0x6E`** (part single buffer)
beyond classic Page A/B/C — see those docs.

**In progress:** Filters — [testing.md — Confirmation queue](testing.md#confirmation-queue).

---

## Request messages

All requests use header `F0 00 20 33 01 <device> … F7`.  
`<device>`: **`0x00`–`0x0F`** individual, **`0x10`** omni (classic).

| Cmd        | Name                        | Body (after device)      | Reply (classic)             |
| ---------- | --------------------------- | ------------------------ | --------------------------- |
| **`0x30`** | **Single Request**          | `30 <bank> <slot>`       | Single Dump (`0x10`)        |
| **`0x31`** | **Multi Request**           | `31 <bank> <slot>`       | Multi Dump (`0x11`)         |
| **`0x32`** | Single Bank Request         | `32 <bank>`              | Bank bulk                   |
| **`0x33`** | Multi Bank Request          | `33 <bank>`              | Bank bulk                   |
| **`0x34`** | **Arrangement Request**     | `34` (TI: often `34 00`) | Multi + Singles — see below |
| **`0x35`** | **Global Request**          | `35`                     | Global data                 |
| **`0x36`** | **Total Request**           | `36`                     | Full device snapshot        |
| **`0x37`** | **Controller Dump Request** | `37 00 <part>`           | MIDI controller snapshot    |

### Single Request (`0x30`)

```text
F0 00 20 33 01 <device> 30 <bank> <slot> F7
```

| Field  | Meaning                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------- |
| `bank` | **`0x00`** edit buffer; **`0x01`–`0x04`** Single banks A–D                                           |
| `slot` | Program **0–127**; if `bank=0x00`, slot = part **`0x00`–`0x0F`** (Multi) or **`0x40`** (Single mode) |

### Global Request (`0x35`)

```text
F0 00 20 33 01 <device> 35 F7
```

Returns global / configuration parameters (classic Page C globals).

### Total Request (`0x36`)

```text
F0 00 20 33 01 <device> 36 F7
```

Returns a full device dump (classic).

### Controller Dump Request (`0x37`)

```text
F0 00 20 33 01 <device> 37 00 <part> F7
```

| Field  | Meaning                                                     |
| ------ | ----------------------------------------------------------- |
| `part` | **`0x00`–`0x0F`** Multi part 1–16; **`0x40`** Single buffer |

### Arrangement Request (`0x34`)

Classic: `F0 … 34 F7`. **TI mk2:** [single-dump.md — Arrangement export](single-dump.md#arrangement-export-dump_single--16).

---

## Dump messages (classic)

### Single Dump (`0x10`)

```text
F0 00 20 33 01 <device> 10 <bank> <slot> [256 bytes] [checksum] F7
```

Checksum (optional): `(device + 0x10 + bank + slot + sum(payload)) & 0x7F`.

### Multi Dump (`0x11`)

```text
F0 00 20 33 01 <device> 11 <bank> <slot> [256 bytes] [checksum] F7
```

TI **`DUMP_MULTI`** is **267 bytes** (expanded payload + header). Classic
256-byte layout is in [Multi dump table](#multi-dump-table-classic-256-byte) below.

---

## MIDI Control Change (Page A map)

When **LowPage = Contr** (default), Page A sound parameters are controlled by
**MIDI CC** on the part channel:

```text
Bc  nn  vv     — status (channel c), CC number = Page A index, value 0–127
```

**Sound parameters** (class `a`) go to the **lowest part number** sharing a
channel. **Performance controllers** (class `p`) go to **all** parts on that
channel and are **not** stored in the Single sound.

| CC / A# | Class   | Name                    | Range / values                                                                        |
| ------- | ------- | ----------------------- | ------------------------------------------------------------------------------------- |
| 0       | p       | Bank Select             | 0–3 Bank A–D                                                                          |
| 1       | p       | Modulation Wheel        |                                                                                       |
| 2       | p       | Breath Controller       |                                                                                       |
| 3       | p       | Contr 3                 |                                                                                       |
| 4       | p       | Foot Controller         |                                                                                       |
| 5       | a       | Portamento Time         | 0–127                                                                                 |
| 6       | p       | Data Slider             |                                                                                       |
| 7       | p       | Channel Volume          | 0–127                                                                                 |
| 8       | p       | Balance                 |                                                                                       |
| 9       | p       | Contr 9                 |                                                                                       |
| 10      | a       | Panorama                | 0–127 (−64..+63)                                                                      |
| 11      | p       | Expression              |                                                                                       |
| 12–16   | p       | Contr 12–16             |                                                                                       |
| 17      | a       | Osc1 Shape              | TI Classic: `00` wave, `01`–`3F` Wave>Saw, `40` Saw, `41`–`7E` Saw>Pulse, `7F` Pulse — [Osc 1 Classic](single-live-edit.md#shape-0x11--wave--saw-blend--pure-saw) |
| 18      | a       | Osc1 Pulsewidth         | 0–127                                                                                 |
| 19      | a       | Osc1 Wave Select        | 64 waves `00`–`3F` — TI: [Osc 1 Classic / Spectral Wave](single-live-edit.md#shape-spectral-wave) |
| 20      | a       | Osc1 Semitone           | −64..+63                                                                              |
| 21      | a       | Osc1 Keyfollow          | −64..+63; **Norm** = +32 → `60` — [Osc 1 Classic](single-live-edit.md#shape-spectral-wave) |
| 22      | a       | Osc2 Shape              | −64..+63                                                                              |
| 23      | a       | Osc2 Pulsewidth         | 0–127                                                                                 |
| 24      | a       | Osc2 Wave Select        | 0–64                                                                                  |
| 25      | a       | Osc2 Semitone           | −64..+63                                                                              |
| 26      | a       | Osc2 Detune             | 0–127                                                                                 |
| 27      | a       | Osc2 FM Amount          | 0–127                                                                                 |
| 28      | a       | Osc2 Sync               | 0/1                                                                                   |
| 29      | a       | Osc2 Filt Env Amt       | −64..+63                                                                              |
| 30      | a       | FM Filt Env Amt         | −64..+63                                                                              |
| 31      | a       | Osc2 Keyfollow          | −64..+63 (default 32)                                                                 |
| 32      | p       | Bank Select             | 0–3                                                                                   |
| 33      | a       | Osc Balance             | −100..+100 % — [Osc 1 Classic](single-live-edit.md#shape-spectral-wave) |
| 34      | a       | Suboscillator Volume    | 0–127                                                                                 |
| 35      | a       | Suboscillator Shape     | 0 Square / 1 Triangle                                                                 |
| 36      | a       | Osc Mainvolume          | TI Saturation **Osc Volume**: bipolar −64..+63 — [Saturation — Osc Volume](single-live-edit.md#saturation--osc-volume-cmd0x70-param-0x24) |
| 37      | a       | Noise Volume            | 0–127                                                                                 |
| 38      | a       | Ringmodulator Volume    | 0–127                                                                                 |
| 40      | a       | Cutoff                  | 0–127 — TI: [Filter 1 Cutoff](single-live-edit.md#filter-1-cutoff-cmd0x70-param-0x28) |
| 41      | a       | Cutoff2                 | −64..+63 — TI: [Filter 2 Offset](single-live-edit.md#filter-2-offset-cmd0x70-param-0x29) |
| 42      | a       | Filter1 Resonance       | 0–127 — TI: [Filter 1 Resonance](single-live-edit.md#filter-1-resonance-cmd0x70-param-0x2a) |
| 43      | a       | Filter2 Resonance       | 0–127 — TI: [Filter 2 Resonance](single-live-edit.md#filter-2-resonance-cmd0x70-param-0x2b) |
| 44      | a       | Filter1 Env Amt         | 0–127 — TI: [Filter 1 Envelope Amount](single-live-edit.md#filter-1-envelope-amount-cmd0x70-param-0x2c) |
| 45      | a       | Filter2 Env Amt         | 0–127 — TI: [Filter 2 Envelope Amount](single-live-edit.md#filter-2-envelope-amount-cmd0x70-param-0x2d) |
| 46      | a       | Filter1 Keyfollow       | −64..+63 — TI: [Filter 1 Keyfollow](single-live-edit.md#filter-1-keyfollow-cmd0x70-param-0x2e) |
| 47      | a       | Filter2 Keyfollow       | −64..+63 — TI: [Filter 2 Keyfollow](single-live-edit.md#filter-2-keyfollow-cmd0x70-param-0x2f) |
| 48      | a       | Filter Balance          | −64..+63 — TI: [Filter Balance](single-live-edit.md#filter-balance-cmd0x70-param-0x30) |
| 49      | a       | Saturation Curve        | 0–6 Off..Shaper                                                                       |
| 51      | a       | Filter1 Mode            | 0–3 classic; TI **8** modes `00`–`07` — [Filter 1 Mode](single-live-edit.md#filter-1-mode-cmd0x70-param-0x33) |
| 52      | a       | Filter2 Mode            | 0 LP / 1 HP / 2 BP / 3 BS — TI: [Filter 2 Mode](single-live-edit.md#filter-2-mode-cmd0x70-param-0x34) (4 only) |
| 53      | a       | Filter Routing          | 0 Ser4 / 1 Ser6 / 2 Par4 / 3 Split — TI: [Filter Routing](single-live-edit.md#filter-routing-cmd0x70-param-0x35) |
| 54–58   | a       | Filter Env A/D/S/ST/R   | TI Filter 1 ADSR: `36`–`3A` — [Filter 1 envelope](single-live-edit.md#filter-1-envelope-adsr) |
| 59–63   | a       | Amp Env A/D/S/ST/R      | TI: `3B`–`3F` — [Amplifier envelope](single-live-edit.md#amplifier-envelope-adsr) |
| 64      | p       | Hold Pedal              |                                                                                       |
| 65      | p       | Portamento Pedal        |                                                                                       |
| 66      | p       | Sostenuto Pedal         |                                                                                       |
| 67–78   | a       | Lfo1 Rate..FiltGain Amt |                                                                                       |
| 79–90   | a       | Lfo2 Rate..Pan Lfo2 Amt |                                                                                       |
| 91      | a       | Patch Volume            | 0–127 — TI: [control-change.md](control-change.md)                                    |
| 93      | a       | Transpose               | −64..+63 — TI: [control-change.md](control-change.md)                                 |
| 94      | a       | Key Mode                | 0–4 Poly / Mono1–4 — TI: [control-change.md](control-change.md)                       |
| 97      | a       | Unison Mode             | 0/1                                                                                   |
| 98      | a       | Unison Detune           | 0–127                                                                                 |
| 99      | a       | Unison Panorama Spread  | 0–127                                                                                 |
| 100     | a       | Unison Lfo Phase        | −64..+63                                                                              |
| 101     | a       | Input Mode              | 0 Off / 1 Dynamic / 2 Static                                                          |
| 102     | a       | Input Select            | 0–8 In1L..                                                                            |
| 105–110 | a       | Chorus Mix..Shape       |                                                                                       |
| 113–118 | a,ms,np | Effect Send, Delay *    |                                                                                       |
| 123     | p       | All Notes Off           |                                                                                       |

Example: `B0 21 40` — CC **33** (Osc Balance) = 64 on channel 1.

---

## Single parameters — Page B (`cmd=0x71`)

| B#      | Name                                            | Range / values                                                                  |
| ------- | ----------------------------------------------- | ------------------------------------------------------------------------------- |
| 1       | Arp Mode                                        | 0–6 Off, Up, Down, Up&Down, AsPlayed, Random, Chord                             |
| 3       | Arp Octave Range                                | 0–3                                                                             |
| 4       | Arp Hold Enable                                 | 0/1                                                                             |
| 7       | Lfo3 Rate                                       | 0–127                                                                           |
| 8       | Lfo3 Shape                                      | 0–5                                                                             |
| 9       | Lfo3 Mode                                       | 0 Poly / 1 Mono                                                                 |
| 10      | Lfo3 Keyfollow                                  | 0–127                                                                           |
| 11      | Lfo3 Destination                                | 0–5                                                                             |
| 12      | Osc Lfo3 Amount                                 | 0–127                                                                           |
| 13      | Lfo3 Fade-In Time                               | 0–127                                                                           |
| 16      | Clock Tempo                                     | 63–190 BPM                                                                      |
| 17      | Arp Clock                                       | 1–17                                                                            |
| 18–21   | Lfo1/2/3/Delay Clock                            | Off, 1/64..                                                                     |
| 25      | Control Smooth Mode                             | 0 Off / 1 On / 2 Auto / 3 Note — TI: [single-live-edit.md](single-live-edit.md) |
| 26      | Bender Range Up                                 | −64..+63 — TI: [multis-live-edit.md](multis-live-edit.md)                       |
| 27      | Bender Range Down                               | −64..+63 — TI: [multis-live-edit.md](multis-live-edit.md)                       |
| 28      | Bender Scale                                    | 0 Linear / 1 Exponential — TI: [single-live-edit.md](single-live-edit.md)       |
| 30–33   | Filter env polarity, cutoff link, keytrack base | F1 **`0x1E`**, F2 **`0x1F`**; cutoff link **`0x20`** — [Cutoff Link](single-live-edit.md#filter-cutoff-link-cmd0x71-param-0x20); key base **`0x21`** — [Key Follow Base](single-live-edit.md#filter-key-follow-base-cmd0x71-param-0x21) |
| 35      | Osc Init Phase                                  |                                                                                 |
| 36      | Punch Intensity                                 |                                                                                 |
| 39      | Vocoder Mode                                    | 0–12                                                                            |
| 47–57   | Velocity amounts                                |                                                                                 |
| 60–61   | Amp / Pan velocity                              |                                                                                 |
| 62–63   | Definable1/2 Single                             |                                                                                 |
| 64–78   | Assign 1–3 sources/destinations/amounts         |                                                                                 |
| 112     | Filter Select                                   | 0 Filt1 / 1 Filt2 / 2 Filt1*2                                                   |
| 113–122 | Single Name Char 1–10                           | ASCII 32–127                                                                    |

---

## Single parameters — Page A (`cmd=0x70`)

Full list: see [CC / Page A table](#midi-control-change-page-a-map) (indices
0–127; gaps at 39, 50, 92, 95–96, 103–104, 111–112, 119–122 are undefined
in the 1999 doc).

---

## Page C — Multi & Global (`cmd=0x72`) — selected

| C#    | Class | Name                                          | Notes                                          |
| ----- | ----- | --------------------------------------------- | ---------------------------------------------- |
| 5–14  | m,np  | Multi Name Char 1–10                          | ASCII                                          |
| 22    | m,np  | Delay Output Select                           |                                                |
| 31–33 | m,bpc | Part Bank Select/Change, Program Change       |                                                |
| 34    | m     | Part MIDI Channel                             | 0–15 → ch 1–16                                 |
| 35–36 | m     | Part Low/High Key                             |                                                |
| 37–38 | m     | Part Transpose / Detune                       |                                                |
| 39    | m     | Part Volume                                   |                                                |
| 40    | m     | Part MIDI Volume Init                         |                                                |
| 41    | m     | Part Output Select                            |                                                |
| 72    | m     | Part Enable                                   |                                                |
| 73    | m     | Part MIDI Volume Enable                       |                                                |
| 74    | m     | Part Hold Pedal Enable                        | TI: [multis-live-edit.md](multis-live-edit.md) |
| 77    | m     | Note Steal Priority                           |                                                |
| 78    | m     | Part Prog Change Enable                       |                                                |
| 85–87 | g     | Global Prog Change / Multi Prog / Glob Vol RX |                                                |
| 93–99 | g     | Device ID, MIDI control pages, dump tx/rx     |                                                |
| 106   | g     | MIDI Clock Rx                                 |                                                |
| 118   | g     | Memory Protect                                | TI: [global-live-edit.md](global-live-edit.md) |
| 124   | g     | Global MIDI Channel                           |                                                |
| 125   | g     | LED Mode                                      | TI: [global-live-edit.md](global-live-edit.md) |
| 126   | g     | LCD Contrast                                  | TI: [global-live-edit.md](global-live-edit.md) |
| 127   | g     | Master Volume                                 |                                                |

Class legend: **p** performance (CC, not stored); **a** sound A; **b** sound B;
**m** multi; **g** global; **ms** multi/single; **np** non-part-sensitive;
**bpc** bank/program change.

---

## Multi dump table (classic 256-byte)

Payload byte indices for **1999 Multi dump** (not TI 267-byte layout):

| Bytes   | Field                                                          |
| ------- | -------------------------------------------------------------- |
| 0–3     | Internal                                                       |
| 4–13    | Multi name (10 × ASCII)                                        |
| 14      | Internal                                                       |
| 15      | Multi Clock Tempo (63–190 BPM)                                 |
| 16      | Internal                                                       |
| 17–22   | Multi delay time/feedback/rate/depth/shape/output              |
| 23      | Multi delay clock                                              |
| 24–31   | Internal                                                       |
| 32–47   | Part 1–16 bank number                                          |
| 48–63   | Part 1–16 program number                                       |
| 64–79   | Part 1–16 MIDI channel                                         |
| 80–95   | Part 1–16 low key                                              |
| 96–111  | Part 1–16 high key                                             |
| 112–127 | Part 1–16 transpose                                            |
| 128–143 | Part 1–16 detune                                               |
| 144–159 | Part 1–16 volume                                               |
| 160–175 | Part 1–16 MIDI volume init                                     |
| 176–191 | Part 1–16 output select                                        |
| 192–207 | Part 1–16 effect send                                          |
| 208–239 | Internal                                                       |
| 240–255 | Part state bitfield (enable, vol RX, hold, priority, prog chg) |

**Part state bitfield** (one byte per part): bit0 Enable; bit1 Vol RX; bit2
Hold; bit5 Priority; bit6 Prog Change.

Compare TI offsets in [multis-dump.md](multis-dump.md) — same fields, different
header/padding and **267-byte** wire format.

---

## Confirming on Virus TI mk2

1. Use [testing.md — Confirmation queue](testing.md#confirmation-queue): work
   **one LCD menu (category) at a time**, matching [single-dump.md](single-dump.md)
   sections — not random order through this file.
2. Hypothesis: Page **A** index *N* → live **`cmd=0x70`**, param **`N`** (hex),
   when global Page A = **SysEx**; else **MIDI CC** *N* ([waf80.md](#midi-control-change-page-a-map)).
3. Unconfirmed rows stay here until captured on hardware and copied into
   [single-live-edit.md](single-live-edit.md) / dump docs.
4. **Do not assume** 1999 **256-byte** dumps match TI **524** / **267-byte**
   wire formats — diff hardware captures ([multis-dump.md](multis-dump.md)).
