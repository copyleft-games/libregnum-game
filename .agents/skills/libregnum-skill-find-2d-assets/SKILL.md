---
name: libregnum-skill-find-2d-assets
description: Find licensed 2D sprites, tiles, UI, fonts and audio for libregnum. Use when searching public or free game assets.
---

# Skill: Find 2D Assets

Find art that matches the game and preserve evidence that the selected files can be used.

## When to Use

Requests for free/public sprites, tilesets, UI, fonts or sounds.

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

1. Read [asset sources and conventions](../../../docs/assets.org). Extract subject, style, pixel dimensions, palette, animation needs, license constraints and size budget from the brief.
2. Search current creator pages: start with Kenney for sprites/UI/audio and OpenGameArt for alternatives. Query subject plus dimensions/style and inspect multiple candidates.
3. Inspect each asset page and included license, author, attribution requirements, file formats and dependencies. Do not infer permission from "free" or a site's general reputation.
4. Return a short comparison with direct source/license links and an explicit choice. Prefer CC0; identify attribution and modification obligations for CC-BY.
5. Follow [asset intake](../libregnum-skill-import-assets/SKILL.md) to download selected files and pin archive/member hashes. Preserve font/audio licenses just like images.
6. Check alpha, tile gutters, sprite pivots, filter mode and audio playback in the target game. Record changes and remaining visual/device checks.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

A sourced comparison and selected manifest entries with licensed, standardized runtime files.

## Examples

**Input:** Find 16x16 dungeon sprites that can ship in the game.

**Result:** A comparison records exact creator/license URLs, author, dimensions and selection reasons. The chosen PNG members are pinned, credited and checked at integer scaling; collision data remains separate.

## Constraints

Do not download arbitrary bulk catalogs, bypass provider access controls or assume a sprite sheet is a ready-made game map.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
