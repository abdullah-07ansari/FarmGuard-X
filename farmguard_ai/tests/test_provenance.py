import unittest
import tempfile
import json
from pathlib import Path
from farmguard_ai.src.data.provenance import ProvenanceManager, ProvenanceError


class TestProvenance(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manifest_path = Path(self.temp_dir.name) / "provenance_manifest.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_license_approval(self):
        record = ProvenanceManager.verify_and_log(
            dataset_name="TestDataset",
            source_url="https://example.com/data",
            license_name="CC BY 4.0",
            dataset_dir=Path(self.temp_dir.name),
            output_manifest_path=self.manifest_path
        )
        self.assertTrue(self.manifest_path.exists())
        self.assertEqual(record["verification_status"], "APPROVED")

    def test_unapproved_license_raises_error(self):
        with self.assertRaises(ProvenanceError):
            ProvenanceManager.verify_and_log(
                dataset_name="TestDataset",
                source_url="https://example.com/data",
                license_name="Proprietary Non-Commercial Strict",
                dataset_dir=Path(self.temp_dir.name),
                output_manifest_path=self.manifest_path
            )


if __name__ == "__main__":
    unittest.main()
