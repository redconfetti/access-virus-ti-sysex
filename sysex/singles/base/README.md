# Base Single

This is the RAM A - 127 program known as "-INIT-". This will be the base
program that we will compare to others.

Other patches that differ slightly from this base patch will only include
notes on the parameters that should differ using the same sections and
bullet list structure as that below.

For presets that have certain features enabled, or a different "mode" or "type"
chosen, additional parameters under a group of related parameters may become
present, and should be expected as such.

## Oscillators

* Common - Editable from 'Edit' button menu for Oscillators
  * Phase Init: Off
  * Key Mode: Poly
  * Osc Volume: 0
  * Portamento: Off
  * Punch: 50.0%
  * Filter Envelope > Sync: +0%
* Ring Modulator
  * Volume: Off
* Noise
  * Volume: Off
* Sub Oscillator
  * Volume: 0
  * Shape: Square
* Oscillator 1
  * Mode: Classic
  * Shape: Sawtooth
  * Pulse width: 50.0%
  * Semitone: +0
  * Key Follow: Norm
  * Balance: +0%
* Oscillator 2
  * Mode: Classic
  * Shape: Sawtooth
  * Pulse width: 50.0%
  * Semitone: +0
  * Key Follow: Norm
  * Balance: +0%
  * Detune: 32
  * FM Mode: Pos Triangle
  * FM Amount: 0%
  * Filter Envelope > Pitch: +0%
  * Sync: Off
  * Filter Envelope > FM: +0%
* Oscillator 3
  * Mode/Wave: Off

## Mixer

It appears that the Mixer section controls the same parameters as those included
above from the Oscillator section.

* Oscillator Balance: +0%
* Sub Oscillator Volume: 0
* Oscillator Volume: 0
* Noise Volume: Off

## Filters

* Common
  * Routing: Serial 4
  * Filter Balance: +0
  * Cutoff Link: On
  * Key Follow Base: C2
* Filter Envelope
  * Attack: 0
  * Decay: 46
  * Sustain: 0%
  * Sustain Slope: +0
  * Release: 127
* Amplifier Envelope
  * Attack: 0
  * Decay: 127
  * Sustain: 100%
  * Sustain Slope: +0
  * Release: 4
* Saturation
  * Type: Off
  * Osc Volume: 0
* Filter 1
  * Cutoff: 127
  * Resonance: 0
  * Envelope Amount: 0%
  * Mode: Low Pass
  * Key Follow: +0
  * Envelope Polarity: Positive
* Filter 2
  * Offset: 0%
  * Resonance: 0
  * Envelope Amount: 0%
  * Mode: Low Pass
  * Key Follow: +0
  * Envelope Polarity: Positive

## Arpeggiator

* Mode: Off

## Modulators / LFOs

* LFO 1
  * Clock: Off
  * Rate: 48
  * Shape: Triangle
  * Contour: +0
  * Mode: Poly
  * Envelope Mode: Off
  * Trigger Phase: Off
  * Key Follow: Off
  * Destinations
    * Osc 1 Pitch: +0%
    * Osc 1+2 Pitch: <- ->
    * Osc 2 Pitch: +0%
    * Pulse Width: +0%
    * Resonance: +0%
    * Filter Gain: +0%
    * Assign Target: Off
    * Amount: +0%
* LFO 2
  * Clock: Off
  * Rate: 48
  * Shape: Triangle
  * Contour: +0
  * Mode: Poly
  * Envelope Mode: Off
  * Trigger Phase: Off
  * Key Follow: Off
  * Destinations
    * Cutoff 1: +0%
    * Cutoff 1+2: <- ->
    * Cutoff 2: +0%
    * Shape 1+2: +0%
    * FM Amount: +0%
    * Panorama: +0%
    * Assign Target: Off
    * Amount: +0%
* LFO 3
  * Clock: Off
  * Rate: 94
  * Shape: Triangle
  * Mode: Poly
  * Key Follow: Off
  * Destinations
    * Fade In: 0
    * Assign Target: Osc 1+2 Pitch
    * Amount: 0%

## Matrix

* Slot 1
  * Option 1
    * Type: Mod Wheel
    * Amount: -36
    * Assignment: LFO 3 Assign Amount
  * Option 2
    * Type: Off
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Off
    * Amount: 0
    * Assignment: Off
* Slot 2
  * Option 1
    * Type: Off
    * Amount: 0
    * Assignment: Off
  * Option 2
    * Type: Off
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Off
    * Amount: 0
    * Assignment: Off
* Slot 3
  * Option 1
    * Type: Off
    * Amount: 0
    * Assignment: Off
  * Option 2
    * Type: Off
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Off
    * Amount: 0
    * Assignment: Off
* Slot 4
  * Option 1
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 2
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Mod Wheel  
    * Amount: 0
    * Assignment: Off
* Slot 5
  * Option 1
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 2
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Mod Wheel  
    * Amount: 0
    * Assignment: Off
* Slot 6
  * Option 1
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 2
    * Type: Mod Wheel
    * Amount: 0
    * Assignment: Off
  * Option 3
    * Type: Mod Wheel  
    * Amount: 0
    * Assignment: Off

## Effects

* Delay
  * Type: Classic
  * Send: Off
  * Feedback: 0%
  * Delay Time: 349.5
* Reverb
  * Mode: Reverb
  * Type: Large Room
  * Send: Off
  * Time: 68
  * Damping: 15.6%
  * Clock: Off
  * Coloration: +0
  * Predelay: 5.5
* Low EQ
  * Frequency (Hz): 78
  * Gain: Off
* Mid EQ
  * Frequency (Hz): 1046
  * Q-Factor: 1.02
  * Gain: Off
* High EQ
  * Frequency (kHz): 10.6
  * Gain: Off
* Distortion
  * Type: Off
* Character
  * Type: Analog Boost
  * Intensity: 31.3%
  * Frequency: 32
* Chorus
  * Type: Classic
  * Rate: 69
  * Depth: 12.5%
  * Feedback: +0%
  * Delay: 127
  * Mix: Off
  * LFO Wave: Triangle
* Phaser
  * Mix: Off
* Vocoder
  * Mode: Off

## Edit Menu Parameters

These are the parameters that are edited through the 'Edit' button menu.

* Common
  * Tempo: 120 bpm
  * Patch Volume: 100
  * Panorama: 0 (Center)
  * Transpose: 0 (Center)
  * Smooth Mode: On
  * Bend Down: -2
  * Bend Up: +2
  * Bender Scale: Exponential
* Unison
  * Voices: Off
  * Pan Spread: 100%
* Envelope 3
  * Attack: 20
  * Decay: 70
  * Release: 70
  * Sustain: 0%
  * Sustain Slope: +0
* Envelope 4
  * Attack: 20
  * Decay: 70
  * Release: 70
  * Sustain: 0%
  * Sustain Slope: +0
* Velocity Map
  * Volume: +0%
  * Panorama: +0%
  * FM Amount: +0%
  * Osc 1 Shape: +0%
  * Osc2 Shape: +0%
  * Pulse Width: +0%
  * Filter 1 Env Amount: +0%
  * Resonance 1: +0%
  * Filter 2 Env Amount: +0%
  * Resonance 2: +0%
* Inputs
  * Atomizer: Off
  * Input Mode: Off
* Surround
  * Output: Out 1 L+R
  * Balance: -64
* Categories
  * Name Cat 1: Off
  * Name Cat 2: Off
* Soft Knob 1
  * Function As: Off
* Soft Knob 2
  * Function As: Off
* Soft Knob 3
  * Function As: Off
