# Base Multi

The multi sysex dump in base.syx contains 17 messages. The first message
is 267 bytes in length. I assume this contains Multi settings, and
the 16 messages included in the dump that follow (524 bytes each) represent
each of the "-INIT-" programs.

Each program should be identical to the base dump in
`sysex/singles/base/base.syx`, as it's the same exact patch. However perhaps
they differ because each program has to address the slot in the Multi buffer
that the message is addressed to.

The Multi is named "INIT MULTI", and only Part 1 and 2 are enabled.

I saved this multi to slot #32 in the Multi bank, so I expected it to be a
reference multi, but that might not be the case. The Virus TI mk2 might be setup
to always dump from the Multi Edit Buffer, even though the device will
discard the Part parameters if saved to Multi bank slots 17-128. I've actually
tested this myself and noticed that behavior specifically (Part specific
parameters were discarded).
