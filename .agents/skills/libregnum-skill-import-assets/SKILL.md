---
name: libregnum-skill-import-assets
description: Download and verify pinned game asset packs. Use to import ZIP/direct files, preserve licenses or generate credits.
---

# Skill: Asset Intake

Import selected licensed files reproducibly into this repository with the bundled Python tool.

## When to Use

Downloading chosen packs, registering asset provenance, validating hashes or preparing credits.

## Prerequisites

Python 3, a reviewed source/license and a writable checkout. HTTPS fetching
needs network access; --from-file can use an already-downloaded pinned file.
Runtime media checks additionally need a built engine and its graphics/audio context.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

First read [the engine recipe](references/engine-recipe.md) for this task. It
links the inspected headers, implementations and tests, identifies defaults and
missing game behavior, and gives concrete failure cases. Recheck those sources
when the pinned engine changes. All commands run from the repository root.

1. Read [the complete intake procedure](../../../docs/assets.org) and tools/assets.py. Use Python 3; run every command from the repository root.
2. Inspect the source page and license. Download into temporary storage and list archive contents. Never execute asset-provided scripts.
3. Add the pack to data/assets/manifest.json with source/download/license URLs, author, attribution, license text, changes, archive hash and selected member hashes. Preserve all model sidecars.
4. Run `python3 tools/assets.py validate`, then `python3 tools/assets.py fetch PACK_ID` or use `--from-file` for an already-downloaded pinned archive.
5. Run `make assets-verify` and the appropriate graphics/audio import check. Changed installed packs must be preserved; investigate rather than overwriting them.
6. Run `python3 tools/assets.py credits > data/assets/CREDITS.md`. Commit the manifest, selected files, provenance and licenses together. Report formats and visual checks not yet validated.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

When recording asset provenance and acceptance, copy and adapt the
[output template](templates/asset-dossier.org.template) into docs/; replace the example
with the actual game or asset case and fill in observed verification results.

## Output Format

Verified data/assets/<pack>/ files, manifest entries, provenance, LICENSE.txt and generated CREDITS.md.

## Examples

**Input:** Reproduce the bundled Kenney tile from its pinned download.

**Result:** `python3 tools/assets.py fetch kenney-tiny-dungeon` verifies an existing pack or imports the pinned member. `make assets-verify` passes and regenerated CREDITS.md matches the manifest; altered files cause failure without being overwritten.

## Constraints

Do not invent hashes or license text, bypass checksum failures, overwrite user edits or use unsupported licenses as if they were CC0.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
