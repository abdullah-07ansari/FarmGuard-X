"""
Class Weight Calculation Module for FarmGuard X.
Computes inverse-frequency class weights strictly from the TRAINING set split
to compensate for dataset class imbalance without data leakage.
"""

import csv
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict
import numpy as np


class ClassWeightError(Exception):
    """Exception raised for errors during class weight calculation."""
    pass


class ClassWeightCalculator:
    @staticmethod
    def verify_training_population_consistency(
        manifest_csv_path: Path,
        num_classes: int = 8
    ) -> Dict[int, int]:
        """
        Verifies that the training sample population counted for class weights
        matches the training sample population extracted by DataLoader exactly.
        Raises ClassWeightError if any discrepancy is detected.
        """
        from farmguard_ai.src.data.loader import DataLoader

        file_paths, class_ids = DataLoader.parse_manifest_split(manifest_csv_path, "train")
        loader_counts: Dict[int, int] = defaultdict(int)
        for c_id in class_ids:
            loader_counts[c_id] += 1

        manifest_counts: Dict[int, int] = defaultdict(int)
        with open(manifest_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["split_assignment"] == "train":
                    manifest_counts[int(row["class_id"])] += 1

        for c_id in range(num_classes):
            c_loader = loader_counts.get(c_id, 0)
            c_manifest = manifest_counts.get(c_id, 0)
            if c_loader != c_manifest:
                raise ClassWeightError(
                    f"Consistency assertion failure for class_id {c_id}: "
                    f"DataLoader extracted {c_loader} training samples, "
                    f"but manifest weight calculator found {c_manifest} samples."
                )

        return dict(loader_counts)

    @classmethod
    def compute_weights_from_manifest(
        cls,
        manifest_csv_path: Path,
        num_classes: int = 8,
        method: str = "inverse_frequency"
    ) -> Dict[int, float]:
        """
        Calculates class weights strictly using rows where split_assignment == 'train'.
        Guarantees that no validation or test set data influences class weighting.
        Enforces cross-component consistency with DataLoader.
        """
        if not manifest_csv_path.exists():
            raise ClassWeightError(f"Split manifest file not found at: {manifest_csv_path}")

        # Enforce consistency assertion between DataLoader and ClassWeightCalculator
        cls.verify_training_population_consistency(manifest_csv_path, num_classes)

        train_class_counts: Dict[int, int] = defaultdict(int)
        total_train_samples = 0

        with open(manifest_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # STRICT REQUIREMENT: Only count training set rows
                if row["split_assignment"] == "train":
                    class_id = int(row["class_id"])
                    train_class_counts[class_id] += 1
                    total_train_samples += 1

        if total_train_samples == 0:
            raise ClassWeightError("No training samples found in split_manifest.csv.")

        class_weights: Dict[int, float] = {}

        if method == "inverse_frequency":
            # Formula: w_i = N / (K * n_i)
            for class_id in range(num_classes):
                n_i = train_class_counts.get(class_id, 0)
                if n_i == 0:
                    raise ClassWeightError(f"Training set has 0 samples for class_id {class_id}.")
                w_i = total_train_samples / (num_classes * n_i)
                class_weights[class_id] = float(w_i)

        elif method == "effective_number":
            # Formula: W_i = (1 - beta) / (1 - beta^n_i)
            beta = 0.99
            for class_id in range(num_classes):
                n_i = train_class_counts.get(class_id, 0)
                if n_i == 0:
                    raise ClassWeightError(f"Training set has 0 samples for class_id {class_id}.")
                effective_num = 1.0 - (beta ** n_i)
                w_i = (1.0 - beta) / effective_num
                class_weights[class_id] = float(w_i)

            # Normalize so weights sum to num_classes
            total_w = sum(class_weights.values())
            for class_id in class_weights:
                class_weights[class_id] = float(class_weights[class_id] * num_classes / total_w)

        else:
            raise ClassWeightError(f"Unsupported class weighting method: {method}")

        return class_weights
