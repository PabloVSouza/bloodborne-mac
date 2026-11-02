# Shaders compiled during play

[← The PS4 layers](README.md)

The game's shaders are GCN code for the PS4's GPU. They are converted for the platform, and compiling
them at first use stalls the game. Converting them stays: the maintainer's decision is to convert
them once, ahead of time, rather than replace them by hand.

## What we did

- **A compile step** in the launcher's recompiler settings: off by default, it builds shaders and
  pipelines from the player's own game files, with nothing recorded and nothing shipped.
- **Pipelines from the engine's rules:** which targets, blends and vertex formats each pass uses.
- **Shaders independent of the draw** where the source never read what differed.
- **Compute strides read at run time,** so a structure's size is no longer a shader form, and mixes
  of formats across a program's bindings.
- **One text per shader on Metal:** translations that differ only in numbering are one source.

## Where it stands

After the step, 253 of the 295 sources one session in Iosefka's Clinic used were already built
(86%): 132 of 136 fragment, 83 of 93 vertex, 38 of 61 compute and 0 of 5 tessellation.

From empty caches, a first play's worst frame is 561 ms, with 10 frames over 100 ms. That is one run,
standing still. With no step at all it was 1.9 s; with recorded states it is 258 ms. The step takes
441 s.

## What is left

- The port's own compute kernels, tessellation stages, and the vertex and fragment forms still
  missed.
- Why 656,734 of the planned pipelines fail to build.
- Movement, combat and other areas, none of which are measured.
- Vulkan's build path: planning is shared, building is per backend.
