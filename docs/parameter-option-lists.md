# Parameter option lists

Enumerated UI options for Virus TI parameters. **Index** is the zero-based
list position; for most panel enums **`stored = index`** (exceptions: [Soft Knob Destinations](#soft-knob-destinations), [Soft Knob Names](#soft-knob-names) use per-row **`<value>`**) (hex in tables as
**`<value>`**).

Live-edit docs ([single-live-edit.md](single-live-edit.md),
[multis-live-edit.md](multis-live-edit.md)) record **`cmd` / `param` / encoding**
only — **option names live here**. Link with:

```markdown
See [Option name](parameter-option-lists.md#anchor).
```

See [waf80.md](waf80.md) for classic Page A/B parameter indices.

## Index

| Section | Used by |
| ------- | ------- |
| [Secondary output routing](#secondary-output-routing) | Edit Single → Surround → **Output**; Edit Multi → **Secondary Output** (`73`/`2D`) |
| [Input Mode](#input-mode) | Edit Single → Inputs (`6F`/`7C`) |
| [Input Select](#input-select) | Edit Single → Inputs (`6F`/`7D`) |
| [Atomizer preset](#atomizer-preset) | Edit Single → Inputs → **Atomizer** (`6F`/`7E`) |
| [Patch name categories](#patch-name-categories) | Edit Single → Categories → **Name Cat 1** / **Name Cat 2** (`71`/`7B`, `71`/`7C`) |
| [Soft Knob Destinations](#soft-knob-destinations) | Soft Knob **Function As…** — `71`/`3E`, `3F`, `40` (wire `<value>` per row) |
| [Soft Knob Names](#soft-knob-names) | Soft Knob **Name** — `71`/`33`, `34`, `35` (wire `<value>` per row) |
| [Mod Matrix Sources](#mod-matrix-sources) | Mod matrix **Source** |
| [Mod Matrix Destinations](#mod-matrix-destinations) | Mod matrix **Destination** |
| [Wavetable Names](#wavetable-names) | Osc wavetable wave select |

LCD↔wire curves (not simple enums): [Osc 1 Classic Pulse Width](#osc-1-classic--pulse-width-lcd),
[Osc 1 Hypersaw Density](#osc-1-hypersaw--density-lcd).

---

## Secondary output routing

**Off** plus **Out 1 L** … **USB 3 R**. **`00`** = Off; otherwise
**primary routing index + 1** (see [Output routing (primary)](multis-live-edit.md#output-routing-enum-0x29)).

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

3 options (`00`–`02`). Panel visible when [Input Mode](#input-mode) is **Dynamic** or **Static**.

| Index | `<value>` | Option  |
| ----- | --------- | ------- |
| 0     | `00`      | Left    |
| 1     | `01`      | L + R   |
| 2     | `02`      | Right   |

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

## Patch name categories

**Edit Single → Categories → Name Cat 1** / **Name Cat 2** (same list on both).
Virus TI **Search by Category** / browser filter names; **`stored = index`**.

23 options (`0`–`22`).

| Index | `<value>` | Option        |
| ----- | --------- | ------------- |
| 0     | `00`      | Off           |
| 1     | `01`      | Acid          |
| 2     | `02`      | Arpeggiator   |
| 3     | `03`      | Atomizer      |
| 4     | `04`      | Bass          |
| 5     | `05`      | Classic       |
| 6     | `06`      | Decay         |
| 7     | `07`      | Digital       |
| 8     | `08`      | Drums         |
| 9     | `09`      | EFX           |
| 10    | `0A`      | FM            |
| 11    | `0B`      | Input         |
| 12    | `0C`      | Lead          |
| 13    | `0D`      | Organ         |
| 14    | `0E`      | Pad           |
| 15    | `0F`      | Percussion    |
| 16    | `10`      | Piano         |
| 17    | `11`      | Pluck         |
| 18    | `12`      | String        |
| 19    | `13`      | Vocoder       |
| 20    | `14`      | Favourites 1  |
| 21    | `15`      | Favourites 2  |
| 22    | `16`      | Favourites 3  |

---

## Soft Knob Destinations

Soft Knob 1/2/3 **Function As…** — panel menu order (**128** names).
**`<value>`** is the SysEx destination byte (not the table index).
TI mk2 capture: **`cmd=0x71`** — **Function As…** Knob 1 **`3E`** (WAF80 **B#62** *Definable1 Single*),
Knob 2 **`3F`** (**B#63** *Definable2 Single*), Knob 3 **`40`**.
Indices **59** / **61** use LCD names **Freq Shifter Mix** / **FreqShifter Frequency**.

| Index | `<value>` | Option |
| ----- | --------- | ------ |
| 0 | `00` | Off |
| 1 | `40` | Aftertouch |
| 2 | `55` | Analog Boost Int |
| 3 | `56` | Analog Boost Tune |
| 4 | `6F` | Arp Hold |
| 5 | `69` | Arp Mode |
| 6 | `6C` | Arp Note Length |
| 7 | `6E` | Arp Octaves |
| 8 | `6A` | Arp Pattern |
| 9 | `6B` | Arp Resolution |
| 10 | `6D` | Arp Swing |
| 11 | `48` | Assign 1 Amount 1 |
| 12 | `49` | Assign 2 Amount 1 |
| 13 | `4A` | Assign 2 Amount 2 |
| 14 | `4B` | Assign 3 Amount 1 |
| 15 | `4C` | Assign 3 Amount 2 |
| 16 | `4D` | Assign 3 Amount 3 |
| 17 | `73` | Assign 4 Amount 1 |
| 18 | `74` | Assign 5 Amount 1 |
| 19 | `75` | Assign 6 Amount 1 |
| 20 | `06` | Balance |
| 21 | `3E` | Bend Up |
| 22 | `3F` | Bend Down |
| 23 | `02` | Breath |
| 24 | `0F` | Channel Volume |
| 25 | `19` | Chorus Delay |
| 26 | `18` | Chorus Depth |
| 27 | `1A` | Chorus Feedback |
| 28 | `16` | Chorus Mix |
| 29 | `17` | Chorus Rate |
| 30 | `4E` | Clock Tempo |
| 31 | `03` | Control 03 |
| 32 | `07` | Control 09 |
| 33 | `09` | Control 12 |
| 34 | `0A` | Control 13 |
| 35 | `0B` | Control 14 |
| 36 | `0C` | Control 15 |
| 37 | `0D` | Control 16 |
| 38 | `05` | Data Entry |
| 39 | `54` | Delay Coloration |
| 40 | `1F` | Delay Depth |
| 41 | `1D` | Delay Feedback |
| 42 | `1E` | Delay Rate |
| 43 | `1C` | Delay Time |
| 44 | `57` | Distortion Intensity |
| 45 | `71` | EQ Mid Frequency |
| 46 | `70` | EQ Mid Gain |
| 47 | `72` | EQ Mid Q-Factor |
| 48 | `1B` | Effect Send (Delay) |
| 49 | `76` | Effect Send (Reverb) |
| 50 | `08` | Expression |
| 51 | `27` | Filter Env > FM Amount |
| 52 | `26` | Filter Env > Osc 2 Pitch |
| 53 | `2C` | Filter 1 Env Amount |
| 54 | `2E` | Filter 1 Key Follow |
| 55 | `2A` | Filter 1 Resonance |
| 56 | `2D` | Filter 2 Env Amount |
| 57 | `2F` | Filter 2 Key Follow |
| 58 | `2B` | Filter 2 Resonance |
| 59 | `7F` | Freq Shifter Mix *(LCD name)* |
| 60 | `04` | Foot Pedal |
| 61 | `58` | FreqShifter Frequency *(LCD name)* |
| 62 | `4F` | Input Thru |
| 63 | `30` | LFO 1 Contour |
| 64 | `5C` | LFO 1 > Assign Amount |
| 65 | `35` | LFO 1 > Filter Gain |
| 66 | `31` | LFO 1 > Osc 1 |
| 67 | `32` | LFO 1 > Osc 2 |
| 68 | `33` | LFO 1 > Pulse Width |
| 69 | `34` | LFO 1 > Resonance |
| 70 | `36` | LFO 2 Contour |
| 71 | `5D` | LFO 2 > Assign Amount |
| 72 | `39` | LFO 2 > Cutoff 1 |
| 73 | `3A` | LFO 2 > Cutoff 2 |
| 74 | `38` | LFO 2 > FM Amount |
| 75 | `3B` | LFO 2 > Panorama |
| 76 | `37` | LFO 2 > Shape |
| 77 | `3C` | LFO 3 Rate |
| 78 | `3D` | LFO 3 > Assign Amount |
| 79 | `01` | Modulation Wheel |
| 80 | `53` | Noise Color |
| 81 | `29` | Noise Volume |
| 82 | `50` | Osc Initial Phase |
| 83 | `79` | Osc 1 F-Shift |
| 84 | `7B` | Osc 1 F-Spread |
| 85 | `7D` | Osc 1 Interpolation |
| 86 | `23` | Osc 1 Key Follow |
| 87 | `77` | Osc 1 Local Detune |
| 88 | `22` | Osc 1 Pitch |
| 89 | `21` | Osc 1 Pulse Width |
| 90 | `20` | Osc 1 Wave Select |
| 91 | `7A` | Osc 2 F-Shift |
| 92 | `7C` | Osc 2 F-Spread |
| 93 | `7E` | Osc 2 Interpolation |
| 94 | `28` | Osc 2 Key Follow |
| 95 | `78` | Osc 2 Local Detune |
| 96 | `25` | Osc 2 Pulse Width |
| 97 | `24` | Osc 2 Wave Select |
| 98 | `5B` | Osc 3 Detune |
| 99 | `5A` | Osc 3 Pitch |
| 100 | `59` | Osc 3 Volume |
| 101 | `10` | Panorama |
| 102 | `0E` | Patch Volume |
| 103 | `60` | Phaser Depth |
| 104 | `62` | Phaser Feedback |
| 105 | `61` | Phaser Frequency |
| 106 | `5E` | Phaser Mix |
| 107 | `5F` | Phaser Rate |
| 108 | `63` | Phaser Spread |
| 109 | `12` | Portamento |
| 110 | `51` | Punch Intensity |
| 111 | `66` | Reverb Coloration |
| 112 | `65` | Reverb Dampening |
| 113 | `64` | Reverb Decay |
| 114 | `67` | Reverb Feedback |
| 115 | `52` | Ring Modulator |
| 116 | `68` | Surround Balance |
| 117 | `11` | Transpose |
| 118 | `13` | Unison Detune |
| 119 | `15` | Unison LFO Phase |
| 120 | `14` | Unison Spread |
| 121 | `41` | Velo > FM Amount |
| 122 | `42` | Velo > Filt 1 Env Amount |
| 123 | `43` | Velo > Filt 2 Env Amount |
| 124 | `47` | Velo > Panorama |
| 125 | `44` | Velo > Resonance 1 |
| 126 | `45` | Velo > Resonance 2 |
| 127 | `46` | Velo > Volume |

---

## Soft Knob Names

Soft Knob 1/2/3 **Name** LCD label — **`71`/`33`**, **`34`**, **`35`**.

88 panel options. **Index** is the **alphabetical** menu order on the Virus (e.g.
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

Mod Matrix slot **Source**.

40 options (`0`–`39`).

| Index | Option           |
| ----- | ---------------- |
| 0     | Off              |
| 1     | Pitch Bend       |
| 2     | Channel Pressure |
| 3     | Mod Wheel        |
| 4     | Breath           |
| 5     | Controller 3     |
| 6     | Foot Pedal       |
| 7     | Data Entry       |
| 8     | Balance          |
| 9     | Controller 9     |
| 10    | Expression       |
| 11    | Controller 12    |
| 12    | Controller 13    |
| 13    | Controller 14    |
| 14    | Controller 15    |
| 15    | Controller 16    |
| 16    | Hold Pedal       |
| 17    | Portamento Sw    |
| 18    | Sost Pedal       |
| 19    | Amp Envelope     |
| 20    | Filter Envelope  |
| 21    | Envelope 3       |
| 22    | Envelope 4       |
| 23    | LFO 1 bipolar    |
| 24    | LFO 1 unipolar   |
| 25    | LFO 2 bipolar    |
| 26    | LFO 2 unipolar   |
| 27    | LFO 3 bipolar    |
| 28    | LFO 3 unipolar   |
| 29    | Velocity On      |
| 30    | Velocity Off     |
| 31    | Key Follow       |
| 32    | Random           |
| 33    | Arp Input        |
| 34    | AnaKey1 Fine     |
| 35    | AnaKey 2 Fine    |
| 36    | AnaKey1 Coarse   |
| 37    | AnaKey2 Coarse   |
| 38    | 1% Constant      |
| 39    | 10% Constant     |

## Mod Matrix Destinations

Mod Matrix slot **Destination**.

122 options (`0`–`121`).

| Index | Option                   |
| ----- | ------------------------ |
| 0     | Off                      |
| 1     | Amp Env Attack           |
| 2     | Amp Env Decay            |
| 3     | Amp Env Slope            |
| 4     | Amp Env Sustain          |
| 5     | Amp Env Release          |
| 6     | Arp Note Length          |
| 7     | Arp Pattern              |
| 8     | Arp Swing Factor         |
| 9     | Chorus Delay             |
| 10    | Chorus Feedback          |
| 11    | Chorus Mix               |
| 12    | Chorus Mod Depth         |
| 13    | Chorus Mod Rate          |
| 14    | Delay Coloration         |
| 15    | Delay Feedback           |
| 16    | Delay Mod Depth          |
| 17    | Delay Mod Rate           |
| 18    | Delay Send               |
| 19    | Delay Time               |
| 20    | Distortion Intensity     |
| 21    | Distortion Mix           |
| 22    | EQ Mid Frequency         |
| 23    | EQ Mid Gain              |
| 24    | Filter Env > FM/Sync     |
| 25    | Filter Env > Osc 2 Pitch |
| 26    | Filter Balance           |
| 27    | Filter Env Attack        |
| 28    | Filter Env Decay         |
| 29    | Filter Env Slope         |
| 30    | Filter Env Sustain       |
| 31    | Filter Env Release       |
| 32    | Filter 1 Cutoff          |
| 33    | Filter 1 Env Amount      |
| 34    | Filter 1 Resonance       |
| 35    | Filter 2 Cutoff          |
| 36    | Filter 2 Env Amount      |
| 37    | Filter 2 Resonance       |
| 38    | Filterbank Poles         |
| 39    | Filterbank Resonance     |
| 40    | Filterbank Slope         |
| 41    | Filterbank Frequency     |
| 42    | LFO 1 > Assign Amount    |
| 43    | LFO 1 Contour            |
| 44    | LFO 1 Rate               |
| 45    | LFO 1 > Filter Gain      |
| 46    | LFO 1 > Osc 1 Pitch      |
| 47    | LFO 1 > Osc 2 Pitch      |
| 48    | LFO 1 > Pulse Width      |
| 49    | LFO 1 > Resonance        |
| 50    | LFO 2 > Assign Amount    |
| 51    | LFO 2 Contour            |
| 52    | LFO 2 Rate               |
| 53    | LFO 2 > Cutoff 1         |
| 54    | LFO 2 > Cutoff 2         |
| 55    | LFO 2 > FM Amount        |
| 56    | LFO 2 > Panorama         |
| 57    | LFO 2 > Shape            |
| 58    | LFO 3 > Assign Amount    |
| 59    | LFO 3 Rate               |
| 60    | Noise Color              |
| 61    | Noise Volume             |
| 62    | Oscillator Balance       |
| 63    | Oscillator Volume        |
| 64    | Osc 1 F-Shift            |
| 65    | Osc 1 F-Spread           |
| 66    | Osc 1 Interpolation      |
| 67    | Osc 1 Pitch              |
| 68    | Osc 1 Pulse Width        |
| 69    | Osc 1 Shape/Index        |
| 70    | Osc 1 Wave Select        |
| 71    | Osc 2 Detune             |
| 72    | Osc 2 FM Amount          |
| 73    | Osc 2 F-Shift            |
| 74    | Osc 2 F-Spread           |
| 75    | Osc 2 Interpolation      |
| 76    | Osc 2 Pitch              |
| 77    | Osc 2 Pulse Width        |
| 78    | Osc 2 Shape/Index        |
| 79    | Osc 2 Wave Select        |
| 80    | Osc 3 Detune             |
| 81    | Osc 3 Pitch              |
| 82    | Osc 3 Volume             |
| 83    | Sub Osc Volume           |
| 84    | Pan Spread               |
| 85    | Panorama                 |
| 86    | Patch Volume             |
| 87    | Phaser Feedback          |
| 88    | Phaser Frequency         |
| 89    | Phaser Mix               |
| 90    | Phaser Mod Depth         |
| 91    | Phaser Mod Rate          |
| 92    | Portamento               |
| 93    | Punch Intensity          |
| 94    | Reverb Send              |
| 95    | Reverb Coloration        |
| 96    | Reverb Dampening         |
| 97    | Reverb Time              |
| 98    | Reverb PreDelay          |
| 99    | Ring Modulator           |
| 100   | Slot 1 Amount 1          |
| 101   | Slot 1 Amount 2          |
| 102   | Slot 1 Amount 3          |
| 103   | Slot 2 Amount 1          |
| 104   | Slot 2 Amount 2          |
| 105   | Slot 2 Amount 3          |
| 106   | Slot 3 Amount 1          |
| 107   | Slot 3 Amount 2          |
| 108   | Slot 3 Amount 3          |
| 109   | Slot 4 Amount 1          |
| 110   | Slot 4 Amount 2          |
| 111   | Slot 4 Amount 3          |
| 112   | Slot 5 Amount 1          |
| 113   | Slot 5 Amount 2          |
| 114   | Slot 5 Amount 3          |
| 115   | Slot 6 Amount 1          |
| 116   | Slot 6 Amount 2          |
| 117   | Slot 6 Amount 3          |
| 118   | Surround Balance         |
| 119   | Transpose                |
| 120   | Unison Detune            |
| 121   | Unison LFO Phase         |

## Wavetable Names

Oscillator **Wavetable** wave select names (`cmd=0x70`, `param=0x13`,
**Mode `02`**).
**Wire** = index **`00`–`63`** for panel indices **0–99**. Order confirmed
on TI mk2 hardware (full **+** sweep).

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

## Osc 1 Classic — Pulse Width (LCD)

Hardware sweep for **Osc 1 Pulse Width** (`cmd=0x70`, `param=0x12`, **Shape ≥ `40`**).
**Wire:** `pct = 50 + stored × 50 / 127` — see
[single-live-edit.md — Pulse Width](single-live-edit.md#pulse-width-shape--sawtooth).
**LCD:** `round(pct + 0.4, 0.1)` in most of the range (partial map below; not every
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
[single-live-edit.md — Density](single-live-edit.md#oscillator-1--hypersaw).
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
