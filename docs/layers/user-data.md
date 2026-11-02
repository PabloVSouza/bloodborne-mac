# PS4 user data

[← The PS4 layers](README.md)

PS4 shaders find their resources through user data, and often through pointers inside it. The
converted shaders still expect that layout, so a walker follows those pointers and flattens the
result into a buffer the shader reads.

## What we did

- **An inventory (N2.2):** shaders use the user data only to locate their resources.
- **Mesh draws from the draw state (N2.3):** the flat buffer filled from the engine's state, exactly.
- **Other draw kinds and compute (N2.4):** most read their resources straight from registers the
  engine sets.

With `BB_RENDER_BOUNDARY=flat`, 92% of draw shader stages and 79% of dispatch shader stages skip the
walker.

## Where it stands

0% for players: the walker runs for everyone, because that mode is a developer switch. In that mode
the shaders themselves do not change: the same flat buffer is filled another way, and compute
programs still learn their slots from the walker. The observer also costs about 45 CPU points.

## What is left

The rest of the draw kinds, a cheaper observer, and the mode on by default.
