---
name: skill-game-top-down
description: Build top-down libregnum adventures and RPGs. Use for tile movement, interactions, quests or inventories.
---

# Skill: Top-down Adventure

Compose movement and content systems into a small explorable room.

## When to Use

Top-down action, RPGs, dungeon exploration or NPC interactions.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [genre recipes](../../../docs/genres.org), lrg-top-down-template.h and deps/libregnum/examples/game-top-down-demo.c.
2. Define map coordinates, collision layers, interaction distance and stable content IDs.
3. Build one room, door and NPC using input actions. Connect dialog, quest and inventory modules only as the loop needs them.
4. Separate walkability and interaction tests from rendering. Cover diagonal movement, blocked cells, out-of-range interaction and full inventory.
5. Apply [game systems](../../../docs/game-systems.org) to state transitions and persistence. Test quest progress after save/reload.
6. Import art using [2D asset search](../skill-find-2d-assets/SKILL.md), then check layer order, hitboxes and text readability.

## Output Format

Room traversal and interactions, deterministic tests and documented content IDs.

## Examples

Create a key-and-door room where talking to an NPC grants a quest and the key unlocks the exit.

## Constraints

Do not identify persistent objects by translated display names or assume a texture atlas is an engine tilemap.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
