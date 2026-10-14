"""
TensorFlow Dataset Construction & Loading Module for FarmGuard X.
Reads split_manifest.csv, enforces 224x224 RGB image resizing, MobileNetV2 [-1.0, 1.0]
pixel normalization, one-hot label encoding, and training-only data augmentation.
"""

import csv
from pathlib import Path
from typing import Dict, Any, List, Tuple
import tensorflow as tf
from farmguard_ai.src.data.augmentation import AugmentationPipeline


class DataLoaderError(Exception):
    """Exception raised during dataset construction."""
    pass


class DataLoader:
    @staticmethod
    def parse_manifest_split(
        manifest_csv_path: Path,
        split_name: str
    ) -> Tuple[List[str], List[int]]:
        """
        Parses split_manifest.csv and extracts image file paths and class IDs for the target split.
        """
        if not manifest_csv_path.exists():
            raise DataLoaderError(f"Split manifest file not found at: {manifest_csv_path}")

        file_paths: List[str] = []
        class_ids: List[int] = []

        with open(manifest_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["split_assignment"] == split_name:
                    image_path = Path(row["file_path"])

                    # Resolve repository-relative paths from the project root or CWD portably.
                    if not image_path.is_absolute():
                        repo_root = manifest_csv_path.resolve().parent.parent.parent
                        if (repo_root / image_path).exists():
                            image_path = repo_root / image_path
                        elif (Path.cwd() / image_path).exists():
                            image_path = Path.cwd() / image_path
                        else:
                            image_path = repo_root / image_path

                    file_paths.append(str(image_path.resolve()))
                    class_ids.append(int(row["class_id"]))


        if not file_paths:
            raise DataLoaderError(f"No records found for split '{split_name}' in manifest {manifest_csv_path}")

        return file_paths, class_ids

    @staticmethod
    def preprocess_image_and_label(
        file_path: tf.Tensor,
        class_id: tf.Tensor,
        target_size: Tuple[int, int] = (224, 224),
        num_classes: int = 8
    ) -> Tuple[tf.Tensor, tf.Tensor]:
        """
        TensorFlow map function: reads raw file, decodes RGB image, performs aspect-ratio center crop/resize
        to (224, 224), normalizes pixels to [-1.0, 1.0], and one-hot encodes class label.
        """
        # Read raw file bytes
        img_bytes = tf.io.read_file(file_path)
        # Decode image as 3-channel RGB
        img = tf.io.decode_image(img_bytes, channels=3, expand_animations=False)
        img = tf.image.convert_image_dtype(img, tf.float32) # Scale to [0.0, 1.0]

        # Resize to (224, 224)
        img_resized = tf.image.resize(img, target_size, method=tf.image.ResizeMethod.BILINEAR)

        # MobileNetV2 Normalization: Scale [0.0, 1.0] -> [-1.0, 1.0]
        # Formula: (img * 2.0) - 1.0
        img_normalized = (img_resized * 2.0) - 1.0

        # One-hot encode label to num_classes (8)
        one_hot_label = tf.one_hot(class_id, depth=num_classes)

        return img_normalized, one_hot_label

    @classmethod
    def build_dataset(
        cls,
        manifest_csv_path: Path,
        split_name: str,
        target_size: Tuple[int, int] = (224, 224),
        batch_size: int = 32,
        num_classes: int = 8,
        is_training: bool = False,
        seed: int = 42
    ) -> tf.data.Dataset:
        """
        Constructs an optimized tf.data.Dataset pipeline for the specified split.
        Applies augmentation ONLY when is_training is True.
        """
        file_paths, class_ids = cls.parse_manifest_split(manifest_csv_path, split_name)

        path_ds = tf.data.Dataset.from_tensor_slices(file_paths)
        label_ds = tf.data.Dataset.from_tensor_slices(class_ids)
        raw_ds = tf.data.Dataset.zip((path_ds, label_ds))

        if is_training:
            raw_ds = raw_ds.shuffle(buffer_size=min(len(file_paths), 1000), seed=seed, reshuffle_each_iteration=True)

        # Map preprocessing
        ds = raw_ds.map(
            lambda p, l: cls.preprocess_image_and_label(p, l, target_size, num_classes),
            num_parallel_calls=tf.data.AUTOTUNE
        )

        # Apply augmentation STRICTLY to training datasets
        if is_training:
            aug_layer = AugmentationPipeline.get_training_augmentation_layer()
            ds = ds.map(
                lambda img, lbl: (aug_layer(img, training=True), lbl),
                num_parallel_calls=tf.data.AUTOTUNE
            )

        ds = ds.batch(batch_size)
        ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)

        return ds
