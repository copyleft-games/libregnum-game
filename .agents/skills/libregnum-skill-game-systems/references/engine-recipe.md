# State, input and ECS ownership

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/gamestate/lrg-game-state-manager.h](../../../../deps/libregnum/src/gamestate/lrg-game-state-manager.h) — inspect `lrg_game_state_manager_push`.
- [src/gamestate/lrg-game-state-manager.c](../../../../deps/libregnum/src/gamestate/lrg-game-state-manager.c) — inspect `lrg_game_state_manager_update`, `lrg_game_state_manager_handle_input`.
- [src/ecs/lrg-world.h](../../../../deps/libregnum/src/ecs/lrg-world.h) — inspect `lrg_world_add_object`.
- [src/ecs/lrg-game-object.h](../../../../deps/libregnum/src/ecs/lrg-game-object.h) — inspect `lrg_game_object_add_component`.
- [src/input/lrg-input-manager.h](../../../../deps/libregnum/src/input/lrg-input-manager.h) — inspect `lrg_input_manager_poll`.
- [tests/test-gamestate.c](../../../../deps/libregnum/tests/test-gamestate.c) — inspect `lrg_game_state_manager`.
- [tests/test-input.c](../../../../deps/libregnum/tests/test-input.c) — inspect `lrg_input_manager`.

## Ownership table
| Operation | Contract | Caller action |
|-----------|----------|---------------|
| state manager push/replace | transfer full | Relinquish that reference; use g_steal_pointer for an autoptr |
| world add_object | transfer none, world retains | Release caller reference when no longer needed |
| game object add_component | transfer none, object retains | Release caller reference independently |
| get component/current state | borrowed | Do not unref unless you first retained it |
| get_objects/get_components lists | transfer container | Free list container, not borrowed elements |

Never generalize "adding consumes ownership" across engine modules.

## Pause and state transitions
Blocking and transparent are independent state properties. Updates start at the
lowest blocking state found from the top; rendering starts at the lowest visible
state under transparent overlays. A transparent blocking pause menu can display
play underneath while stopping its updates. Input walks top to bottom until
handled, so the pause state's handler must consume gameplay actions appropriately.
Prefer template transition APIs in template callbacks and inspect their deferral
logic. Do not assume snapshotting stack length makes arbitrary removals safe in
every iteration. Test transition from an update/input callback and repeated pause.

## Input frames
Engine/template updates poll the input manager. A custom loop owns one poll per
frame, before action queries. Polling again per subsystem or per fixed step
advances snapshots and can lose edge events. Multiple readers should observe the
same frame; test held axis, first press, release and disconnected source behavior.

## ECS integration
Define world/component ownership and remove signal handlers with their owners.
Test a component removed while its target disappears, transform hierarchy changes
and collision-layer filtering. Rendering reads simulation state; it does not apply
damage or move entities. Content loading and audio have dedicated skills so their
validation/context requirements are not hidden inside a general ECS recipe.
