# The PS4's C and file libraries

[← The PS4 layers](README.md)

The game does not only use its own code. `libc.prx`, the PS4's C library, and `libSceFios2.prx`, its
file streaming library, ship with the game and run as game code.

## What we did

- Both modules are linked into the game's image at start, on the player's device.
- The busiest C library functions are replaced by host code (`src/runtime_libc.c`): `memcpy`,
  `memset`, the mutexes and nearly all of the game's `operator new` and `delete`.
- The recompiled library calls those host functions directly, which is where most of the fall in
  translator calls came from.

## Where it stands

0 of the 2 modules are recompiled. Everything in them that has not been replaced runs in the
translator, even with the recompiled library.

## What is left

Recompiling both modules, or replacing what the game uses of them with host code.
