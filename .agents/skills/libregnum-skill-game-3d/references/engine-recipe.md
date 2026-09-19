# 3D movement, cameras and media

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/template/lrg-fps-template.c](../../../../deps/libregnum/src/template/lrg-fps-template.c) — inspect `lrg_fps_template_real_check_ground`.
- [src/template/lrg-third-person-template.h](../../../../deps/libregnum/src/template/lrg-third-person-template.h) — inspect `check_camera_collision`, `update_camera_orbit`.
- [src/template/lrg-third-person-template.c](../../../../deps/libregnum/src/template/lrg-third-person-template.c) — inspect `lrg_third_person_template_real_check_camera_collision`.
- [deps/graylib/src/graphics/grl-model.h](../../../../deps/libregnum/deps/graylib/src/graphics/grl-model.h) — inspect `grl_model_new_from_file`.
- [tests/test-template-3d.c](../../../../deps/libregnum/tests/test-template-3d.c) — inspect `lrg_fps_template`.

## Establish the scene contract
Document meters per unit, axes, model origin, collider size, camera eye height and
clip planes. The FPS default tests a flat floor with a small tolerance; it is not
a triangle-mesh collision solver. Third-person check_camera_collision returns
unchanged coordinates and FALSE by default. An orbit camera therefore needs a
game-specific obstruction query to avoid passing through walls.

## Model import sequence
Load after graphics startup on the context-owning thread. GrlModel's file loader
returns an owned GObject; release it before context teardown. Keep models separate
from collision shapes. A GLB may still reference an external texture: inspect
URIs and preserve relative paths, as the included barrel does.
Test an imported model at intended scale, with visible normals/materials and
known lighting. Successful mesh upload alone does not prove material correctness.
For animation, inspect grl-model-animation.h and the sample's skeleton/clip layout;
verify a specific clip instead of promising general exporter compatibility.

## Camera and controller checks
Implement obstruction from target toward desired camera position with a clear
collision margin and recovery policy. Test near walls, under low ceilings and
when teleporting/resetting. Release/reacquire mouse capture on focus transitions.
Test slope/edge grounding against the selected solver, high-speed movement,
restart, near clipping and controller movement independent of mouse look.
Use the racing skill for track checkpoints and surface/vehicle contracts.

Example result: a courtyard with a capsule controller, barrel with its texture,
obstruction-aware orbit camera and a documented world-scale measurement.
