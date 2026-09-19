# Physics Layers and Queries contracts

Read when implementing this skill. Audited engine pin: `6750d12e3102ad1b263828705695c8a750cd7fc1`.
Recheck the source before using these contracts with another revision.

## Source trail

- [src/physics/lrg-rigid-body.h](../../../../deps/libregnum/src/physics/lrg-rigid-body.h) — inspect `lrg_rigid_body_set_collision_mask`.
- [src/physics/lrg-rigid-body.c](../../../../deps/libregnum/src/physics/lrg-rigid-body.c) — inspect `collision_layer`.
- [src/physics/lrg-physics-world.h](../../../../deps/libregnum/src/physics/lrg-physics-world.h) — inspect `lrg_physics_world_raycast_filtered`.
- [src/physics/lrg-physics-world.c](../../../../deps/libregnum/src/physics/lrg-physics-world.c) — inspect `raycast_impl`.
- [tests/test-physics.c](../../../../deps/libregnum/tests/test-physics.c) — inspect `test_raycast_filters`, `test_collision_filters`.

## Pair filtering
`lrg_rigid_body_set_collision_layer()` sets membership bits; `set_collision_mask()`
sets accepted partner bits. Both directions must match for a collision pair.
Defaults are layer 1 and all mask bits. Changes affect subsequent steps without
re-adding the body. At least one body must be dynamic for the world to process
a pair; static/kinematic pairs are skipped. Trigger pairs still require matching masks and emit body
notifications without the normal solid-contact resolution path.
World membership retains bodies. Query hit pointers are borrowed; retain a
reference if they must survive world removal. AABB/point query arrays transfer
the container only, not ownership of each body.

## Ray queries
`lrg_physics_world_raycast_filtered()` accepts a closed start/end segment, layer
mask, include-triggers flag and optional ignored body, followed by optional hit
body/position/normal outputs. Only membership bits affect query filtering; body
collision masks do not. Zero query mask matches nothing. The legacy `raycast()`
includes all layers and triggers, even layer-zero bodies.

The nearest shape AABB wins; ties use world insertion order. Bounds are used for
circles and rotated bodies too: do not describe this as exact mesh/circle testing.
Starting inside/on a bound returns the start with zero normal. Corner ties use
the X-face normal. Nonfinite endpoints and zero-length segments miss. Misses
clear all outputs. Tiny nonzero segments remain valid; large finite endpoints
are handled using double intermediates. The query is 2D, not the 3D camera API.

## Verification
Use `tests/test-physics.c` as the executable caller: pairs with asymmetric masks,
triggers, high membership bits, ignored caster, zero filter, nearest versus
insertion order, equal-distance ties, endpoints on bounds, inside starts,
nonfinite/zero/tiny segments and output clearing. Game tests should additionally
cover occluded interactions and friendly-fire rules. Run root `make test` for
consumer behavior; run `make -C deps/libregnum test` for engine modifications.
