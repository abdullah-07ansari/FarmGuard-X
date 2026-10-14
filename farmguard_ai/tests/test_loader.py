import unittest
import tempfile
import csv
from pathlib import Path
from PIL import Image
import tensorflow as tf
from farmguard_ai.src.data.loader import DataLoader, DataLoaderError


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manifest_path = Path(self.temp_dir.name) / "split_manifest.csv"

        # Create dummy image files
        img_dir = Path(self.temp_dir.name) / "imgs"
        img_dir.mkdir(parents=True, exist_ok=True)

        self.img1_path = img_dir / "img1.jpg"
        img = Image.new("RGB", (256, 256), color=(255, 0, 0))
        img.save(self.img1_path)

        # Create split manifest
        fieldnames = ["file_path", "class_id", "split_assignment"]
        rows = [
            {"file_path": str(self.img1_path), "class_id": "2", "split_assignment": "train"},
            {"file_path": str(self.img1_path), "class_id": "5", "split_assignment": "val"}
        ]
        with open(self.manifest_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_manifest_parsing(self):
        paths, ids = DataLoader.parse_manifest_split(self.manifest_path, "train")
        self.assertEqual(len(paths), 1)
        self.assertEqual(ids[0], 2)

    def test_image_preprocessing_shapes_and_normalization(self):
        img_norm, one_hot = DataLoader.preprocess_image_and_label(
            file_path=tf.constant(str(self.img1_path)),
            class_id=tf.constant(2),
            target_size=(224, 224),
            num_classes=8
        )
        self.assertEqual(img_norm.shape, (224, 224, 3))
        self.assertEqual(one_hot.shape, (8,))

        # Check normalization range [-1.0, 1.0]
        min_val = tf.reduce_min(img_norm).numpy()
        max_val = tf.reduce_max(img_norm).numpy()
        self.assertGreaterEqual(min_val, -1.0)
        self.assertLessEqual(max_val, 1.0)


if __name__ == "__main__":
    unittest.main()
