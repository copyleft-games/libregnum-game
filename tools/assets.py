#!/usr/bin/env python3
"""Pinned asset intake. Python 3 standard library only; see docs/assets.org."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

LIMIT = 256 * 1024 * 1024
LICENSES = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    if not isinstance(value, str) or not value or "\\" in value or any(ord(c) < 32 for c in value):
        raise ValueError("expected a nonempty POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ("", ".", "..") for p in value.split("/")) or ":" in value:
        raise ValueError(f"unsafe path: {value}")
    return value


def https(value):
    if not isinstance(value, str):
        raise ValueError("expected HTTPS URL")
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"expected public HTTPS URL without credentials: {value}")


def checksum(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("expected lowercase SHA-256")


def read_manifest(root):
    data = json.loads((root / "data/assets/manifest.json").read_text())
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != 1 or not isinstance(data.get("packs"), list):
        raise ValueError("expected manifest version 1 and packs array")
    ids = set()
    for pack in data["packs"]:
        if not isinstance(pack, dict):
            raise ValueError("expected pack object")
        name = pack["id"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in ids:
            raise ValueError(f"invalid or duplicate pack id: {name}")
        ids.add(name)
        if pack["license"] not in LICENSES:
            raise ValueError("intake supports CC0 and CC-BY 3.0/4.0; review other licenses separately")
        for field in ("author", "attribution", "license_text", "changes"):
            if not isinstance(pack[field], str) or not pack[field].strip():
                raise ValueError(f"{name}: missing {field}")
        for field in ("source_url", "license_url", "download_url"):
            https(pack[field])
        checksum(pack["sha256"])
        if pack["format"] not in ("zip", "file") or not isinstance(pack["files"], list) or not pack["files"]:
            raise ValueError(f"{name}: expected zip/file and nonempty files")
        if pack["format"] == "file" and len(pack["files"]) != 1:
            raise ValueError("a direct file pack must have exactly one file")
        paths = {"LICENSE.txt", "provenance.json"}
        for entry in pack["files"]:
            if not isinstance(entry, dict):
                raise ValueError("expected file object")
            relative(entry["source"])
            path = relative(entry["path"])
            folded = path.casefold()
            if any(folded == p.casefold() or folded.startswith(p.casefold() + "/") or p.casefold().startswith(folded + "/") for p in paths):
                raise ValueError(f"{name}: conflicting output path {path}")
            paths.add(path)
            checksum(entry["sha256"])
    return data


def destination(root, name):
    base = root / "data/assets"
    target = base / name
    if base.is_symlink() or (root / "data").is_symlink() or target.is_symlink():
        raise ValueError("asset destination must not be a symlink")
    return target


def verify_pack(root, pack):
    target = destination(root, pack["id"])
    expected = {entry["path"]: entry["sha256"] for entry in pack["files"]}
    expected["LICENSE.txt"] = digest((pack["license_text"] + "\n").encode())
    expected["provenance.json"] = digest((json.dumps(pack, indent=2, sort_keys=True) + "\n").encode())
    actual = set()
    for path in target.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symlink in installed pack: {path}")
        if path.is_file():
            actual.add(path.relative_to(target).as_posix())
    if actual != set(expected):
        raise ValueError(f"{pack['id']}: missing or unexpected files")
    for name, sha in expected.items():
        if digest((target / name).read_bytes()) != sha:
            raise ValueError(f"{pack['id']}: checksum mismatch for {name}")


class HTTPSOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        https(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    https(url)
    request = urllib.request.Request(url, headers={"User-Agent": "libregnum-game-assets/1"})
    with urllib.request.build_opener(HTTPSOnly()).open(request, timeout=60) as response:
        https(response.geturl())
        data = response.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("download exceeds 256 MiB; split the pack or use a smaller export")
    return data


def fetch_pack(root, pack, local=None):
    target = destination(root, pack["id"])
    if target.exists():
        verify_pack(root, pack)
        return
    if local is not None:
        with Path(local).open("rb") as stream:
            data = stream.read(LIMIT + 1)
    else:
        data = download(pack["download_url"])
    if len(data) > LIMIT or digest(data) != pack["sha256"]:
        raise ValueError(f"{pack['id']}: download size or checksum mismatch")
    archive = zipfile.ZipFile(io.BytesIO(data)) if pack["format"] == "zip" else None
    try:
        if archive:
            names = set()
            size = 0
            for info in archive.infolist():
                relative(info.filename.rstrip("/"))
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode) or info.filename in names:
                    raise ValueError("archive contains symlink or duplicate member")
                names.add(info.filename)
                size += info.file_size
            if size > 2 * LIMIT:
                raise ValueError("archive expands beyond 512 MiB")
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".asset-", dir=target.parent) as temp:
            stage = Path(temp) / "pack"
            stage.mkdir()
            for entry in pack["files"]:
                content = archive.read(entry["source"]) if archive else data
                if digest(content) != entry["sha256"]:
                    raise ValueError(f"checksum mismatch for {entry['source']}")
                path = stage / entry["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            (stage / "LICENSE.txt").write_text(pack["license_text"] + "\n")
            (stage / "provenance.json").write_text(json.dumps(pack, indent=2, sort_keys=True) + "\n")
            # rename only a new directory; never replace an installed pack.
            if target.exists() or target.is_symlink():
                raise ValueError(f"destination appeared during import: {target}")
            stage.rename(target)
    finally:
        if archive:
            archive.close()


def credits(manifest):
    lines = ["# Asset credits", "", "Generated from data/assets/manifest.json.", ""]
    for pack in sorted(manifest["packs"], key=lambda item: item["id"]):
        lines.extend([f"## {pack['id']}", "", pack["attribution"], "",
                      f"Author: {pack['author']}", f"Source: {pack['source_url']}",
                      f"License: {pack['license']} ({pack['license_url']})",
                      f"Changes: {pack['changes']}", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("verify")
    sub.add_parser("credits")
    fetch = sub.add_parser("fetch")
    fetch.add_argument("ids", nargs="*")
    fetch.add_argument("--from-file", type=Path, help="use a local pinned download for one named pack")
    args = parser.parse_args()
    try:
        manifest = read_manifest(args.root)
        if args.command == "fetch":
            selected = args.ids or [p["id"] for p in manifest["packs"]]
            if set(selected) - {p["id"] for p in manifest["packs"]}:
                raise ValueError("unknown pack id")
            if args.from_file and len(selected) != 1:
                raise ValueError("--from-file requires one pack")
            for pack in manifest["packs"]:
                if pack["id"] in selected:
                    fetch_pack(args.root, pack, args.from_file)
        elif args.command == "verify":
            for pack in manifest["packs"]:
                verify_pack(args.root, pack)
        elif args.command == "credits":
            sys.stdout.write(credits(manifest))
        else:
            print(f"Validated {len(manifest['packs'])} asset packs")
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print(f"assets: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
