# Arpeggiator

Edit Single — **Arpeggiator** (**EDIT ARP** on the panel).

Part of [Live Edit](README.md). Enumerated options:
[parameter-options.md](../parameter-options.md).
Dump worksheet: [Single parameter map](../dumps/single.md#arpeggiator)
· Multi: [Edit Multi](edit-multi.md).

```text
F0 00 20 33 01 00 71 <part> <param> <value> F7 # Page B (EDIT ARP settings)
F0 00 20 33 01 00 6E <part> <param> <value> F7 # Part buffer (loop length, …)
F0 00 20 33 01 00 6F <part> <param> <value> F7 # User-pattern step data
```

Param IDs are **not global** — **`0x0F`** on **`cmd=0x71`** is **Arpeggiator Mode**, not
[Multi Tempo / Master Clock](edit-single.md#multi-tempo--master-clock-0x0f-cmd0x72) on
**`cmd=0x72`**. User-pattern **Loop Length** uses **`6E`/`7F`** — not
[Oscillators SELECT](../oscillators.md#oscillators-select) (`71`/`7F`).

## Panel reference

**LCD:** **EDIT ARP**. Which rows appear depends on **Mode** — see
[Arpeggiator panel visibility](../parameter-options.md#arpeggiator-panel-visibility).
**Mode** = **Off** → **Mode** only. **Mode** = **Down** → **Mode** + **Hold**.
Full settings (**Up**, **Up&Down**, **As Played**, **Random**, **Chord**) → six
rows. **Arp>Matrix** → **Pattern** + **Resolution** only — see
[Arpeggiator panel visibility](../parameter-options.md#arpeggiator-panel-visibility).

## Settings

**`DUMP_SINGLE`** offsets (Single edit buffer **`30 00 40`**, `<part>=0x40`; TI mk2
dump correlate):

| Control     | Live edit | Dump offset |
| ----------- | --------- | ----------- |
| Mode        | `71`/`0F` | **`0x097`** |
| Pattern     | `71`/`02` | **`0x08A`** |
| Octaves     | `71`/`03` | **`0x08B`** |
| Hold        | `71`/`04` | **`0x08C`** |
| Note Length | `71`/`05` | **`0x08D`** |
| Swing       | `71`/`06` | **`0x08E`** |
| Resolution  | `71`/`11` | **`0x099`** |

### Mode (`0x0F`, `cmd=0x71`) {#arpeggiator-mode-cmd0x71-param-0x0f}

**EDIT ARP → Mode**. **`stored = index`**
— full list in [Arpeggiator Mode](../parameter-options.md#arpeggiator-mode).
**Off** (`00`) disables the arpeggiator; any other mode runs the arp with that
pattern direction. The front-panel **ARP** on/off control selects **Up** (`01`)
when enabled in hardware tests.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 0F <value> F7` |
| Panel range    | Off … Arp>Matrix (`00`–`07`)                |
| Confirmed      | Hardware TX (TI mk2)                        |

```text
F0 00 20 33 01 00 71 00 0F 00 F7 # Off (arp disabled)
F0 00 20 33 01 00 71 00 0F 01 F7 # Up (panel ARP on)
F0 00 20 33 01 00 71 00 0F 02 F7 # Down
F0 00 20 33 01 00 71 00 0F 03 F7 # Up&Down
F0 00 20 33 01 00 71 00 0F 04 F7 # As Played
F0 00 20 33 01 00 71 00 0F 05 F7 # Random
F0 00 20 33 01 00 71 00 0F 06 F7 # Chord
F0 00 20 33 01 00 71 00 0F 07 F7 # Arp>Matrix
```

### Pattern (`0x02`, `cmd=0x71`) {#arpeggiator-pattern-cmd0x71-param-0x02}

**EDIT ARP → Pattern**. **`stored = <value>`** — **User** (`00`), presets **2**–
**64** (`01`–`3F`; LCD = **`stored + 1`**). Full map:
[Arpeggiator Pattern](../parameter-options.md#arpeggiator-pattern). Hidden when
**Mode** = **Off** or **Down** (visible on full settings modes and **Arp>Matrix**).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 02 <value> F7`          |
| Panel range    | User, **2** … **64** (`00`–`3F`)                     |
| Confirmed      | Hardware TX (TI mk2; full settings + **Arp>Matrix**) |

```text
F0 00 20 33 01 00 71 00 02 00 F7 # User
F0 00 20 33 01 00 71 00 02 01 F7 # 2
F0 00 20 33 01 00 71 00 02 3F F7 # 64
```

### Octaves (`0x03`, `cmd=0x71`) {#arpeggiator-octaves-cmd0x71-param-0x03}

**EDIT ARP → Octaves**.
**`stored = octaves − 1`** (**`00`–`03`** → LCD **1**–**4**). Enum:
[Arpeggiator Octaves](../parameter-options.md#arpeggiator-octaves). Full settings
modes only — hidden when **Mode** = **Off**, **Down**, or **Arp>Matrix**.

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 03 <value> F7` |
| Panel range    | **1**–**4** octaves (`00`–`03`)             |
| Confirmed      | Hardware TX (TI mk2; full settings modes)   |

```text
F0 00 20 33 01 00 71 00 03 00 F7 # 1 octave
F0 00 20 33 01 00 71 00 03 03 F7 # 4 octaves
```

### Resolution (`0x11`, `cmd=0x71`) {#arpeggiator-resolution-cmd0x71-param-0x11}

**EDIT ARP → Resolution**. **`stored = <value>`** — tempo grid **1/128** …
**1/2**; full map in
[Arpeggiator Resolution](../parameter-options.md#arpeggiator-resolution). Hidden
when **Mode** = **Off** or **Down** (visible on full settings modes and
**Arp>Matrix**).

| Item           | Value                                                |
| -------------- | ---------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 11 <value> F7`          |
| Panel range    | **1/128** … **1/2** (`01`–`11`; no **Off**)          |
| Confirmed      | Hardware TX (TI mk2; full settings + **Arp>Matrix**) |

```text
F0 00 20 33 01 00 71 00 11 01 F7 # 1/128
F0 00 20 33 01 00 71 00 11 11 F7 # 1/2
```

### Note Length (`0x05`, `cmd=0x71`) {#arpeggiator-note-length-cmd0x71-param-0x05}

**EDIT ARP → Note Length**. Bipolar **`stored = ui + 64`** — LCD curve:
[Arpeggiator Note Length](../parameter-options.md#arpeggiator-note-length-lcd).
Full settings modes only — hidden when **Mode** = **Off**, **Down**, or
**Arp>Matrix**.

| Item           | Value                                             |
| -------------- | ------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 05 <value> F7`       |
| Panel range    | **−100.0..+100.0 %** (`00`–`7F`; **+0 %** @ `40`) |
| Confirmed      | Hardware TX (TI mk2; full settings modes)         |

```text
F0 00 20 33 01 00 71 00 05 00 F7 # −100.0 %
F0 00 20 33 01 00 71 00 05 40 F7 # +0.0 %
F0 00 20 33 01 00 71 00 05 7F F7 # +100.0 %
```

### Swing Factor (`0x06`, `cmd=0x71`) {#arpeggiator-swing-factor-cmd0x71-param-0x06}

**EDIT ARP → Swing Factor**. **`00`** = **Off**; **`01`–`7F`** = swing amount —
mostly **XX.X %**, with five **16x** shorthand labels (**16B**–**16F**) at sparse
wire values. LCD map: [Arpeggiator Swing Factor](../parameter-options.md#arpeggiator-swing-factor-lcd).
Full settings modes only — hidden when **Mode** = **Off**, **Down**, or
**Arp>Matrix**.

| Item           | Value                                         |
| -------------- | --------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 06 <value> F7`   |
| Panel range    | **Off**; **50.2..75.0 %** + **16B** … **16F** |
| Confirmed      | Hardware TX (TI mk2; full settings modes)     |

```text
F0 00 20 33 01 00 71 00 06 00 F7 # Off
F0 00 20 33 01 00 71 00 06 01 F7 # 50.2 %
F0 00 20 33 01 00 71 00 06 15 F7 # 16B
F0 00 20 33 01 00 71 00 06 42 F7 # 16D
F0 00 20 33 01 00 71 00 06 7F F7 # 75.0 %
```

### Hold (`0x04`, `cmd=0x71`) {#arpeggiator-hold-cmd0x71-param-0x04}

**EDIT ARP → Hold**. **`00`** = **Off**,
**`01`** = **On** — [Arpeggiator Hold](../parameter-options.md#arpeggiator-hold).
Hidden when **Mode** = **Off** or **Arp>Matrix**. On **Down**, the only setting
besides **Mode**; on full settings modes, last row of the block.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 04 <value> F7`         |
| Panel range    | **Off** / **On** (`00` / `01`)                      |
| Confirmed      | Hardware TX (TI mk2; **Down**, full settings modes) |

```text
F0 00 20 33 01 00 71 40 04 00 F7 # Off (Single edit buffer)
F0 00 20 33 01 00 71 40 04 01 F7 # On
```

## Pattern editor

User-pattern programming (**Pattern** = **User**). Settings use **`cmd=0x71`**;
**loop length** uses **`cmd=0x6E`**; per-step data uses **`cmd=0x6F`** (three
params per step — [step triplet](../parameter-options.md#arpeggiator-step-triplet)).

The same values live in **`DUMP_SINGLE`** — host editors typically patch the
524-byte single buffer and transmit the whole dump, rather than stepping through
**32** live-edit messages per field.

### User pattern in `DUMP_SINGLE` {#arpeggiator-user-pattern-dump}

Correlated from **`-INIT-`** baseline ([`init-multi-arrangement.syx`](../artifacts/sysex/init-multi-arrangement.syx)
Part 1, 524-byte single). Dump byte order matches the live-edit triplet
(**length**, **velocity**, **enable**).

| Field         | Dump offset (step *n*)    | Encoding                                                    |
| ------------- | ------------------------- | ----------------------------------------------------------- |
| Loop length   | **`0x189`**               | **`stored = steps − 1`**                                    |
| Step length   | **`0x18A + (n − 1) × 3`** | same as [Step Length](#arpeggiator-step-length-cmd0x6f)     |
| Step velocity | **+1** from step base     | same as [Step Velocity](#arpeggiator-step-velocity-cmd0x6f) |
| Step enable   | **+2** from step base     | same as [Step Enable](#arpeggiator-step-enable-cmd0x6f)     |

Step **1** → **`0x18A`…`0x18C`**; step **32** → **`0x1E7`…`0x1E9`**. On
**`-INIT-`**, loop length = **`0x1F`** (32 steps); each step length =
**`0x40`** (+0 %), velocity = **`0x64`** (100), enable alternates **`01`** /
**`00`**.

Worksheet: [Single parameter map](../dumps/single.md#arpeggiator).

### Loop Length (`0x7F`, `cmd=0x6E`) {#arpeggiator-loop-length-cmd0x6e-param-0x7f}

User arpeggiator pattern **loop length** — **1**–**32** steps.
**`stored = steps − 1`** (**`00`–`1F`**). Enum anchors:
[Arpeggiator Loop Length](../parameter-options.md#arpeggiator-loop-length).

| Item           | Value                                       |
| -------------- | ------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6E <part> 7F <value> F7` |
| Panel range    | **1**–**32** steps (`00`–`1F`)              |
| Confirmed      | SysEx TX (TI mk2)                           |

```text
F0 00 20 33 01 00 6E 00 7F 00 F7 # 1 step
F0 00 20 33 01 00 6E 00 7F 01 F7 # 2 steps
F0 00 20 33 01 00 6E 00 7F 0F F7 # 16 steps
F0 00 20 33 01 00 6E 00 7F 1F F7 # 32 steps
```

### Step Length (`cmd=0x6F`) {#arpeggiator-step-length-cmd0x6f}

User-pattern **step length** — steps **1**–**32**. Param **`(step − 1) × 3`**
(step **1** → **`00`**, step **32** → **`5D`**). Standard Virus bipolar **%**
encoding **`stored = ui + 64`** — same family as [Arpeggiator Note
Length](../parameter-options.md#arpeggiator-note-length-lcd). Map:
[Arpeggiator Step Length](../parameter-options.md#arpeggiator-step-length).

| Item           | Value                                                    |
| -------------- | -------------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 6F <part> <param> <value> F7`         |
| Step *n* param | **`(n − 1) × 3`** (`00` … `5D`)                          |
| Panel range    | **−100.0..+100.0 %** (`00`–`7F`; **+0.0 %** @ `40`)      |
| Confirmed      | Param stride (step **32** → **`5D`**); SysEx TX (TI mk2) |

```text
F0 00 20 33 01 00 6F 00 5D 00 F7 # Step 32 length −100.0 %
F0 00 20 33 01 00 6F 00 5D 40 F7 # Step 32 length +0.0 %
F0 00 20 33 01 00 6F 00 5D 7F F7 # Step 32 length +100.0 %
```

### Step Velocity (`cmd=0x6F`) {#arpeggiator-step-velocity-cmd0x6f}

User-pattern **step velocity** — steps **1**–**32**. Param
**`0x01 + (step − 1) × 3`**; **`stored = lcd`** (**`00`–`7F`**). Map:
[Arpeggiator Step Velocity](../parameter-options.md#arpeggiator-step-velocity).

| Item           | Value                                            |
| -------------- | ------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6F <part> <param> <value> F7` |
| Step *n* param | **`0x01 + (n − 1) × 3`** (`01` … `5E`)           |
| Value encoding | **`0`–`127`** direct                             |
| Confirmed      | SysEx TX (TI mk2; all **32** steps)              |

```text
F0 00 20 33 01 00 6F 00 01 00 F7 # Step 1 velocity 0
F0 00 20 33 01 00 6F 00 01 7F F7 # Step 1 velocity 127
F0 00 20 33 01 00 6F 00 5E 7F F7 # Step 32 velocity 127
```

### Step Enable (`cmd=0x6F`) {#arpeggiator-step-enable-cmd0x6f}

User-pattern **step on/off** — steps **1**–**32**. Param
**`0x02 + (step − 1) × 3`**; **`00`** off, **`01`** on. Map:
[Arpeggiator Step Enable](../parameter-options.md#arpeggiator-step-enable).

| Item           | Value                                            |
| -------------- | ------------------------------------------------ |
| Message format | `F0 00 20 33 01 00 6F <part> <param> <value> F7` |
| Step *n* param | **`0x02 + (n − 1) × 3`** (`02` … `5F`)           |
| Value encoding | **`00`** off · **`01`** on                       |
| Confirmed      | SysEx TX (TI mk2; steps **1**–**32**)            |

```text
F0 00 20 33 01 00 6F 00 02 00 F7 # Step 1 off
F0 00 20 33 01 00 6F 00 02 01 F7 # Step 1 on
F0 00 20 33 01 00 6F 00 5F 01 F7 # Step 32 on
```
