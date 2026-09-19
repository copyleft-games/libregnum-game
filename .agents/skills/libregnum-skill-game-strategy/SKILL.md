---
name: libregnum-skill-game-strategy
description: Build libregnum tycoon, idle and deckbuilder games. Use for economies, cards, offline progress or deterministic simulation.
---

# Skill: Strategy and Progression

Implement testable rule systems for management, card and incremental games.

## When to Use

Tycoon placement, economies, idle progression, combat/poker deckbuilders or racing-2d simulation rules.

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

1. Read [genre recipes](../../../docs/genres.org) and the selected template implementation. Use the micro-tycoon, deckbuilder or chocolate-chip-clicker example as appropriate.
2. Define stable IDs, units, time source, deterministic seeds and save versions. Compose final deckbuilder templates rather than subclassing them.
3. Implement one complete loop: producer/consumer, draw/play/discard, or earn/buy/prestige. For racing-2d use ordered checkpoints and explicit vehicle units.
4. Test domain failures: insufficient funds, occupied tiles, card-zone ownership, reshuffle, score ties, clock rollback and offline rewards applied once.
5. Use [save and test](../libregnum-skill-game-save-test/SKILL.md) for migration and replay checks.
6. Check UI readability, keyboard/controller focus and fast/paused simulation separately from rule tests.

## Verification

Run `make starter-check` after changing this bundle. Run
`make engine-contract-check` with initialized dependencies to check the recorded
source symbols against the pin. For implementation changes, run the owning C
tests and any required display/audio checks from the recipe. Report skipped
checks explicitly; source-symbol checks do not prove runtime behavior.

## Output Format

A small progression loop, deterministic GTests and documented persistence semantics.

## Examples

**Input:** Create an idle workshop with one generator and upgrade.

**Result:** Purchase rules reject insufficient funds and offline progress uses the template application path once. Tests cover cap/rollback and resume twice; persisted snapshot changes are documented.

## Constraints

Do not use frame count as elapsed wall time or silently reset player progression on a schema mismatch.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
