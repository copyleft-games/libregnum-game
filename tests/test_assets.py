"""Hermetic asset intake regressions: no internet or graphics context."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SPEC = importlib.util.spec_from_file_location("assets", Path(__file__).resolve().parents[1] / "tools/assets.py")
assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assets)


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "data/assets").mkdir(parents=True)
        self.content = b"a tiny test texture"
        self.payload = self.zip({"art/tile.png": self.content})
        self.pack = {
            "id": "test-pack", "author": "Fixture Artist", "attribution": "Tile by Fixture Artist",
            "license": "CC0-1.0", "license_text": "Fixture license evidence", "changes": "None",
            "source_url": "https://example.org/tile", "license_url": "https://example.org/license",
            "download_url": "https://example.org/tile.zip", "format": "zip",
            "sha256": assets.digest(self.payload),
            "files": [{"source": "art/tile.png", "path": "textures/tile.png", "sha256": assets.digest(self.content)}]
        }
        self.write_manifest()

    def zip(self, files):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        return buffer.getvalue()

    def write_manifest(self):
        (self.root / "data/assets/manifest.json").write_text(json.dumps({"version": 1, "packs": [self.pack]}))

    def fetch(self):
        with patch.object(assets, "download", return_value=self.payload):
            assets.fetch_pack(self.root, assets.read_manifest(self.root)["packs"][0])

    def test_fetch_verify_idempotence_and_credits(self):
        self.fetch()
        assets.verify_pack(self.root, self.pack)
        with patch.object(assets, "download", side_effect=AssertionError("must not redownload")):
            assets.fetch_pack(self.root, self.pack)
        self.assertIn("Fixture Artist", assets.credits(assets.read_manifest(self.root)))

    def test_tamper_is_preserved_and_rejected(self):
        self.fetch()
        path = self.root / "data/assets/test-pack/textures/tile.png"
        path.write_bytes(b"user edits")
        with self.assertRaises(ValueError):
            self.fetch()
        self.assertEqual(path.read_bytes(), b"user edits")

    def test_bad_download_is_atomic(self):
        self.payload = b"bad download"
        with self.assertRaises(ValueError):
            self.fetch()
        self.assertFalse((self.root / "data/assets/test-pack").exists())

    def test_bad_member_hash_is_atomic(self):
        self.pack["files"][0]["sha256"] = "0" * 64
        self.write_manifest()
        with self.assertRaises(ValueError):
            self.fetch()
        self.assertFalse((self.root / "data/assets/test-pack").exists())

    def test_traversal_even_in_unselected_member(self):
        self.payload = self.zip({"../escape": b"bad", "art/tile.png": self.content})
        self.pack["sha256"] = assets.digest(self.payload)
        self.write_manifest()
        with self.assertRaises(ValueError):
            self.fetch()
        self.assertFalse((self.root / "data/escape").exists())

    def test_invalid_manifest_fields(self):
        original = copy.deepcopy(self.pack)
        for field, value in (("id", "../bad"), ("license", "free"), ("author", ""),
                             ("sha256", "bad"), ("download_url", "http://example.org/tile"),
                             ("download_url", "https://user:secret@example.org/tile")):
            with self.subTest(field=field, value=value):
                self.pack = dict(original, **{field: value})
                self.write_manifest()
                with self.assertRaises(ValueError):
                    assets.read_manifest(self.root)

    def test_bad_output_paths(self):
        for value in ("/tmp/file", "../file", "a/../file", "a\\b", "C:/file", "a//b", "LICENSE.txt", "provenance.json/x"):
            with self.subTest(value=value):
                self.pack["files"][0]["path"] = value
                self.write_manifest()
                with self.assertRaises(ValueError):
                    assets.read_manifest(self.root)

    def test_duplicate_ids(self):
        (self.root / "data/assets/manifest.json").write_text(json.dumps({"version": 1, "packs": [self.pack, self.pack]}))
        with self.assertRaises(ValueError):
            assets.read_manifest(self.root)

    def test_symlink_destination(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "data/assets/test-pack").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.fetch()
        self.assertEqual(list(outside.iterdir()), [])

    def test_symlink_archive(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = 0o120777 << 16
            archive.writestr(info, "../outside")
        self.payload = buffer.getvalue()
        self.pack["sha256"] = assets.digest(self.payload)
        self.write_manifest()
        with self.assertRaises(ValueError):
            self.fetch()

    def test_local_direct_file(self):
        self.pack.update(format="file", sha256=assets.digest(self.content))
        self.write_manifest()
        download = self.root / "download.png"
        download.write_bytes(self.content)
        assets.fetch_pack(self.root, assets.read_manifest(self.root)["packs"][0], download)
        assets.verify_pack(self.root, self.pack)

    def test_missing_and_extra_files(self):
        with self.assertRaises(ValueError):
            assets.verify_pack(self.root, self.pack)
        self.fetch()
        (self.root / "data/assets/test-pack/extra").write_text("untracked content")
        with self.assertRaises(ValueError):
            assets.verify_pack(self.root, self.pack)

    def test_size_limit(self):
        with patch.object(assets, "LIMIT", 1):
            with self.assertRaises(ValueError):
                self.fetch()

    def test_manifest_shape(self):
        for value in ([], None, {"version": True, "packs": []}, {"version": 1, "packs": [None]}):
            with self.subTest(value=value):
                (self.root / "data/assets/manifest.json").write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    assets.read_manifest(self.root)

    def test_output_prefix_collision(self):
        self.pack["files"].append({"source": "b", "path": "Textures", "sha256": "0" * 64})
        self.write_manifest()
        with self.assertRaises(ValueError):
            assets.read_manifest(self.root)

    def test_nested_model_sidecars(self):
        self.payload = self.zip({"scene/model.gltf": b"model", "scene/Textures/color.png": b"texture"})
        self.pack["sha256"] = assets.digest(self.payload)
        self.pack["files"] = [
            {"source": "scene/model.gltf", "path": "models/model.gltf", "sha256": assets.digest(b"model")},
            {"source": "scene/Textures/color.png", "path": "models/Textures/color.png", "sha256": assets.digest(b"texture")}
        ]
        self.write_manifest()
        self.fetch()
        assets.verify_pack(self.root, self.pack)
        self.assertEqual((self.root / "data/assets/test-pack/models/Textures/color.png").read_bytes(), b"texture")

    def test_missing_archive_member(self):
        self.pack["files"][0]["source"] = "missing.png"
        self.write_manifest()
        with self.assertRaises(KeyError):
            self.fetch()
        self.assertFalse((self.root / "data/assets/test-pack").exists())

    def test_insecure_redirect_rejected(self):
        with self.assertRaises(ValueError):
            assets.HTTPSOnly().redirect_request(None, None, 302, "", {}, "http://example.org/tile")


if __name__ == "__main__":
    unittest.main()
