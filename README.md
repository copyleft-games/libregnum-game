# Libregnum Game Starter Kit

A C/GObject game starter for [libregnum](https://gitlab.com/copyleft-games/libregnum),
with thirteen selectable engine templates, practical game-development guides,
project-local skills and agents, and a reproducible asset pipeline.

## Start here

```sh
git submodule update --init --recursive
make check-deps
make -j8
make run ARGS='--genre platformer'
```

The default is `platformer`. Use `build/release/libregnum-game --list-genres` for
top-down, shooter, twin-stick, shmup, tycoon, racing, FPS, third-person,
deckbuilder and idle options. These launch engine templates; build your own
world, rules and UI using the matching guide and engine example.

1. [Getting started](docs/getting-started.org): customize, build, test and package.
2. [Genre recipes](docs/genres.org): template choices and first-playable milestones.
3. [Game systems](docs/game-systems.org): input, ECS, UI, content, saves and audio.
4. [Asset workflow](docs/assets.org): find, download, verify, load and credit media.
5. [Skills and agents](.agents/README.md): focused instructions for an assistant.
6. [Repository evaluation](docs/starter-audit.org): findings, fixes and limits.

## Assets you can reproduce

The kit includes a small licensed 2D tile and 3D barrel sample. Their source URLs,
archive/member hashes, original license text and selected file paths are pinned
in [the manifest](data/assets/manifest.json). The barrel's texture sidecar is
included. [Credits](data/assets/CREDITS.md) are generated from that manifest.

```sh
make assets-validate       # Validate manifest structure and metadata
make assets-fetch          # Fetch only absent packs; verify existing packs
make assets-verify         # Verify all installed files and provenance
make assets-credits        # Print generated credits
make assets-smoke          # Load PNG/GLB using a display/OpenGL context
```

To add assets, follow the [intake procedure](docs/assets.org). Downloads are
checksum-pinned and installed per pack; altered files are preserved and reported.
The normal test suite does not use the network or open a window.

## Build and test

| Command | Purpose |
|---------|---------|
| `make`, `make game` | Build the engine prerequisites and game |
| `make deps` | Build the engine and its dependencies |
| `make run ARGS='--genre top-down'` | Launch a selected starter |
| `make test` | Run game GTests and Python starter checks |
| `make engine-contract-check` | Check recipe source evidence against the engine pin |
| `make starter-check` | Check tooling, skills, documentation links and credits with Python 3 |
| `make clean`, `make clean-all` | Clean game builds / also clean engine output |
| `make help` | List build options and utility targets |

Set `GAME_NAME` and version components in `config.mk`; add sources explicitly to
`GAME_SRCS` in `Makefile`. C tests named `tests/test-*.c` are auto-discovered.
Use `DEBUG=1`, with `ASAN=1` / `UBSAN=1` when needed. Start a fresh build when
changing instrumentation or link mode. `STATIC=1`, `WINDOWS=1`, `STEAM=1` and
`MCP=1` are available build options, with their own toolchain/SDK requirements.

For a smaller engine build during game development:

```sh
make -j8 test BUILD_GIR=0 BUILD_EXAMPLES=0 BUILD_TESTS=0
```

Those flags disable engine auxiliary builds, not the root game's test runner.
The install target installs the binary only; shipping needs a deliberate data,
credits and runtime-library layout. See the getting-started guide.

## Requirements

Python 3 for starter tooling. Fedora build packages:

```text
gcc make pkgconf-pkg-config
glib2-devel json-glib-devel libdex-devel libyaml-devel libsoup3-devel
gobject-introspection-devel mesa-libGL-devel libX11-devel
```

`make check-deps` reports the current environment. The explicit `make install-deps`
target invokes Fedora's package manager; install packages only as appropriate for
your host. A working display/OpenGL context is required to play or run the asset
smoke check. Optional engine modules may need additional packages; inspect the
pinned engine's configuration and diagnostics.

## Layout

```text
src/                  Entry point and genre factory; add game modules here
tests/                GTest and hermetic Python regression tests
data/assets/          Manifest, selected asset packs, licenses and credits
docs/                 Org-mode game and workflow guides
.agents/skills/       Fifteen task-specific skills
.agents/agents/       Six portable specialist role definitions
tools/                Asset importer, starter validator and GPU import check
deps/libregnum/       Pinned engine submodule, examples and API documentation
```

## License

Code: [AGPL-3.0-or-later](LICENSE). Third-party assets retain their individual
licenses; see each pack's `LICENSE.txt` and [asset credits](data/assets/CREDITS.md).
