# Authoritative MMO Gameplay contracts

Read when implementing this skill. Audited engine pin: `6750d12e3102ad1b263828705695c8a750cd7fc1`.
Recheck the source before using these contracts with another revision.

## Source trail

- [examples/mmo-client.py](../../../../deps/libregnum/examples/mmo-client.py) — read for this workflow.
- [src/net/lrg-net-server.h](../../../../deps/libregnum/src/net/lrg-net-server.h) — read for this workflow.
- [src/mmo/lrg-mmo-datagram.h](../../../../deps/libregnum/src/mmo/lrg-mmo-datagram.h) — read for this workflow.

- [src/mmo/lrg-mmo-realm.h](../../../../deps/libregnum/src/mmo/lrg-mmo-realm.h) — inspect `lrg_mmo_realm_accept_command`.
- [src/mmo/lrg-mmo-realm.c](../../../../deps/libregnum/src/mmo/lrg-mmo-realm.c) — inspect `lrg_mmo_realm_advance`.
- [src/mmo/lrg-mmo-replicator.h](../../../../deps/libregnum/src/mmo/lrg-mmo-replicator.h) — inspect `lrg_mmo_replicator_build_page`.
- [src/mmo/lrg-mmo-replicator.c](../../../../deps/libregnum/src/mmo/lrg-mmo-replicator.c) — inspect `pending_cursor`.
- [examples/mmo-simulation.c](../../../../deps/libregnum/examples/mmo-simulation.c) — inspect `simulate`.
- [examples/mmo-runtime.py](../../../../deps/libregnum/examples/mmo-runtime.py) — inspect `checkpoint`.
- [tests/test-mmo.c](../../../../deps/libregnum/tests/test-mmo.c) — inspect `lrg_mmo_realm_login`.
- [tests/test-mmo-completion.c](../../../../deps/libregnum/tests/test-mmo-completion.c) — inspect `fair_pages`.
- [docs/modules/mmo/runtime.org](../../../../deps/libregnum/docs/modules/mmo/runtime.org) — inspect `DTLS`.

## Host and transport
Create `LrgMmoRealm` and register zones before admission. `login()` accepts a
verified account and real nonzero transport peer ID; it does not authenticate.
Realm account/zone strings are borrowed until mutation. Realm and replication
objects belong to one thread. Set `LrgNetServer:max-peers` explicitly: its
unlimited compatibility default is separate from realm capacity. Drive both the
owning main context and transport `poll()`; neither substitutes for the other.

`accept_command()` uses a nonzero increasing 64-bit sequence and server monotonic
microseconds, with a burst of 100 and refill of 50/second. Admission is separate
from ownership, collision, range and cooldown checks. `advance()` emits 50 ms
ticks, at most eight per call, dropping excess whole ticks. Failed commands do
not keep idle sessions alive; call `expire()` and clean up on `session-ended`.

## Replication and recovery
Publish stable entity IDs with public bytes through `upsert()`. State is capped
at 64 KiB/entity; interest radius is at most four cell sizes. `build()` returns
an owned `(ta(ttddday)at)` GVariant, capped at 1 MiB. `build_page()` permits
128–1048576-byte budgets. Apply a complete page atomically before acknowledgment;
queueing a send is not acknowledgment. Pending snapshots are unchanged on retry.
The implementation uses an acknowledged rotating cursor for dirty updates;
wire entries are sorted. The header's older low-ID fairness wording is incomplete:
inspect the implementation and `fair_pages` test before modifying scheduling.

On logout call `forget()` and release session entities. Reconnect/world reset
requires a fresh stream identity, empty client replica and full baseline. Keep
private account data out of replication. The runtime example commits checkpoints
and command receipts under a lease fence before replying; ambiguous storage
failure stops admission until authority and state are recovered.

## Selecting reference integrations
Start with `examples/mmo-simulation.c` for an in-memory, already-authenticated
walkthrough. `examples/mmo-runtime.py` and `mmo-client.py` provide a terminal TLS
host/client, with their own length-prefixed JSON protocol. Do not mix that wire
format with the separate LRGM service protocol. Run their `--help` from the
engine directory; Python GI requires the generated typelib/shared library paths.
Read `docs/modules/mmo/runtime.org` before extending recovery or the DTLS option.
DTLS requires connected UDP sockets, mutual certificates, bounded handshake
polling and application retries; it does not supply reliable delivery or QUIC.

## Verification
Cover spoofed ownership, duplicate/rate-limited commands, full zones, tick
catch-up, dropped/wrong acknowledgments, paginated convergence and restart.
The source tests listed below are evidence, not executed checks. For engine
changes run `make -C deps/libregnum test`; opt into real TLS/runtime integration
with `make -C deps/libregnum test-mmo-runtime`. These can use sockets/devices and
must not be added to the root hermetic starter checks. Local success is not a
player-capacity benchmark or a deployed MMO.
