import unittest

from scripts.guide_utils import load_json
from scripts.render_roadbook import render_roadbook


class RenderRoadbookTest(unittest.TestCase):
    def test_contains_core_sections_and_embedded_data(self):
        html = render_roadbook(load_json("tests/fixtures/v2-city-minimal.json"))
        for marker in (
            'data-section="overview"', 'data-section="route"',
            'data-section="daily-plan"', 'data-section="food-stay"',
            'data-section="budget"', 'id="roadbook-data"',
        ):
            self.assertIn(marker, html)
        self.assertNotIn("{{", html)
        self.assertIn('data-theme="lake-city"', html)

    def test_escapes_user_content_and_embedded_json(self):
        guide = load_json("tests/fixtures/v2-city-minimal.json")
        guide["meta"]["title"] = '<script>alert("x")</script>'
        guide["notes"] = ["</script><script>alert(1)</script>"]
        html = render_roadbook(guide)
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertNotIn("</script><script>alert(1)</script>", html)

    def test_has_no_remote_runtime_dependency(self):
        html = render_roadbook(load_json("tests/fixtures/v2-city-minimal.json"))
        self.assertNotIn('<link rel="stylesheet" href="http', html)
        self.assertNotIn('<script src="http', html)


if __name__ == "__main__":
    unittest.main()
