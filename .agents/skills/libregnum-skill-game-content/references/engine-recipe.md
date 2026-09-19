# Validated definitions and live reload

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

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
