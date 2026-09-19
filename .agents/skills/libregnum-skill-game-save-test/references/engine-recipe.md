# Save sections, atomicity and migration

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/save/lrg-saveable.h](../../../../deps/libregnum/src/save/lrg-saveable.h) — inspect `get_save_id`, `save`, `load`.
- [src/save/lrg-save-manager.c](../../../../deps/libregnum/src/save/lrg-save-manager.c) — inspect `lrg_save_manager_register`, `lrg_save_context_enter_section`.
- [src/save/lrg-save-context.h](../../../../deps/libregnum/src/save/lrg-save-context.h) — inspect `lrg_save_context_set_version`, `lrg_save_context_has_key`.
- [tests/test-save.c](../../../../deps/libregnum/tests/test-save.c) — inspect `test_saveable_interface`.

## Saveable contract
Implement get_save_id, save and load with the exact interface signatures. The ID
is a stable borrowed string unique among registered objects. Register retains a
reference in a hash table keyed by ID; a duplicate ID replaces the prior entry.
Prevent duplicates in your game registration layer rather than expecting an error.
Unregister when a session object must no longer participate in saves.

The manager begins/enters the save-ID section before invoking each saveable.
Do not begin the same outer section again inside the implementation. Use nested
sections only for your own structured data. Standalone context tests must enter
the corresponding section themselves. Missing sections are skipped by the manager;
required-state absence is a game migration/validation decision.

## Loading is not a global transaction
The manager iterates registered saveables and stops on a failed load. Objects
loaded earlier may already have changed, and hash iteration is not a dependency
order. Never promise all-or-nothing world restore from this API alone.
For atomic game restore, decode/validate into temporary game state, resolve IDs,
then commit the validated aggregate; otherwise explicitly recover/reset after a
partial failure. Do not mutate live state field-by-field before validation.

## Schema and test plan
Version the save format and distinguish missing keys from legitimate zero values
using has_key. Reject malformed/range-invalid data and unknown required IDs.
Use isolated temporary directories and deterministic seeds; never real player saves.
Test version-one migration, corrupt YAML, absent section/key, duplicate IDs,
second-object load failure and save/reload at each progression boundary.

Example output: inventory saveable plus a migration fixture whose old item IDs
are mapped explicitly, a failing fixture that leaves the live inventory intact,
and documentation defining what happens if world-level restore fails.
