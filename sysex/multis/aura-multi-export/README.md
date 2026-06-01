# AURA Multi Export

I tried to save a 'multi' from the AURA Plugin for the Access Virus, but it
only saves the entire Multi bank to a .MID file.

Instead I used a MIDI Monitor program to capture what it sends to the Access
Virus when I load a Multi.

The whole point of this project is actually for me to deliver the specifications
for a full multi arrangement to AURA plugin developers so that they can
support embedded multis using their software.

## Message No. 1

F0 00 20 33 01 00 72 01 20 00 F7

## Message No. 2

F0 00 20 33 01 00 72 01 21 20 F7

## Message No. 3

Here is the actual Multi (267 bytes).

F0 00 20 33 01 00 11 00 00 02 00 00 00 49 4E 49 54 20 4D 55 4C 54 49 00 39 01 3C 00 10 00 01 01 00 40 40 40 40 40 40 40 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 7F 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 45 45 45 45 45 45 45 45 45 45 45 45 45 45 45 45 32 F7

## Response Message

F0 00 20 33 01 00 73 00 10 00 F7

## Analysis Notes

### High-confidence observations

- This exchange does **not** look like an arrangement dump.
  - There is exactly one returned `DUMP_MULTI` message (`cmd=0x11`) of 267 bytes.
  - There are no follow-up 16 `DUMP_SINGLE` (`cmd=0x10`) messages.
  - Therefore this capture is consistent with a **reference/multi-only export path**.

- Message #3 decodes as:
  - `F0 00 20 33 01 00 11 00 00 ... 32 F7`
  - `cmd=0x11` (`DUMP_MULTI`)
  - `bank=0x00`, `program=0x00` in the dump header
  - Payload length aligns with TI multi payload size expectations (256-byte body + framing/checksum).

- The payload clearly contains the ASCII multi name:
  - `49 4E 49 54 20 4D 55 4C 54 49` -> `INIT MULTI`

### Notes on Messages #1 and #2

- Message #1: `F0 00 20 33 01 00 72 01 20 00 F7`
- Message #2: `F0 00 20 33 01 00 72 01 21 20 F7`

Interpretation (probable):

- `cmd=0x72` appears to be a **parameter-page command** (real-time edit/control style),
  likely used here by AURA as a setup/select step before requesting/receiving the multi dump.
- The `(01,20,00)` and `(01,21,20)` triplets likely represent parameter writes
  (part/page index + parameter + value), but exact symbolic meaning of `0x20` / `0x21`
  still needs mapping.

### Response Message interpretation

- Response: `F0 00 20 33 01 00 73 00 10 00 F7`
- `cmd=0x73` is likely a page-D parameter/control response or acknowledgement.
- It likely confirms state/set-operation completion before or after the multi transfer.

### Practical implication for this project

- This capture supports your suspicion that AURA can use a **reference-style multi transfer**
  path (multi-only), in contrast to the Virus panel export behavior you observed that tends
  to produce arrangement-like dumps (multi + 16 singles).

### Open questions to resolve with another capture

- Capture the exact sequence when AURA exports a different multi slot (e.g. slot 17 vs 32)
  and compare Message #1/#2 values to identify whether `0x20`/`0x21` encode bank+program.
- Capture whether AURA ever requests `cmd=0x34` (arrangement request) in any workflow.
