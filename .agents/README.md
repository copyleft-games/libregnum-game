# Game development skills and roles

These resources live with the project so they describe the pinned engine and
its actual build/data conventions. Skills use `SKILL.md` frontmatter; roles
are portable Markdown documents. Agent loading is tool-dependent: explicitly
ask your assistant to read a role file when automatic discovery is unavailable.
No global installation, model choice, or automatic delegation is required.

| Task | Skill |
|------|-------|
| Start a game and choose its template | [Bootstrap](skills/skill-game-bootstrap/SKILL.md) |
| Jumping, level collision, camera | [Platformer](skills/skill-game-platformer/SKILL.md) |
| Exploration, NPCs, inventory | [Top-down](skills/skill-game-top-down/SKILL.md) |
| Aiming, projectiles, waves | [Shooter](skills/skill-game-shooter/SKILL.md) |
| FPS, third-person, 3D racing | [3D game](skills/skill-game-3d/SKILL.md) |
| Tycoon, cards, idle, simulation | [Strategy](skills/skill-game-strategy/SKILL.md) |
| ECS, input, UI, sound, YAML | [Systems](skills/skill-game-systems/SKILL.md) |
| Persistence and verification | [Save/test](skills/skill-game-save-test/SKILL.md) |
| Public/free 2D art, UI and audio | [Find 2D assets](skills/skill-find-2d-assets/SKILL.md) |
| Public/free models and materials | [Find 3D assets](skills/skill-find-3d-assets/SKILL.md) |
| Download, validate, credit assets | [Intake](skills/skill-import-assets/SKILL.md) |

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
