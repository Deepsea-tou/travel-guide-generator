import json
import tempfile
import unittest
from pathlib import Path

from scripts.extract_local_profile import empty_profile, extract_profile


class ExtractLocalProfileTest(unittest.TestCase):
    def test_extracts_allowlisted_signals_without_raw_content_or_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = "喜欢森林、湖泊、慢行和建筑，不喜欢排队与频繁搬酒店"
            (root / "旅行偏好模型.md").write_text(raw, encoding="utf-8")
            (root / "私人日记.md").write_text("求婚秘密", encoding="utf-8")
            result = extract_profile(root)
            encoded = json.dumps(result, ensure_ascii=False)
            self.assertIn("nature.forest", result["positive_signals"])
            self.assertIn("friction.queues", result["negative_signals"])
            self.assertNotIn(raw, encoded)
            self.assertNotIn(str(root), encoded)
            self.assertNotIn("求婚秘密", encoded)

    def test_missing_and_empty_allowlisted_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "装备体系.md").write_text("", encoding="utf-8")
            result = extract_profile(root)
            self.assertEqual(empty_profile(), result)

    def test_non_directory_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "existing directory"):
            extract_profile("/path/that/does/not/exist")


if __name__ == "__main__":
    unittest.main()
