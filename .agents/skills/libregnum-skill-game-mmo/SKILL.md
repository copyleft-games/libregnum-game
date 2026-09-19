---
name: libregnum-skill-game-mmo
description: Build libregnum shared-world gameplay. Use for network sessions, authoritative ticks, interest replication, client reconciliation and reconnect recovery.
---

# Skill: Authoritative MMO Gameplay

Implement this workflow against the pinned engine with explicit ownership,
failure handling and tests at the owning layer.

## When to Use

Build libregnum shared-world gameplay. Use for network sessions, authoritative ticks, interest replication, client reconciliation and reconnect recovery.

## Prerequisites

Read root AGENTS.md. Initialize the pinned engine for source inspection; C work
requires the compiler/dependencies listed in README.md. Documentation checks need
Python 3. Commands below run from the project root unless stated otherwise. MMO builds also need SQLite, OpenSSL, zlib and libpq development packages; TLS needs a GIO TLS backend. Python reference hosts need Python GObject bindings and built GIR/typelibs.

## Instructions

1. Define player ownership, zones, public replicated state and reconnect behavior.
2. Read [the engine recipe](references/engine-recipe.md), then inspect the linked
   headers, implementations and reference host before choosing TCP/TLS or DTLS.
3. Bound unauthenticated peers and messages, verify identity, admit commands using
   the real transport peer, and run game authorization before changing state.
4. Integrate fixed ticks, spatial publication, client application and explicit
   acknowledgments. Implement logout, expiry and fresh baselines on reconnect.
5. For durable commands, read [MMO services](../libregnum-skill-game-mmo-services/SKILL.md)
   and implement receipts and fenced writes before reporting a committed result.
6. Run `make starter-check` and `make engine-contract-check` after documentation
   changes, and `make test` for C integration changes. Run the recipe's optional
   engine/integration checks only in their stated environments; report skips.
7. Update org-mode game documentation and report implemented behavior and checks.

## Output Format

Game integration and meaningful tests at the owning layer, org documentation
under docs/, and a report separating source checks from runtime validation.

## Examples

**Input:** Make two players share a zone and recover after a lost connection.

**Result:** A host authenticates Alice and Bob, assigns server-owned characters,
rejects Bob's attempt to move Alice, and publishes only public position/health.
A dropped acknowledgment resends the same delta. Reconnecting resets the client
world and receives a fresh baseline. Tests cover replay, zone isolation, expired
sessions and wrong acknowledgment sequences.

## Constraints

Use inspected signatures and transfer annotations; preserve unrelated changes.
Do not infer implemented behavior from a type name or claim unexecuted tests.
Keep device/network checks separate from hermetic starter checks. Do not push
or spawn subagents without user instructions.
