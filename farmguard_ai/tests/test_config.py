import unittest
import tempfile
from pathlib import Path
import yaml
import numpy as np
from farmguard_ai.src.config import Config, ConfigError


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "test_config.yaml"

        self.valid_yaml = {
            "experiment_name": "test_exp",
            "seed": 42,
            "invariants": {
                "image_size": [224, 224],
                "channels": 3,
                "num_classes": 8,
                "normalization": "mobilenet_v2",
                "labels": {
                    0: "Potato___Early_blight",
                    1: "Potato___Late_blight",
                    2: "Potato___healthy",
                    3: "Tomato___Bacterial_spot",
                    4: "Tomato___Early_blight",
                    5: "Tomato___Late_blight",
                    6: "Tomato___Yellow_Leaf_Curl_Virus",
                    7: "Tomato___healthy"
                }
            },
            "data": {
                "split_ratios": [0.70, 0.15, 0.15]
            }
        }

        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.valid_yaml, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_config_loading(self):
        cfg = Config.from_yaml(self.config_path)
        self.assertEqual(cfg.experiment_name, "test_exp")
        self.assertEqual(cfg.seed, 42)
        self.assertEqual(cfg.image_size, (224, 224))
        self.assertEqual(cfg.num_classes, 8)

    def test_seed_locking(self):
        Config.set_seed(42)
        val1 = np.random.rand()
        Config.set_seed(42)
        val2 = np.random.rand()
        self.assertEqual(val1, val2)

    def test_invalid_image_size_raises_error(self):
        self.valid_yaml["invariants"]["image_size"] = [300, 300]
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.valid_yaml, f)

        with self.assertRaises(ConfigError):
            Config.from_yaml(self.config_path)


if __name__ == "__main__":
    unittest.main()
