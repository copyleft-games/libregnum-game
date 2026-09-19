# Projectiles and specialization

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-shooter-2d-template.h](../../../../deps/libregnum/src/template/lrg-shooter-2d-template.h) — inspect `spawn_projectile`, `update_projectiles`, `on_projectile_hit`.
- [src/template/lrg-shooter-2d-template.c](../../../../deps/libregnum/src/template/lrg-shooter-2d-template.c) — inspect `lrg_shooter_2d_template_real_update_projectiles`.
- [src/template/lrg-twin-stick-template.h](../../../../deps/libregnum/src/template/lrg-twin-stick-template.h) — inspect `G_DECLARE_DERIVABLE_TYPE`, `update_aim`.
- [src/template/lrg-shmup-template.h](../../../../deps/libregnum/src/template/lrg-shmup-template.h) — inspect `G_DECLARE_DERIVABLE_TYPE`, `on_graze`.
- [tests/test-template-2d.c](../../../../deps/libregnum/tests/test-template-2d.c) — inspect `lrg_shooter_2d_template`.

## Implemented defaults and missing gameplay
The shooter already keeps a bounded projectile pool with active slots, IDs,
owner IDs, speed and lifetime. Spawning can fail when capacity is exhausted.
Default updates integrate position and expire projectiles by lifetime/play area.
The hit hook emits a signal: movement alone is not enemy collision detection,
damage, faction policy or score awarding. Do not add a second pool reflexively.
The base firing direction is upward. Twin-stick and shmup are derivable classes;
use their actual header hooks for aiming/dashing or bomb/graze/life behavior.

## Add a weapon and wave
Specify aim normalization, projectile radius, owner/faction filtering and a
single hit-resolution owner. Expire or mark the projectile before another overlap
can award the same hit. Decide piercing, invulnerability and kill credit explicitly.
Keep IDs stable for the active lifetime and remove stale target references.
Use simulation time for cooldowns and seeded wave schedules. Full pools must not
consume ammunition or advance cooldown unless that is the chosen rule.

## Verification recipe
Spawn one projectile toward one enemy and assert one health change and one score
award. Cover two overlaps in a frame, enemy removal during hit dispatch, pool
exhaustion, zero direction, lifetime boundary and out-of-bounds removal. Restart
resets active projectiles, RNG and wave counters. Manually check mouse/stick aim,
controller dead zones, focus loss and pause. Test at different frame rates before
claiming deterministic behavior; variable-step floating-point integration may differ.

Example output: a one-wave arena with deterministic spawn tests, damage ownership
documented in docs/, and measured pool capacity for the target frame budget.
