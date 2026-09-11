import unittest

from scripts.guide_utils import load_json
from scripts.render_roadbook import render_roadbook


class FrontendContractTest(unittest.TestCase):
    def setUp(self):
        self.html = render_roadbook(load_json("tests/fixtures/v2-city-minimal.json"))

    def test_exposes_accessible_planning_controls(self):
        for marker in (
            'class="day-nav"', 'class="item-check"', 'class="budget-input"',
            'class="packing-check"', 'data-action="shift-day"',
            'data-action="toggle-details"', 'data-action="print"', 'aria-live="polite"',
        ):
            self.assertIn(marker, self.html)

    def test_interaction_runtime_is_embedded(self):
        self.assertIn("travel-roadbook:v", self.html)
        self.assertIn("localStorage", self.html)
        self.assertIn("recalculateBudget", self.html)


if __name__ == "__main__":
    unittest.main()
