# Platformer collision and timing

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-platformer-template.h](../../../../deps/libregnum/src/template/lrg-platformer-template.h) — inspect `update_physics`, `check_ground`, `check_wall`.
- [src/template/lrg-platformer-template.c](../../../../deps/libregnum/src/template/lrg-platformer-template.c) — inspect `lrg_platformer_template_real_update_physics`, `lrg_platformer_template_real_check_ground`.
- [examples/game-platformer-demo.c](../../../../deps/libregnum/examples/game-platformer-demo.c) — inspect `demo_platformer_draw_world`.
- [tests/test-template-2d.c](../../../../deps/libregnum/tests/test-template-2d.c) — inspect `lrg_platformer_template`.

## What the base actually does
Ground detection compares player_y to ground_y. The default wall hook returns
false. update_physics integrates velocity and then clamps player_y to ground_y;
a custom check_ground alone does not replace that clamp. The base draws using
player_x as horizontal center and player_y as feet, with a separate hitbox.
There is no check_ceiling vfunc in this class. Do not invent one.

## Implement a real level
1. Define a consistent tile origin, feet/center convention and hitbox. Keep art
   offsets and transparent margins outside collision calculations.
2. The flat ground level is private to the base implementation; there is no public
   ground-level setter in this pin. For platforms, walls and
   ceilings, own update_physics/resolution deliberately; use the engine demo as
   a starting algorithm and inspect its compromises before copying it.
3. Resolve horizontal and vertical movement against world solids. Handle large
   steps by swept collision or bounded substeps; test contact without tunneling.
4. Keep grounded, jump-buffer and coyote state consistent with the chosen solver.
   Calling the parent and then applying another gravity integration doubles motion.
5. Keep landing events distinct from remaining grounded. Restart clears velocity,
   timers and wall state; camera reset follows the new spawn.

## Failure matrix
| Case | Required observation |
|------|----------------------|
| Head hits ceiling while rising | Upward velocity stops; player stays outside solid |
| Leaves a ledge | Coyote grace expires at the documented boundary |
| Jump pressed before landing | One buffered jump, not a repeated jump |
| High delta across thin tile | No tunneling through the tile |
| Death during wall slide | Restart has no stale slide or jump timer |
| Sprite replaced with padded image | Physics bounds remain unchanged |

Example result: one room with floor, raised ledge, ceiling, collectible and exit;
a table-driven solver test covers each contact direction, and manual play checks
jump feel plus camera/pixel scaling. A headless constructor test is insufficient.
