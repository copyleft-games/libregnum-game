# 2D search and selection dossier

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/core/lrg-asset-manager.h](../../../../deps/libregnum/src/core/lrg-asset-manager.h) — inspect `lrg_asset_manager_load_texture`, `lrg_asset_manager_load_font`, `lrg_asset_manager_load_sound`.
- [deps/graylib/deps/raylib/src/config.h](../../../../deps/libregnum/deps/graylib/deps/raylib/src/config.h) — inspect `SUPPORT_FILEFORMAT_PNG`.
- [tests/test-asset-manager.c](../../../../deps/libregnum/tests/test-asset-manager.c) — inspect `test_asset_dispatch_errors`.

## Brief before search
Extract subject, perspective, pixel density, palette, tile size, frame count,
pivots, atlas format, UI scaling, audio style and license constraints. If the brief
is vague, use a small coherent pack matching the existing scene and state the
assumption. A 16×16 side-view sprite is not interchangeable with an isometric tile.

## Candidate evidence
Use current primary creator pages, not search snippets or mirror claims. The
source directory in docs/assets.org is a starting list, not permanent permission.
For each candidate record title/author, exact source URL, license URL and included
license file, format/dimensions, dependencies, download size and selection reason.
Compare two or three relevant candidates when available; explain if only one fits.
CC0 reduces attribution friction; CC-BY needs credit and modification records.
Reject unknown permission rather than marking it CC0 to satisfy the importer.
Fonts and sounds need the same evidence; a UI pack may bundle a separately licensed font.

## Technical intake
Use the import skill. Preserve alpha and sprite margins, choose nearest filtering
for pixel art, and document atlas gutters/frame rectangles. Record conversion
commands/settings and original hashes when exporting SVG/PSD to PNG or audio to
WAV/OGG. The manifest's output hash must describe the actual shipped bytes.
The current importer copies selected bytes unchanged; converted files need their
own reviewed direct-file provenance, not a false claim of unmodified ZIP intake.

Example dossier: Tiny Dungeon by Kenney, 16×16 PNG, creator asset page and included
CC0 notice, selected tile IDs and unchanged-byte hashes. Result: a manifest pack,
credits, a rendered tile at integer scaling, and a note that map collision is
separate data. Search alone is not a completed asset integration.
