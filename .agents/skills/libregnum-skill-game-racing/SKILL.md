---
name: libregnum-skill-game-racing
description: Build 2D and 3D racing games with libregnum. Use for tracks, checkpoints, laps, vehicle surfaces and resets.
---

# Skill: Racing Game

Deliver the requested behavior using the pinned engine's actual contracts.

## When to Use

tracks, checkpoints, laps, vehicle surfaces and resets.

## Prerequisites

Read root AGENTS.md. Initialize the engine for source inspection. C changes need
the compiler/dependencies listed in README.md; source/document checks need Python 3.
All commands below run from the repository root.

## Instructions

1. Establish the requested behavior, current implementation and acceptance criteria.
2. Read [the engine recipe](references/engine-recipe.md) for the exact hooks,
   defaults, ownership and failure cases. Inspect its linked source/tests.
3. Implement one end-to-end operation at the owning layer, with documented
   lifecycle, data layout and error handling. Preserve unrelated behavior.
4. Add meaningful tests from the recipe's failure cases. Run `make test` for C
   changes and `make starter-check` for skill/document/tooling changes.
5. Run `make engine-contract-check` against initialized pinned sources. This is
   source-evidence validation, not execution of engine tests. Run device checks
   separately when applicable and report any unavailable configuration.
6. Document controls/API changes and report files, checks and limitations.

## Output Format

Implementation and tests at the owning layer, org documentation under docs/,
and a report distinguishing automated, manual and untested behavior.

## Examples

**Input:** Build a three-checkpoint track with one complete lap.

**Result:** Track progression rejects repeated overlaps, reverse finish crossing and skipped checkpoints. Vehicle reset clears velocity and repositions the camera without awarding a checkpoint.

## Constraints

Use the verified signatures and transfer annotations. Do not suppress failures,
assume a stub is implemented or expand into unrelated subsystems. Preserve user
changes; pushing requires the user's authorization. Do not spawn subagents.
