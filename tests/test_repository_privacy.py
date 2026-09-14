import subprocess
import unittest
from pathlib import Path


class RepositoryPrivacyTest(unittest.TestCase):
    def test_tracked_files_do_not_contain_local_private_markers(self):
        root = Path(__file__).resolve().parents[1]
        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True
        ).splitlines()
        forbidden = (
            "/" + "Users/",
            ".chatgpt" + "-projects",
            "个人" + "知识库",
            "file:" + "//",
        )
        violations = []
        for relative in tracked:
            if relative == "tests/test_repository_privacy.py":
                continue
            path = root / relative
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for marker in forbidden:
                if marker in content:
                    violations.append(f"{relative}: {marker}")
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
