---
name: libregnum-skill-game-bootstrap
description: Choose and customize a libregnum game starter. Use when starting a new game or choosing its template.
---

# Skill: Game Bootstrap

Start a small complete game loop using the pinned engine templates.

## When to Use

Starting a game, choosing a genre, or turning a brief into a first playable.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read repository AGENTS.md and [getting started](../../../docs/getting-started.org). Inspect config.mk, src/game-starter.c and the selected template header.
2. Read [genre recipes](../../../docs/genres.org) and write a brief using [game brief](../../../docs/game-brief.org). Choose perspective, input, target hardware and one complete loop.
3. Launch `make run ARGS='--genre platformer'` (substitute the selected genre). Distinguish engine defaults from game-specific geometry and rules.
4. Replace the relevant factory branch with a game subclass or compose a final template. Add explicit GAME_SRCS entries and keep rules separate from drawing.
5. Implement start/play/results/restart, then add a small deterministic rule test. Run `make test` and manually exercise the selected genre on a display.
6. Document controls and any unsupported features. Keep the first milestone bounded before adding more content.

## Output Format

A configured game, focused source modules, meaningful tests and docs/game-brief.org.

## Examples

Start a keyboard/controller dungeon game: select top-down, implement one room and door, test blocked movement and room completion.

## Constraints

Do not subclass final engine types. Do not infer full subsystem support from a type name.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
