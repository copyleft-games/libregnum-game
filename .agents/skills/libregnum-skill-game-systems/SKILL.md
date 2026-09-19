---
name: libregnum-skill-game-systems
description: Integrate libregnum ECS, input, UI, audio and YAML content. Use when adding common game systems or engine extensions.
---

# Skill: Game Systems

Integrate reusable engine systems at their existing ownership and lifecycle boundaries.

## When to Use

Input actions, ECS components, HUDs, audio, animation, data definitions or missing engine capabilities.

## Prerequisites

A checkout with pinned engine sources and a game brief. See README.md for C
build packages. Python 3 runs starter/source checks; runtime tests require the
selected engine build and device-dependent checks need their graphics/audio context.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

First read [the engine recipe](references/engine-recipe.md) for this task. It
links the inspected headers, implementations and tests, identifies defaults and
missing game behavior, and gives concrete failure cases. Recheck those sources
when the pinned engine changes. All commands run from the repository root.

1. Read [game systems](../../../docs/game-systems.org), repository instructions, and the actual headers/implementations for the system involved.
2. Trace one operation through its owner and callers. Record ownership, initialization order, thread/context requirements and error paths.
3. Implement the smallest integrated behavior; separate rules from presentation. For YAML, register types before loading and use a real engine schema/example.
4. Add tests for malformed data, destroyed targets, missing input, or failed loads. Keep ordinary tests independent of display/audio/network.
5. Exercise device/context paths explicitly. Use [asset intake](../libregnum-skill-import-assets/SKILL.md) when loading external media.
6. For a missing reusable capability, change the owning libregnum module with source/header/build/tests/docs, commit its submodule first and then the parent gitlink.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

Integrated behavior, relevant tests, ownership documentation and scoped dependency commits when needed.

## Examples

**Input:** Pause gameplay while showing the scene underneath a menu.

**Result:** A transparent blocking pause state consumes gameplay input and preserves menu navigation. Tests exercise push/pop ownership and repeated pause/resume without extra input polls.

## Constraints

Do not invent APIs or introduce a second engine loop. Do not treat a stub or header declaration as tested functionality.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
