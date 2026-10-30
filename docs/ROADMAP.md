# Roadmap

[← Documentation](README.md)

The plan, in order. Where things stand now: [Status](STATUS.md). When an item lands it moves to
**Done** with where it landed; release notes say what changed for players.

Changes taken from other ports and forks (bbport, Supermedo's Windows fork, the Huax-1839 and
Wooloomooloo2 macOS ports, DiAvisoo) are adopted only after an A/B on our build (same save, route
and settings, alternating runs), and are credited in the same commit (CREDITS, the wiki, the
commit message, a code comment; the runtime's `docs/UPSTREAM.md` records them).

## Now

- **N2, the native renderer's next step** (the first item of Next, below), the maintainer's focus
  from 2026-10-29. N5, the native Metal renderer, is accepted (Done).

## Next

In this order (maintainer, 2026-10-29: the native renderer first):

1. **N2, shaders from the draw state, then native shaders ahead of time** (runtime). N6 found
   every input of a draw in the engine's draw state; the shaders still read the PS4 user data, so
   N2 builds them to read the draw state's slots instead: mesh draws first, then the other draw
   kinds. Then the game's shaders are built once, ahead of time, on the player's device, as native
   shaders for each platform (Metal libraries on macOS and iOS, SPIR-V for Vulkan): a launcher
   step, like the recompiled-code build (the maintainer's decision, 2026-10-30). Until a player
   runs it, and for anything it did not foresee, shaders convert at first use as now. Its steps are in the runtime's
   [NATIVE_RENDERER.md](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md#n2-shaders-from-the-draw-state-then-ahead-of-time).
2. **Memory for Macs with 8 and 16 GB** (runtime): a 16 GB M1 Pro ran out of memory in the
   Forbidden Woods ([#8](https://github.com/bloodborne-native/bloodborne-mac/issues/8)), and 8 GB
   Macs are still sold. Main's peak footprint is 5.7 GB in Cathedral Ward (7.8 GB before the
   recompiled library stopped keeping the game decoded); next, the iPhone's compact memory layout
   as a Mac mode (the game's memory as one file mapping, Metal's view of it, nothing pinned), each
   step measured in footprint and FPS.
3. **N3, textures as objects** (runtime): textures taken as the objects the engine creates and
   releases, without a second copy of each in Metal (about 1–1.5 GB in Cathedral Ward).
4. **The recompiler's memory ordering** (recomp): ordering kept only around the engine's
   synchronization, which R4.4 named, with the maintainer's conditions (the generator's analysis,
   a safety case and a long play session). The rest of its CPU work is measured: calls left to the
   translator 69,600 a second to 9,400; flags, private frames, vector barriers and the host-call
   path gain little or nothing.

## Later

**Checks owed** (no code expected):

- Physics in play with the frame-rate hooks: running above 90 FPS, cloth, corpses.
- Laurence's cinematic above 30 FPS (needs a save near it).
- Frame-rate A/B of the motion-vector crash fix (expected nil).
- Real occlusion queries counted at the game's resolution (bbport 0.6's memory model): check ours.

**Bugs** (causes not isolated):

- Blood on already killed enemies can be pale with bright edges after a save reload.
- The camera after an in-game cutscene sometimes starts in front of the character.
- Five GPU tests (motion-shader, scene-resolution, taa-shader, camera-motion, translation-memory)
  no longer compile; they are listed in `runtime/gpu/CMakeLists.txt` instead of run.

**From other forks** (each measured on our build first):

- bbport 0.7: cloth fluttering above 30 FPS (Havok's stiffness per substep) and the play time
  counted correctly above 30 FPS; the point-light shadow wedges and the HUD's item-icon grid
  (check on Metal first); the frame limiter, the FPS drop after loading another save, the hit
  collector's cap. The list: the runtime's `docs/UPSTREAM.md`.

- Mods: more folder layouts load, and folders that do not are named (Supermedo `dd2314e`).
- An external FPS patch replaces the built-in preset (Supermedo `8042500`).
- Field of view; mute in the background (Supermedo `b75e811`).
- MoltenVK without Metal argument buffers (+13–16% FPS there) and with prefilled command buffers
  (fewer late frames there): A/B on the MoltenVK fallback.
- Queue the game's compute work before waiting for the previous submission (a black loading screen
  there).
- A texture budget that does not count the game's memory pool (their #19): check Metal's
  working-set limit on 16–18 GB Macs.
- The draw-list task lock (a stuck loading screen there): check whether our command-buffer guard
  covers it.
- Character-name entry in fullscreen (the IME text box): check ours first.
- DiAvisoo/bbport-mac-optimized's ideas, reviewed separately.

**Launcher:**

- Import and export complete save sets; manage the backup history.

**Graphics:**

- Background shader compilation: a missing pipeline compiles on a worker and its draw is skipped
  until ready, behind a setting.

**iOS** (the proof of concept: the game at 23 FPS at 960×540 on an iPhone 17 Pro Max, bound by
the CPU without JIT; on `main` since 2026-10-29,
[write-up](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/IOS_POC.md);
how code is organized: [Architecture](ARCHITECTURE.md#where-code-lives)):

1. Done (2026-10-29): the proof of concept merged to `main`, its platform code behind
   `TARGET_OS_IPHONE` (the game's mutex as host code stays iOS-only: it costs on the Mac), its
   general fixes for every platform (hashing without the decode cache, no JIT on iOS, the UI
   scale). bloodborne-ios builds from the runtime's `main` too (its core and GPU library compile;
   not yet run on the phone from it).
2. The iOS platform code in the runtime's platform layer behind an `ios-arm64` CMake preset and a
   compile-only CI job: the compact memory layout as a named mode, the system call and Metal
   format differences.
3. The runtime as a library with a small C API, `bb-probe` a thin program around it, and what
   `run.sh` and the Python scripts do moved into the runtime or the launcher (the Mac gains too).
4. bloodborne-ios (private while a proof of concept): the launcher as its interface (Tauri on iOS,
   the game in the same process), game files and saves on the phone, touch controls.
5. Toward 30 FPS on the phone: thread QoS, the PS4's own libraries through the recompiler, other
   spinning waits, MetalFX at a lower render resolution.

## Not taken

- **Seamless co-op (BBSC):** not supported for now (maintainer, 2026-10-26). BBSC is built on the
  game's internals, which no repository here may carry. A separately built and hosted module the
  runtime loads through a plugin interface could be discussed with BBSC's developer.
- **shadPS4's public online server** (bbport 0.51's module): it accepts only shadPS4's own builds.
- **bbport 0.6's new memory model** and the Windows fork's VRAM budget fixes: we use the unified
  pool.
- **Discrete-GPU and other platforms' fixes** from bbport 0.6 and the Windows fork (NVIDIA, Intel,
  Polaris, Steam Deck, AppImage, Windows), DLSS, frame generation, bbport's FSR 4.1.1 Vulkan
  assets, `VK_EXT_device_fault` (MoltenVK lacks it). Our FSR 4.1.1 runs on the Mac's GPU (0.8.3).
- **The Windows fork's stretched-polygon fixes** (`9566a1d`, `5012c6f`): bugs of its newer shadPS4
  base that our push block and index binding do not have. Its barrier memo (`08cd804`): we have it.

## Done

Where each landed; the release notes say what changed for players.

**CPU and recompiler** (bloodborne-recomp):

- R0–R3: every function recompiled and running in the game, with less CPU time than the translator
  (R3, 2026-10-25).
- The recompiled library built from the launcher with a downloaded LLVM toolchain (recomp
  `aa47a95`, runtime `8d2d469`, launcher `adec5ac`).
- R4: the engine's render code, synchronization and 20 busiest functions named and described
  (recomp `annotations/`, 2026-10-28).
- A faster translator (recomp #15, #16, #17, #18) and the runtime's own math and wide-string
  calls (runtime #7); the game's threads at user-interactive QoS (runtime #8).

**Graphics** (bloodborne-runtime):

- The native Metal renderer: every pipeline in Metal, the frame drawn through Metal, the render
  adapter (A0–A6, M1–M4), native startup without Vulkan or MoltenVK; the default since 0.9.0 RC 1,
  accepted as N5 (the maintainer, 2026-10-29). MoltenVK stays selectable as a fallback until the
  maintainer decides whether it leaves the macOS app.
- MetalFX (runtime PR #2) on the native frame; FSR 4.1.1 on the Mac's GPU with the MoltenVK renderer
  (runtime #1, 0.8.3).
- N0 (scope), N1 (frame planning: deferred clears).
- N6, the engine's render boundary (2026-10-28, merged 2026-10-29: runtime `cf0ce17d`; mesh draws
  recognised with the recompiled library too, recomp `8c49bc7`): the engine's draws matched to
  their packets and observed; every buffer address and resource slot found from its draw state;
  mesh draws bind their resources from it (`BB_RENDER_BOUNDARY=observe|mesh`).
- Crashes fixed: character motion vectors (runtime `57fba4f`), the GX worker with live dynamic
  shadows (`e8e14a3`), outputs above 1080p (`74c556e`), character lighting above 3.5 million
  pixels (`b2ff9cd`, `ab31a4c`); the shader cache no longer rebuilds every launch (`e8e14a3`,
  PR #3, `0e940e9`).
- Small fixes from bbport 0.6 and the Windows fork: the blur-kernel assertion, the larger GX
  command heap, stale texture formats, garbage PM4 headers, null vertex-buffer tables, early flip
  IRQs (runtime `63f043a`).

**bbport 0.6, ported by hand** (runtime): the renderer fixes; the present's wait; the frame rate
through hooks (F3 for 30 FPS); Laurence's cinematic above 30 FPS; effects switched live; aspect
ratios; keyboard and mouse with a menu pointer; button prompts for the device in use; online
(Seamless Hunt and The Hunter's Dream, runtime `49e2d2c`).

**bbport 0.7, ported by hand** (runtime): the GX occlusion query guard, the crash at `0x2169edc`
(whp199's PR #343; runtime `994846bb`). Its occlusion intervals were measured without a gain on
Metal and not taken.

**Memory and the recompiled library** (2026-10-29): hashing without the decode cache, from the
iPhone work (recomp `da077b8`: the peak footprint 7.8 GB to 5.7 GB); 99 more jump tables and the C
library's character tables and busiest calls on the host (recomp `0f344f8`, runtime `540a91b1`:
translator calls 69,600 a second to 9,400).

**Release candidates learn of newer releases** (launcher `9466d2d`): a candidate build carries its
tag and checks candidates too, so it is told about the next candidate and the final release.

**Releases:** 0.9.2 (2026-10-29): the recompiled-code build fixed (app issue #9), bbport 0.7's cloth,
play time and `0x2169edc` guard, about 2 GB less memory with the recompiled code. 0.9.1 (2026-10-28): the shader cache fix for black walls after long play (app issue
#7). 0.9.0 (2026-10-28): the release candidates' changes, the recompiled code page, a
faster translator, game threads on the performance cores, the on-screen keyboard fix.

**Launcher:** profiles and saves; trophies, with notices drawn by the game; settings shared with
the in-game menu (runtime `8cbcf64`, launcher `1dc03d8`); the save editor (attributes, Blood
Echoes, Insight, items, weapons, armor, gems and their slots; launcher `6f6f64a` to `1d77932`); the
Online page; the Recompiled code page; the slate-and-gold look, mirrored in the game's menus.
