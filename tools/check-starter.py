#!/usr/bin/env python3
"""Validate skills, role docs, linked resources and generated credits."""
import argparse
from pathlib import Path
import sys
import assets
from starter_validation import AGENT_SECTIONS, bundle_errors, check_links, section_errors, validate_skill

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT, engine_root=None):
    root = root.resolve()
    errors, skipped = [], 0
    skills = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    agents = sorted((root / ".agents/agents").glob("*/agent.md"))
    if not skills or not agents:
        errors.append("expected populated skill and agent catalogs")
    for path in skills:
        errors.extend(f"{path.relative_to(root)}: {error}" for error in validate_skill(path) + bundle_errors(path.parent))
    for path in agents:
        errors.extend(f"{path.relative_to(root)}: {error}" for error in section_errors(path.read_text(), AGENT_SECTIONS))
        if not path.parent.name.startswith("agent-"):
            errors.append(f"bad agent name: {path}")
    documents = list((root / ".agents").rglob("*.md"))
    documents += [root / "README.md", root / "AGENTS.md"]
    documents += list((root / "docs").glob("*.org"))
    for path in documents:
        found, count = check_links(root, path, engine_root)
        errors.extend(f"{path.relative_to(root)}: {error}" for error in found)
        skipped += count
    manifest = assets.read_manifest(root)
    if (root / "data/assets/CREDITS.md").read_text() != assets.credits(manifest):
        errors.append("stale data/assets/CREDITS.md; regenerate with tools/assets.py credits")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(skills)} skills, {len(agents)} agents, bundle resources, documentation links and credits")
    if skipped:
        print(f"Skipped {skipped} engine links: use --engine-root PATH or initialize deps/libregnum")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-root", type=Path)
    args = parser.parse_args()
    engine = args.engine_root or ROOT / "deps/libregnum"
    if args.engine_root and not (engine / "src/libregnum.h").is_file():
        parser.error("--engine-root must contain src/libregnum.h")
    sys.exit(check(engine_root=engine.resolve() if (engine / "src/libregnum.h").is_file() else None))
