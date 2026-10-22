import tempfile
import unittest
from pathlib import Path

import tidysloth


class TidySlothTests(unittest.TestCase):
    def test_categorize_file(self):
        self.assertEqual(tidysloth.categorize_file(Path("hello.py")), "Code")
        self.assertEqual(tidysloth.categorize_file(Path("paper.pdf")), "Documents")
        self.assertEqual(tidysloth.categorize_file(Path("photo.png")), "Images")
        self.assertEqual(tidysloth.categorize_file(Path("bundle.zip")), "Archives")
        self.assertEqual(tidysloth.categorize_file(Path("blob.bin")), "Others")

    def test_tidy_dry_run_does_not_move_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "example.py"
            sample.write_text("print('ok')", encoding="utf-8")

            result = tidysloth.tidy_command(root, dry_run=True)

            self.assertEqual(result, 0)
            self.assertTrue(sample.exists())
            self.assertFalse((root / "Code" / "example.py").exists())
            self.assertTrue((root / tidysloth.INDEX_FILENAME).exists())

    def test_tidy_moves_file_into_category_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "notes.txt"
            sample.write_text("hello", encoding="utf-8")

            result = tidysloth.tidy_command(root, dry_run=False)

            self.assertEqual(result, 0)
            self.assertFalse(sample.exists())
            self.assertTrue((root / "Documents" / "notes.txt").exists())
            self.assertTrue((root / tidysloth.INDEX_FILENAME).exists())


if __name__ == "__main__":
    unittest.main()
