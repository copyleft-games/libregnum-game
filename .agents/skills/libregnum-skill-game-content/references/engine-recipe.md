# Validated definitions and live reload

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/core/lrg-registry.c](../../../../deps/libregnum/src/core/lrg-registry.c) — read for this workflow.
- [src/core/lrg-asset-manager.c](../../../../deps/libregnum/src/core/lrg-asset-manager.c) — read for this workflow.
- [tests/test-asset-dependencies.c](../../../../deps/libregnum/tests/test-asset-dependencies.c) — read for this workflow.

- [src/core/lrg-data-loader.h](../../../../deps/libregnum/src/core/lrg-data-loader.h) — inspect `lrg_data_loader_load_file_validated`, `lrg_data_loader_load_file`.
- [src/core/lrg-registry.h](../../../../deps/libregnum/src/core/lrg-registry.h) — inspect `lrg_registry_register`.
- [src/core/lrg-asset-manager.h](../../../../deps/libregnum/src/core/lrg-asset-manager.h) — inspect `lrg_asset_manager_load_object`, `lrg_asset_manager_reload_object`, `lrg_asset_manager_watch_object`.
- [tests/test-data-loader.c](../../../../deps/libregnum/tests/test-data-loader.c) — inspect `lrg_data_loader_load_file_validated`.
- [tests/test-asset-manager.c](../../../../deps/libregnum/tests/test-asset-manager.c) — inspect `lrg_asset_manager_reload_object`.

## Choose the correct loader
Register the YAML type name with its GType before loading. load_file expects a
root type field, with other fields mapped to properties. Use load_file_validated
for strict property checking; do not assume older permissive APIs have identical
validation. Custom decoders still own application invariants and cross-ID rules.
The direct data loader returns an owned object. Asset-manager load_object returns
a borrowed cached definition. Keep mutable run state separate from shared definitions.

## Reload semantics
reload_object validates a replacement before swapping the cache. Invalid edits
retain the old object; a changed GType is rejected. Existing references are not
mutated in place. Hold your own reference and handle object-reloaded to replace
consumer references intentionally, with a policy for existing spawned objects.
Resolved file paths are pinned until unload; changing search paths is not a
retroactive retarget of an already-cached definition.

watch_object is opt-in and watches the parent directory. Events are debounced on
the calling thread's thread-default GMainContext; iterate that context to deliver
reloads. All access belongs on that thread. Loader changes/unload/destruction stop
watches. Do not start a watcher on a context nobody drives.

## Verification recipe
Test unknown/unwritable property, numeric range, invalid enum, absent type, custom
decoder failure and missing referenced item ID. Then test valid reload replacing
the object, invalid reload retaining it, type change rejection, atomic rename,
delete/recreate and teardown with a queued event. Separate renderer checks from
headless definition validation. Tile images and map schemas remain distinct.

Example result: an enemy definition whose valid health edit affects new spawns,
whose invalid edit reports an error without replacing the cached object, and whose
old live enemy keeps an explicitly documented snapshot of its definition.

## Dependency reloads at the current pin
Use `lrg_asset_manager_add_object_dependency(name, dependency)` only after both
objects are cached. Duplicate links are harmless; cycles reject. Reloading a
source validates every transitive dependent before replacing any cached object.
Failure preserves the whole batch; success publishes the batch before emitting
signals in dependency order. Recursive reload returns `G_IO_ERROR_PENDING`.
Unload removes incident dependency links. This does not mutate existing consumer
references or infer dependencies from arbitrary fields. Test a diamond graph,
a cycle, invalid dependent rollback and signal-triggered unload using
[the dependency tests](../../../../deps/libregnum/tests/test-asset-dependencies.c).

Engine startup now registers the core scene/definition catalog idempotently,
preserving existing names. Register game-specific definitions explicitly; the
catalog excludes abstract types and device resources. Inspect
[the registry implementation](../../../../deps/libregnum/src/core/lrg-registry.c)
for exact catalog names before relying on automatic registration.
