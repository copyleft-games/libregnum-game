---
name: libregnum-skill-game-mmo-services
description: Integrate libregnum MMO services. Use for transactional storage, authentication, social/economy operations, party matchmaking, seasons and fenced recovery.
---

# Skill: MMO Persistence and Services

Implement this workflow against the pinned engine with explicit ownership,
failure handling and tests at the owning layer.

## When to Use

Integrate libregnum MMO services. Use for transactional storage, authentication, social/economy operations, party matchmaking, seasons and fenced recovery.

## Prerequisites

Read root AGENTS.md. Initialize the pinned engine for source inspection; C work
requires the compiler/dependencies listed in README.md. Documentation checks need
Python 3. Commands below run from the project root unless stated otherwise. MMO builds also need SQLite, OpenSSL, zlib and libpq development packages; TLS needs a GIO TLS backend. Python reference hosts need Python GObject bindings and built GIR/typelibs.

## Instructions

1. Define the trusted actor, transaction boundary, stable operation ID and retry
   behavior for one service operation.
2. Read [the engine recipe](references/engine-recipe.md), following the relevant
   service header and tests before composing auth, store, social or market APIs.
3. Use worker-owned stores and services. Verify identity before resolving actor
   arguments, keep database calls off the simulation loop and propagate errors.
4. Implement atomic writes, exact retry receipts and lease fencing where needed.
   Reconcile ambiguous outcomes before accepting new gameplay commands.
5. Integrate with [MMO gameplay](../libregnum-skill-game-mmo/SKILL.md); document private credentials,
   backup/restore and the chosen optional integration checks.
6. Run `make starter-check` and `make engine-contract-check` after documentation
   changes, and `make test` for C integration changes. Run the recipe's optional
   engine/integration checks only in their stated environments; report skips.
7. Update org-mode game documentation and report implemented behavior and checks.

## Output Format

Game integration and meaningful tests at the owning layer, org documentation
under docs/, and a report separating source checks from runtime validation.

## Examples

**Input:** Make an inventory purchase safe when the client loses its reply.

**Result:** The worker commits currency and inventory in one `a(stay)` batch via
`lrg_mmo_store_commit_once()` with operation ID `purchase-alice-0042`. Retrying
that exact batch returns success with `duplicate=TRUE`; altered contents under
the same ID fail. Tests reopen the database and verify one charge and one item.

## Constraints

Use inspected signatures and transfer annotations; preserve unrelated changes.
Do not infer implemented behavior from a type name or claim unexecuted tests.
Keep device/network checks separate from hermetic starter checks. Do not push
or spawn subagents without user instructions.
