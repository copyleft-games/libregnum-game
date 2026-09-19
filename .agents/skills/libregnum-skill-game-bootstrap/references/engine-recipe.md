# Template lifecycle and first playable

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-game-template.h](../../../../deps/libregnum/src/template/lrg-game-template.h) — inspect `lrg_game_template_startup`, `lrg_game_template_shutdown_game`, `create_initial_state`, `register_types`.
- [src/template/lrg-game-template.c](../../../../deps/libregnum/src/template/lrg-game-template.c) — inspect `lrg_game_template_startup`, `lrg_input_manager_poll`, `lrg_audio_manager_update`.
- [tests/test-template.c](../../../../deps/libregnum/tests/test-template.c) — inspect `test_game_template_input_frame`.

## Host ownership and startup order
`lrg_game_template_run` supplies the standalone host. Hosted startup borrows the
engine and retains the host window; the game must not start/stop another engine.
The source order is configure → borrow host resources → create state/input/event/
settings objects → input bindings → register types → pre_startup → initial state
push → post_startup. Constructors alone do not provide a running state manager.
Load content only when its context exists. `register_types` precedes definitions.
Shutdown calls the game hook before clearing states. A state may still refer to
shared assets during its exit: release state-owned resources in state teardown,
and game-owned resources at a point where consumers no longer use them.

## Choose the implementation boundary
For a derivable template, override the declared vfunc with its exact signature;
chain the parent when preserving its work. Combat/poker deckbuilders are final:
compose states or use their derivable parent. Twin-stick and shmup are derivable
in this pin despite older engine prose claiming otherwise.
Keep the factory in src/game-starter.c as the one routing table. Add explicit
GAME_SRCS entries. Put input-independent rules in modules that GTest can exercise.
Start with one complete start/play/result/restart loop; a template constructor
is not a level, encounter, track or persistence implementation.

## Timing decision
The template polls input once per host frame. Its fixed-step path calls
fixed_update and the state manager inside the accumulator loop; the variable
path uses pre_update/post_update around state updates. Do not assume changing
use-fixed-timestep migrates a genre's pre_update physics into fixed_update.
Trace the selected class and choose one simulation owner; never advance both.
The accumulator clamps long frames and caps updates. Test stall recovery,
zero delta, multiple simulation steps and one-shot input consumed once.

## First-playable acceptance example
Input: a 640×360 top-down key-and-door prototype.
Result: a game class selected by the factory, one collision room, an inventory
rule module, title/play/result transitions and tests proving the door cannot open
without a key. Include the launch command, controls, data root and save policy.
Restart must restore the same initial state without stale signal handlers.

## Template timers at the current pin
The template constructs its timer manager before startup and exposes it as a
borrowed object through `lrg_game_template_get_timer_manager()`. It advances once
per host frame before fixed/variable gameplay hooks and clears after state exit
hooks on shutdown. Do not double-update it. For pause/scale semantics and
state-owned cancellation, read [gameplay utilities](../../libregnum-skill-gameplay-utilities/SKILL.md).
