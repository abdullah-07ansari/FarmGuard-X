"""
Specimen & Plant Grouping Module for FarmGuard X.
Assigns group_id to records, strictly distinguishing verified specimen metadata
from inferred/near-duplicate hash clusters and fallback unknown individual specimens.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from farmguard_ai.src.data.deduplicator import Deduplicator


class SpecimenGrouper:
    def __init__(self, hamming_threshold: int = 6):
        self.hamming_threshold = hamming_threshold

    @staticmethod
    def extract_metadata_group_id(file_path_str: str) -> str:
        """
        Attempts to extract a verified plant/leaf specimen ID from filename patterns
        (e.g., 'leaf_042_v1.jpg', 'plant_8492_idx1.png', 'specimen-A94-01.jpg').
        Returns empty string if no verified metadata pattern exists.
        """
        filename = Path(file_path_str).stem.lower()

        # Pattern 1: leaf_XXX or plant_XXX or specimen_XXX
        match = re.search(r'(leaf[_\-]\d+|plant[_\-]\d+|specimen[_\-]\w+)', filename)
        if match:
            return match.group(1)

        return ""

    def assign_groups(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assigns group_id and group_provenance to each image record.
        Rules:
        1. Exact duplicate -> inherits primary image's group_id.
        2. Explicit filename metadata -> group_id = extracted_metadata (provenance='verified_metadata').
        3. Near-duplicate hash cluster -> group_id = inferred_cluster_XXX (provenance='inferred_dhash').
        4. Unique fallback -> group_id = unique_specimen_XXX (provenance='unassigned_unique').
        """
        dhash_list: List[Tuple[int, str, str]] = []  # (index, dhash, class_name)

        for idx, rec in enumerate(records):
            if rec.get("is_exact_duplicate", False):
                continue

            path_str = rec["file_path"]
            extracted_id = self.extract_metadata_group_id(path_str)

            if extracted_id:
                rec["group_id"] = f"verified_{extracted_id}"
                rec["group_provenance"] = "verified_metadata"
            else:
                rec["group_id"] = None
                rec["group_provenance"] = None
                dhash_list.append((idx, rec["dhash"], rec["class_name"]))

        # Step 2: Near-duplicate clustering for unassigned records within the same class
        cluster_count = 0
        assigned_indices = set()

        for i in range(len(dhash_list)):
            idx_i, hash_i, class_i = dhash_list[i]
            if idx_i in assigned_indices:
                continue

            cluster_members = [idx_i]
            for j in range(i + 1, len(dhash_list)):
                idx_j, hash_j, class_j = dhash_list[j]
                if idx_j in assigned_indices or class_i != class_j:
                    continue

                dist = Deduplicator.hamming_distance(hash_i, hash_j)
                if dist <= self.hamming_threshold:
                    cluster_members.append(idx_j)

            if len(cluster_members) > 1:
                cluster_id = f"inferred_cluster_{cluster_count:04d}"
                cluster_count += 1
                for idx_m in cluster_members:
                    records[idx_m]["group_id"] = cluster_id
                    records[idx_m]["group_provenance"] = "inferred_dhash"
                    assigned_indices.add(idx_m)
            else:
                # Single unique image with no metadata or near-duplicates
                records[idx_i]["group_id"] = f"unique_specimen_{records[idx_i]['md5_hash'][:10]}"
                records[idx_i]["group_provenance"] = "unassigned_unique"
                assigned_indices.add(idx_i)

        # Step 3: Assign exact duplicates to their original specimen group_id
        md5_to_group = {r["md5_hash"]: r.get("group_id") for r in records if r.get("group_id") is not None}
        for rec in records:
            if rec.get("is_exact_duplicate", False):
                md5_val = rec["md5_hash"]
                rec["group_id"] = md5_to_group.get(md5_val, f"duplicate_{md5_val[:10]}")
                rec["group_provenance"] = "duplicate_inherited"

        return records
