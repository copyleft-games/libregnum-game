# Economies, cards and offline progression

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-tycoon-template.c](../../../../deps/libregnum/src/template/lrg-tycoon-template.c) — inspect `lrg_tycoon_template_real_update_economy`.
- [src/template/lrg-idle-template.c](../../../../deps/libregnum/src/template/lrg-idle-template.c) — inspect `lrg_idle_template_process_offline_progress`.
- [src/template/lrg-deckbuilder-combat-template.h](../../../../deps/libregnum/src/template/lrg-deckbuilder-combat-template.h) — inspect `G_DECLARE_FINAL_TYPE`.
- [src/template/lrg-deckbuilder-poker-template.h](../../../../deps/libregnum/src/template/lrg-deckbuilder-poker-template.h) — inspect `G_DECLARE_FINAL_TYPE`.
- [tests/test-template-idle.c](../../../../deps/libregnum/tests/test-template-idle.c) — inspect `lrg_idle_template`.
- [tests/test-template-deckbuilder.c](../../../../deps/libregnum/tests/test-template-deckbuilder.c) — inspect `lrg_deckbuilder`.

## Tycoon transaction boundary
The template manages time speed, grid presentation, days and economy tick hooks.
Entering build mode shows a grid; it is not a complete atomic placement/purchase.
Keep occupancy, resource cost, construction and cancellation in one game rule
operation. Validate all preconditions before mutating either balance or grid.
Tick callbacks are a scheduling mechanism: attach actual producers/consumers
explicitly and avoid double-scaling delta when time speed is already applied.

## Deckbuilder ownership
Combat and poker templates are final in this pin. Compose their APIs or select
the derivable base when a new class hierarchy is required. Maintain exactly one
zone owner per card instance and distinguish definitions from copies in a run.
Choose effect ordering and seeded shuffle semantics before implementing UI.
Test reshuffle with an empty discard, hand/energy limits, interrupted effects,
scoring ties, and a save that resumes the same deterministic rule state.

## Idle resume sequence
process_offline_progress reads the calculator snapshot, returns NULL for absent
or nonpositive elapsed time, simulates using efficiency/cap hooks, notifies the
game, applies progress via the idle mixin, then takes a new snapshot. The return
value is an owned BigNumber; do not apply it again after the template did so.
Persist the updated state/snapshot coherently so a crash/reload does not repeat a
reward. Decide clock rollback, cap and rounding rules and test them with a
controllable clock in the game rule layer. Use big-number APIs for large values.

Example: one workshop producer and upgrade, tested for insufficient funds,
occupied placement, paused ticking, capped offline income and resume twice.
Connect its UI only after the rule operation and persistence contract are clear.
