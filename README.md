# Access Virus SysEx

The mission of this project is to document the specifications for Access Virus
TI mk2 multi exports in SysEx format, with some notes concerning Single exports
as they relate to multi exports.

The developer of this project will generate SysEx dumps from an Access Virus
TI mk2 synthesizer that represent different programs, along with
details that are known about the SysEx dump. Cursor AI agents will assist
with analyzing these artifacts and doing comparison to discover the meanings
of the SysEx binary data. Sysex dumps will be contained in the 'sysex' folder.

## Access Virus Banks

The Access Virus TI mk2 supports four RAM banks, each storing 128 programs each.

* RAM A
* RAM B
* RAM C
* RAM D

It also supports 26 ROM banks (ROM A - ROM Z), each also storing 128 programs
each. I'm not sure how bank references are structured in SysEx dumps.

## Access Virus SysEx Dumps

The following types of dumps are supported by the Access Virus

1. Single Buffer - Represents a single program/preset present in the temporary
   memory buffer.
2. Single Bank - Represents 128 programs stored in a RAM bank, targetting the
   same RAM bank that the data was exported from (Bank A, B, C, or D).
3. Controller Dump - A Single program, but in the form of a succession of
   individual parameter changes. Can take the form of MIDI CCs and Sysex.
4. Arrangement - All 16 sounds in the current Multi buffer or Sequencer mode
   buffer, plus the additional "multi" settings. This type of export is the
   primary focus of this project.
5. Multi Bank - All Multi programs inside of a Multi bank. For the Virus TI
   series, the first 16 "multi" programs stored are Embedded Multis that store
   the "multi" settings, but also all the parameters for each of the 16 included
   programs. Multi programs stored in Multi bank slots 17 - 128 are "reference"
   multis that do not store the program data, but instead reference a bank
   and program for each of the 16 programs that make up the reference Multi.
6. Remote Patches - All Remote templates (of no interest to this project)

### Virus TI Multis

In earlier Virus models, Multi mode programs consisted of 16 Parts, each one
referencing a Single program. The downside: Multi programs depended on the
location of all their referenced Singles, so if you changed any program
while working in Single mode, Multi programs would change accordingly.

The Virus TI series includes one Multi bank that stores 128 multis. The first
16 multis store all parameters for all of the 16 singles that are included
in the multi. This is known as an "embedded multi".

From operating system revision 1.1 onwards, there is another 112 referencing
Multi mode programs in order to supply you with old and new fashion Multi mode
program. The additional programs can be accessed on slot 17-127.

The "Multi" data that is stored in a "Multi" program, for both embedded and
reference type multis, is as follows.

**Official parameter list for this project.** The fields below match the **Virus TI**
**Edit Multi** screen (TI manual). They are the target set for mapping the
267-byte `DUMP_MULTI` payload. See [docs/multis.md](docs/multis.md) for dump
offsets and [docs/live-sysex.md](docs/live-sysex.md) for live-only controls
(e.g. Reverb Send while editing a part).

*Not on Edit Multi:* per-part effect sends (Reverb Send), shared Multi Delay
(OS4 docs), and CONFIG globals — [docs/multis.md](docs/multis.md#beyond-edit-multi).

* Global (Edit Multi)
  * Multi Program Name
  * Master Clock Tempo: 63–190 bpm — tempo for all parts in the Multi,
    overriding Single-program Master Clock settings
  * Keyboard to MIDI: Disabled / Enabled — **global** (one built-in keyboard).
    **TI Keyboard and Polar** on the panel; **desktop module** has no keyboard.
    Live `0x72` param `0x40` works from AURA; **not stored in `DUMP_MULTI`**
    on the desktop module (same as live-only for multi file purposes).
* Part (Edit Multi)
  * Part Enable: On/Off
  * Bank — reference multis only: bank from which a Single is copied into the part
  * Program: 0–127 — reference multis only: program number to copy into the part
  * Volume: −64 to +63 — balance between parts (AURA: **Part Level**)
  * Panorama: −64 to +63 — part stereo position; overrides the Single parameter
  * MIDI Channel: 1–16
  * Output: Out 1 L … USB 3 R (analog Out 1–3 and USB 1–3, each L / L+R / R)
  * Transpose: −48 to +48 semitones — adds to the Single transpose value
  * Detune: −64 to +63
  * Priority: Low / High — note-stealing preference when voices are exhausted
  * Init Volume: Off, 1–127 — MIDI volume (CC#7) when the Multi is selected
  * Low Key / High Key: C−2 to G8 — part note range (inverted range = outside range enabled)
  * Hold Pedal: Disabled / Enabled — MIDI CC#64 (sustain)
  * Volume RX: Disabled / Enabled — MIDI CC#7
  * Program Change: Disabled / Enabled — part responds to MIDI Program Change;
    CONFIG “Program Change” global is ignored for parts
