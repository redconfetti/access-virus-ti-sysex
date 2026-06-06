# Arpeggiator

Edit Single — **Arpeggiator** (**EDIT ARP** on the panel).

Part of [Live Edit](README.md). Enumerated options:
[parameter-options.md](../parameter-options.md).
Dump worksheet: [Single parameter map](../dumps/single.md#arpeggiator)
· Multi: [Edit Multi](edit-multi.md).

```text
F0 00 20 33 01 00 71 <part> <param> <value> F7   # Page B single (Arpeggiator settings)
```

Param IDs are **not global** — **`0x0F`** here is **Arpeggiator Mode** on **`cmd=0x71`**, not
[Multi Tempo / Master Clock](edit-single.md#multi-tempo--master-clock-0x0f-cmd0x72) on
**`cmd=0x72`**.

## Panel reference

**LCD:** **EDIT ARP**. Which rows appear depends on **Mode** — see
[Arpeggiator panel visibility](../parameter-options.md#arpeggiator-panel-visibility).
**Mode** = **Off** → **Mode** only. **Mode** = **Down** → **Mode** + **Hold**.
Full settings (**Up**, **Up&Down**, **As Played**, **Random**, **Chord**) → six
rows. **Arp>Matrix** → **Pattern** + **Resolution** only — see
[Arpeggiator panel visibility](../parameter-options.md#arpeggiator-panel-visibility).

## Settings

### Mode (`0x0F`, `cmd=0x71`) {#arpeggiator-mode-cmd0x71-param-0x0f}

**EDIT ARP → Mode** (Page B **#1** *Arp Mode* in WAF80). **`stored = index`**
— full list in [Arpeggiator Mode](../parameter-options.md#arpeggiator-mode).
**Off** (`00`) disables the arpeggiator; any other mode runs the arp with that
pattern direction. The front-panel **ARP** on/off control selects **Up** (`01`)
when enabled in hardware tests.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 0F <value> F7`         |
| Panel range    | Off … Arp>Matrix (`00`–`07`)                        |
| Confirmed      | Hardware TX (TI mk2)                                |

```text
F0 00 20 33 01 00 71 00 0F 00 F7   # Off (arp disabled)
F0 00 20 33 01 00 71 00 0F 01 F7   # Up (panel ARP on)
F0 00 20 33 01 00 71 00 0F 02 F7   # Down
F0 00 20 33 01 00 71 00 0F 03 F7   # Up&Down
F0 00 20 33 01 00 71 00 0F 04 F7   # As Played
F0 00 20 33 01 00 71 00 0F 05 F7   # Random
F0 00 20 33 01 00 71 00 0F 06 F7   # Chord
F0 00 20 33 01 00 71 00 0F 07 F7   # Arp>Matrix
```

### Pattern (`0x02`, `cmd=0x71`) {#arpeggiator-pattern-cmd0x71-param-0x02}

**EDIT ARP → Pattern**. **`stored = <value>`** — **User** (`00`), presets **2**–
**64** (`01`–`3F`; LCD = **`stored + 1`**). Full map:
[Arpeggiator Pattern](../parameter-options.md#arpeggiator-pattern). Hidden when
**Mode** = **Off** or **Down** (visible on full settings modes and **Arp>Matrix**).

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 02 <value> F7`         |
| Panel range    | User, **2** … **64** (`00`–`3F`)                    |
| Confirmed      | Hardware TX (TI mk2; full settings + **Arp>Matrix**) |

```text
F0 00 20 33 01 00 71 00 02 00 F7   # User
F0 00 20 33 01 00 71 00 02 01 F7   # 2
F0 00 20 33 01 00 71 00 02 3F F7   # 64
```

### Octaves (`0x03`, `cmd=0x71`) {#arpeggiator-octaves-cmd0x71-param-0x03}

**EDIT ARP → Octaves** (WAF80 Page B **#3** *Arp Octave Range*).
**`stored = octaves − 1`** (**`00`–`03`** → LCD **1**–**4**). Enum:
[Arpeggiator Octaves](../parameter-options.md#arpeggiator-octaves). Full settings
modes only — hidden when **Mode** = **Off**, **Down**, or **Arp>Matrix**.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 03 <value> F7`         |
| Panel range    | **1**–**4** octaves (`00`–`03`)                       |
| Confirmed      | Hardware TX (TI mk2; full settings modes)           |

```text
F0 00 20 33 01 00 71 00 03 00 F7   # 1 octave
F0 00 20 33 01 00 71 00 03 03 F7   # 4 octaves
```

### Resolution (`0x11`, `cmd=0x71`) {#arpeggiator-resolution-cmd0x71-param-0x11}

**EDIT ARP → Resolution** (WAF80 Page B **#17** *Arp Clock*; worksheet label
**Clock / Resolution**). **`stored = <value>`** — tempo grid **1/128** …
**1/2**; full map in
[Arpeggiator Resolution](../parameter-options.md#arpeggiator-resolution). Hidden
when **Mode** = **Off** or **Down** (visible on full settings modes and
**Arp>Matrix**).

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 11 <value> F7`         |
| Panel range    | **1/128** … **1/2** (`01`–`11`; no **Off**)           |
| Confirmed      | Hardware TX (TI mk2; full settings + **Arp>Matrix**) |

```text
F0 00 20 33 01 00 71 00 11 01 F7   # 1/128
F0 00 20 33 01 00 71 00 11 11 F7   # 1/2
```

### Note Length (`0x05`, `cmd=0x71`) {#arpeggiator-note-length-cmd0x71-param-0x05}

**EDIT ARP → Note Length**. Bipolar **`stored = ui + 64`** — LCD curve:
[Arpeggiator Note Length](../parameter-options.md#arpeggiator-note-length-lcd).
Full settings modes only — hidden when **Mode** = **Off**, **Down**, or
**Arp>Matrix**.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 05 <value> F7`         |
| Panel range    | **−100.0..+100.0 %** (`00`–`7F`; **+0 %** @ `40`)   |
| Confirmed      | Hardware TX (TI mk2; full settings modes)           |

```text
F0 00 20 33 01 00 71 00 05 00 F7   # −100.0 %
F0 00 20 33 01 00 71 00 05 40 F7   # +0.0 %
F0 00 20 33 01 00 71 00 05 7F F7   # +100.0 %
```

### Swing Factor (`0x06`, `cmd=0x71`) {#arpeggiator-swing-factor-cmd0x71-param-0x06}

**EDIT ARP → Swing Factor**. **`00`** = **Off**; **`01`–`7F`** = swing amount —
mostly **XX.X %**, with five **16x** shorthand labels (**16B**–**16F**) at sparse
wire values. LCD map: [Arpeggiator Swing Factor](../parameter-options.md#arpeggiator-swing-factor-lcd).
Full settings modes only — hidden when **Mode** = **Off**, **Down**, or
**Arp>Matrix**.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 06 <value> F7`         |
| Panel range    | **Off**; **50.2..75.0 %** + **16B** … **16F**        |
| Confirmed      | Hardware TX (TI mk2; full settings modes)           |

```text
F0 00 20 33 01 00 71 00 06 00 F7   # Off
F0 00 20 33 01 00 71 00 06 01 F7   # 50.2 %
F0 00 20 33 01 00 71 00 06 15 F7   # 16B
F0 00 20 33 01 00 71 00 06 42 F7   # 16D
F0 00 20 33 01 00 71 00 06 7F F7   # 75.0 %
```

### Hold (`0x04`, `cmd=0x71`) {#arpeggiator-hold-cmd0x71-param-0x04}

**EDIT ARP → Hold** (WAF80 Page B **#4** *Arp Hold Enable*). **`00`** = **Off**,
**`01`** = **On** — [Arpeggiator Hold](../parameter-options.md#arpeggiator-hold).
Hidden when **Mode** = **Off** or **Arp>Matrix**. On **Down**, the only setting
besides **Mode**; on full settings modes, last row of the block.

| Item           | Value                                               |
| -------------- | --------------------------------------------------- |
| Message format | `F0 00 20 33 01 00 71 <part> 04 <value> F7`         |
| Panel range    | **Off** / **On** (`00` / `01`)                        |
| Confirmed      | Hardware TX (TI mk2; **Down**, full settings modes) |

```text
F0 00 20 33 01 00 71 00 04 00 F7   # Off
F0 00 20 33 01 00 71 00 04 01 F7   # On
```
