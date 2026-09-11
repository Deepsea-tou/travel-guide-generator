import copy
import unittest
from datetime import date

from scripts.guide_utils import load_json
from scripts.validate_roadbook import validate_roadbook


def fixture():
    return load_json("tests/fixtures/v2-city-minimal.json")


def codes(report, collection):
    return {item["code"] for item in report[collection]}


class ValidateRoadbookTest(unittest.TestCase):
    def test_minimal_city_roadbook_passes(self):
        self.assertTrue(validate_roadbook(fixture())["valid"])

    def test_dynamic_source_without_verification_is_an_error(self):
        guide = fixture()
        guide["sources"] = [{"id": "weather", "title": "天气", "dynamic": True}]
        report = validate_roadbook(guide)
        self.assertIn("source.verification.missing", codes(report, "errors"))

    def test_old_dynamic_source_is_stale(self):
        guide = fixture()
        guide["sources"] = [{"id": "weather", "title": "天气", "dynamic": True, "verified_at": "2025-01-01"}]
        report = validate_roadbook(guide, today=date(2026, 9, 11))
        self.assertIn("source.stale", codes(report, "warnings"))

    def test_hiking_day_requires_retreat_and_stop_conditions(self):
        guide = fixture()
        guide["trip"]["primary_mode"] = "hiking"
        report = validate_roadbook(guide)
        self.assertIn("hiking.retreat_points.missing", codes(report, "errors"))
        self.assertIn("hiking.stop_conditions.missing", codes(report, "errors"))

    def test_excessive_driving_warns(self):
        guide = fixture()
        guide["trip"]["primary_mode"] = "road_trip"
        guide["days"][0].update({
            "driving_segments": [{"duration_min": 420}], "fuel_or_charge": ["服务区"],
            "parking": ["酒店"], "stop_conditions": [{"trigger": "封路", "action": "绕行"}],
        })
        report = validate_roadbook(guide)
        self.assertIn("road_trip.driving.excessive", codes(report, "warnings"))


if __name__ == "__main__":
    unittest.main()
