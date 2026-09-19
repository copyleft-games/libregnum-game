# Game development skills and roles

These resources live with the project so they describe the pinned engine and
its actual build/data conventions. Skills use `SKILL.md` frontmatter; roles
are portable Markdown documents. Agent loading is tool-dependent: explicitly
ask your assistant to read a role file when automatic discovery is unavailable.
No global installation, model choice, or automatic delegation is required.
All project skill names and matching directories start with `libregnum-`
(for example, `libregnum-skill-game-bootstrap`).

| Task | Skill |
|------|-------|
| Start a game and choose its template | [Bootstrap](skills/libregnum-skill-game-bootstrap/SKILL.md) |
| Jumping, level collision, camera | [Platformer](skills/libregnum-skill-game-platformer/SKILL.md) |
| Exploration, NPCs, inventory | [Top-down](skills/libregnum-skill-game-top-down/SKILL.md) |
| Aiming, projectiles, waves | [Shooter](skills/libregnum-skill-game-shooter/SKILL.md) |
| FPS, third-person, 3D racing | [3D game](skills/libregnum-skill-game-3d/SKILL.md) |
| Tycoon, cards, idle, simulation | [Strategy](skills/libregnum-skill-game-strategy/SKILL.md) |
| ECS, input, UI, sound, YAML | [Systems](skills/libregnum-skill-game-systems/SKILL.md) |
| Persistence and verification | [Save/test](skills/libregnum-skill-game-save-test/SKILL.md) |
| Public/free 2D art, UI and audio | [Find 2D assets](skills/libregnum-skill-find-2d-assets/SKILL.md) |
| Public/free models and materials | [Find 3D assets](skills/libregnum-skill-find-3d-assets/SKILL.md) |
| YAML definitions and live reload | [Content](skills/libregnum-skill-game-content/SKILL.md) |
| Music, effects and audio lifetime | [Audio](skills/libregnum-skill-game-audio/SKILL.md) |
| Tracks, laps and vehicle surfaces | [Racing](skills/libregnum-skill-game-racing/SKILL.md) |
| Shared-world sessions, replication and reconnect | [MMO gameplay](skills/libregnum-skill-game-mmo/SKILL.md) |
| Auth, transactional services and recovery | [MMO services](skills/libregnum-skill-game-mmo-services/SKILL.md) |
| Timers, random previews, curves and inspection | [Gameplay utilities](skills/libregnum-skill-gameplay-utilities/SKILL.md) |
| Grid/mesh navigation and route editing | [Navigation](skills/libregnum-skill-game-navigation/SKILL.md) |
| Collision layers and filtered raycasts | [Physics](skills/libregnum-skill-game-physics/SKILL.md) |
| Missing engine behavior and fixes | [Engine extension](skills/libregnum-skill-engine-extension/SKILL.md) |
| Download, validate, credit assets | [Intake](skills/libregnum-skill-import-assets/SKILL.md) |

| Role | Focus |
|------|-------|
| [Game architect](agents/agent-game-architect/agent.md) | Brief, template, first playable |
| [2D gameplay](agents/agent-2d-gameplay/agent.md) | Movement, combat and interactions |
| [3D gameplay](agents/agent-3d-gameplay/agent.md) | Cameras, models and world scale |
| [Simulation designer](agents/agent-simulation-designer/agent.md) | Economy, cards and progression |
| [Asset curator](agents/agent-asset-curator/agent.md) | Source research and reproducible intake |
| [Game verifier](agents/agent-game-verifier/agent.md) | Tests, saves and release checks |

Example: “Read the asset-curator role and find CC0 16x16 dungeon sprites; import
only the tiles we need and regenerate credits.” Run `make starter-check` after
editing this directory to validate frontmatter, required sections and local links.

Every skill includes a linked `references/engine-recipe.md` with inspected APIs,
ownership, defaults and failure cases. Read only the recipe needed for the task.
See [authoring/validation](../docs/skill-structure.org) for bundle layout, checks
and the distinction between source evidence and executed engine tests.
