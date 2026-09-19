---
name: libregnum-skill-game-3d
description: Build libregnum first-person, third-person and racing scenes. Use for 3D cameras, model integration or vehicle prototypes.
---

# Skill: 3D Game

Bring a small scene, player and imported model together with explicit units and ownership.

## When to Use

FPS, third-person action, 3D racing, camera or model integration.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [genre recipes](../../../docs/genres.org) and the FPS, third-person or racing-3d header. Inspect the corresponding game-*-demo.c in deps/libregnum/examples/.
2. Define axes, world scale, player/collider dimensions and camera conventions. Build a floor and one interaction before a large world.
3. Use [3D asset search](../libregnum-skill-find-3d-assets/SKILL.md). Load models after context startup and release them before window shutdown.
4. Keep colliders independent of mesh detail. Validate materials and animation clips in-game rather than inferring support from glTF recognition.
5. Test grounding, camera obstruction, reset and simulation rules. For racing, test ordered checkpoints and backwards start-line crossing.
6. Exercise mouse capture, focus restoration, near clipping and frame time on target hardware.

## Output Format

A small 3D scene with documented scale, model provenance, tests and display verification.

## Examples

Create a third-person courtyard with an imported barrel, camera obstruction handling and a reset point.

## Constraints

Do not claim 3D collision or PBR/animation compatibility until the specific behavior has been exercised.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
