import unittest
import tempfile
import json
from pathlib import Path
from farmguard_ai.src.data.auditor import DatasetAuditor


class TestAuditor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_path = Path(self.temp_dir.name) / "audit.json"
        self.md_path = Path(self.temp_dir.name) / "audit.md"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_audit_report_generation(self):
        provenance_info = {
            "dataset_name": "TestDataset",
            "source_repository": "https://example.com/repo",
            "license": "CC BY 4.0",
            "license_verified": True
        }
        valid_records = [
            {"class_name": "Potato___healthy"},
            {"class_name": "Tomato___Early_blight"}
        ]
        corrupt_logs = []
        split_records = [
            {"class_name": "Potato___healthy", "group_id": "g1", "split_assignment": "train", "is_exact_duplicate": False},
            {"class_name": "Tomato___Early_blight", "group_id": "g2", "split_assignment": "val", "is_exact_duplicate": False}
        ]
        split_summary = {"total_images": 2, "train_images": 1, "val_images": 1, "test_images": 0}
        leakage_status = {"status": "PASSED_ZERO_LEAKAGE"}

        report = DatasetAuditor.generate_audit_report(
            provenance_info=provenance_info,
            valid_records=valid_records,
            corrupt_logs=corrupt_logs,
            split_records=split_records,
            split_summary=split_summary,
            leakage_status=leakage_status,
            output_json_path=self.json_path,
            output_md_path=self.md_path
        )

        self.assertEqual(report["valid_images_count"], 2)
        self.assertTrue(self.json_path.exists())
        self.assertTrue(self.md_path.exists())


if __name__ == "__main__":
    unittest.main()
