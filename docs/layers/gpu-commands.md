# PS4 GPU commands

[← The PS4 layers](README.md)

The game does not call a graphics API. It writes PS4 GPU command buffers, and the runtime decodes
them every frame to find out what to draw. That takes about 0.6 of a core.

## What we did

- **Found the engine's render boundary (N6):** the engine's draw methods and the state they read.
  99.94% of the engine's draws match their packets, with state and resources agreeing.
- **Every input of a draw found in the draw state:** buffer addresses and resource slots.
- Mesh draws can bind their resources from that state.

All of this is behind `BB_RENDER_BOUNDARY`, a developer switch. No player build sets it, and without
it the hooks are not installed.

## Where it stands

0% in practice: every draw and dispatch is still decoded, with every switch. What exists is the
knowledge of where the draws come from, and working code that observes them.

## What is left

Taking draws from the engine instead of from the packets, for every draw kind, and then no longer
decoding them.
