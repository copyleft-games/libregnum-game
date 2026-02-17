# Libregnum Game Template

A template repository for creating games with [libregnum](https://gitlab.com/copyleft-games/libregnum), a GObject-based game engine built on graylib.

Fork this repo and start building your game.

## Quick Start

```bash
# Clone with submodules
git clone --recursive <your-fork-url>
cd libregnum-game

# Install dependencies (Fedora)
make install-deps

# Build and run
make run
```

## Project Structure

```
libregnum-game/
├── Makefile                # Root build orchestration
├── config.mk               # Build configuration (game name, version, options)
├── rules.mk                # Build rules and helpers
├── src/                     # Game source files
│   └── main.c              # Entry point
├── tests/                   # Unit tests (test-*.c)
├── data/                    # Game data files (YAML, textures, sounds, etc.)
├── docs/                    # Game documentation
└── deps/
    └── libregnum/           # Engine library (git submodule)
```

## Build Commands

```bash
make                    # Build libregnum + game
make game               # Build only the game (deps must be built)
make deps               # Build only libregnum
make run                # Build and run
make test               # Build and run tests
make clean              # Clean game build artifacts
make clean-all          # Clean everything (including libregnum)
make help               # Show all targets and options
```

## Build Options

| Option | Default | Description |
|--------|---------|-------------|
| `DEBUG=1` | 0 | Debug build with `-g3 -O0` |
| `ASAN=1` | 0 | AddressSanitizer (requires `DEBUG=1`) |
| `UBSAN=1` | 0 | UndefinedBehaviorSanitizer (requires `DEBUG=1`) |
| `STATIC=1` | 0 | Static linking for shipping |
| `STEAM=1` | 0 | Enable Steam SDK integration |
| `MCP=1` | 0 | Enable MCP support (AI debugging) |
| `WINDOWS=1` | 0 | Cross-compile for Windows (requires mingw64) |
| `GAME_NAME=x` | `libregnum-game` | Set the game binary name |
| `PREFIX=path` | `/usr/local` | Installation prefix |

## Customizing

1. **Rename your game**: Set `GAME_NAME` in `config.mk` or pass it on the command line
2. **Add source files**: Create `.c` files under `src/` and add them to `GAME_SRCS` in `Makefile`
3. **Add tests**: Create `test-*.c` files under `tests/` (auto-discovered)
4. **Add game data**: Place YAML configs, textures, sounds under `data/`
5. **Update version**: Edit `VERSION_MAJOR`, `VERSION_MINOR`, `VERSION_MICRO` in `config.mk`

## Dependencies

### Required (Fedora packages)

```bash
gcc make pkgconf-pkg-config
glib2-devel json-glib-devel
libdex-devel libyaml-devel libsoup3-devel
gobject-introspection-devel
mesa-libGL-devel libX11-devel
```

### Submodules

- `deps/libregnum/` - The game engine (includes graylib, yaml-glib, raylib)

Initialize submodules if not cloned with `--recursive`:

```bash
git submodule update --init --recursive
```

## License

AGPLv3 - See [LICENSE](LICENSE)
