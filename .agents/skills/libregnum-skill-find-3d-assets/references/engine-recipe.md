# 3D search and compatibility dossier

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [deps/graylib/src/graphics/grl-model.h](../../../../deps/libregnum/deps/graylib/src/graphics/grl-model.h) — inspect `grl_model_new_from_file`, `grl_model_get_mesh_count`.
- [deps/graylib/src/graphics/grl-model-animation.h](../../../../deps/libregnum/deps/graylib/src/graphics/grl-model-animation.h) — inspect `grl_model_animation`.
- [deps/graylib/deps/raylib/src/config.h](../../../../deps/libregnum/deps/graylib/deps/raylib/src/config.h) — inspect `SUPPORT_FILEFORMAT_GLTF`, `SUPPORT_FILEFORMAT_OBJ`.

## Match the scene
Record style, axes, units, origin/pivot, triangle and texture budget, material
channels, skeleton/animation requirements and target hardware. Compare relevant
creator packs from the asset-source guide, with exact license evidence and source
links. Avoid downloading full catalogs to obtain one prop.

## Inspect before claiming compatibility
List ZIP members and inspect glTF/GLB JSON references. A GLB can contain external
image URIs. Keep buffers/textures and their case-sensitive relative paths; OBJ
may need MTL and texture files. Reject remote/escaping references for a local game
bundle or convert them into explicit local assets with provenance.
The pinned raylib enables standard glTF/OBJ paths, not every glTF extension.
Check compressed geometry, texture compression, PBR channel usage, skinning and
clip names against the actual loader. Authoring .blend/FBX files require export.

## Conversion record
Record source archive hash, exporter version, units/axis/transform settings,
material baking, texture conversion and clip selection. Re-open the export before
importing it. The bundled importer is byte-preserving, so do not label a converted
output as an unchanged member of the original archive. Keep its original evidence
and a separately reviewed runtime-file manifest record.

## Acceptance
Load in a graphics context, check nonempty meshes, then inspect material appearance,
scale and orientation in a scene with known lighting. Exercise the required clip
and root-motion policy for animated assets. Derive separate collision proxies.
Example: the Kenney barrel must include models/Textures/colormap.png relative to
models/barrel.glb; a mesh-only load success misses that material dependency.
