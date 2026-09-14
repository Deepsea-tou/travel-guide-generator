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
        self.assertEqual([], shared["privacy"]["private_paths"])

    def test_rejects_unclassified_local_path_in_value(self):
        local_path = "/" + "Users/example/secret.txt"
        with self.assertRaises(PrivacyError):
            sanitize_for_share({"privacy": {"sensitive_fields": []}, "description": local_path})

    def test_rejects_other_unix_absolute_paths(self):
        local_path = "/private/tmp/secret.txt"
        with self.assertRaisesRegex(PrivacyError, "local path"):
            sanitize_for_share({"privacy": {"sensitive_fields": []}, "description": local_path})

    def test_rejects_windows_file_urls_and_path_keys(self):
        cases = (
            {"description": r"C:\Users\alice\secret.txt"},
            {"description": "C:/Users/alice/secret.txt"},
            {"description": "FILE:///private/tmp/secret.txt"},
            {"metadata": {"/private/tmp/secret.txt": "private"}},
        )
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaisesRegex(PrivacyError, "local path"):
                sanitize_for_share({"privacy": {"sensitive_fields": []}, **payload})

    def test_rejects_sensitive_value_copied_under_another_key(self):
        source = {
            "privacy": {"sensitive_fields": ["companion_name"]},
            "profile": {"companion_name": "Private Person"},
            "description": "Private Person prefers a quiet room",
        }
        with self.assertRaisesRegex(PrivacyError, "sensitive value"):
            sanitize_for_share(source)


if __name__ == "__main__":
    unittest.main()
