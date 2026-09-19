---
name: libregnum-skill-game-top-down
description: Build top-down libregnum adventures and RPGs. Use for tile movement, interactions, quests or inventories.
---

# Skill: Top-down Adventure

Compose movement and content systems into a small explorable room.

## When to Use

Top-down action, RPGs, dungeon exploration or NPC interactions.

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

1. Read [genre recipes](../../../docs/genres.org), lrg-top-down-template.h and deps/libregnum/examples/game-top-down-demo.c.
2. Define map coordinates, collision layers, interaction distance and stable content IDs.
3. Build one room, door and NPC using input actions. Connect dialog, quest and inventory modules only as the loop needs them.
4. Separate walkability and interaction tests from rendering. Cover diagonal movement, blocked cells, out-of-range interaction and full inventory.
5. Apply [game systems](../../../docs/game-systems.org) to state transitions and persistence. Test quest progress after save/reload.
6. Import art using [2D asset search](../libregnum-skill-find-2d-assets/SKILL.md), then check layer order, hitboxes and text readability.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

Room traversal and interactions, deterministic tests and documented content IDs.

## Examples

**Input:** An NPC grants a quest to find the key that opens the next room.

**Result:** Stable NPC, key and door IDs connect dialog/inventory/quest state. Tests cover full inventory, missing key, repeated interaction and save/reload before opening the door.

## Constraints

Do not identify persistent objects by translated display names or assume a texture atlas is an engine tilemap.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
