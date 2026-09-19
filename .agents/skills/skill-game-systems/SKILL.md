---
name: skill-game-systems
description: Integrate libregnum ECS, input, UI, audio and YAML content. Use when adding common game systems or engine extensions.
---

# Skill: Game Systems

Integrate reusable engine systems at their existing ownership and lifecycle boundaries.

## When to Use

Input actions, ECS components, HUDs, audio, animation, data definitions or missing engine capabilities.

## Prerequisites

A checkout of this repository and its pinned engine; see README.md for build
packages. Asset search needs browsing/network access; intake needs Python 3.
Load only the references relevant to the task. Paths in commands are repository-relative.

## Instructions

1. Read [game systems](../../../docs/game-systems.org), repository instructions, and the actual headers/implementations for the system involved.
2. Trace one operation through its owner and callers. Record ownership, initialization order, thread/context requirements and error paths.
3. Implement the smallest integrated behavior; separate rules from presentation. For YAML, register types before loading and use a real engine schema/example.
4. Add tests for malformed data, destroyed targets, missing input, or failed loads. Keep ordinary tests independent of display/audio/network.
5. Exercise device/context paths explicitly. Use [asset intake](../skill-import-assets/SKILL.md) when loading external media.
6. For a missing reusable capability, change the owning libregnum module with source/header/build/tests/docs, commit its submodule first and then the parent gitlink.

## Output Format

Integrated behavior, relevant tests, ownership documentation and scoped dependency commits when needed.

## Examples

Add a pause menu that freezes simulation but retains keyboard/controller navigation and resumes safely.

## Constraints

Do not invent APIs or introduce a second engine loop. Do not treat a stub or header declaration as tested functionality.
Preserve unrelated changes. Do not push or contact other people without the user's instruction.
