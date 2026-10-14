"""
MobileNetV2 Model Architecture Builder for FarmGuard X.
Instantiates ImageNet-pretrained MobileNetV2 backbone, constructs 8-class classification head,
and configures layer trainability for Two-Phase Transfer Learning.
"""

from typing import Tuple, Dict, Any
import tensorflow as tf


class ModelBuilderError(Exception):
    """Exception raised during model construction."""
    pass


class ModelBuilder:
    @staticmethod
    def build_mobilenet_v2(
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        num_classes: int = 8,
        dropout_rate: float = 0.3,
        weights: str = "imagenet"
    ) -> tf.keras.Model:
        """
        Builds MobileNetV2 model with custom classification head for 8 classes.
        Input shape: (224, 224, 3), Outputs: 8-class softmax logits.
        """
        if input_shape != (224, 224, 3):
            raise ModelBuilderError(f"Invalid input_shape {input_shape}. Must be (224, 224, 3).")
        if num_classes != 8:
            raise ModelBuilderError(f"Invalid num_classes {num_classes}. Must be 8.")

        # Base ImageNet pre-trained MobileNetV2 backbone
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights=weights
        )

        inputs = base_model.input
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
        x = tf.keras.layers.Dropout(rate=dropout_rate, name="head_dropout")(x)
        outputs = tf.keras.layers.Dense(units=num_classes, activation="softmax", name="predictions")(x)

        model = tf.keras.Model(inputs=inputs, outputs=outputs, name="farmguard_mobilenet_v2")
        return model

    @classmethod
    def configure_phase1(cls, model: tf.keras.Model) -> Tuple[tf.keras.Model, Dict[str, int]]:
        """
        Configures Phase 1 (Feature Extractor):
        Freezes the entire MobileNetV2 backbone. Only classification head layers remain trainable.
        """
        # Identify backbone layers vs head layers
        head_layer_names = {"global_avg_pool", "head_dropout", "predictions"}

        for layer in model.layers:
            if layer.name in head_layer_names:
                layer.trainable = True
            else:
                layer.trainable = False

        trainable_count = sum(1 for layer in model.layers if layer.trainable)
        non_trainable_count = sum(1 for layer in model.layers if not layer.trainable)

        stats = {
            "total_layers": len(model.layers),
            "trainable_layers": trainable_count,
            "non_trainable_layers": non_trainable_count
        }
        return model, stats

    @classmethod
    def configure_phase2(
        cls,
        model: tf.keras.Model,
        unfreeze_top_n_layers: int = 30
    ) -> Tuple[tf.keras.Model, Dict[str, int]]:
        """
        Configures Phase 2 (Controlled Fine-Tuning):
        Unfreezes the top N layers of the MobileNetV2 backbone while keeping bottom layers frozen.
        """
        total_layers = len(model.layers)
        unfreeze_start_index = max(0, total_layers - unfreeze_top_n_layers)

        for i, layer in enumerate(model.layers):
            if i >= unfreeze_start_index:
                layer.trainable = True
            else:
                layer.trainable = False

        trainable_count = sum(1 for layer in model.layers if layer.trainable)
        non_trainable_count = sum(1 for layer in model.layers if not layer.trainable)

        stats = {
            "total_layers": total_layers,
            "unfreeze_top_n_layers": unfreeze_top_n_layers,
            "trainable_layers": trainable_count,
            "non_trainable_layers": non_trainable_count
        }
        return model, stats
