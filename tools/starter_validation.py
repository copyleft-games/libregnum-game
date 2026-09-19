"""Validation for this repository's deliberately small skill metadata schema."""
import json
from pathlib import Path
import re

SKILL_SECTIONS = ("When to Use", "Prerequisites", "Instructions", "Output Format", "Examples", "Constraints")
AGENT_SECTIONS = ("Capabilities", "Skills", "Tools", "Instructions", "Constraints")


def parse_metadata(text):
    """Parse YAML string scalars: plain, JSON-quoted, single-quoted, > and |.

    Only name/description fields are supported. Reject other YAML constructs
    explicitly instead of accidentally accepting malformed YAML as metadata.
    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("frontmatter must start on line one")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("unterminated frontmatter") from error
    fields = {}
    index = 1
    while index < end:
        line = lines[index]
        match = re.fullmatch(r"(name|description):[ \t]*(.*)", line)
        if not match or match[1] in fields:
            raise ValueError("unknown, duplicate or malformed metadata field")
        key, raw = match.groups()
        index += 1
        if raw in (">", "|"):
            block = []
            while index < end and (lines[index].startswith("  ") or not lines[index]):
                block.append(lines[index][2:] if lines[index] else "")
                index += 1
            if not block or any(not item for item in block):
                raise ValueError("block scalars require nonempty two-space-indented lines")
            value = (" " if raw == ">" else "\n").join(block)
        elif raw.startswith('"'):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as error:
                raise ValueError("invalid quoted scalar") from error
        elif raw.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", raw):
                raise ValueError("invalid single-quoted scalar")
            value = raw[1:-1].replace("''", "'")
        else:
            if (not raw or not raw[0].isalpha() or re.search(r":(?:\s|$)", raw) or " #" in raw
                    or raw.lower() in ("null", "true", "false", "~")
                    or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", raw)):
                raise ValueError("expected a supported YAML string scalar")
            value = raw
        if not isinstance(value, str) or not value.strip():
            raise ValueError("metadata strings must be nonempty")
        fields[key] = value
    if fields.keys() != {"name", "description"}:
        raise ValueError("name and description are required")
    return fields


def section_errors(text, sections):
    errors = []
    for heading in sections:
        match = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not match or not match[1].strip():
            errors.append(f"missing or empty section: {heading}")
    return errors


def validate_skill(path):
    text = path.read_text(encoding="utf-8")
    errors = section_errors(text, SKILL_SECTIONS)
    try:
        metadata = parse_metadata(text)
        if not re.fullmatch(r"libregnum-[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"]):
            errors.append("skill name must use libregnum- and lowercase kebab-case")
        if metadata["name"] != path.parent.name:
            errors.append("skill name must match its directory")
    except ValueError as error:
        errors.append(str(error))
    if "**Input:**" not in text or "**Result:**" not in text:
        errors.append("example must include concrete Input and Result")
    return errors


def local_links(text):
    links = re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text)
    links += re.findall(r"\[\[file:([^\]]+)\]", text)
    return [link.split("#")[0] for link in links if "://" not in link and not link.startswith("#")]


def check_links(root, path, engine_root=None):
    errors, skipped = [], 0
    for link in local_links(path.read_text(encoding="utf-8")):
        target = (path.parent / link).resolve()
        if not target.is_relative_to(root):
            errors.append(f"link escapes repository: {link}")
            continue
        relative = target.relative_to(root)
        if relative.parts[:2] == ("deps", "libregnum"):
            if engine_root is None:
                skipped += 1
                continue
            target = engine_root.joinpath(*relative.parts[2:])
        if not target.is_file():
            errors.append(f"broken file link: {link}")
    return errors, skipped


def bundle_errors(folder):
    """Every bundled reference/template/helper must be reachable from SKILL.md."""
    root = folder.resolve()
    pending = [root / "SKILL.md"]
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        if path.suffix != ".md":
            continue
        for link in local_links(path.read_text(encoding="utf-8")):
            target = (path.parent / link).resolve()
            if target.is_relative_to(root):
                pending.append(target)
    errors = []
    for kind in ("references", "templates", "scripts", "assets"):
        for path in (root / kind).rglob("*"):
            if path.is_file() and path not in seen:
                errors.append(f"unlinked bundle resource: {path.relative_to(root)}")
    return errors
