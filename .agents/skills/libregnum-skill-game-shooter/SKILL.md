---
name: libregnum-skill-game-shooter
description: Build libregnum shooters, twin-stick games and shmups. Use for aiming, projectiles, waves or damage rules.
---

# Skill: Shooter

Build a reproducible combat loop with clear projectile and damage ownership.

## When to Use

2D shooters, twin-stick aiming, scrolling shmups or wave encounters.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [genre recipes](../../../docs/genres.org), the shooter/twin-stick/shmup headers and deps/libregnum/examples/game-shmup-demo.c.
2. Select scrolling/camera behavior, aiming inputs, collision layers and enemy spawn policy. Use composition for final templates.
3. Implement one weapon, enemy, wave, health/score display and restart through one damage path.
4. Separate spawn timing and simulation from draw frames; expose the random seed.
5. Test hit deduplication, friendly-fire policy, projectile lifetime, death, wave completion and restart state.
6. Check controller dead zones, focus loss and pause on a real window. Profile before adding projectile pools.

## Output Format

A complete wave loop with seeded tests and input/weapon documentation.

## Examples

Make a twin-stick arena where five enemies spawn, one projectile awards one hit, and restart resets score.

## Constraints

Do not subclass final twin-stick/shmup templates or let multiple collision callbacks award duplicate kills.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
