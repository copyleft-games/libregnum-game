# Reproducible intake and failure recovery

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/core/lrg-asset-manager.h](../../../../deps/libregnum/src/core/lrg-asset-manager.h) — inspect `lrg_asset_manager_load_asset`, `lrg_asset_manager_load_object`.
- [deps/graylib/src/graphics/grl-model.h](../../../../deps/libregnum/deps/graylib/src/graphics/grl-model.h) — inspect `grl_model_new_from_file`.
- [tests/test-asset-manager.c](../../../../deps/libregnum/tests/test-asset-manager.c) — inspect `test_asset_dispatch_errors`.

## Tool contract
Run commands from the repository root. tools/assets.py is the intake tool, not an
engine asset pack loader. Its JSON manifest defines copy-only ZIP or direct-file
imports; the runtime uses filesystem paths. It does not convert models, resolve
sidecars automatically, or decide whether an uploader owns the media.
Read docs/assets.org for the complete required fields and current supported licenses.

## Intake sequence
1. Download to temporary storage and inspect the actual archive/license. Pin the
   full download hash, then each selected member's uncompressed-byte hash.
2. Choose a unique provider-pack ID and explicit output paths. Preserve model URI
   layout. Include creator, attribution, source/license/download URLs, original
   license text and truthful changes. Never invent a hash from a filename.
3. Validate before fetching. `fetch PACK --from-file FILE` reproduces a pinned
   download offline. `fetch PACK` uses HTTPS and refuses a changed remote payload.
4. Verify installed files and provenance, then load through the actual GPU/audio
   API. Generate credits and review the resulting diff before shipping.

## Failure recovery
| Failure | Required response |
|---------|-------------------|
| Download hash differs | Keep failed input outside runtime data; re-review upstream version/license |
| Installed pack edited | Preserve it; compare with manifest before a deliberate new version/import |
| Missing texture despite model load | Inspect URI, add sidecar to manifest, reimport intentionally |
| Unsupported license | Use a separately reviewed workflow; do not relabel it |
| Batch fails after first pack | First successful pack remains; rerun missing packs after fixing the cause |
| Provider requires login or throttles | Use its supported access method; never bypass gates |

The tool bounds download/expanded sizes and rejects unsafe paths, archive symlinks
and collisions. This does not sandbox a media decoder. Run a single importer per
trusted checkout. Preserve local edits and never blanket-delete asset directories.

Example result: a new versioned prop pack, reproducible member hashes, LICENSE.txt,
provenance.json and regenerated credits, plus actual import and visual results.
