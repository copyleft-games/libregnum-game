# Gameplay Timing and Editing Utilities contracts

Read when implementing this skill. Audited engine pin: `6750d12e3102ad1b263828705695c8a750cd7fc1`.
Recheck the source before using these contracts with another revision.

## Source trail

- [src/core/lrg-timer-manager.h](../../../../deps/libregnum/src/core/lrg-timer-manager.h) — inspect `lrg_timer_manager_reschedule`.
- [src/core/lrg-timer-manager.c](../../../../deps/libregnum/src/core/lrg-timer-manager.c) — inspect `lrg_timer_manager_update`.
- [src/core/lrg-random-stream.h](../../../../deps/libregnum/src/core/lrg-random-stream.h) — inspect `lrg_random_stream_copy`.
- [src/core/lrg-random-stream.c](../../../../deps/libregnum/src/core/lrg-random-stream.c) — inspect `lrg_random_stream_advance`.
- [src/tween/lrg-keyframe-curve.h](../../../../deps/libregnum/src/tween/lrg-keyframe-curve.h) — inspect `lrg_keyframe_curve_get_key`.
- [src/tween/lrg-keyframe-curve.c](../../../../deps/libregnum/src/tween/lrg-keyframe-curve.c) — inspect `lrg_keyframe_curve_sample`.
- [src/ai/lrg-blackboard.h](../../../../deps/libregnum/src/ai/lrg-blackboard.h) — inspect `lrg_blackboard_dup_keys`.
- [src/ai/lrg-blackboard.c](../../../../deps/libregnum/src/ai/lrg-blackboard.c) — inspect `lrg_blackboard_dup_string`.
- [tests/test-timer-manager.c](../../../../deps/libregnum/tests/test-timer-manager.c) — inspect `lrg_timer_manager_reschedule`.
- [tests/test-random-stream.c](../../../../deps/libregnum/tests/test-random-stream.c) — inspect `lrg_random_stream_restore`.
- [tests/test-gameplay-utilities.c](../../../../deps/libregnum/tests/test-gameplay-utilities.c) — inspect `test_random_copy`.
- [tests/test-keyframe-curve.c](../../../../deps/libregnum/tests/test-keyframe-curve.c) — inspect `lrg_keyframe_curve_sample`.
- [tests/test-template.c](../../../../deps/libregnum/tests/test-template.c) — inspect `test_game_template_timer_lifetime`.

## Timers
`lrg_game_template_get_timer_manager()` returns a borrowed manager. Templates
advance it once per host frame before fixed/variable updates; do not update it
again. Scaled time pauses and follows gameplay scaling; unscaled time receives
raw nonnegative host delta. Standalone loops own a manager and call `update()`
with both deltas. Calls are confined to one thread. Connect receiver lifetimes
with `g_signal_connect_object()` and cancel state timers on exit.

`add(delay, repeat, unscaled)` returns a nonzero ID or zero for invalid input.
Zero-delay one-shots wait for a positive delta. Repeats require a positive delay,
fire at most once/update, and retain phase across missed intervals: 3.25 seconds
on a one-second repeat leaves 0.75 seconds. Delivery is registration ordered.
One-shots are removed before callbacks. `reschedule()` retains ID, repeat/clock
and pause state; it replaces the countdown and suppresses a pending old delivery.
A completed one-shot needs a new timer. Shutdown clears timers, not signal handlers.

## Random streams
`new(seed, selector)` creates an owned PCG32 stream. `copy()` returns an owned
independent object with identical state, not a statistically independent stream.
Use separate selectors for separate draw sequences. Snapshot strings are owned;
`restore()` validates before mutation. Save them as strings, not floating numbers.
`advance()` skips raw outputs in logarithmic time: `next_uint()` consumes one,
`next_double()` two, and `bounded()` a variable number. Snapshot unknown draw
positions. This is not cryptographic randomness or whole-game deterministic replay.

## Curves and blackboards
`LrgKeyframeCurve` is an owned clock-free sampler, not a seekable tween manager.
Keys are sorted, duplicate times replace, and each key supplies outgoing easing.
Finite times outside [0,1] work. Empty sampling and NaN diagnose invalid use;
infinite sample times clamp. `copy()` gives an independent editable curve;
`get_key()`, `remove_key()`, `clear()` and `get_time_range()` support editors.
Removing a key preserves its predecessor's outgoing easing. Invalid get/range
requests return false and reset outputs. Easing may overshoot; do not assume a
bounded result even though interpolation uses double arithmetic for large spans.

`lrg_blackboard_dup_keys()` returns a sorted, owned, NULL-terminated string vector
(use `g_strfreev`); `dup_string()` returns an owned string or NULL for missing,
wrong-type or NULL values (use `g_free`). `get_size()` counts entries, including
NULL strings. Copies survive source mutation; concurrent access still requires
caller synchronization. For editable routes read [navigation](../../libregnum-skill-game-navigation/SKILL.md).

## Verification
Use timer tests for pause, zero delta, stale IDs, rescheduling during delivery,
repeat phase and teardown; random tests for copy/restore and raw draw counts;
curve tests for duplicate/empty/extreme times; utility tests for owned inspection
values after the source is cleared. Inspect `test-template.c` for automatic timer
advancement. `make -C deps/libregnum test` executes engine tests when changing
these implementations; source hash validation alone does not execute them.
