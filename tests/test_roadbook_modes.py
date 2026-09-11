import unittest

from scripts.roadbook_modes import apply_personalization, policy_for, select_mode


class RoadbookModesTest(unittest.TestCase):
    def test_explicit_mode_wins(self):
        result = select_mode({"primary_mode": "hiking", "destination": "杭州"})
        self.assertEqual("hiking", result["primary_mode"])
        self.assertEqual(1.0, result["confidence"])

    def test_keywords_infer_mixed_mode(self):
        result = select_mode({"style": "城市慢游加一天徒步"})
        self.assertEqual("hiking", result["primary_mode"])
        self.assertIn("city", result["secondary_modes"])

    def test_relaxed_city_policy_caps_core_experiences(self):
        policy = policy_for("city", {"pace": "relaxed"})
        self.assertEqual(3, policy["max_core_experiences_per_day"])
        self.assertTrue(policy["prefer_single_hotel"])

    def test_hiking_and_driving_have_safety_requirements(self):
        self.assertIn("retreat_points", policy_for("hiking", {})["required_sections"])
        self.assertEqual(6, policy_for("road_trip", {})["max_net_driving_hours"])

    def test_personalization_records_rules_without_overriding_request(self):
        roadbook = {"personalization": {"applied_rules": []}, "preferences": {}}
        profile = {"positive_signals": ["nature.forest"], "negative_signals": [], "rules": ["prefer_single_hotel"]}
        result = apply_personalization(roadbook, profile, {"pace": "intensive"})
        self.assertEqual("intensive", result["personalization"]["pace"])
        self.assertIn("prefer_single_hotel", result["personalization"]["applied_rules"])


if __name__ == "__main__":
    unittest.main()
