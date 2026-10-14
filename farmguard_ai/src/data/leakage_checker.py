"""
Automated Data Leakage Verification Module for FarmGuard X.
Executes programmatic set-intersection assertions to guarantee zero group overlap,
zero candidate cluster split-crossing, and zero duplicate hash overlap across splits.
Fails loudly by raising DataLeakageError if leakage is detected.
"""

import csv
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict


class DataLeakageError(Exception):
    """Critical exception raised when data leakage is detected between splits."""
    pass


class LeakageChecker:
    @classmethod
    def verify_records(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes programmatic leakage assertions directly on image records.
        """
        train_groups: Set[str] = set()
        val_groups: Set[str] = set()
        test_groups: Set[str] = set()

        train_md5: Set[str] = set()
        val_md5: Set[str] = set()
        test_md5: Set[str] = set()

        cluster_splits: Dict[str, Set[str]] = defaultdict(set)

        for r in records:
            g_id = r["group_id"]
            md5_val = r["md5_hash"]
            split = r["split_assignment"]
            prov = r.get("group_provenance", "")

            if split == "train":
                train_groups.add(g_id)
                train_md5.add(md5_val)
            elif split == "val":
                val_groups.add(g_id)
                val_md5.add(md5_val)
            elif split == "test":
                test_groups.add(g_id)
                test_md5.add(md5_val)
            else:
                raise DataLeakageError(f"Invalid split assignment '{split}' for record {r['file_path']}")

            if prov == "inferred_dhash":
                cluster_splits[g_id].add(split)

        # 1. Group Intersections (Specimen-Level Leakage Check)
        train_val_group_leak = train_groups & val_groups
        train_test_group_leak = train_groups & test_groups
        val_test_group_leak = val_groups & test_groups

        if train_val_group_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(train_val_group_leak)} group IDs overlap between Train and Val splits! "
                f"Sample leaked groups: {list(train_val_group_leak)[:3]}"
            )
        if train_test_group_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(train_test_group_leak)} group IDs overlap between Train and Test splits! "
                f"Sample leaked groups: {list(train_test_group_leak)[:3]}"
            )
        if val_test_group_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(val_test_group_leak)} group IDs overlap between Val and Test splits! "
                f"Sample leaked groups: {list(val_test_group_leak)[:3]}"
            )

        # 2. Hash Intersections (Exact File Leakage Check)
        train_val_md5_leak = train_md5 & val_md5
        train_test_md5_leak = train_md5 & test_md5
        val_test_md5_leak = val_md5 & test_md5

        if train_val_md5_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(train_val_md5_leak)} MD5 hashes overlap between Train and Val splits!"
            )
        if train_test_md5_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(train_test_md5_leak)} MD5 hashes overlap between Train and Test splits!"
            )
        if val_test_md5_leak:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(val_test_md5_leak)} MD5 hashes overlap between Val and Test splits!"
            )

        # 3. Near-Duplicate Candidate Cluster Isolation Check
        cross_split_clusters = [g_id for g_id, splits in cluster_splits.items() if len(splits) > 1]
        if cross_split_clusters:
            raise DataLeakageError(
                f"CRITICAL LEAKAGE: {len(cross_split_clusters)} near-duplicate candidate clusters cross split boundaries! "
                f"Leaked candidate cluster IDs: {cross_split_clusters[:3]}"
            )

        return {
            "status": "PASSED_ZERO_LEAKAGE",
            "train_groups": len(train_groups),
            "val_groups": len(val_groups),
            "test_groups": len(test_groups),
            "train_unique_hashes": len(train_md5),
            "val_unique_hashes": len(val_md5),
            "test_unique_hashes": len(test_md5),
            "inferred_clusters_verified": len(cluster_splits),
            "cross_split_clusters": 0
        }

    @classmethod
    def verify_manifest_file(cls, manifest_csv_path: Path) -> Dict[str, Any]:
        """
        Reads an exported split_manifest.csv and executes zero-leakage assertions.
        """
        if not manifest_csv_path.exists():
            raise DataLeakageError(f"Split manifest file not found: {manifest_csv_path}")

        records = []
        with open(manifest_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

        return cls.verify_records(records)
