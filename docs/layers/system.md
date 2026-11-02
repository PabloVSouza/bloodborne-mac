# The PS4's system

[← The PS4 layers](README.md)

A PS4 game calls its system for threads, memory, files, saves, input, audio, video, network and
trophies. Normally that needs the console's firmware.

## What we did

The runtime answers those calls with its own code (`src/runtime_*.c`). No PS4 firmware runs:

- Threads, locks, memory and the clock.
- Files, with mods layered over the game folder, and saves.
- Pads through SDL3, plus keyboard and mouse.
- Audio through LibAtrac9, and video through FFmpeg.
- Trophies, kept locally.
- Network and PSN imports: offline answers, or the optional online module, which plays on the
  Seamless Hunt and The Hunter's Dream community pools.

## Where it stands

100% of the system runs as host code. The game still reaches it through PS4 interfaces: it makes the
calls a PS4 game makes, and the runtime translates what they mean.

## What is left

Calling each platform directly from recompiled code, where that gains something, instead of going
through the PS4's interfaces. Platform differences are in `src/platform.{c,h}`: Linux and macOS.
