# Track progression and vehicle surfaces

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-racing-2d-template.h](../../../../deps/libregnum/src/template/lrg-racing-2d-template.h) — inspect `get_surface_at`, `on_checkpoint_passed`, `update_vehicle`.
- [src/template/lrg-racing-3d-template.h](../../../../deps/libregnum/src/template/lrg-racing-3d-template.h) — inspect `check_checkpoints`, `on_checkpoint_reached`.
- [src/template/lrg-racing-3d-template.c](../../../../deps/libregnum/src/template/lrg-racing-3d-template.c) — inspect `lrg_racing_3d_template_real_check_checkpoints`.
- [tests/test-template-3d.c](../../../../deps/libregnum/tests/test-template-3d.c) — inspect `lrg_racing_3d_template`.
- [tests/test-template-2d.c](../../../../deps/libregnum/tests/test-template-2d.c) — inspect `lrg_racing_2d_template`.

## Choose the dimensional contract
2D and 3D use different hook names. The 2D template exposes get_surface_at and
on_checkpoint_passed; 3D exposes check_checkpoints and on_checkpoint_reached.
The 3D default check_checkpoints is a no-op, so merely drawing a track cannot
count laps. Read the corresponding template before sharing rule code between them.

## One-lap prototype
Specify distance/speed/angle units, acceleration/braking/traction, checkpoint
volumes, required order and direction. Keep lap rules independent of rendering.
Use entry-edge detection or a cooldown so remaining inside a gate cannot repeatedly
award progress. Require all gates before start-line completion; choose a policy
for reversing, teleporting, shortcutting and off-track reset.
Track surface queries affect vehicle behavior but are not a collision mesh. Add
contacts and barriers appropriate to the chosen dimension. Reset camera and
vehicle velocity together without silently awarding the gate at the reset point.

## Test matrix
Check out-of-order gate, repeated overlap, backwards crossing, missed gate,
reset inside gate, countdown start, finish lockout and different frame deltas.
Record an ordered lap trace and assert exactly one lap. Manually test steering,
boost feedback, camera shake and speed readability on the target input device.

Example result: a three-gate loop with a surface patch, vehicle reset, a lap HUD,
and a headless progression test that rejects crossing the finish backwards.
