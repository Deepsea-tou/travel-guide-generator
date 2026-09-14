import tempfile
import unittest
from pathlib import Path

from scripts.export_roadbook import export_roadbook_bundle
from scripts.guide_utils import load_json


class ExportRoadbookTest(unittest.TestCase):
    def setUp(self):
        self.fixture = load_json("tests/fixtures/v2-city-minimal.json")

    def test_direct_export_rejects_invalid_mode_payload(self):
        guide = dict(self.fixture)
        guide["trip"] = {**guide["trip"], "primary_mode": "hiking"}
        guide["quality"] = {"valid": True, "status": "pass"}
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "validation"):
                export_roadbook_bundle(guide, Path(directory) / "guide")

    def test_direct_share_export_rejects_unsanitized_payload(self):
        guide = dict(self.fixture)
        guide["privacy"] = {
            "output_scope": "share",
            "private_paths": [],
            "sensitive_fields": ["private_note"],
        }
        guide["private_note"] = "do not publish"
        guide["quality"] = {"valid": True, "status": "pass"}
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "sanitized"):
                export_roadbook_bundle(guide, Path(directory) / "guide")


if __name__ == "__main__":
    unittest.main()
