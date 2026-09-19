#!/usr/bin/env python3
"""Check pinned source evidence. This does not execute the engine or its tests."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate_records(root, engine, manifest):
    errors = []
    if manifest.get("version") != 1 or not manifest.get("records"):
        return ["expected nonempty version-one engine evidence"]
    covered = set()
    for record in manifest["records"]:
        skill, name = record["skill"], record["path"]
        covered.add(skill)
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"unsafe engine path: {name}")
            continue
        path = engine / relative
        if not path.is_file():
            errors.append(f"missing engine source: {name}")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            errors.append(f"source changed; re-audit recipe before updating evidence: {name}")
        for symbol in record["symbols"]:
            if symbol not in data.decode("utf-8"):
                errors.append(f"missing symbol {symbol}: {name}")
        if not (root / ".agents/skills" / skill / "references/engine-recipe.md").is_file():
            errors.append(f"missing recipe for {skill}")
    expected = {p.parent.name for p in (root / ".agents/skills").glob("*/SKILL.md")}
    if covered != expected:
        errors.append("engine evidence must cover exactly the current skill catalog")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-root", type=Path, default=ROOT / "deps/libregnum")
    args = parser.parse_args()
    try:
        manifest = json.loads((ROOT / "docs/engine-contracts.json").read_text())
        tree = subprocess.check_output(["git", "ls-tree", "HEAD", "deps/libregnum"], cwd=ROOT, text=True)
        pinned = tree.split()[2]
        actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.engine_root, text=True).strip()
        if pinned != manifest["engine_commit"] or actual != pinned:
            raise ValueError("engine HEAD, parent gitlink and audited engine_commit must match")
        errors = validate_records(ROOT, args.engine_root, manifest)
        if errors:
            raise ValueError("\n".join(errors))
        print(f"Checked {len(manifest['records'])} source records at {pinned}; no engine tests executed")
        return 0
    except (OSError, ValueError, KeyError, IndexError, subprocess.CalledProcessError) as error:
        print(f"engine-contracts: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
