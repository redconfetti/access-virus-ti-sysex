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
reference type multis, is as follows:

* Global Parameters
  * Multi Program Name
  * Master Clock Tempo: 63 bpm to 190 bpm - Specifies the tempo that applies
    to all parts in the Multi, overriding any Master Clock/Tempo parameters
    included in the Single programs
  * Global routing settings
* Part Settings
  * Part Enable: On/Off
  * Bank: Selects the bank from which a Single program is automatically copied
    into the current part (used only with reference multis)
  * Program: 0 to 127 - Selects the Single program to be automatically copied
    into the current Part (usedo nly with referene multis)
  * Volume: -64 to +63 - Bipolar parameter for balancing levels between
    different Parts
  * Panorama: -64 to +63 - Stereo position of the Part. Overrides/overwrites the
    Single parameter of the same name.
  * MIDI Channel: 01 to 16 - The MIDI channel to which this Part will respond.
  * Output: Out 1 L ... USB2 R - Sends this Part to the selected analogue or USB
    output. Each option is either OUT or USB, with L (left), R (right) or
    L+R (Left + Right). There are 3 analog outputs (OUT 1, OUT 2, OUT 3), and 3
    USB  outputs (USB 1, USB 2, USB 3)
  * Transpose: -48 to +48 semitones - Part transposition. Adds/subtracts from
    the Single parameter of the same name.
  * Detune: -64 to +63 - Tunes all pitched elements (oscillators, filters)
    within a fairly narrow range.
  * Priority: Low/High - Specifies whether note-stealing will favor the current
    Part when all voices in the Virus have been used up. The Virus TI has plenty
    of voices and applies a very clever note-stealing algorithm, so you should
    seldom (or never) notice this happening.
  * Init Volume: Off, 1 to 127 - Initializes MIDI volume (CC#7) for the current
    Part whenever this Multi program is selected. See Volume RX below.
  * Low Key: C-2 to G8 - The lowest MIDI note to which this Part will respond.
    If this is higher than High Key (see below) the range between Low Key and
    High Key is disabled, and all notes outside this range are enabled.
  * High Key: C-2 to G8 - The highest MIDI note to which this Part will respond.
    If this is set lower than Low Key (see above), the range between Low Key
    and High Key is disabled, and all notes outside this range are enabled.
  * Hold Pedal: Disabled/Enabled - Specifies whether the Part will respond to
    MIDI CC#64 (usually a Sustain Pedal)
  * Volume RX: Disabled/Enabled - Specifies whether the Part will respond to
    MIDI CC#7 (Volume)
  * Prog Change: Disabled/Enabled - Specifies whether the Part will respond to
    MIDI Program Change messages. The global "Program Change" parameter in the
    CONFIG menu is ignored.
  * Patch Volume: Quick access to the Patch Volume parameter, used for balancing
    levels between different programs.
