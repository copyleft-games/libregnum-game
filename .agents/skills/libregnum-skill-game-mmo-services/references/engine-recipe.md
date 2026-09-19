# MMO Persistence and Services contracts

Read when implementing this skill. Audited engine pin: `6750d12e3102ad1b263828705695c8a750cd7fc1`.
Recheck the source before using these contracts with another revision.

## Source trail

- [docs/modules/mmo/services.org](../../../../deps/libregnum/docs/modules/mmo/services.org) — read for this workflow.
- [docs/modules/mmo/completion.org](../../../../deps/libregnum/docs/modules/mmo/completion.org) — read for this workflow.
- [examples/mmo-runtime.py](../../../../deps/libregnum/examples/mmo-runtime.py) — read for this workflow.

- [src/mmo/lrg-mmo-store.h](../../../../deps/libregnum/src/mmo/lrg-mmo-store.h) — inspect `lrg_mmo_store_commit_once`.
- [src/mmo/lrg-mmo-store.c](../../../../deps/libregnum/src/mmo/lrg-mmo-store.c) — inspect `G_IO_ERROR_WRONG_ETAG`.
- [src/mmo/lrg-mmo-auth.h](../../../../deps/libregnum/src/mmo/lrg-mmo-auth.h) — inspect `lrg_mmo_auth_prepare_recovery`.
- [src/mmo/lrg-mmo-social.h](../../../../deps/libregnum/src/mmo/lrg-mmo-social.h) — inspect `lrg_mmo_social_new`.
- [src/mmo/lrg-mmo-market.h](../../../../deps/libregnum/src/mmo/lrg-mmo-market.h) — inspect `lrg_mmo_market_new`.
- [src/mmo/lrg-mmo-matchmaker.h](../../../../deps/libregnum/src/mmo/lrg-mmo-matchmaker.h) — inspect `lrg_mmo_matchmaker_enqueue_party`.
- [src/mmo/lrg-mmo-matchmaker.c](../../../../deps/libregnum/src/mmo/lrg-mmo-matchmaker.c) — inspect `lrg_mmo_matchmaker_take`.
- [src/mmo/lrg-mmo-season.h](../../../../deps/libregnum/src/mmo/lrg-mmo-season.h) — inspect `lrg_mmo_season_record`.
- [tests/test-mmo-services.c](../../../../deps/libregnum/tests/test-mmo-services.c) — inspect `lrg_mmo_store_commit_once`.
- [tests/test-mmo-runtime.c](../../../../deps/libregnum/tests/test-mmo-runtime.c) — inspect `parties`.
- [tests/test-mmo-completion.c](../../../../deps/libregnum/tests/test-mmo-completion.c) — inspect `postgres`.
- [examples/mmo-admin.py](../../../../deps/libregnum/examples/mmo-admin.py) — inspect `smtp`.
- [docs/modules/mmo/runtime.org](../../../../deps/libregnum/docs/modules/mmo/runtime.org) — inspect `Patroni`.

## Storage and ownership
`lrg_mmo_store_new()` opens SQLite; `new_postgres()` opens libpq storage. Both
return owned GObjects and are synchronous/thread-confined. Each worker creates
its own store and service objects; marshal results to the simulation context.
`read()` returns owned GBytes and a revision. `commit()` accepts an `a(stay)`
batch of key, expected revision, bytes: zero is create-only, otherwise exact CAS.
At most 256 distinct records and 1 MiB per record; conflict rolls back the batch
with `G_IO_ERROR_WRONG_ETAG`. Reload and revalidate intent for a fresh transaction.

`commit_once()` binds an operation ID to the exact batch and durable receipt.
For an ambiguous reply, retry unchanged bytes AND revisions with the same ID.
Do not reprice a purchase under an old receipt. `commit_fenced()` checks a live
zone lease in the transaction; route every zone-owned write through fencing.
It is a different API from `commit_once()`: do not assume their guarantees
compose automatically. Follow the runtime checkpoint/receipt integration for both.
PostgreSQL connection failures are not silently reconnected or replayed.
SQLite online `backup()` refuses an existing destination; PostgreSQL recovery
uses its documented dump/restore tooling. Verify restores in isolated storage.

## Service selection and identity
Inspect only the service needed for the task:
- Auth: password/token verification, TOTP, bans and one-use recovery. Actor IDs
  must come from verified sessions; operator attribution is not authorization.
- Social and market: use membership/ownership checks and transactional escrow
  instead of composing separate debit/credit calls in the host.
- Matchmaker: `enqueue_party()` takes account/rating tuples after the host checks
  membership and consent. Capacity counts members. Any member's cancellation or
  expiry removes the whole ticket. Greedy FIFO packing may leave a match queued.
- Season: record results only from trusted authority, using a stable match ID.
  Exact retries succeed after season end; changed results at that ID reject.

`prepare_recovery()` reads the verified mailbox; its private `(ss)` delivery
result is for the adapter, not the anonymous requester. Public endpoints return
a generic response. `examples/mmo-admin.py` supplies verified TLS SMTP and
operator workflows; inspect it without sending mail or changing live accounts.

## Verification and operational boundaries
Use temporary SQLite databases for conflicts, exact/changed retries, reopen,
rollback, stale fences, permission rejection and whole-party cancellation.
`tests/test-mmo-services.c`, `test-mmo-completion.c` and `test-mmo-runtime.c`
exercise these contracts. PostgreSQL cases require `LRG_TEST_POSTGRES` pointing
to a disposable database; report skipped backend coverage explicitly.
From the project root, optional checks are:
`make -C deps/libregnum test-mmo-gi`,
`make -C deps/libregnum test-mmo-content`, and
`make -C deps/libregnum/examples check-mmo-server`.
Read the runtime operations document before the explicit Podman HA laboratory
(`make -C deps/libregnum test-mmo-ha`). It needs its prebuilt image and disposable
resources; local election tests do not validate physical-host fencing or WAN SLOs.
