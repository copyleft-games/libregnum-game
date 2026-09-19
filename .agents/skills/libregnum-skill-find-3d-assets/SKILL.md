---
name: libregnum-skill-find-3d-assets
description: Find licensed 3D models, materials and animations for libregnum. Use when searching free props, characters or environments.
---

# Skill: Find 3D Assets

Choose model assets that fit both the visual brief and the pinned runtime loader.

## When to Use

Requests for public/free models, animated characters, PBR materials or environment art.

## Prerequisites

A game art brief, browsing/network access for creator/license evidence, and
Python 3 for intake. Engine sources are needed to check format support; an
appropriate graphics/audio device is needed for runtime acceptance.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

First read [the engine recipe](references/engine-recipe.md) for this task. It
links the inspected headers, implementations and tests, identifies defaults and
missing game behavior, and gives concrete failure cases. Recheck those sources
when the pinned engine changes. All commands run from the repository root.

1. Read [asset sources and formats](../../../docs/assets.org). Determine visual style, units, axes, triangle/texture budget, animation needs and target hardware.
2. Search current Kenney, Quaternius and Poly Haven asset pages. Compare direct links, licenses, formats, size and material/rig requirements.
3. Verify the exact downloadable pack's license and contents. Site code/logos and third-party assets can have different terms from a site's primary assets.
4. Prefer self-contained GLB or OBJ with all sidecars. If only authoring files exist, export supported glTF/OBJ and record tool version/settings and changes.
5. Use [asset intake](../libregnum-skill-import-assets/SKILL.md). Preserve texture/buffer paths; never flatten dependent model files.
6. Load via grl_model_new_from_file in a graphics context. Check material appearance, scale, orientation, collider separation and animation compatibility; report unsupported features.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

Candidate comparison, pinned model files, license/provenance and import/visual check results.

## Examples

**Input:** Find a low-poly barrel compatible with the current loader.

**Result:** A source/license dossier selects the Kenney GLB and its texture sidecar. The imported manifest pins both files, and the report separates mesh import from shading and scale inspection.

## Constraints

Do not promise FBX/Blender import or full glTF extension support. Do not add an engine loader when an existing supported export meets the need.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
