---
name: libregnum-skill-game-bootstrap
description: Choose and customize a libregnum game starter. Use when starting a new game or choosing its template.
---

# Skill: Game Bootstrap

Start a small complete game loop using the pinned engine templates.

## When to Use

Starting a game, choosing a genre, or turning a brief into a first playable.

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

1. Read repository AGENTS.md and [getting started](../../../docs/getting-started.org). Inspect config.mk, src/game-starter.c and the selected template header.
2. Read [genre recipes](../../../docs/genres.org) and write a brief using [game brief](../../../docs/game-brief.org). Choose perspective, input, target hardware and one complete loop.
3. Launch `make run ARGS='--genre platformer'` (substitute the selected genre). Distinguish engine defaults from game-specific geometry and rules.
4. Replace the relevant factory branch with a game subclass or compose a final template. Add explicit GAME_SRCS entries and keep rules separate from drawing.
5. Implement start/play/results/restart, then add a small deterministic rule test. Run `make test` and manually exercise the selected genre on a display.
6. Document controls and any unsupported features. Keep the first milestone bounded before adding more content.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

When recording first-playable acceptance, copy and adapt the
[output template](templates/first-playable.org.template) into docs/; replace the example
with the actual game or asset case and fill in observed verification results.

## Output Format

A configured game, focused source modules, meaningful tests and docs/game-brief.org.

## Examples

**Input:** Start a 640x360 dungeon game with one room and a locked exit.

**Result:** src/game-starter.c selects a top-down game class; a key/door rule test proves the exit stays locked until pickup. docs/game-brief.org records controls, restart behavior and the data root.

## Constraints

Do not subclass final engine types. Do not infer full subsystem support from a type name.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
