---
name: libregnum-skill-game-3d
description: Build libregnum first-person, third-person and racing scenes. Use for 3D cameras, model integration or vehicle prototypes.
---

# Skill: 3D Game

Bring a small scene, player and imported model together with explicit units and ownership.

## When to Use

FPS, third-person action, 3D racing, camera or model integration.

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

1. Read [genre recipes](../../../docs/genres.org) and the FPS, third-person or racing-3d header. Inspect the corresponding game-*-demo.c in deps/libregnum/examples/.
2. Define axes, world scale, player/collider dimensions and camera conventions. Build a floor and one interaction before a large world.
3. Use [3D asset search](../libregnum-skill-find-3d-assets/SKILL.md). Load models after context startup and release them before window shutdown.
4. Keep colliders independent of mesh detail. Validate materials and animation clips in-game rather than inferring support from glTF recognition.
5. Test grounding, camera obstruction, reset and simulation rules. For racing, test ordered checkpoints and backwards start-line crossing.
6. Exercise mouse capture, focus restoration, near clipping and frame time on target hardware.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

A small 3D scene with documented scale, model provenance, tests and display verification.

## Examples

**Input:** Add a barrel prop and an orbit camera to a courtyard.

**Result:** The GLB and external texture load after graphics startup; a camera obstruction query resolves against courtyard colliders. The report records scale, shading, focus restoration and reset checks.

## Constraints

Do not claim 3D collision or PBR/animation compatibility until the specific behavior has been exercised.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
