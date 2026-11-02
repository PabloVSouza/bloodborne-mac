# PS4 textures and memory

[← The PS4 layers](README.md)

The PS4's CPU and GPU share one memory, and the game is written around that. It writes data and the
GPU reads it from the same place. Nothing tells the runtime what is a texture, so shadPS4's texture
cache infers it from GPU memory, and each texture exists twice: in the game's memory and as a GPU
texture, about 1-1.5 GB.

## What we did

- On Macs, whose memory is also shared, the GPU uses the game's memory pool in place.
- GPU-only textures are never evicted, which drew them dark.
- The recompiled library no longer keeps the game decoded: the peak footprint went from 7.8 GB to
  5.7 GB in Iosefka's Clinic.

## Where it stands

0%: N3 has not started. Textures are still inferred and held twice.

## What is left

Taking textures as the objects the engine creates and releases, which removes the second copy.

This layer exists on every platform, and it costs more on PCs with a separate GPU memory, where shared
data has to be copied and kept in sync. Reading GPU results back there is slow, and the game assumes
it is cheap.
