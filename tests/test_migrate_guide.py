import json
import unittest
from pathlib import Path

from scripts.migrate_guide import migrate_to_v2


class MigrateGuideTest(unittest.TestCase):
    def test_v1_guide_becomes_v2_without_mutating_source(self):
        source = {
            "schema_version": "1.0",
            "meta": {"title": "杭州三日", "destination": "杭州", "days": 0},
            "preferences": {"pace": "relaxed", "primary_mode": "city"},
            "days": [],
            "extension": {"keep": True},
        }
        result = migrate_to_v2(source)
        self.assertEqual("2.0", result["schema_version"])
        self.assertEqual("city", result["trip"]["primary_mode"])
        self.assertEqual("personal", result["privacy"]["output_scope"])
        self.assertTrue(result["extension"]["keep"])
        self.assertEqual("1.0", source["schema_version"])

    def test_v2_migration_is_idempotent(self):
        source = {"schema_version": "2.0", "trip": {}, "privacy": {}, "days": []}
        self.assertEqual(source, migrate_to_v2(source))

    def test_unknown_version_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported schema_version"):
            migrate_to_v2({"schema_version": "9.0"})

    def test_schema_declares_mode_conditional_requirements(self):
        schema = json.loads(Path("references/roadbook-schema.json").read_text(encoding="utf-8"))
        encoded = json.dumps(schema)
        for field in ("rest_windows", "rain_alternatives", "elevation", "supplies", "water", "retreat_points", "driving_segments"):
            self.assertIn(field, encoded)
        self.assertIn("allOf", schema)


if __name__ == "__main__":
    unittest.main()
