import json
import unittest

from scripts.sanitize_share_version import PrivacyError, sanitize_for_share


class SanitizeShareVersionTest(unittest.TestCase):
    def test_removes_private_nested_fields_and_local_provenance(self):
        local_path = "/" + "Users/example/knowledge"
        source = {
            "privacy": {"output_scope": "personal", "sensitive_fields": ["companion_name"]},
            "companion_name": "Private Person",
            "notes": [{"privacy": "private", "text": "Private Event"}, {"privacy": "share", "text": "Bring water"}],
            "profile": {"source_path": local_path, "signals": ["nature.forest"]},
            "days": [],
        }
        shared = sanitize_for_share(source)
        encoded = json.dumps(shared, ensure_ascii=False)
        for marker in ("Private Person", "Private Event", local_path, "source_path"):
            self.assertNotIn(marker, encoded)
        self.assertIn("Bring water", encoded)
        self.assertEqual("share", shared["privacy"]["output_scope"])

    def test_rejects_unclassified_local_path_in_value(self):
        local_path = "/" + "Users/example/secret.txt"
        with self.assertRaises(PrivacyError):
            sanitize_for_share({"privacy": {"sensitive_fields": []}, "description": local_path})


if __name__ == "__main__":
    unittest.main()
