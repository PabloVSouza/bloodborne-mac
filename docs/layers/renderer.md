# The renderer

[← The PS4 layers](README.md)

The renderer comes from shadPS4. It reads the PS4 commands the game writes and works out what to draw,
and every frame is that translation. On a Mac it used to go through one more, MoltenVK, from Vulkan
to Metal.

## What we did

- **A render adapter (N4):** the renderer records through the project's own GPU interface.
- **A Metal backend (N5):** on macOS the renderer reaches Metal directly, the default since 0.9.0.
  MoltenVK stays selectable as a fallback. This removed one translation, not the renderer's own.
- **Frame planning (N1):** clears deferred into the next pass's load action.
- **Lossless texture compression**, adapted from MojahedAbushawish's work for bloodborne_mac_port:
  36.3-36.7 FPS to 48.0-49.2 in Iosefka's Clinic on an M3 Pro.

## Where it stands

0%: rendering is not native. Every frame is PS4 commands translated into Metal calls, drawing with
shaders converted from PS4 code. The N4 and N5 milestones are finished, but a finished milestone does
not make the layer native.

## What is left

The renderer working from the engine's own draws and objects, which is what the
[GPU commands](gpu-commands.md), [user data](user-data.md) and
[textures](textures-memory.md) layers are about. Whether MoltenVK leaves the macOS app is still to be
decided. Other platforms use the Vulkan backend; Linux does today.

Details: [Native renderer](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md).
