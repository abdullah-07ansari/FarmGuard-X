import unittest
import tempfile
from pathlib import Path
from PIL import Image
from farmguard_ai.src.data.validator import DataValidator
from farmguard_ai.src.config import Config


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.corrupt_log = Path(self.temp_dir.name) / "corrupt.log"
        self.validator = DataValidator(target_labels=Config.APPROVED_LABELS, min_dim=(224, 224))

        # Create dummy valid image folder & file
        class_folder = self.raw_dir / "Potato___healthy"
        class_folder.mkdir(parents=True, exist_ok=True)

        valid_img_path = class_folder / "valid_leaf.jpg"
        img = Image.new("RGB", (256, 256), color=(0, 255, 0))
        img.save(valid_img_path)

        # Create dummy small image (dimension error)
        small_img_path = class_folder / "small_leaf.jpg"
        img_small = Image.new("RGB", (100, 100), color=(255, 0, 0))
        img_small.save(small_img_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_validation_filtering(self):
        records, corrupt_logs = self.validator.validate_dataset(self.raw_dir, self.corrupt_log)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["class_name"], "Potato___healthy")
        self.assertTrue(any("Dimension Error" in log for log in corrupt_logs))


if __name__ == "__main__":
    unittest.main()
