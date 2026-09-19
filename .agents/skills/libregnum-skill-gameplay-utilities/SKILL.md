---
name: libregnum-skill-gameplay-utilities
description: Use libregnum timers, random streams and editing utilities. Trigger for cooldowns, deterministic previews, keyframe editing or blackboard inspection.
---

# Skill: Gameplay Timing and Editing Utilities

Implement this workflow against the pinned engine with explicit ownership,
failure handling and tests at the owning layer.

## When to Use

Use libregnum timers, random streams and editing utilities. Trigger for cooldowns, deterministic previews, keyframe editing or blackboard inspection.

## Prerequisites

Read root AGENTS.md. Initialize the pinned engine for source inspection; C work
requires the compiler/dependencies listed in README.md. Documentation checks need
Python 3. Commands below run from the project root unless stated otherwise.

## Instructions

1. Identify the owning clock, mutable state and lifetime of the requested utility.
2. Read [the engine recipe](references/engine-recipe.md); choose timers for delayed
   gameplay, random streams for reproducible draws, curves for sampling, or
   blackboard copies for inspection. Load only the relevant source trail.
3. Use the template-owned timer manager once per frame, or an explicitly driven
   standalone manager. Cancel state-owned actions when leaving that state.
4. Separate preview copies from live state and preserve random snapshots in saves.
   Keep inspected values owned across mutations; handle empty/invalid inputs.
5. Add deterministic tests using supplied deltas and seeds, with no sleeps.
6. Run `make starter-check` and `make engine-contract-check` after documentation
   changes, and `make test` for C integration changes. Run the recipe's optional
   engine/integration checks only in their stated environments; report skips.
7. Update org-mode game documentation and report implemented behavior and checks.

## Output Format

Game integration and meaningful tests at the owning layer, org documentation
under docs/, and a report separating source checks from runtime validation.

## Examples

**Input:** Preview a loot roll without changing the next real roll.

**Result:** This headless assertion leaves the original stream untouched until
its final draw; use it inside a GTest function including `<libregnum.h>`.

```c
g_autoptr(LrgRandomStream) loot = lrg_random_stream_new (42, 54);
g_autoptr(LrgRandomStream) preview = lrg_random_stream_copy (loot);
guint32 expected = lrg_random_stream_bounded (preview, 20);

g_assert_cmpuint (lrg_random_stream_bounded (loot, 20), ==, expected);
```

## Constraints

Use inspected signatures and transfer annotations; preserve unrelated changes.
Do not infer implemented behavior from a type name or claim unexecuted tests.
Keep device/network checks separate from hermetic starter checks. Do not push
or spawn subagents without user instructions.
