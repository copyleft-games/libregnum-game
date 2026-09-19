# Navigation and Route Editing contracts

Read when implementing this skill. Audited engine pin: `6750d12e3102ad1b263828705695c8a750cd7fc1`.
Recheck the source before using these contracts with another revision.

## Source trail

- [src/pathfinding/lrg-pathfinder.h](../../../../deps/libregnum/src/pathfinding/lrg-pathfinder.h) — inspect `lrg_pathfinder_find_path`.
- [src/pathfinding/lrg-pathfinder.c](../../../../deps/libregnum/src/pathfinding/lrg-pathfinder.c) — inspect `LRG_PATHFINDING_ERROR_ITERATION_LIMIT`.
- [src/pathfinding/lrg-nav-mesh.h](../../../../deps/libregnum/src/pathfinding/lrg-nav-mesh.h) — inspect `lrg_nav_mesh_bake`.
- [src/pathfinding/lrg-nav-mesh.c](../../../../deps/libregnum/src/pathfinding/lrg-nav-mesh.c) — inspect `lrg_nav_mesh_find_path`.
- [src/pathfinding/lrg-path.h](../../../../deps/libregnum/src/pathfinding/lrg-path.h) — inspect `lrg_path_append_path`.
- [src/pathfinding/lrg-path.c](../../../../deps/libregnum/src/pathfinding/lrg-path.c) — inspect `lrg_path_foreach`.
- [tests/test-pathfinding.c](../../../../deps/libregnum/tests/test-pathfinding.c) — inspect `test_pathfinder_iteration_limit`.
- [tests/test-nav-mesh.c](../../../../deps/libregnum/tests/test-nav-mesh.c) — inspect `test_obstacle_corridor`.
- [tests/test-gameplay-utilities.c](../../../../deps/libregnum/tests/test-gameplay-utilities.c) — inspect `test_path_append_path`.

## Grid search
`LrgNavGrid` and `LrgPathfinder` are GObjects; `find_path()` returns an owned boxed
`LrgPath`, released with `lrg_path_free()` or its autoptr, never object unref.
Inspect `set_allow_diagonal()` and corner policy before choosing movement rules.
The default heuristic uses cost-scaled Manhattan/octile distance. Zero-cost cells
and custom neighbor graphs fall back to Dijkstra. Custom heuristics must be
finite nonnegative lower bounds, zero at the goal; do not mutate during search.

`set_max_iterations()` bounds node expansions, not wall time or initial cost
scanning. Zero is unlimited. Start and goal count when expanded; identical
endpoints return without expansion. Goal reached on the final allowed expansion
succeeds. Distinguish `LRG_PATHFINDING_ERROR_ITERATION_LIMIT` from `NO_PATH`.
A new attempt is a fresh search, not a continuation token. Verify smoothing
against terrain and corner rules before applying it to actor movement.

## Mesh navigation
`LrgNavMesh` is a thread-confined final GObject. `bake()` accepts XYZ (Y up) and
triangle indices, discards degenerate/steep triangles and joins exact shared
complete edges, including duplicated positions. Non-manifold edges reject.
Failed bake preserves prior mesh and flags. Supply unobstructed walkable surfaces
with agent clearance already included: this API does not subtract obstacles or
voxelize arbitrary render geometry.

`project()` limits endpoint projection by 3D distance. `find_path()` returns an
owned flat array of doubles (free with `g_free`), with a coordinate count, not a
point count. The path contains projected endpoints and shared-edge midpoints.
Its centroid-cost corridor is not the globally shortest geometric route.
`set_enabled()` blocks polygons until a new successful bake; replan existing
routes yourself. Projection/connectivity failures use `G_IO_ERROR_NOT_FOUND`.

## Route editing
`set_point()`, `remove_point()`, `truncate()` and `append_path()` reset stored cost
when geometry changes. No-op edits preserve cost; legacy append/prepend/reverse
keep their existing behavior. `get_distance()` is Euclidean grid-coordinate
length, independent of terrain cost. Append copies points, allows self-append,
keeps duplicate endpoints and does not validate a connecting route.
`foreach()` snapshots original points and indices; callback mutations do not
alter the iteration. Nested iteration sees current state. If a callback frees
the path, clear its owning pointer to avoid later double-free.

## Verification
Adapt `test-pathfinding.c`, `test-nav-mesh.c` and `test-gameplay-utilities.c`:
blocked/invalid endpoints, budget exhaustion, zero/subunit costs, disconnected
triangles, narrow corridors, projection limits, failed bake preserving state,
polygon blocking, invalid edit indices and self-append. Run engine tests when
changing engine behavior and root `make test` for game steering integration.
A valid path is not proof that a rendered character fits through a corridor.
