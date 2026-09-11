import tempfile
import unittest
from pathlib import Path

from scripts.build_roadbook import build_roadbook
from scripts.guide_utils import load_json


EXAMPLES = (
    "hangzhou-city-3d.json",
    "huangshan-hiking-2d.json",
    "plateau-road-trip-5d.json",
)


class ExampleBuildTest(unittest.TestCase):
    def test_every_mode_builds_a_share_safe_six_file_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            for filename in EXAMPLES:
                with self.subTest(filename=filename):
                    result = build_roadbook(
                        load_json(Path("examples") / filename),
                        Path(directory) / Path(filename).stem,
                        output_scope="share",
                    )
                    self.assertEqual("pass", result["status"], result["report"])
                    self.assertEqual(6, len(result["files"]))
                    combined = "\n".join(
                        Path(path).read_text(encoding="utf-8")
                        for path in result["files"].values()
                    )
                    self.assertNotIn("{{", combined)
                    self.assertNotIn("/" + "Users/", combined)


if __name__ == "__main__":
    unittest.main()
