#!/usr/bin/env python3
"""Check the local starter docs/skill contract without third-party dependencies."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def check():
    errors = []
    skills = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    agents = sorted((ROOT / ".agents/agents").glob("*/agent.md"))
    if not skills or not agents:
        errors.append("expected populated skill and agent catalogs")
    for path in skills:
        text = path.read_text()
        # Deliberately constrain this repo to YAML's plain single-line scalar subset.
        match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", text)
        if not match or match[1] != path.parent.name or not match[2].strip():
            errors.append(f"invalid skill metadata: {path.relative_to(ROOT)}")
        elif ": " in match[2] or " #" in match[2] or match[2][0] in "[]{}&*!|>'\"%@`":
            errors.append(f"description must use the supported plain YAML scalar subset: {path}")
        for heading in ("When to Use", "Prerequisites", "Instructions", "Output Format", "Examples", "Constraints"):
            if f"## {heading}\n" not in text:
                errors.append(f"missing {heading}: {path}")
    for path in agents:
        text = path.read_text()
        if not path.parent.name.startswith("agent-"):
            errors.append(f"bad agent name: {path}")
        for heading in ("Capabilities", "Skills", "Tools", "Instructions", "Constraints"):
            if f"## {heading}\n" not in text:
                errors.append(f"missing {heading}: {path}")
    documents = skills + agents + [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / ".agents/README.md"]
    documents += list((ROOT / "docs").glob("*.org"))
    for path in documents:
        text = path.read_text()
        links = re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text)
        links += re.findall(r"\[\[file:([^\]]+)\]", text)
        for link in links:
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            if not target.exists():
                errors.append(f"broken link {link}: {path.relative_to(ROOT)}")
    sys.path.insert(0, str(ROOT / "tools"))
    import assets
    manifest = assets.read_manifest(ROOT)
    if (ROOT / "data/assets/CREDITS.md").read_text() != assets.credits(manifest):
        errors.append("stale data/assets/CREDITS.md; regenerate with tools/assets.py credits")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {len(skills)} skills, {len(agents)} agents, documentation links and credits")
    return 0


if __name__ == "__main__":
    sys.exit(check())
