# The graphics API

[← The PS4 layers](README.md)

The renderer comes from shadPS4, which draws with Vulkan. On a Mac that meant one more translation,
MoltenVK, between the renderer and Metal.

## What we did

- **A render adapter (N4):** the renderer records through the project's own GPU interface.
- **A Metal backend (N5):** every frame drawn by Metal directly, the default since 0.9.0. MoltenVK
  stays selectable as a fallback.
- **Frame planning (N1):** clears deferred into the next pass's load action.
- **Lossless texture compression**, adapted from MojahedAbushawish's work for bloodborne_mac_port:
  36.3-36.7 FPS to 48.0-49.2 in Iosefka's Clinic on an M3 Pro.

## Where it stands

On macOS, the renderer talks to Metal with nothing in between. The Vulkan backend stays as the
renderer for other platforms; Linux uses it today.

## What is left

Whether MoltenVK leaves the macOS app is still to be decided.

Details: [Native renderer](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md).
