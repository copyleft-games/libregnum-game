# Libregnum Game Template - Project Guide

## Project Overview

This is a template repository for building games with libregnum, a GObject-based game engine. The engine is included as a git submodule at `deps/libregnum/`.

For full engine API documentation, see `deps/libregnum/CLAUDE.md`.

## Directory Structure

```
libregnum-game/
├── Makefile            # Root build orchestration
├── config.mk           # Build configuration
├── rules.mk            # Build rules and helpers
├── src/                # Game source files
│   └── main.c          # Entry point (modify this)
├── tests/              # Unit tests (test-*.c, auto-discovered)
├── data/               # Game data (YAML configs, textures, sounds)
├── docs/               # Game documentation
└── deps/
    └── libregnum/      # Engine library (git submodule)
        ├── src/        # 55+ engine modules, 310+ headers
        ├── deps/
        │   ├── graylib/    # GObject wrapper for raylib
        │   └── yaml-glib/  # YAML parsing with GObject
        └── CLAUDE.md   # Full engine API reference
```

## Build System

### Build Commands

```bash
make              # Build deps + game
make game         # Build only game (deps must exist)
make deps         # Build only libregnum
make run          # Build and run
make test         # Build and run tests
make clean        # Clean game artifacts
make clean-all    # Clean everything including libregnum
make help         # Show all targets
```

### Build Options

All options are passed on the command line:

```bash
make DEBUG=1      # Debug build (-g3 -O0)
make ASAN=1       # AddressSanitizer (needs DEBUG=1)
make UBSAN=1      # UndefinedBehaviorSanitizer (needs DEBUG=1)
make STATIC=1     # Static linking (for shipping)
make STEAM=1      # Steam SDK integration
make MCP=1        # MCP support (AI debugging)
make WINDOWS=1    # Cross-compile for Windows
make GAME_NAME=x  # Custom binary name
```

### Adding Source Files

1. Create `.c` files under `src/` (subdirectories supported)
2. Add them to `GAME_SRCS` in `Makefile`
3. The pattern rule `$(OBJDIR)/%.o: src/%.c` handles all subdirectories

### Adding Tests

1. Create `test-*.c` files under `tests/`
2. Tests are auto-discovered via `$(wildcard tests/test-*.c)`
3. Each test links against all game objects (minus main.o) + libregnum
4. Run with `make test`

## C Standard and Code Style

- **Standard**: `gnu89` (GNU C89 extensions, no `-pedantic`)
- **Warnings**: `-Wall -Wextra -Werror` (zero tolerance)
- **Comments**: Always `/* */`, never `//`
- **Naming**:
  - Defines: `UPPERCASE_SNAKE_CASE`
  - Types/Classes: `PascalCase`
  - Functions/Variables: `lowercase_snake_case`

### Function Signature Style

```c
GDateTime *
function_name(
    gint        arg1,
    gpointer    arg2
){
    /* ... */
}
```

## Engine Usage Patterns

### Includes

```c
#include <libregnum.h>          /* Master include (everything) */

/* Or individual modules */
#include <libregnum/core/lrg-engine.h>
#include <libregnum/ecs/lrg-world.h>
#include <libregnum/graphics/lrg-camera2d.h>
```

### Engine Lifecycle

```c
LrgEngine *engine = lrg_engine_get_default();
lrg_engine_startup(engine, &error);
/* game loop */
lrg_engine_update(engine, delta_time);
lrg_engine_shutdown(engine);
```

### Using Templates (Quick Start)

```c
#include <libregnum.h>

int
main(int argc, char *argv[])
{
    g_autoptr(LrgPlatformerTemplate) game = NULL;

    game = g_object_new(LRG_TYPE_PLATFORMER_TEMPLATE,
                         "title", "My Platformer",
                         "virtual-width", 320,
                         "virtual-height", 240,
                         "gravity", 980.0f,
                         "jump-height", 64.0f,
                         NULL);

    return lrg_game_template_run(LRG_GAME_TEMPLATE(game), argc, argv);
}
```

### Memory Management

```c
/* GObjects: use g_object_unref or g_autoptr */
g_autoptr(LrgEngine) engine = lrg_engine_get_default();

/* GBoxed types from graylib: use *_free(), NOT g_object_unref() */
g_autoptr(GrlColor) color = grl_color_new(255, 100, 100, 255);

/* WRONG - segfault! GrlColor is GBoxed, not GObject */
/* g_object_unref(color); */
```

### Transfer Semantics

```c
/* (transfer full) means the callee takes ownership - do NOT unref */
LrgGameState *state = g_object_new(MY_TYPE_STATE, NULL);
lrg_game_state_manager_push(manager, state);
/* Do NOT call g_object_unref(state) here */
```

## Key Engine Modules

| Module | Purpose |
|--------|---------|
| `core/` | Engine, Registry, DataLoader, AssetManager, AssetPack |
| `ecs/` | World, GameObject, Component + Transform/Sprite/Collider |
| `graphics/` | Window, Camera (7 types), Renderer, Drawable |
| `input/` | Keyboard, Mouse, Gamepad, InputMap/Action/Binding |
| `audio/` | AudioManager, Sound, Music, ProceduralAudio |
| `ui/` | 8 widgets, 3 layouts, Theme, Canvas |
| `tilemap/` | Tileset, TilemapLayer, Tilemap |
| `dialog/` | DialogNode, DialogTree, DialogRunner |
| `quest/` | QuestDef, QuestObjective, QuestInstance, QuestLog |
| `inventory/` | ItemDef, ItemStack, Inventory, Equipment |
| `save/` | SaveManager, SaveGame, Saveable interface |
| `ai/` | BehaviorTree, Blackboard, BTNode hierarchy |
| `pathfinding/` | NavGrid, Pathfinder (A*) |
| `physics/` | PhysicsWorld, RigidBody, Collision |
| `gamestate/` | GameState, GameStateManager, MainMenu, PauseMenu |
| `template/` | Game templates (Platformer, FPS, TopDown, Tycoon, etc.) |

## Game Templates Available

| Template | Genre |
|----------|-------|
| `LrgPlatformerTemplate` | 2D platformer (gravity, jump, coyote time) |
| `LrgTopDownTemplate` | Top-down RPG/adventure (4/8-way movement) |
| `LrgShooter2DTemplate` | 2D shooter (projectiles, health, waves) |
| `LrgTwinStickTemplate` | Twin-stick shooter (dual analog) |
| `LrgShmupTemplate` | Scrolling shoot-em-up |
| `LrgTycoonTemplate` | Tycoon/management (grid building) |
| `LrgRacing2DTemplate` | Top-down racing |
| `LrgFPSTemplate` | First-person shooter (WASD + mouse) |
| `LrgThirdPersonTemplate` | Third-person action (orbit camera) |
| `LrgRacing3DTemplate` | 3D racing |
| `LrgDeckbuilderCombatTemplate` | Slay the Spire-style deckbuilder |
| `LrgDeckbuilderPokerTemplate` | Balatro-style poker deckbuilder |
| `LrgIdleTemplate` | Idle/incremental game |

## Testing

Tests use GLib testing framework (GTest):

```c
#include <glib.h>
#include <libregnum.h>

static void
test_example(void)
{
    g_assert_cmpint(1 + 1, ==, 2);
}

int
main(int argc, char *argv[])
{
    g_test_init(&argc, &argv, NULL);
    g_test_add_func("/example/basic", test_example);
    return g_test_run();
}
```

## Dependencies

### Required (Fedora packages)

```
gcc make pkgconf-pkg-config
glib2-devel json-glib-devel
libdex-devel libyaml-devel libsoup3-devel
gobject-introspection-devel
mesa-libGL-devel libX11-devel
```

### Submodule

```bash
git submodule update --init --recursive
```

## Files to Modify When Starting a New Game

1. `config.mk` - Set `GAME_NAME` and `VERSION`
2. `src/main.c` - Your game entry point
3. `Makefile` - Add source files to `GAME_SRCS`
4. `README.md` - Update project description

## Detailed Engine Reference

For full API documentation including all GObject types, interfaces, derivable
hierarchies, singleton managers, and code examples, see:

```
deps/libregnum/CLAUDE.md
```
