---
name: libregnum-skill-find-2d-assets
description: Find licensed 2D sprites, tiles, UI, fonts and audio for libregnum. Use when searching public or free game assets.
---

# Skill: Find 2D Assets

Find art that matches the game and preserve evidence that the selected files can be used.

## When to Use

Requests for free/public sprites, tilesets, UI, fonts or sounds.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [asset sources and conventions](../../../docs/assets.org). Extract subject, style, pixel dimensions, palette, animation needs, license constraints and size budget from the brief.
2. Search current creator pages: start with Kenney for sprites/UI/audio and OpenGameArt for alternatives. Query subject plus dimensions/style and inspect multiple candidates.
3. Inspect each asset page and included license, author, attribution requirements, file formats and dependencies. Do not infer permission from "free" or a site's general reputation.
4. Return a short comparison with direct source/license links and an explicit choice. Prefer CC0; identify attribution and modification obligations for CC-BY.
5. Follow [asset intake](../libregnum-skill-import-assets/SKILL.md) to download selected files and pin archive/member hashes. Preserve font/audio licenses just like images.
6. Check alpha, tile gutters, sprite pivots, filter mode and audio playback in the target game. Record changes and remaining visual/device checks.

## Output Format

A sourced comparison and selected manifest entries with licensed, standardized runtime files.

## Examples

Find a 16x16 dungeon tile set: inspect Kenney Tiny Dungeon, record its CC0 evidence, import selected PNGs and test pixel filtering.

## Constraints

Do not download arbitrary bulk catalogs, bypass provider access controls or assume a sprite sheet is a ready-made game map.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
