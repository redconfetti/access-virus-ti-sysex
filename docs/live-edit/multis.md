# Edit Multi

Part of [Documentation](../../README.md#documentation). Paging:
[virus.md](../misc/virus.md#paging).

Live SysEx notes for Multi edit behavior.

```text
F0 00 20 33 01 00 72 <part> <param> <value> F7
```

Some parameters use **`cmd=0x71`** instead of **`0x72`** (same byte layout):

```text
F0 00 20 33 01 00 71 <part> <param> <value> F7
```

**Secondary Output** uses **`cmd=0x73`** — see [Secondary Output](#secondary-output).

- **`<part>`** — zero-based part index (`00` = Part 1, `0F` = Part 16)
- **`<param>`** — Multi edit parameter ID
- **`<value>`** — parameter value (encoding depends on parameter)

Single-related live edits (`cmd=0x6E`, `cmd=0x10`) are in
[single.md](single/single.md).

Enumerated options: [parameter-options.md](../reference/parameter-options.md).

## Summary

| Param ID | Memory / Target              | Parameter        | Description                                  |
| -------- | ---------------------------- | ---------------- | -------------------------------------------- |
| `0x0F`   | Global (`0x18` in dump)      | Master Clock     | Global Multi tempo                           |
| `0x23`   | `0x59 + part`                | Low Key          | Part low key limit                           |
| `0x24`   | `0x69 + part`                | High Key         | Part high key limit                          |
| `0x25`   | `0x79 + part`                | Transpose        | Part transposition                           |
| `0x26`   | `0x89 + part`                | Detune           | Part detune                                  |
| `0x1A`   | **Not in dump**              | Bend Up          | Pitch bend up limit (`cmd=0x71`)             |
| `0x1B`   | **Not in dump**              | Bend Down        | Pitch bend down limit (`cmd=0x71`)           |
| `0x27`   | `0x99 + (part−1)`            | Volume           | Part level (Part 16 at `0xA8`)               |
| `0x20`   | `0x29 + (part−1)`            | Bank             | Single bank index (P1 at `0x29`)             |
| `0x21`   | `0x39 + (part−1)`            | Program          | Single program 0–127 (P1 at `0x39`)          |
| `0x22`   | `0x49 + (part−1)`            | MIDI Channel     | Part MIDI channel 1–16 (P1 at `0x49`)        |
| `0x28`   | `0xA9 + (part−1)`            | Init Volume      | MIDI volume on multi select (Part 16 `0xB8`) |
| `0x29`   | `0xC8 + part`                | Output Routing   | Part output bus and channel                  |
| `0x2D`   | **Not in dump** (`cmd=0x73`) | Secondary Output | Second output bus (`cmd=0x73`)               |
| `0x2B`   | `0xD8 + part`                | Panorama         | Part pan position                            |
| `0x40`   | **Not in dump** (desktop)    | Keyboard-related | Keyboard global behavior control             |
| `0x48`   | `0xF8 + part` (packed flags) | Enable           | Part on/off                                  |
| `0x49`   | `0xF8 + part` (packed flags) | Volume RX        | Receive MIDI CC#7                            |
| `0x4A`   | `0xF8 + part` (packed flags) | Hold Pedal       | Sustain pedal behavior                       |
| `0x4D`   | `0xF8 + part` (packed flags) | Priority         | Note-steal priority                          |
| `0x4E`   | `0xF8 + part` (packed flags) | Program Change   | Program Change response                      |

**Not in this table (not in Multi Dump):** **Secondary Output** (`73` /
`0x2D`), **Bend Up/Down** (`71` / `0x1A`, `0x1B` — in **Single Dump**
only), **Direct Monitoring** (VC **Live**). See
[Runtime-only Edit Multi](../dumps/multi.md#runtime-only-edit-multi).
**Solo** in some host UIs manipulates **`0x48` Enable** on other parts.

## Parameters

Each section below follows the live-edit doc pattern: **Live edit** wire bytes,
panel path, Multi Dump offset (when stored), value table, and example SysEx.

### Master Clock Tempo

**Live edit:** `cmd=0x72`, param `0x0F`.

**Edit Multi → Master Clock** — global Multi tempo (not per-part). Multi Dump
byte **`0x18`** (after the 10-byte name at `0x0D`–`0x16` and null at `0x17`).

Encoding: **`stored = bpm − 63`** (UI **63..190** → **`00`..`7F`**).

| BPM | `<value>` |
| --- | --------- |
| 63  | `00`      |
| 120 | `39`      |
| 124 | `3D`      |
| 190 | `7F`      |

```text
F0 00 20 33 01 00 72 00 0F 39 F7 # 120 bpm
F0 00 20 33 01 00 72 00 0F 3D F7 # 124 bpm
```

Use **`<part>=0x00`** in captures; tempo is global for the Multi.

### Low Key

**Live edit:** `cmd=0x72`, param `0x23`.

**Edit Multi → Part *n* → Low Key** — lowest note the part responds to. Multi
Dump byte **`0x59 + part`** (direct note index, C1..G9 domain).

| Notes | `<value>`  |
| ----- | ---------- |
| C1    | `00`       |
| …     | `00`..`7F` |
| G9    | `7F`       |

```text
F0 00 20 33 01 00 72 00 23 00 F7 # Part 1 Low Key C1
F0 00 20 33 01 00 72 0F 23 00 F7 # Part 16 Low Key C1
```

### High Key

**Live edit:** `cmd=0x72`, param `0x24`.

**Edit Multi → Part *n* → High Key** — highest note the part responds to. Multi
Dump byte **`0x69 + part`**.

| Notes | `<value>`  |
| ----- | ---------- |
| C1    | `00`       |
| …     | `00`..`7F` |
| G9    | `7F`       |

```text
F0 00 20 33 01 00 72 00 24 00 F7 # Part 1 High Key C1
F0 00 20 33 01 00 72 0F 24 7F F7 # Part 16 High Key G9
```

### Transpose

**Live edit:** `cmd=0x72`, param `0x25`.

**Edit Multi → Part *n* → Transpose** — semitone offset added to the part’s
Single. Multi Dump byte **`0x79 + part`**. **Live** and **dump** encodings
differ — table below is the **live-edit** wire map.

| UI (live) | `<value>` |
| --------- | --------- |
| −63       | `00`      |
| +1        | `40`      |
| +64       | `7F`      |

```text
F0 00 20 33 01 00 72 00 25 00 F7 # Part 1 transpose minimum
F0 00 20 33 01 00 72 01 25 7F F7 # Part 2 transpose maximum
```

Dump storage uses **`stored = ui + 64`** (−48..+48 semitones) at the same
offset — see [multi.md](../dumps/multi.md#transpose).

### Detune

**Live edit:** `cmd=0x72`, param `0x26`.

**Edit Multi → Part *n* → Detune** — fine pitch offset. Multi Dump byte
**`0x89 + part`**. Live and dump both use **`stored = ui + 64`**
(UI **−64..+63**).

| UI    | `<value>` |
| ----- | --------- |
| −64   | `00`      |
| 0     | `40`      |
| +63   | `7F`      |

```text
F0 00 20 33 01 00 72 00 26 00 F7 # Part 1 detune minimum
F0 00 20 33 01 00 72 00 26 40 F7 # Part 1 detune 0
F0 00 20 33 01 00 72 00 26 7F F7 # Part 1 detune maximum
```

### Bend Up

**Live edit:** `cmd=0x71`, param `0x1A`.

**Edit Multi → Part *n* → Bend Up** — same control as **Edit Single → Common →
Bend Up**. Sent via **`cmd=0x71`**, not **`0x72`**. **Not in Multi Dump** —
stored in **Single Dump** for the part Single. See
[multi.md — Bend limits](../dumps/multi.md#bend-limits-not-in-multi-dump).

Encoding: **`stored = ui + 64`** (UI **−64..+63**).

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| 0   | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 00 1A 00 F7 # −64
F0 00 20 33 01 00 71 00 1A 40 F7 # 0
F0 00 20 33 01 00 71 00 1A 7F F7 # +63
```

### Bend Down

**Live edit:** `cmd=0x71`, param `0x1B`.

**Edit Multi → Part *n* → Bend Down** — same encoding and transport as
[Bend Up](#bend-up). **Not in Multi Dump**.

| UI  | `<value>` |
| --- | --------- |
| −64 | `00`      |
| 0   | `40`      |
| +63 | `7F`      |

```text
F0 00 20 33 01 00 71 00 1B 00 F7 # −64
F0 00 20 33 01 00 71 00 1B 40 F7 # 0
F0 00 20 33 01 00 71 00 1B 7F F7 # +63
```

### Volume

**Live edit:** `cmd=0x72`, param `0x27`.

**Edit Multi → Part *n* → Volume** — part balance / level. Multi Dump bytes
**`0x99..0xA8`** (`0x99 + (part−1)`; Part 16 at **`0xA8`**). Live encoding
matches [Transpose](#transpose) live wire map (**−63..+64**, not dump **`ui + 64`**
).

| UI (live) | `<value>` |
| --------- | --------- |
| −63       | `00`      |
| +1        | `40`      |
| +64       | `7F`      |

```text
F0 00 20 33 01 00 72 00 27 40 F7 # Part 1 volume (example)
F0 00 20 33 01 00 72 0F 27 6E F7 # Part 16 volume +46 → dump 0x6E at 0xA8
```

### Init Volume

**Live edit:** `cmd=0x72`, param `0x28`.

**Edit Multi → Part *n* → Init Volume** — MIDI volume (CC#7) applied when the
Multi is selected. Multi Dump bytes **`0xA9..0xB8`** (`0xA9 + (part−1)`).

| UI      | `<value>`  |
| ------- | ---------- |
| Off     | `00`       |
| 1..127  | `01`..`7F` |

```text
F0 00 20 33 01 00 72 00 28 00 F7 # Part 1 Init Volume off
F0 00 20 33 01 00 72 00 28 40 F7 # Part 1 Init Volume 64
```

### Bank

**Live edit:** `cmd=0x72`, param `0x20`.

**Edit Multi → Part *n* → Bank** — which Single bank the part loads from. Multi
Dump byte **`0x29 + (part−1)`**. Live value = [Part bank index](../dumps/multi.md#part-bank-index)
(`00` = RAM A, `01` = RAM B, `04` = ROM A, …).

| Bank (example) | `<value>` |
| -------------- | --------- |
| RAM A          | `00`      |
| RAM B          | `01`      |

```text
F0 00 20 33 01 00 72 00 20 00 F7 # Part 1 → RAM A
F0 00 20 33 01 00 72 00 20 01 F7 # Part 1 → RAM B (LCD RAM-B)
```

### Program

**Live edit:** `cmd=0x72`, param `0x21`.

**Edit Multi → Part *n* → Program** — program number within the selected bank.
Multi Dump byte **`0x39 + (part−1)`** — stored byte equals UI program number
(`00` = 0, `40` = 64, `41` = 65).

| UI program | `<value>` |
| ---------- | --------- |
| 0          | `00`      |
| 64         | `40`      |
| 65         | `41`      |

```text
F0 00 20 33 01 00 72 00 21 00 F7 # Part 1 program 0
F0 00 20 33 01 00 72 00 21 41 F7 # Part 1 program 65
```

To load a stored Single into a part: set **Bank** / **Program** via **`0x72`**, then
**Single Dump** upload (`0x10`):

```text
F0 00 20 33 01 00 72 00 20 00 F7  # Part 1 → RAM A
F0 00 20 33 01 00 72 00 21 40 F7  # Part 1 → program 64
```

### MIDI Channel

**Live edit:** `cmd=0x72`, param `0x22`.

**Edit Multi → Part *n* → MIDI Channel** — part MIDI channel (**1–16**). Multi
Dump byte **`0x49 + (part−1)`**. Wire value is **zero-based** (channel **1** →
**`00`**, channel **16** → **`0F`**).

| MIDI channel | `<value>` |
| ------------ | --------- |
| 1            | `00`      |
| 2            | `01`      |
| 16           | `0F`      |

```text
F0 00 20 33 01 00 72 00 22 00 F7 # Part 1 channel 1
F0 00 20 33 01 00 72 00 22 01 F7 # Part 1 channel 2
F0 00 20 33 01 00 72 00 22 0F F7 # Part 1 channel 16
```

### Output Routing

**Live edit:** `cmd=0x72`, param `0x29`.

**Edit Multi → Part *n* → Output** — analog/USB output bus and channel. Multi
Dump byte **`0xC8 + part`**.

| `<value>` | Routing          |
| --------- | ---------------- |
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R |
| `06`–`08` | Out 3: L, L+R, R |
| `09`–`0B` | USB 1: L, L+R, R |
| `0C`–`0E` | USB 2: L, L+R, R |
| `0F`–`11` | USB 3: L, L+R, R |

```text
F0 00 20 33 01 00 72 00 29 00 F7 # Part 1 Out 1 L
F0 00 20 33 01 00 72 00 29 03 F7 # Part 1 Out 2 L
```

Full labels: [parameter-options.md](../reference/parameter-options.md).

### Secondary Output

**Live edit:** `cmd=0x73`, param `0x2D`.

**Edit Multi → Part *n* → Secondary Output** — rear/surround bus (same wire as
**Edit Single → Surround → Output**). **Not in Multi Dump**. Enum:
[Secondary output routing](../reference/parameter-options.md#secondary-output-routing).

**`00`** = Off; otherwise **`stored = primary_index + 1`** through **`12`**
(USB 3 R) — same routes as [Output Routing](#output-routing).

```text
F0 00 20 33 01 00 73 00 2D 00 F7 # Edit Multi Part 1 — Off
F0 00 20 33 01 00 73 00 2D 01 F7 # Out 1 L
F0 00 20 33 01 00 73 00 2D 0A F7 # USB 1 L
F0 00 20 33 01 00 73 40 2D 04 F7 # Single edit buffer — Out 2 L
```

Single mode uses **`<part>=0x40`**. See
[multi.md](../dumps/multi.md#secondary-output-not-in-multi-dump).

### Panorama

**Live edit:** `cmd=0x72`, param `0x2B`.

**Edit Multi → Part *n* → Panorama** — overrides the Single’s pan for this part.
Multi Dump byte **`0xD8 + part`**. Direct wire values (not bipolar **`ui + 64`**
).

| Setting | `<value>` |
| ------- | --------- |
| Off     | `00`      |
| Center  | `40`      |

```text
F0 00 20 33 01 00 72 00 2B 00 F7 # Part 1 Panorama off
F0 00 20 33 01 00 72 00 2B 40 F7 # Part 1 Panorama center
```

### Keyboard-related

**Live edit:** `cmd=0x72`, param `0x40`.

**Edit Multi → Keyboard to MIDI** (desktop: no keyboard hardware; wire still
accepted). Global scope — use **`<part>=0x00`**. **Not in Multi Dump** on the
desktop module.

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `01`  | On      |

```text
F0 00 20 33 01 00 72 00 40 00 F7 # Off
F0 00 20 33 01 00 72 00 40 01 F7 # On
```

### Enable

**Live edit:** `cmd=0x72`, param `0x48`.

**Edit Multi → Part *n* → Enable** — part on/off. Packed flag at Multi Dump
**`0xF8 + part`** (bit **`0x01`**: INIT **`0x45`**; off **`0x44`**, on
**`0x45`**). Host **Mute** / **Solo** UIs may toggle this flag.

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `01`  | On      |

```text
F0 00 20 33 01 00 72 00 48 00 F7 # Part 1 off
F0 00 20 33 01 00 72 00 48 01 F7 # Part 1 on
F0 00 20 33 01 00 72 07 48 00 F7 # Part 8 off (dump 0x100: 0x45→0x44)
F0 00 20 33 01 00 72 0F 48 00 F7 # Part 16 off
F0 00 20 33 01 00 72 0F 48 01 F7 # Part 16 on
```

Several booleans share one byte per part — diff from INIT (`0x45`) when
probing one flag; see [Packed flags](../dumps/multi.md#packed-flags-at-0xf8--part).

### Volume RX

**Live edit:** `cmd=0x72`, param `0x49`.

**Edit Multi → Part *n* → Volume RX** — receive MIDI CC#7 for this part. Packed
flag at **`0xF8 + part`** (**`+0x02`** when enabled).

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `01`  | On      |

```text
F0 00 20 33 01 00 72 00 49 00 F7 # Part 1 Volume RX off
F0 00 20 33 01 00 72 00 49 01 F7 # Part 1 Volume RX on
F0 00 20 33 01 00 72 0F 49 00 F7 # Part 16 Volume RX off
F0 00 20 33 01 00 72 0F 49 01 F7 # Part 16 Volume RX on
```

### Hold Pedal

**Live edit:** `cmd=0x72`, param `0x4A`.

**Edit Multi → Part *n* → Hold Pedal** — sustain pedal (MIDI CC#64) behavior.
Packed flag at **`0xF8 + part`**.

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `01`  | On      |

```text
F0 00 20 33 01 00 72 00 4A 00 F7 # Part 1 Hold Pedal off
F0 00 20 33 01 00 72 00 4A 01 F7 # Part 1 Hold Pedal on
F0 00 20 33 01 00 72 0F 4A 00 F7 # Part 16 Hold Pedal off
F0 00 20 33 01 00 72 0F 4A 01 F7 # Part 16 Hold Pedal on
```

### Priority

**Live edit:** `cmd=0x72`, param `0x4D`.

**Edit Multi → Part *n* → Priority** — voice-steal priority when voices are
exhausted. Packed flag at **`0xF8 + part`** (**`+0x20`** for High).

| Value | Meaning |
| ----- | ------- |
| `00`  | Low     |
| `01`  | High    |

```text
F0 00 20 33 01 00 72 00 4D 00 F7 # Part 1 Priority Low
F0 00 20 33 01 00 72 0F 4D 01 F7 # Part 16 Priority High
```

### Program Change

**Live edit:** `cmd=0x72`, param `0x4E`.

**Edit Multi → Part *n* → Program Change** — MIDI Program Change response.
Packed flag at **`0xF8 + part`** (**`±0x40`** vs INIT).

| Value | Meaning |
| ----- | ------- |
| `00`  | Off     |
| `01`  | On      |

```text
F0 00 20 33 01 00 72 00 4E 00 F7 # Part 1 Program Change off
F0 00 20 33 01 00 72 0F 4E 00 F7 # Part 16 Program Change off
F0 00 20 33 01 00 72 0F 4E 01 F7 # Part 16 Program Change on
```
