import unittest

from scripts.export_guide import ics_text


class ExportGuideTest(unittest.TestCase):
    def test_ics_rejects_timezone_line_injection(self):
        guide = {
            "meta": {"timezone": "Asia/Shanghai\r\nX-INJECTED:1", "destination": "test"},
            "days": [{"date": "2026-10-01", "items": [{"name": "A", "start": "09:00", "end": "10:00"}]}],
        }
        with self.assertRaisesRegex(ValueError, "timezone"):
            ics_text(guide)


if __name__ == "__main__":
    unittest.main()
