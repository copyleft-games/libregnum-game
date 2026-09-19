# Audio ownership and update loop

Read this when implementing or reviewing this skill. Engine paths below are
relative to the pinned submodule; check the pin before relying on the findings.

## Source trail

- [src/audio/lrg-audio-manager.h](../../../../deps/libregnum/src/audio/lrg-audio-manager.h) — inspect `lrg_audio_manager_update`, `lrg_audio_manager_play_music_from_file`, `lrg_audio_manager_set_master_volume`.
- [src/core/lrg-asset-manager.h](../../../../deps/libregnum/src/core/lrg-asset-manager.h) — inspect `lrg_asset_manager_load_sound`, `lrg_asset_manager_load_music`.
- [src/template/lrg-game-template.c](../../../../deps/libregnum/src/template/lrg-game-template.c) — inspect `lrg_audio_manager_update`.
- [tests/test-audio.c](../../../../deps/libregnum/tests/test-audio.c) — inspect `lrg_audio_manager`.

## Device and resource lifetime
Initialize the audio device before decoding playable resources. Short effects
and streaming music have different ownership/update needs. Asset-manager loads
return borrowed cached sound/music objects; retain only when a longer lifetime
is required. Release game-owned resources before device teardown.
The game template calls lrg_audio_manager_update once in its frame path. A custom
loop must provide the update; do not add a second updater in every scene. Merely
loading a music resource does not establish who plays, updates or stops it.

## Integrate feedback
Define action-to-sound mappings, polyphony/overlap policy and master/music/effects
volumes. Debounce repeated events, especially landing and overlapping damage.
Preload latency-sensitive effects after startup and never decode them per frame.
Choose pause/focus behavior: simulation pause and music pause are independent.
Use the engine bank APIs only after reading their expected format and examples.

## Verification boundary
Test event routing and volume state without assuming a device exists. Keep an
explicit device check for actual playback, looping, fades, focus and resource
teardown. A skipped audio test is not proof the sound was heard. Verify licenses,
sample format and loudness before committing a pack; avoid clipping when several
effects overlap. Imported fonts and audio retain separate licenses if bundled.

Example result: a jump effect triggered once, looped background music, saved
volume controls and a documented manual device test through pause/resume/restart.
