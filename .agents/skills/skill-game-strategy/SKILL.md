---
name: skill-game-strategy
description: Build libregnum tycoon, idle and deckbuilder games. Use for economies, cards, offline progress or deterministic simulation.
---

# Skill: Strategy and Progression

Implement testable rule systems for management, card and incremental games.

## When to Use

Tycoon placement, economies, idle progression, combat/poker deckbuilders or racing-2d simulation rules.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [genre recipes](../../../docs/genres.org) and the selected template implementation. Use the micro-tycoon, deckbuilder or chocolate-chip-clicker example as appropriate.
2. Define stable IDs, units, time source, deterministic seeds and save versions. Compose final deckbuilder templates rather than subclassing them.
3. Implement one complete loop: producer/consumer, draw/play/discard, or earn/buy/prestige. For racing-2d use ordered checkpoints and explicit vehicle units.
4. Test domain failures: insufficient funds, occupied tiles, card-zone ownership, reshuffle, score ties, clock rollback and offline rewards applied once.
5. Use [save and test](../skill-game-save-test/SKILL.md) for migration and replay checks.
6. Check UI readability, keyboard/controller focus and fast/paused simulation separately from rule tests.

## Output Format

A small progression loop, deterministic GTests and documented persistence semantics.

## Examples

Make an idle workshop with one generator and upgrade; verify capped offline income is granted once per resume.

## Constraints

Do not use frame count as elapsed wall time or silently reset player progression on a schema mismatch.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
