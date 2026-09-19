---
name: libregnum-skill-game-save-test
description: Test game rules and persistence with libregnum. Use for save/load, migrations, deterministic behavior or release verification.
---

# Skill: Save and Test

Protect player progress and make gameplay regression checks repeatable.

## When to Use

Saving, migration, regression tests, deterministic replays or release preparation.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [game systems](../../../docs/game-systems.org) and save module headers plus their tests. Identify persistent state, stable IDs and the save version.
2. Implement persistence through LrgSaveable/LrgSaveManager using their actual contracts. Store user saves outside game assets.
3. Use temporary directories and deterministic seeds in GTest. Cover fresh saves, round trips, corruption, missing files, migrations and unknown content IDs.
4. Test the affected gameplay invariant (one reward, one card owner, ordered laps, atomic purchases), not just object creation.
5. Run `make test`, then selected debug/sanitizer builds with fresh objects. Run `make assets-verify`; keep display/network checks explicit.
6. Document manual focus/resize/reconnect/save-permission checks and the package contents. Report every skipped target or unavailable dependency.

## Output Format

Meaningful automated tests, versioned save handling and reproducible release checks.

## Examples

Migrate a version-one inventory save while preserving known item IDs and reporting unavailable content.

## Constraints

Never modify real player saves in tests or call a graphics skip proof that rendering passed.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
