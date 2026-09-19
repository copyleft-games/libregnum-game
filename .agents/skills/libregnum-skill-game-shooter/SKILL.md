---
name: libregnum-skill-game-shooter
description: Build libregnum shooters, twin-stick games and shmups. Use for aiming, projectiles, waves or damage rules.
---

# Skill: Shooter

Build a reproducible combat loop with clear projectile and damage ownership.

## When to Use

2D shooters, twin-stick aiming, scrolling shmups or wave encounters.

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

1. Read [genre recipes](../../../docs/genres.org), the shooter/twin-stick/shmup headers and deps/libregnum/examples/game-shmup-demo.c.
2. Select scrolling/camera behavior, aiming inputs, collision layers and enemy spawn policy. Inspect the derivable twin-stick/shmup hooks when specializing them.
3. Implement one weapon, enemy, wave, health/score display and restart through one damage path.
4. Separate spawn timing and simulation from draw frames; expose the random seed.
5. Test hit deduplication, friendly-fire policy, projectile lifetime, death, wave completion and restart state.
6. Check controller dead zones, focus loss and pause on a real window. Profile before adding projectile pools.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

A complete wave loop with seeded tests and input/weapon documentation.

## Examples

**Input:** Create a twin-stick arena with a five-enemy wave.

**Result:** A derivable twin-stick game uses the existing projectile pool and one damage owner. Tests cover duplicate overlaps, exhausted capacity and restart clearing active projectiles and score.

## Constraints

Twin-stick and shmup are derivable in this pin. Do not let multiple collision callbacks award duplicate kills.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
