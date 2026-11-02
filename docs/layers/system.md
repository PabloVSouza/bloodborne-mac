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

0%: no PS4 firmware runs, and all of the answers are our code, but the layer is still a translation.
The game makes the calls a PS4 game makes, and the runtime turns each one into what the platform
does.

## What is left

Recompiled code calling each platform directly, instead of going through the PS4's interfaces. Platform differences are in `src/platform.{c,h}`: Linux and macOS.
