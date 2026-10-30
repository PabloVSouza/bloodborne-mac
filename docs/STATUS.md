# Status

[← Documentation](README.md)

Where the whole project stands: what is released, what is on main, what is being worked on and
what comes next. Updated 2026-10-29. The plan in order: [Roadmap](ROADMAP.md). Each repository's
own status: [runtime](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md#progress),
[recompiler](https://github.com/bloodborne-native/bloodborne-recomp/blob/main/docs/RECOMPILATION.md#milestones),
[launcher](https://github.com/bloodborne-native/bloodborne-launcher/blob/main/README.md#status).

## At a glance

- **Released:** 0.9.2, on 2026-10-29: building the recompiled code works again, cloth no longer
  flutters at high frame rates, the rare `0x2169edc` crash is guarded and the recompiled code
  uses about 2 GB less memory ([notes](releases/v0.9.2.md)). 0.9.0 brought the native Metal
  renderer, online play, the save editor and the recompiled code page ([notes](releases/v0.9.0.md)).
- **Playable** on Apple Silicon: about 40 FPS in play at native 1080p on an M3 Pro with the Metal
  renderer in 0.9.2 ([performance](guide/performance.md)). On `main`, lossless texture compression
  (2026-10-30, adapted from [MojahedAbushawish](https://github.com/MojahedAbushawish)'s lazy texture usages for Wooloomooloo2's [bloodborne_mac_port](https://github.com/Wooloomooloo2/bloodborne_mac_port), #33) gives
  48.0–49.2 FPS standing in Iosefka's Clinic against 36.3–36.7.
- **Now:** the native renderer (the maintainer's focus from 2026-10-29): N2, shaders built to
  read the engine's draw state instead of the PS4 user data, then the game's shaders built ahead
  of time as native shaders for each platform. The Metal renderer (N5) is accepted (2026-10-29).
- **Memory for smaller Macs:** a 16 GB M1 Pro ran out of memory in the Forbidden Woods with the
  MoltenVK renderer ([#8](https://github.com/bloodborne-native/bloodborne-mac/issues/8), closed:
  the default Metal renderer does not run out there). The game's peak footprint
  in Iosefka's Clinic is down from 7.8 GB to 5.7 GB on main (the recompiled library no longer keeps
  the whole game decoded); next, the iPhone's compact memory layout as a Mac mode, toward 8 GB Macs.
- **The recompiler's CPU work:** calls left to the translator down from 69,600 a second to 9,400;
  what is left (memory ordering) waits for the maintainer's conditions.

## Milestones

Each bar has 20 blocks, one per 5% of the milestone's defined steps.

| Milestone | Progress | State |
|---|---|---|
| **CPU** (bloodborne-recomp) | | |
| R0–R2 · groundwork, prototype, every function recompiled | 100% `████████████████████` | The game runs on 240,978 recompiled functions; the translator remains the fallback |
| R3 · speed | 100% `████████████████████` | 14% less CPU time than the translator at the same frame rate |
| The library built from the launcher | 100% `████████████████████` | 13.5 minutes on an M3 Pro, no Xcode needed |
| R4 · names for the engine's code | 100% `████████████████████` | 204 functions named; the draw state, models, materials and shaders described |
| The recompiler's CPU work | 30% `██████░░░░░░░░░░░░░░` | The first plan measured (flags, private frames, vector barriers, the host-call path: little or nothing); more jump tables and host C library calls: translator calls 69,600 a second to 9,400, 342% to 339%; next, memory ordering (the maintainer's conditions) |
| **Graphics** (bloodborne-runtime) | | |
| N0 · scope, N1 · frame planning | 100% `████████████████████` | Deferred clears |
| N4 · render adapter | 100% `████████████████████` | The renderer on the project's own GPU interface |
| N5 · Metal backend | 100% `████████████████████` | Accepted (the maintainer, 2026-10-29); the default since 0.9.0 RC 1; MoltenVK selectable as a fallback |
| N6 · the engine's render boundary | 100% `████████████████████` | Done (re-scoped 2026-10-28; on main since 2026-10-29): 99.94% of the engine's draws matched to their packets, their state and resources agreeing; every buffer address and resource slot found from the draw state; mesh draws bind their resources from it, with the translator or the recompiled library ([details](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md#n6-the-engines-render-boundary)). The other draw kinds move to N2: converted GCN shaders read the user data themselves, so taking draws over saves nothing until N2 |
| N2 · shaders from the draw state, then native shaders ahead of time | 75% `███████████████░░░░░` | The plan, the inventory, N2.3 and most of N2.4: 92% of draw shader stages and 79% of compute dispatch stages run without the PS4 user data's walker, taking their resources from the engine's state or straight from the registers it sets (opt-in, `BB_RENDER_BOUNDARY=flat`; exact; the observer still costs about 45 CPU points) ([details](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md#n2-shaders-from-the-draw-state-then-ahead-of-time)). Next: the last walker users, then native shaders built ahead of time |
| N3 · textures as objects | 0% `░░░░░░░░░░░░░░░░░░░░` | After N2 |
| **Platforms** | | |
| macOS (Apple Silicon) | | Released |
| iOS | proof of concept | iPhone 17 Pro Max, 960×540: 38–42 FPS uncapped in the first 20 s; capped at 30, it holds 30 once the phone throttles (2026-10-30). The steps to a real app are in the roadmap |
| Linux | runtime only | The Vulkan backend builds and passes its tests (manual CI); no app |

## Releases

| Version | Highlights |
|---|---|
| 0.9.2 | The recompiled-code build fixed (it starts, survives leaving the page, counts as it compiles, Cancel stops it all); cloth at high frame rates and the play time (bbport 0.7); the `0x2169edc` crash guarded (bbport 0.7); about 2 GB less memory and fewer translator calls with the recompiled code |
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

Release notes: [docs/releases](releases/). bbport compatibility: 0.51, plus parts of 0.6 and 0.7
ported by hand (the runtime's [Upstream](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/UPSTREAM.md)).

## On main

Main is 0.9.2, plus:

- **R4** (bloodborne-recomp's `annotations/`): the engine's render boundary, the draw state,
  models, meshes, materials, shader programs, the synchronization primitives and the 20 busiest
  functions, named and described for N6 and the generator. `BB_DRAW_CENSUS=1` (runtime) counts the
  game's draws and locks at that boundary.
- **CI caches:** the app's and the runtime's workflows keep the built dependencies and a compiler
  cache between runs: a release build takes about 25 minutes instead of 60.

## How native it is

| Part | Native now | Still not native |
|---|---|---|
| The game's code | With the recompiled library: 240,975 of 241,031 functions as arm64 code compiled on the player's Mac, 99% of instructions in C; 9,400 calls a second still reach the translator (Iosefka's Clinic) | The library is opt-in (the translator is the default); the game's own C library and file-streaming modules (libc.prx, libSceFios2.prx) run translated, their busiest functions replaced by host code |
| The PS4's system services | Threads, memory, files, saves, input, audio, network and trophies are the runtime's host code; no PS4 firmware | libc.prx and libSceFios2.prx, above |
| Graphics | R5 at 80%: every frame drawn by Metal directly, without Vulkan or MoltenVK; the GCN shaders converted to Metal once and cached (they stay converted, by the maintainer's decision) | The game still writes PS4 GPU command buffers that the runtime decodes each frame (about 0.6 core); N2 (shaders reading the engine's draw state, then ahead of time) and N3 (textures as objects) |
| Platforms | macOS released | iOS a proof of concept; Linux the runtime only |

## Areas

| Area | State |
|---|---|
| Graphics | Native Metal by default, without Vulkan or MoltenVK; MoltenVK selectable as a fallback; Vulkan on Linux. Upscalers: MetalFX with the Metal renderer; FSR 3.1 and FSR 4.1.1 (run on the Mac's GPU) with MoltenVK ([native renderer](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/NATIVE_RENDERER.md)) |
| Game features | bbport 0.6's frame rate through hooks (F3 for 30 FPS), live effects, aspect ratios, keyboard and mouse, Laurence's cinematic above 30 FPS |
| Online | Seamless Hunt and The Hunter's Dream (the runtime's `bbnet20`, GPL-3.0-or-later); tested here without an account, players are testing both pools with 0.9.0 |
| Launcher | Profiles and saves with backups; trophies; the save editor (attributes, items, weapons, armor, gems; an edited save earns no trophies and plays offline only); settings shared with the in-game menu; mods and patches; 20 languages; platform-neutral code with CI on macOS, Linux and Windows ([launcher docs](https://github.com/bloodborne-native/bloodborne-launcher/tree/main/docs)) |

## Open issues

- **Known bugs:** blood on already killed enemies can look pale after a save reload; the camera
  after a cutscene sometimes starts in front of the character. Causes not isolated.
- **The GXRenderThread crash** at `0x2169edc`
  ([#7](https://github.com/bloodborne-native/bloodborne-mac/issues/7)): guarded on main, kept open
  until a long session passes without it.
- **Watch list:** a short white flash in the opening video and an enemy drawn as colour noise
  have not recurred, without a confirmed fix. A crash on death in Central Yharnam
  ([#5](https://github.com/bloodborne-native/bloodborne-mac/issues/5)) could not be reproduced and
  is closed until it happens again. Older rare assertions: the runtime's
  [stability notes](https://github.com/bloodborne-native/bloodborne-runtime/blob/main/docs/STABILITY.md).
- **Only one Mac measured** (M3 Pro); results from M1, M2 and M4 Macs are welcome.
- **Tests:** five GPU tests no longer compile and are not run (roadmap, Later).
