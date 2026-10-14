import unittest
import tempfile
import csv
from pathlib import Path
from farmguard_ai.src.models.class_weights import ClassWeightCalculator, ClassWeightError


class TestClassWeights(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manifest_path = Path(self.temp_dir.name) / "split_manifest.csv"

        # Create dummy split_manifest.csv with known counts:
        # Class 0: 10 train samples
        # Class 1: 20 train samples
        # Classes 2-7: 10 train samples each
        # Total train samples = 90 across 8 classes
        fieldnames = ["file_path", "class_id", "split_assignment"]
        rows = []

        # Class 0 (10)
        for _ in range(10):
            rows.append({"file_path": "/p", "class_id": "0", "split_assignment": "train"})
        # Class 1 (20)
        for _ in range(20):
            rows.append({"file_path": "/p", "class_id": "1", "split_assignment": "train"})
        # Classes 2-7 (10 each)
        for c in range(2, 8):
            for _ in range(10):
                rows.append({"file_path": "/p", "class_id": str(c), "split_assignment": "train"})

        # Add test rows that should NOT be counted
        for _ in range(50):
            rows.append({"file_path": "/p", "class_id": "0", "split_assignment": "test"})

        with open(self.manifest_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_inverse_frequency_weight_calculation(self):
        weights = ClassWeightCalculator.compute_weights_from_manifest(self.manifest_path, num_classes=8)
        self.assertEqual(len(weights), 8)

        # Formula: N / (K * n_i) -> 90 / (8 * 10) = 1.125
        # Class 1: 90 / (8 * 20) = 0.5625
        self.assertAlmostEqual(weights[0], 1.125)
        self.assertAlmostEqual(weights[1], 0.5625)

        # Verify minority class (class 0) has higher weight than majority class (class 1)
        self.assertGreater(weights[0], weights[1])

    def test_population_consistency_verification(self):
        counts = ClassWeightCalculator.verify_training_population_consistency(self.manifest_path, num_classes=8)
        self.assertEqual(counts[0], 10)
        self.assertEqual(counts[1], 20)
        self.assertEqual(sum(counts.values()), 90)


if __name__ == "__main__":
    unittest.main()
