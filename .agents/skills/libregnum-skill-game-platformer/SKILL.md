---
name: libregnum-skill-game-platformer
description: Build libregnum platformers with movement, collision and camera tests. Use for side-scrolling games or jumping mechanics.
---

# Skill: Platformer

Implement a first playable platformer and tune its movement with measurable checks.

## When to Use

Side-scrolling levels, jumping, collision, camera follow or player feel.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [genre recipes](../../../docs/genres.org), lrg-platformer-template.h and deps/libregnum/examples/game-platformer-demo.c.
2. Choose foot position, hitbox size, tile units, virtual resolution and collision-layer conventions. Write them in the game brief.
3. Implement collision hooks against a small level, spawn, exit and restart. Chain parent hooks where required by the template implementation.
4. Add buffered jump/coyote-time and wall movement only when needed. Keep draw_world and draw_ui separate.
5. Test floors, ceilings, corners, ledge departure, respawn and timestep boundaries. Manually check jump feel, camera and pixel scaling.
6. Use [2D asset search](../libregnum-skill-find-2d-assets/SKILL.md) when replacing primitive art; retain collision dimensions independently.

## Output Format

A playable room, collision/movement tests, documented controls and coordinate conventions.

## Examples

Build a one-room jumping puzzle with a collectible, exit, ceiling collision and a reliable restart.

## Constraints

Do not use sprite transparent margins as collision bounds or skip level collision because the template already moves the player.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
