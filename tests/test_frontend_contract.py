import unittest
from pathlib import Path

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

    def test_browser_smoke_has_cross_platform_chromium_fallback(self):
        smoke = Path("tests/browser/roadbook-smoke.cjs").read_text(encoding="utf-8")
        self.assertIn("fs.existsSync(defaultChrome)", smoke)
        self.assertIn("process.env.CHROME_PATH", smoke)
        self.assertIn("chromium.launch(launchOptions)", smoke)


if __name__ == "__main__":
    unittest.main()
