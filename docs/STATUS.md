# Status

[← Documentation](README.md)

Where the whole project stands: what is released, what is on main, what is being worked on and
what comes next. Updated 2026-10-28. The plan in order: [Roadmap](ROADMAP.md). Each repository's
own status: [runtime](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md#progress),
[recompiler](https://github.com/bloodborne-native/bloodborne-recomp/blob/main/docs/RECOMPILATION.md#milestones),
[launcher](https://github.com/bloodborne-native/bloodborne-launcher/blob/main/README.md#status).

## At a glance

- **Released:** 0.9.1, on 2026-10-28: the shader cache no longer turns walls black after long play
  ([notes](releases/v0.9.1.md)); 0.9.0, the same day, brought the native Metal renderer, online
  play, the save editor and the recompiled code page ([notes](releases/v0.9.0.md)).
- **Playable** on Apple Silicon: about 40 FPS in play at native 1080p on an M3 Pro with the Metal
  renderer ([performance](guide/performance.md)).
- **Now:** accepting the native Metal renderer (N5), with players' reports on 0.9.x.
- **Under way:** the recompiler's CPU work: calls left to the translator down from 69,600 a second
  to 9,400 (CPU time 342% to 339% for the first half); the host-call path measured without a
  gain. Left: memory ordering, with the maintainer's conditions.
- **Paused** on the runtime's `n6` branch: N6 is done (the engine's draws observed at its render
  boundary; mesh draws bind their resources from its draw state); N2, shaders built to read the
  draw state instead of the PS4 user data, has its plan and inventory (40%).

## Milestones

Each bar has 20 blocks, one per 5% of the milestone's defined steps.

| Milestone | Progress | State |
|---|---|---|
| **CPU** (bloodborne-recomp) | | |
| R0–R2 · groundwork, prototype, every function recompiled | 100% `████████████████████` | The game runs on 240,978 recompiled functions; the translator remains the fallback |
| R3 · speed | 100% `████████████████████` | 14% less CPU time than the translator at the same frame rate |
| The library built from the launcher | 100% `████████████████████` | 13.5 minutes on an M3 Pro, no Xcode needed |
| R4 · names for the engine's code | 100% `████████████████████` | 204 functions named; the draw state, models, materials and shaders described |
| The recompiler's CPU work | 30% `██████░░░░░░░░░░░░░░` | The first plan measured (flags, private frames, vector barriers: little or nothing); more jump tables and host C library calls: translator calls 69,600 a second to 9,400, 342% to 339%; the host-call path without a gain; next, memory ordering (the maintainer's conditions) |
| **Graphics** (bloodborne-runtime) | | |
| N0 · scope, N1 · frame planning | 100% `████████████████████` | Deferred clears |
| N4 · render adapter | 100% `████████████████████` | The renderer on the project's own GPU interface |
| N5 · Metal backend | 95% `███████████████████░` | The default since 0.9.0 RC 1; the maintainer's play sessions passed; acceptance waits for players' reports on the release candidates and M1/M2 comparisons |
| N6 · the engine's render boundary | 100% `████████████████████` | Done on the runtime's `n6` branch (re-scoped 2026-10-28): 99.94% of the engine's draws matched to their packets, their state and resources agreeing; every buffer address and resource slot found from the draw state; mesh draws bind their resources from it ([details](https://github.com/bloodborne-native/bloodborne-runtime/blob/n6/docs/NATIVE_RENDERER.md#n6-the-engines-render-boundary)). The other draw kinds move to N2: converted GCN shaders read the user data themselves, so taking draws over saves nothing until N2 |
| N2 · shaders from the draw state, then ahead of time | 40% `████████░░░░░░░░░░░░` | On the runtime's `n6` branch: the plan written ([steps](https://github.com/bloodborne-native/bloodborne-runtime/blob/n6/docs/NATIVE_RENDERER.md#n2-shaders-from-the-draw-state-then-ahead-of-time)). The inventory: the game's shaders use the PS4 user data only to locate their resources, so shaders bound to the draw state's slots need none. Next: mesh shaders built that way |
| N3 · textures as objects | 0% `░░░░░░░░░░░░░░░░░░░░` | After N2 |
| **Platforms** | | |
| macOS (Apple Silicon) | | Released |
| iOS | proof of concept | 23 FPS on an iPhone 17 Pro Max; the steps to a real app are in the roadmap |
| Linux | runtime only | The Vulkan backend builds and passes its tests (manual CI); no app |

## Releases

| Version | Highlights |
|---|---|
| 0.9.1 | The shader cache no longer reuses a shader's slot, which drew walls and scenery black after long play; caches are rebuilt once; the draw-preparation threads about 10% less busy |
| 0.9.0 | The release candidates' changes; the recompiled code page (the library built on the player's Mac); a faster translator; the game's threads on the performance cores; the on-screen keyboard no longer reopens after a name is typed |
| 0.9.0 RC 2 | Online play; the save editor; the launcher's new look with Saves and Trophies tabs; in-game menus in its colours; a faster translator; macOS 15 |
| 0.9.0 RC 1 | The native Metal renderer by default (MoltenVK as the fallback); MetalFX on the native frame; button prompts for the device in use; keyboard and mouse in the in-game menu |
| 0.8.3 | Mods and Patches pages fixed; character editing in every language; optional FSR 4.1.1 on Metal; trophy notices drawn by the game |
| 0.8.2 | High-resolution character lighting fixed |
| 0.8.1 | GX worker crash fixed; MetalFX; the shader cache no longer rebuilds every launch |
| 0.8.0 | Motion-vector crash fixed; settings shared with the in-game menu; outputs above 1080p; the experimental Metal renderer |
| 0.7.0 | Stretched geometry fixed; local trophies |
| 0.6.0 | Profiles and saves; the opening-video crash fixed |

Release notes: [docs/releases](releases/). bbport compatibility: 0.51, plus parts of 0.6 ported by
hand.

## On main

Main is 0.9.1, plus:

- **R4** (bloodborne-recomp's `annotations/`): the engine's render boundary, the draw state,
  models, meshes, materials, shader programs, the synchronization primitives and the 20 busiest
  functions, named and described for N6 and the generator. `BB_DRAW_CENSUS=1` (runtime) counts the
  game's draws and locks at that boundary.
- **CI caches:** the app's and the runtime's workflows keep the built dependencies and a compiler
  cache between runs: a release build takes about 25 minutes instead of 60.

## How native it is

| Part | Native now | Still not native |
|---|---|---|
| The game's code | With the recompiled library: 240,975 of 241,031 functions as arm64 code compiled on the player's Mac, 99% of instructions in C; 9,400 calls a second still reach the translator (Cathedral Ward) | The library is opt-in (the translator is the default); the game's own C library and file-streaming modules (libc.prx, libSceFios2.prx) run translated, their busiest functions replaced by host code |
| The PS4's system services | Threads, memory, files, saves, input, audio, network and trophies are the runtime's host code; no PS4 firmware | libc.prx and libSceFios2.prx, above |
| Graphics | R5 at 76%: every frame drawn by Metal directly, without Vulkan or MoltenVK; the GCN shaders converted to Metal once and cached (they stay converted, by the maintainer's decision) | The game still writes PS4 GPU command buffers that the runtime decodes each frame (about 0.6 core); N2 (shaders reading the engine's draw state, then ahead of time) and N3 (textures as objects) |
| Platforms | macOS released | iOS a proof of concept; Linux the runtime only |

## Areas

| Area | State |
|---|---|
| CPU | bbcpu translates the game's x86-64 code to arm64 as it runs (the default); the recompiled library runs it compiled ahead of time from the player's own copy, with 14% less CPU time ([Recompilation](https://github.com/bloodborne-native/bloodborne-recomp/blob/main/docs/RECOMPILATION.md)) |
| Graphics | Native Metal by default, without Vulkan or MoltenVK; MoltenVK selectable until N5 is accepted; Vulkan on Linux. Upscalers: MetalFX with the Metal renderer; FSR 3.1 and FSR 4.1.1 (run on the Mac's GPU) with MoltenVK ([native renderer](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md)) |
| Game features | bbport 0.6's frame rate through hooks (F3 for 30 FPS), live effects, aspect ratios, keyboard and mouse, Laurence's cinematic above 30 FPS |
| Online | Seamless Hunt and The Hunter's Dream (the runtime's `bbnet20`, GPL-3.0-or-later); tested here without an account, players are testing both pools with 0.9.0. Seamless co-op (BBSC) is not supported |
| Launcher | Profiles and saves with backups; trophies; the save editor (attributes, items, weapons, armor, gems; an edited save earns no trophies and plays offline only); settings shared with the in-game menu; mods and patches; 20 languages; platform-neutral code with CI on macOS, Linux and Windows ([launcher docs](https://github.com/bloodborne-native/bloodborne-launcher/tree/main/docs)) |

## Open issues

- **Known bugs:** blood on already killed enemies can look pale after a save reload; the camera
  after a cutscene sometimes starts in front of the character. Causes not isolated.
- **Watch list:** a short white flash in the opening video and an enemy drawn as colour noise
  have not recurred, without a confirmed fix. A GXRenderThread crash in Cathedral Ward
  ([#3](https://github.com/bloodborne-native/bloodborne-mac/issues/3)) and a crash on death in
  Central Yharnam ([#5](https://github.com/bloodborne-native/bloodborne-mac/issues/5)) could not be
  reproduced and are closed until they happen again. Older rare assertions: the runtime's
  [stability notes](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/STABILITY.md).
- **Only one Mac measured** (M3 Pro); results from M1, M2 and M4 Macs are needed for N5's
  acceptance.
- **Tests:** five GPU tests no longer compile and are not run (roadmap, Later).
