import tempfile
import unittest
from pathlib import Path

from scripts.build_roadbook import build_roadbook
from scripts.guide_utils import load_json


class BuildRoadbookTest(unittest.TestCase):
    def setUp(self):
        self.fixture = load_json("tests/fixtures/v2-city-minimal.json")

    def test_builds_six_personal_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build_roadbook(self.fixture, Path(directory) / "guide")
            self.assertEqual("pass", result["status"])
            self.assertEqual(
                {"normalized_json", "quality_json", "html", "markdown", "ics", "geojson"},
                set(result["files"]),
            )
            for path in result["files"].values():
                self.assertTrue(Path(path).exists(), path)

    def test_share_build_removes_sensitive_field(self):
        guide = dict(self.fixture)
        guide["privacy"] = {
            "output_scope": "personal",
            "private_paths": [],
            "sensitive_fields": ["private_note"],
        }
        guide["private_note"] = "do not publish"
        with tempfile.TemporaryDirectory() as directory:
            result = build_roadbook(guide, Path(directory) / "guide", output_scope="share")
            self.assertEqual("pass", result["status"])
            content = Path(result["files"]["normalized_json"]).read_text(encoding="utf-8")
            self.assertNotIn("do not publish", content)

    def test_share_checks_run_before_export(self):
        guide = dict(self.fixture)
        guide["privacy"] = {
            "output_scope": "personal",
            "private_paths": [],
            "sensitive_fields": [],
        }
        guide["images"] = [{"src": "cover.jpg", "metadata_checked": False}]
        with tempfile.TemporaryDirectory() as directory:
            result = build_roadbook(guide, Path(directory) / "guide", output_scope="share")
            self.assertEqual("fail", result["status"])
            self.assertEqual({}, result["files"])
            self.assertTrue(any(error["code"] == "privacy.image_metadata.unchecked" for error in result["report"]["errors"]))

    def test_invalid_roadbook_stops_export(self):
        guide = dict(self.fixture)
        guide["trip"] = {**guide["trip"], "primary_mode": "hiking"}
        with tempfile.TemporaryDirectory() as directory:
            result = build_roadbook(guide, Path(directory) / "guide")
            self.assertEqual("fail", result["status"])
            self.assertEqual({}, result["files"])


if __name__ == "__main__":
    unittest.main()
