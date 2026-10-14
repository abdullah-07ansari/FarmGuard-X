import unittest
import tempfile
from pathlib import Path
import numpy as np
import tensorflow as tf
from farmguard_ai.src.config import Config
from farmguard_ai.src.models.builder import ModelBuilder
from farmguard_ai.src.models.trainer import ModelTrainer


class TestTrainer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "test_config.yaml"

        raw_cfg = {
            "experiment_name": "trainer_test",
            "seed": 42,
            "invariants": {
                "image_size": [224, 224],
                "channels": 3,
                "num_classes": 8,
                "normalization": "mobilenet_v2",
                "labels": {
                    0: "Potato___Early_blight", 1: "Potato___Late_blight", 2: "Potato___healthy",
                    3: "Tomato___Bacterial_spot", 4: "Tomato___Early_blight", 5: "Tomato___Late_blight",
                    6: "Tomato___Yellow_Leaf_Curl_Virus", 7: "Tomato___healthy"
                }
            },
            "data": {
                "experiments_dir": str(Path(self.temp_dir.name) / "04_experiments")
            }
        }
        self.config = Config(raw_cfg, self.config_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_forward_backward_pass_execution(self):
        # Create synthetic micro-batches
        x_synth = np.random.uniform(low=-1.0, high=1.0, size=(4, 224, 224, 3)).astype(np.float32)
        y_synth = np.eye(8)[np.random.choice(8, 4)]
        synth_ds = tf.data.Dataset.from_tensor_slices((x_synth, y_synth)).batch(4)

        model = ModelBuilder.build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=8)
        class_weights = {i: 1.0 for i in range(8)}

        trainer = ModelTrainer(config=self.config)
        summary = trainer.train_two_phase(
            model=model,
            train_ds=synth_ds,
            val_ds=synth_ds,
            class_weights=class_weights,
            epochs_phase1=1,
            lr_phase1=0.001,
            epochs_phase2=2,
            lr_phase2=0.00001,
            unfreeze_top_n=30,
            patience=2
        )

        self.assertEqual(summary["phase1_epochs_completed"], 1)
        self.assertEqual(summary["phase2_epochs_completed"], 2)
        self.assertTrue(Path(summary["best_checkpoint_path"]).exists())
        self.assertTrue(Path(summary["csv_log_path"]).exists())


if __name__ == "__main__":
    unittest.main()
