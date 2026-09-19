---
name: skill-find-3d-assets
description: Find licensed 3D models, materials and animations for libregnum. Use when searching free props, characters or environments.
---

# Skill: Find 3D Assets

Choose model assets that fit both the visual brief and the pinned runtime loader.

## When to Use

Requests for public/free models, animated characters, PBR materials or environment art.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [asset sources and formats](../../../docs/assets.org). Determine visual style, units, axes, triangle/texture budget, animation needs and target hardware.
2. Search current Kenney, Quaternius and Poly Haven asset pages. Compare direct links, licenses, formats, size and material/rig requirements.
3. Verify the exact downloadable pack's license and contents. Site code/logos and third-party assets can have different terms from a site's primary assets.
4. Prefer self-contained GLB or OBJ with all sidecars. If only authoring files exist, export supported glTF/OBJ and record tool version/settings and changes.
5. Use [asset intake](../skill-import-assets/SKILL.md). Preserve texture/buffer paths; never flatten dependent model files.
6. Load via grl_model_new_from_file in a graphics context. Check material appearance, scale, orientation, collider separation and animation compatibility; report unsupported features.

## Output Format

Candidate comparison, pinned model files, license/provenance and import/visual check results.

## Examples

Find a low-poly barrel: choose Kenney Platformer Kit, import its GLB and texture, then check scale and shading in a third-person scene.

## Constraints

Do not promise FBX/Blender import or full glTF extension support. Do not add an engine loader when an existing supported export meets the need.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
