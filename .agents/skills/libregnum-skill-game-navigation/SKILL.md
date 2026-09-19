---
name: libregnum-skill-game-navigation
description: Build libregnum grid and mesh navigation. Use for bounded A-star, walkable triangle meshes, dynamic route blocking and waypoint editing.
---

# Skill: Navigation and Route Editing

Implement this workflow against the pinned engine with explicit ownership,
failure handling and tests at the owning layer.

## When to Use

Build libregnum grid and mesh navigation. Use for bounded A-star, walkable triangle meshes, dynamic route blocking and waypoint editing.

## Prerequisites

Read root AGENTS.md. Initialize the pinned engine for source inspection; C work
requires the compiler/dependencies listed in README.md. Documentation checks need
Python 3. Commands below run from the project root unless stated otherwise.

## Instructions

1. Define coordinate units, agent clearance and grid versus triangle-mesh input.
2. Read [the engine recipe](references/engine-recipe.md), then inspect the selected
   pathfinder header/implementation and matching test fixture.
3. Validate terrain costs or pre-cleared mesh geometry; configure diagonal/corner
   policy, projection tolerance and search budgets explicitly.
4. Distinguish unavailable paths from exhausted search budgets. Replan when
   obstacles change, and validate edited routes before steering an actor.
5. Test route legality and cost independently from rendering; document smoothing,
   agent clearance and what happens when a destination becomes unreachable.
6. Run `make starter-check` and `make engine-contract-check` after documentation
   changes, and `make test` for C integration changes. Run the recipe's optional
   engine/integration checks only in their stated environments; report skips.
7. Update org-mode game documentation and report implemented behavior and checks.

## Output Format

Game integration and meaningful tests at the owning layer, org documentation
under docs/, and a report separating source checks from runtime validation.

## Examples

**Input:** Route a guard around a wall without stalling indefinitely.

**Result:** A grid search uses an explicit expansion budget. An iteration-limit
error schedules a fresh larger-budget search; a no-path error leaves the guard
idle. Tests verify blocked corners, zero-cost terrain and reaching the goal on
the final allowed expansion. Debug route edits invalidate stored terrain costs.

## Constraints

Use inspected signatures and transfer annotations; preserve unrelated changes.
Do not infer implemented behavior from a type name or claim unexecuted tests.
Keep device/network checks separate from hermetic starter checks. Do not push
or spawn subagents without user instructions.
