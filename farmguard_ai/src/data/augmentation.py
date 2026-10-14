"""
Data Augmentation Module for FarmGuard X.
Provides Keras preprocessing layers for training-only data augmentation.
Augmentation is strictly isolated from validation and held-out test datasets.
"""

import tensorflow as tf


class AugmentationPipeline:
    @staticmethod
    def get_training_augmentation_layer(
        rotation_range: float = 0.08,
        contrast_factor: float = 0.2,
        zoom_factor: float = 0.15
    ) -> tf.keras.Sequential:
        """
        Builds a Keras Sequential layer for training-only data augmentation.
        Includes horizontal/vertical flips, rotation (+-30 deg), contrast adjustment, and zoom.
        """
        return tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal_and_vertical"),
            tf.keras.layers.RandomRotation(factor=rotation_range),
            tf.keras.layers.RandomContrast(factor=contrast_factor),
            tf.keras.layers.RandomZoom(height_factor=zoom_factor, width_factor=zoom_factor),
        ], name="training_augmentation_pipeline")
