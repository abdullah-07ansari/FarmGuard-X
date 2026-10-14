import unittest
import tensorflow as tf
from farmguard_ai.src.models.builder import ModelBuilder, ModelBuilderError


class TestModelBuilder(unittest.TestCase):
    def test_mobilenet_v2_construction(self):
        model = ModelBuilder.build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=8, dropout_rate=0.3)
        self.assertEqual(model.input_shape, (None, 224, 224, 3))
        self.assertEqual(model.output_shape, (None, 8))

    def test_configure_phase1_trainable_layers(self):
        model = ModelBuilder.build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=8)
        model, stats = ModelBuilder.configure_phase1(model)

        # Phase 1: Only head layers (3 layers) should be trainable
        self.assertEqual(stats["trainable_layers"], 3)
        self.assertGreater(stats["non_trainable_layers"], 100)

    def test_configure_phase2_trainable_layers(self):
        model = ModelBuilder.build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=8)
        model, stats = ModelBuilder.configure_phase2(model, unfreeze_top_n_layers=30)

        # Phase 2: Top 30 layers should be trainable
        self.assertEqual(stats["trainable_layers"], 30)
        self.assertEqual(stats["unfreeze_top_n_layers"], 30)

    def test_invalid_input_shape_raises_error(self):
        with self.assertRaises(ModelBuilderError):
            ModelBuilder.build_mobilenet_v2(input_shape=(300, 300, 3), num_classes=8)


if __name__ == "__main__":
    unittest.main()
