import unittest
import tempfile
from pathlib import Path
from PIL import Image
from farmguard_ai.src.data.deduplicator import Deduplicator


class TestDeduplicator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.img1_path = Path(self.temp_dir.name) / "img1.jpg"
        self.img2_path = Path(self.temp_dir.name) / "img2.jpg"

        # Create identical images
        img = Image.new("RGB", (224, 224), color=(100, 150, 200))
        img.save(self.img1_path)
        img.save(self.img2_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_md5_exact_duplicate(self):
        md5_1 = Deduplicator.compute_md5(self.img1_path)
        md5_2 = Deduplicator.compute_md5(self.img2_path)
        self.assertEqual(md5_1, md5_2)

    def test_dhash_computation(self):
        dhash1 = Deduplicator.compute_dhash(self.img1_path)
        dhash2 = Deduplicator.compute_dhash(self.img2_path)
        dist = Deduplicator.hamming_distance(dhash1, dhash2)
        self.assertEqual(dist, 0)


if __name__ == "__main__":
    unittest.main()
