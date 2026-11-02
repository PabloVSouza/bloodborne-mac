# The PS4 executable

[← The PS4 layers](README.md)

The game starts from a PS4 executable. It has to be prepared, loaded at fixed addresses and patched
in memory before it can run, and that is true even on an x86-64 PC.

## What we did

- **Prepared in C at start** (`src/runtime_prepare.c`, `src/runtime_patches.c`), on the player's
  device, without Python. The bytes are compared with the older scripts' output.
- **Patches and hooks:** the community's patch collection, plus hooks for the frame rate and other
  features, checked against their bytes.

## Where it stands

0%: the game still starts as a PS4 executable, and the recompiled library loads into it. Only update
1.09 is accepted, because every address in the runtime is an address in that executable.

## What is left

A game that starts as a native program: its own entry point, its memory laid out by the platform, and
hooks built into the code instead of patched in.
