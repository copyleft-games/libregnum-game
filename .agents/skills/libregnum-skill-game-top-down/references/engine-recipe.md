# Top-down collision and interaction contracts

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-top-down-template.h](../../../../deps/libregnum/src/template/lrg-top-down-template.h) — inspect `check_collision`, `on_interact`, `on_interact_target_changed`.
- [src/template/lrg-top-down-template.c](../../../../deps/libregnum/src/template/lrg-top-down-template.c) — inspect `lrg_top_down_template_real_check_collision`.
- [examples/game-top-down-demo.c](../../../../deps/libregnum/examples/game-top-down-demo.c) — inspect `lrg_top_down_template`.
- [tests/test-template-2d.c](../../../../deps/libregnum/tests/test-template-2d.c) — inspect `lrg_top_down_template`.

## Collision contract
check_collision receives a proposed position and output coordinates. The default
writes the proposal unchanged and returns FALSE. A TRUE return means collision
occurred; supply both resolved coordinates. This is not a boolean "can move" API.
For wall sliding, resolve each axis against the same collider footprint. Test a
corner and movement parallel to a wall; normalizing diagonal input belongs before
speed integration, not inside an unrelated sprite update.

## Interaction loop
Define target IDs, distance, facing policy and priority when several targets are
near. on_interact performs the selected action; target-change notifications update
prompts. An NPC may disappear between selection and activation: revalidate the
reference/ID and eligibility before granting an item or entering a dialog.
Use input actions, not duplicate keyboard/controller implementations. A held
button must not repeatedly grant rewards while a dialog owns focus.

## Content and persistence
Keep IDs stable across maps, inventories, quests and saves; translated text is
presentation. Build a small connected flow: NPC grants quest → pickup grants key
→ locked door checks key → exit marks completion. Validate object definitions
with the content-pipeline skill, then enforce game-level references and rules.
Test full inventory, already-completed quest, invalid target, missing destination
and save/reload at each step. Separate pathfinding walkability from render layers.

## Reviewable result
Ship one room and a table of interaction IDs/ranges, collision tests, quest/key
round-trip tests and a launch command. Check controller focus and small-screen
text in a real window. Replacing art must preserve map and interaction units.
