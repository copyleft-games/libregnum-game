---
name: libregnum-skill-game-save-test
description: Test game rules and persistence with libregnum. Use for save/load, migrations, deterministic behavior or release verification.
---

# Skill: Save and Test

Protect player progress and make gameplay regression checks repeatable.

## When to Use

Saving, migration, regression tests, deterministic replays or release preparation.

## Prerequisites

A checkout with pinned engine sources and a game brief. See README.md for C
build packages. Python 3 runs starter/source checks; runtime tests require the
selected engine build and device-dependent checks need their graphics/audio context.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

First read [the engine recipe](references/engine-recipe.md) for this task. It
links the inspected headers, implementations and tests, identifies defaults and
missing game behavior, and gives concrete failure cases. Recheck those sources
when the pinned engine changes. All commands run from the repository root.

1. Read [game systems](../../../docs/game-systems.org) and save module headers plus their tests. Identify persistent state, stable IDs and the save version.
2. Implement persistence through LrgSaveable/LrgSaveManager using their actual contracts. Store user saves outside game assets.
3. Use temporary directories and deterministic seeds in GTest. Cover fresh saves, round trips, corruption, missing files, migrations and unknown content IDs.
4. Test the affected gameplay invariant (one reward, one card owner, ordered laps, atomic purchases), not just object creation.
5. Run `make test`, then selected debug/sanitizer builds with fresh objects. Run `make assets-verify`; keep display/network checks explicit.
6. Document manual focus/resize/reconnect/save-permission checks and the package contents. Report every skipped target or unavailable dependency.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

Meaningful automated tests, versioned save handling and reproducible release checks.

## Examples

**Input:** Migrate an inventory save while protecting the live inventory from corrupt input.

**Result:** A versioned fixture maps old item IDs into temporary state before committing. Tests cover missing keys, invalid IDs and failed restore without partial inventory mutation.

## Constraints

Never modify real player saves in tests or call a graphics skip proof that rendering passed.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
