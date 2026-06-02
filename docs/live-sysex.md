# Live SysEx (multi edit)

Real-time parameter edits while a Multi is loaded — typically from the **AURA plugin** or from the synth when a control sends MIDI without a full dump.

**Program storage** is documented in [multis.md](multis.md) (`DUMP_MULTI`, 267 bytes) for fields on the TI **Edit Multi** screen ([README](../README.md)). Live messages confirm parameter IDs; many fields also appear in the dump at the offsets in [multis.md](multis.md#multi-parameter-map).

**Preferred research path:** change settings on the **Virus LCD**, then capture **`DUMP_MULTI`** from the hardware. Use this guide when you only have live traffic, or to correlate `0x72` param IDs with dump offsets.

---

## `cmd=0x72` — multi parameter change

```
F0 00 20 33 01 00 72 <part> <param> <value> F7
```

- `<part>` — zero-based part index (`00` = Part 1, `0F` = Part 16)
- `<param>` — parameter ID on the multi edit page
- `<value>` — new value (encoding per parameter)

| Param ID | Field | Value encoding | Dump offset (if any) |
|---|---|---|---|
| `0x0F` | Master Clock Tempo | `stored = bpm - 63` | Dump: **`0x17`** |
| `0x23` | Low Key | Direct 7-bit note | `0x59 + part` |
| `0x24` | High Key | Direct 7-bit note | `0x69 + part` |
| `0x25` | Part Transpose | Live: `00` = −63 … `7F` = +64 | Dump: `0x79 + part`, `stored = ui + 64` (TI UI −48..+48) — **not** the same byte values as live |
| `0x27` | Volume | `stored = ui + 64` (bipolar) | `0x99 + part` |
| `0x29` | Part Output routing | Enum — [table below](#part-output-routing-enum-0x29) | `0xB8 + part` |
| `0x2B` | Panorama | `00` = Off, `40` = center, etc. | `0xD8 + part` |
| `0x40` | Keyboard to MIDI (“kbd local”) — **global** | `00` / `01`; live `part=00` | TBD (single byte) — [global](#keyboard-to-midi-0x40--global) |
| `0x48` | Part Enable | `00` / `01` | `0xF8 + part` |
| `0x49` | Volume RX (CC#7) | `00` / `01` | `0xF8` flag `+2` |
| `0x4A` | Hold Pedal (CC#64) | `00` / `01` | `0xF8` flags |
| `0x4D` | Priority | `00` = Low, `01` = High | `0xF8` flag `+0x20` |
| `0x4E` | Program Change | `00` / `01` | `0xF8` flag `±0x40` |

AURA reuses **`0x48`** for track **mute** and **solo** (solo sends Off to all other parts).

### Keyboard to MIDI (`0x40`) — global

Manual name: **Keyboard to MIDI**. AURA: **“kbd local enabled”** (same function).

**Scope:** **Global** for the whole Multi (one built-in keyboard → MIDI). Not a per-part mix parameter. The manual may expose it on a part page, but it applies to the instrument, not Part 1–16 individually.

- **Hardware:** **Virus TI Keyboard** and **Polar** only.
- **TI desktop module:** no panel control; live `0x72` works but **`DUMP_MULTI` unchanged** (enable vs disable captures identical on mk2 module).
- **AURA:** shows the control for all models; live messages use **`part=00`** — treat the part byte as a formality, not “Part 1 only”.

```
F0 00 20 33 01 00 72 00 40 <value> F7
```

| Value | State |
|---|---|
| `00` | Disabled |
| `01` | Enabled |

Confirmed: `F0 00 20 33 01 00 72 00 40 00 F7` (off), `... 72 00 40 01 F7` (on).

**Dump mapping:** On a **TI desktop module**, toggling kbd local does **not** change `DUMP_MULTI` (tested: enable and disable dumps byte-identical). A **keyboard** model might store it elsewhere (device/global settings, or multi only when hardware supports it) — not confirmed.

### Part Output routing enum (`0x29`)

Each output group uses three values: **L**, **L+R**, **R**.

| Value | Routing |
|---|---|
| `00`–`02` | Out 1: L, L+R, R |
| `03`–`05` | Out 2: L, L+R, R |
| `06`–`08` | Out 3: L, L+R, R |
| `09`–`0B` | USB 1: L, L+R, R |
| `0C`–`0E` | USB 2: L, L+R, R (`0D` confirmed) |
| `0F`–`11` | USB 3: L, L+R, R (`10`, `11` confirmed) |

### Example messages (`0x72`)

- `F0 00 20 33 01 00 72 00 25 00 F7` — Part 1 transpose minimum  
- `F0 00 20 33 01 00 72 01 25 7F F7` — Part 2 transpose maximum  
- `F0 00 20 33 01 00 72 0F 24 7F F7` — Part 16 High Key G9  
- `F0 00 20 33 01 00 72 00 24 00 F7` / `... 0F 24 00 F7` — Part 1 / Part 16 High Key C1  
- `F0 00 20 33 01 00 72 00 49 00 F7` / `... 49 01 F7` — Part 1 Volume RX off / on  
- `F0 00 20 33 01 00 72 00 4A 00 F7` / `... 4A 01 F7` — Part 1 Hold Pedal off / on  
- `F0 00 20 33 01 00 72 00 0F 3D F7` — Master Clock 124 bpm (`0x3D` = 124 − 63)  
- `F0 00 20 33 01 00 72 00 48 00 F7` / `... 48 01 F7` — Part 1 Enable off / on  
- `F0 00 20 33 01 00 72 00 40 00 F7` / `... 40 01 F7` — Keyboard to MIDI off / on (global; AURA kbd local)

---

## `cmd=0x6E` — part / single edit buffer

Used while editing a **part’s sound** (not the same as storing a full multi). **Not** in the 267-byte `DUMP_MULTI`.

| Param ID | Field | Notes |
|---|---|---|
| `0x02` | Reverb Send | [Effect send amount](#effect-send-amount-reverb-send) |

### Reverb Send — not in multi dump

- Observed only as **`F0 00 20 33 01 00 6E <part> 02 <value> F7`** (and AURA equivalents).
- **Never** seen to change any byte in a **`DUMP_MULTI`** diff across all captures so far.
- Not listed under **Edit Multi** on the TI mk2 LCD (v5.1.7) — consistent with **part-edit / single-buffer** control, not a stored multi-program field.
- OS4 manuals may label this “Effect Send”; on TI 5.1.7 the live target is **Reverb Send**.

---

## Effect send amount (Reverb Send)

Direct byte `0..127`; `0` = Off. Unity at **`96` (`0x60`)**; **`127` (`0x7F`)** = max send. Values **`97+`** often display as `0/−XdB`.

| Value | Hex | Display |
|---:|---|---|
| 0 | `00` | Off |
| 1 | `01` | −46.2 dB |
| 96 | `60` | 0/0 dB (unity) |
| 127 | `7F` | effect (max) |

Suspected shared encoding for other effect sends (e.g. Delay Send); only Reverb Send confirmed.

| Value | Hex | Display |
|---:|---|---|
| 0 | `00` | Off |
| 1 | `01` | −46.2 dB |
| 2 | `02` | −40.2 dB |
| 10 | `0A` | −26.2 dB |
| 20 | `14` | −20.6 dB |
| 30 | `1E` | −16.6 dB |
| 40 | `28` | −14.0 dB |
| 41 | `29` | −13.75 dB |
| 45 | `2D` | −12.75 dB |
| 54 | `36` | −10.5 dB |
| 57 | `39` | −9.75 dB |
| 90 | `5A` | −1.5 dB |
| 91 | `5B` | −1.25 dB |
| 92 | `5C` | −1.0 dB |
| 93 | `5D` | −0.75 dB |
| 94 | `5E` | −0.5 dB |
| 95 | `5F` | −0.25 dB |
| 96 | `60` | 0/0 dB (unity) |
| 97 | `61` | 0/−0.3 dB |
| 98 | `62` | 0/−0.6 dB |
| 99 | `63` | 0/−0.9 dB |
| 100 | `64` | 0/−1.2 dB |
| 108 | `6C` | 0/−4.1 dB |
| 109 | `6D` | 0/−4.5 dB |
| 110 | `6E` | 0/−5.0 dB |
| 111 | `6F` | 0/−5.5 dB |
| 112 | `70` | 0/−6.0 dB |
| 114 | `72` | 0/−7.2 dB |
| 115 | `73` | 0/−7.8 dB |
| 116 | `74` | 0/−8.5 dB |
| 117 | `75` | 0/−9.3 dB |
| 118 | `76` | 0/−10.1 dB |
| 119 | `77` | 0/−11.0 dB |
| 120 | `78` | 0/−12.0 dB |
| 121 | `79` | 0/−13.2 dB |
| 122 | `7A` | 0/−14.5 dB |
| 123 | `7B` | 0/−16.1 dB |
| 124 | `7C` | 0/−18.1 dB |
| 125 | `7D` | 0/−20.6 dB |
| 126 | `7E` | 0/−24.0 dB |
| 127 | `7F` | effect (max) |

Unlisted values are piecewise / non-linear. Approximations: **`41`–`95`** ≈ **`−0.25 × (96 − value)`** dB; **`1`–`40`** steeper; **`97`–`126`** larger steps toward max.

| Parameter | Cmd | Param | In `DUMP_MULTI`? |
|---|---|---|---|
| Reverb Send | `0x6E` | `0x02` | **No** |
| Delay Send | — | — | Not mapped |

---

## Related: AURA `DUMP_SINGLE` on part enable

When a part is disabled then re-enabled in AURA, a **524-byte** `cmd=0x10` (`DUMP_SINGLE`) loads that part’s single into the edit buffer. Documented in [multis.md](multis.md#aura-behavior-part-enable-sends-dump_single).
