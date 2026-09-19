---
name: libregnum-skill-game-physics
description: Integrate libregnum collision filtering and raycasts. Use for rigid-body layers, trigger policy, line-of-sight tests and nearest-hit queries.
---

# Skill: Physics Layers and Queries

Implement this workflow against the pinned engine with explicit ownership,
failure handling and tests at the owning layer.

## When to Use

Integrate libregnum collision filtering and raycasts. Use for rigid-body layers, trigger policy, line-of-sight tests and nearest-hit queries.

## Prerequisites

Read root AGENTS.md. Initialize the pinned engine for source inspection; C work
requires the compiler/dependencies listed in README.md. Documentation checks need
Python 3. Commands below run from the project root unless stated otherwise.

## Instructions

1. Define named membership bits and a collision matrix for actors, scenery and
   triggers, including whether queries should see each category.
2. Read [the engine recipe](references/engine-recipe.md), including the distinction
   between pair collision masks and ray query layer masks.
3. Configure bodies and use filtered queries with explicit trigger/caster policy.
   Handle misses and borrowed hit lifetimes before applying damage or interaction.
4. Add headless boundary/filter tests and integrate the query with game rules.
5. Document bounding-box approximation and verify gameplay geometry visually when
   shapes, rotations or agent size affect the result.
6. Run `make starter-check` and `make engine-contract-check` after documentation
   changes, and `make test` for C integration changes. Run the recipe's optional
   engine/integration checks only in their stated environments; report skips.
7. Update org-mode game documentation and report implemented behavior and checks.

## Output Format

Game integration and meaningful tests at the owning layer, org documentation
under docs/, and a report separating source checks from runtime validation.

## Examples

**Input:** Keep an actor's sight ray from hitting itself or a trigger.

**Result:** The caller passes the actor as `ignore_body`, disables triggers and
selects scenery membership bits with `lrg_physics_world_raycast_filtered()`.
A test places an ignored actor, a near trigger and a wall along the segment:
the wall is returned. A zero layer mask returns a miss and clears the hit output.

## Constraints

Use inspected signatures and transfer annotations; preserve unrelated changes.
Do not infer implemented behavior from a type name or claim unexecuted tests.
Keep device/network checks separate from hermetic starter checks. Do not push
or spawn subagents without user instructions.
