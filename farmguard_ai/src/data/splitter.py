"""
Grouped Stratified Dataset Splitter & Manifest Generator for FarmGuard X.
Partitions dataset into 70% Train / 15% Val / 15% Test at the specimen group level,
preserving class proportions while ensuring zero group overlap across splits.
"""

import csv
import random
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict
import numpy as np


class SplitterError(Exception):
    """Exception raised for dataset splitting errors."""
    pass


class DatasetSplitter:
    def __init__(self, split_ratios: Tuple[float, float, float] = (0.70, 0.15, 0.15), seed: int = 42):
        if not np.isclose(sum(split_ratios), 1.0):
            raise SplitterError(f"Split ratios {split_ratios} must sum to 1.0.")
        self.train_ratio, self.val_ratio, self.test_ratio = split_ratios
        self.seed = seed

    def split_records(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Splits image records at the group_id level into train, val, and test splits.
        Returns updated records with 'split_assignment' and a summary dictionary.
        """
        random.seed(self.seed)

        # Step 1: Collect unique groups per class
        class_group_map: Dict[int, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))

        for rec in records:
            c_id = rec["class_id"]
            g_id = rec["group_id"]
            class_group_map[c_id][g_id].append(rec)

        # Step 2: Assign groups to splits per class (Stratified Group Partitioning)
        for class_id, groups_dict in class_group_map.items():
            group_ids = list(groups_dict.keys())
            random.shuffle(group_ids)

            num_groups = len(group_ids)
            n_train = int(round(num_groups * self.train_ratio))
            n_val = int(round(num_groups * self.val_ratio))

            # Ensure at least 1 group per split if total groups >= 3
            if num_groups >= 3:
                n_train = max(1, n_train)
                n_val = max(1, n_val)
                n_test = num_groups - (n_train + n_val)
                if n_test <= 0:
                    n_test = 1
                    if n_train > n_val:
                        n_train -= 1
                    else:
                        n_val -= 1

            train_groups = set(group_ids[:n_train])
            val_groups = set(group_ids[n_train:n_train + n_val])
            test_groups = set(group_ids[n_train + n_val:])

            for g_id, recs in groups_dict.items():
                if g_id in train_groups:
                    split_label = "train"
                elif g_id in val_groups:
                    split_label = "val"
                else:
                    split_label = "test"

                for r in recs:
                    r["split_assignment"] = split_label

        # Summary computation
        summary = {
            "total_images": len(records),
            "train_images": sum(1 for r in records if r["split_assignment"] == "train"),
            "val_images": sum(1 for r in records if r["split_assignment"] == "val"),
            "test_images": sum(1 for r in records if r["split_assignment"] == "test"),
        }

        return records, summary

    @staticmethod
    def export_manifest(records: List[Dict[str, Any]], manifest_csv_path: Path) -> Path:
        """Exports the complete auditable split_manifest.csv file."""
        manifest_csv_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "image_id",
            "file_path",
            "class_id",
            "class_name",
            "group_id",
            "group_provenance",
            "md5_hash",
            "dhash",
            "is_exact_duplicate",
            "duplicate_of",
            "split_assignment"
        ]

        with open(manifest_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for idx, rec in enumerate(records):
                writer.writerow({
                    "image_id": f"IMG_{idx:06d}",
                    "file_path": rec["file_path"],
                    "class_id": rec["class_id"],
                    "class_name": rec["class_name"],
                    "group_id": rec["group_id"],
                    "group_provenance": rec["group_provenance"],
                    "md5_hash": rec["md5_hash"],
                    "dhash": rec["dhash"],
                    "is_exact_duplicate": rec.get("is_exact_duplicate", False),
                    "duplicate_of": rec.get("duplicate_of", ""),
                    "split_assignment": rec["split_assignment"]
                })

        return manifest_csv_path
