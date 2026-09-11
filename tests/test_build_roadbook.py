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
        guide["privacy"] = {"output_scope": "personal", "sensitive_fields": ["private_note"]}
        guide["private_note"] = "do not publish"
        with tempfile.TemporaryDirectory() as directory:
            result = build_roadbook(guide, Path(directory) / "guide", output_scope="share")
            content = Path(result["files"]["normalized_json"]).read_text(encoding="utf-8")
            self.assertNotIn("do not publish", content)


if __name__ == "__main__":
    unittest.main()
