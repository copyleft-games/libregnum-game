# Engine changes and source evidence

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/core/lrg-asset-manager.c](../../../../deps/libregnum/src/core/lrg-asset-manager.c) — inspect `lrg_asset_manager_load_asset`.
- [src/core/lrg-data-loader.c](../../../../deps/libregnum/src/core/lrg-data-loader.c) — inspect `lrg_data_loader_load_file_validated`.
- [tests/test-asset-manager.c](../../../../deps/libregnum/tests/test-asset-manager.c) — inspect `test_asset_dispatch_errors`.
- [tests/Makefile](../../../../deps/libregnum/tests/Makefile) — inspect `test-asset-manager`.

## Prove the missing capability
Start with the exact asset/operation, expected behavior and minimal reproduction.
Record the engine gitlink, dependency pins, enabled format/backend options and
error. Read declaration, implementation, callers and tests. Classify the finding
as implemented default, application hook, unsupported format, backend limitation
or defect. A heading in an API inventory is not implementation evidence.
Check whether a supported export already meets the game requirement before adding
a loader. The model file loader exists in graylib; duplicating its cache in game
code is not automatically an engine requirement.

## Change the owning layer
Game rules belong here. Reusable engine orchestration belongs in libregnum;
wrapper/decoder behavior may belong in graylib/raylib. Read each repository's own
instructions before edits. Add the smallest public contract with explicit error,
ownership and thread/context semantics. Register sources, headers, GTypes and
introspection metadata where the existing build requires them.

## Verification and dependency commits
Use a minimal licensed fixture and a regression that fails without the fix.
Keep decoding/context tests separate from pure validation. Check errors as well
as success, borrowed/full ownership, unload/reload and missing sidecars. Run the
owning module tests and relevant build/GIR checks; list pre-existing diagnostics.
Commit from the deepest changed repository outward, then update parent gitlinks.
A local gitlink referring to an unpublished dependency commit is not reproducible
for other clones: report this, and publish dependency commits before parent
commits only when pushing is authorized. Never silently edit detached dependency
files and claim the parent commit contains the fix.

Example result: a reproducible loader defect, narrowly scoped owning-layer fix,
fixture/license, regression test and ordered dependency/parent commits, with the
consumer load path rechecked. If the existing loader works, document its correct
use rather than adding an unused API.
