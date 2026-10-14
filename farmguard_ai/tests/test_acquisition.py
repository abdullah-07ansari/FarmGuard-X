import unittest
import tempfile
from pathlib import Path
from farmguard_ai.src.data.acquisition import DatasetAcquisition, AcquisitionError
from farmguard_ai.src.config import Config


class TestAcquisition(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.raw_dir = Path(self.temp_dir.name) / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.acquisitor = DatasetAcquisition(raw_dir=self.raw_dir, target_labels=Config.APPROVED_LABELS)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_class_mapping_verification(self):
        # Create dummy class folders matching target labels
        (self.raw_dir / "Potato___healthy").mkdir(parents=True, exist_ok=True)
        (self.raw_dir / "Tomato___Early_blight").mkdir(parents=True, exist_ok=True)

        mapped_dirs, missing_classes, unexpected = self.acquisitor.verify_and_map_classes(self.raw_dir)
        self.assertIn("Potato___healthy", mapped_dirs)
        self.assertIn("Tomato___Early_blight", mapped_dirs)
        self.assertEqual(len(missing_classes), 6)

    def test_record_provenance(self):
        manifest_path = Path(self.temp_dir.name) / "provenance_manifest.json"
        record = self.acquisitor.record_provenance(manifest_path, mapped_count=8, commit_hash="abc1234")
        self.assertEqual(record["license"], "CC BY 4.0")
        self.assertEqual(record["provenance_status"], "VERIFIED_COMPLIANT")
        self.assertTrue(manifest_path.exists())


if __name__ == "__main__":
    unittest.main()
