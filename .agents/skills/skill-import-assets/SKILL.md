---
name: skill-import-assets
description: Download and verify pinned game asset packs. Use to import ZIP/direct files, preserve licenses or generate credits.
---

# Skill: Asset Intake

Import selected licensed files reproducibly into this repository with the bundled Python tool.

## When to Use

Downloading chosen packs, registering asset provenance, validating hashes or preparing credits.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [the complete intake procedure](../../../docs/assets.org) and tools/assets.py. Use Python 3; run every command from the repository root.
2. Inspect the source page and license. Download into temporary storage and list archive contents. Never execute asset-provided scripts.
3. Add the pack to data/assets/manifest.json with source/download/license URLs, author, attribution, license text, changes, archive hash and selected member hashes. Preserve all model sidecars.
4. Run `python3 tools/assets.py validate`, then `python3 tools/assets.py fetch PACK_ID` or use `--from-file` for an already-downloaded pinned archive.
5. Run `make assets-verify` and the appropriate graphics/audio import check. Changed installed packs must be preserved; investigate rather than overwriting them.
6. Run `python3 tools/assets.py credits > data/assets/CREDITS.md`. Commit the manifest, selected files, provenance and licenses together. Report formats and visual checks not yet validated.

## Output Format

Verified data/assets/<pack>/ files, manifest entries, provenance, LICENSE.txt and generated CREDITS.md.

## Examples

Reproduce the bundled tile with `python3 tools/assets.py fetch kenney-tiny-dungeon`, then run `make assets-verify`.

## Constraints

Do not invent hashes or license text, bypass checksum failures, overwrite user edits or use unsupported licenses as if they were CC0.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
