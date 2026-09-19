---
name: libregnum-skill-game-platformer
description: Build libregnum platformers with movement, collision and camera tests. Use for side-scrolling games or jumping mechanics.
---

# Skill: Platformer

Implement a first playable platformer and tune its movement with measurable checks.

## When to Use

Side-scrolling levels, jumping, collision, camera follow or player feel.

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

1. Read [genre recipes](../../../docs/genres.org), lrg-platformer-template.h and deps/libregnum/examples/game-platformer-demo.c.
2. Choose foot position, hitbox size, tile units, virtual resolution and collision-layer conventions. Write them in the game brief.
3. Own update_physics and level collision resolution for platforms/walls/ceilings; check_ground alone cannot replace the base flat-ground clamp. Add spawn, exit and restart.
4. Add buffered jump/coyote-time and wall movement only when needed. Keep draw_world and draw_ui separate.
5. Test floors, ceilings, corners, ledge departure, respawn and timestep boundaries. Manually check jump feel, camera and pixel scaling.
6. Use [2D asset search](../libregnum-skill-find-2d-assets/SKILL.md) when replacing primitive art; retain collision dimensions independently.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

A playable room, collision/movement tests, documented controls and coordinate conventions.

## Examples

**Input:** Build a room with a raised ledge and a low ceiling.

**Result:** The game owns a level-aware physics resolver; tests cover floor, wall and ceiling contacts plus buffered jump. Manual checks cover camera scaling and respawn without stale velocity.

## Constraints

Do not use sprite transparent margins as collision bounds or skip level collision because the template already moves the player.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
