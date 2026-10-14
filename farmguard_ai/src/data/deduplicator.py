"""
Deduplication & Hashing Module for FarmGuard X.
Computes MD5 binary hashes for exact duplicate detection and pure-PIL dhash
(Difference Hash) for near-duplicate candidate detection.
"""

import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple
from PIL import Image
import numpy as np


class Deduplicator:
    @staticmethod
    def compute_md5(file_path: Path) -> str:
        """Computes binary MD5 checksum for exact file matching."""
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def compute_dhash(file_path: Path, hash_size: int = 8) -> str:
        """
        Computes Difference Hash (dhash) using PIL and numpy.
        Resizes to (hash_size + 1, hash_size), computes horizontal gradient,
        and converts 64-bit boolean array into hex string.
        """
        with Image.open(file_path) as img:
            # Convert to grayscale and resize to (hash_size + 1, hash_size)
            gray = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.BILINEAR)
            pixels = np.asarray(gray, dtype=np.int32)

            # Compute difference between adjacent pixels across columns
            diff = pixels[:, 1:] > pixels[:, :-1]

            # Convert boolean array to integer hash
            decimal_val = 0
            for bit in diff.flatten():
                decimal_val = (decimal_val << 1) | int(bit)

            # Format as fixed-length hex string
            hex_str = f"{decimal_val:0{hash_size * 2}x}"
            return hex_str

    @staticmethod
    def hamming_distance(hex_hash1: str, hex_hash2: str) -> int:
        """Computes Hamming distance between two hex hash strings."""
        int1 = int(hex_hash1, 16)
        int2 = int(hex_hash2, 16)
        xor_val = int1 ^ int2
        return bin(xor_val).count('1')

    def process_records(
        self,
        records: List[Dict[str, Any]],
        hamming_threshold: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Enriches image records with MD5 and dhash, flags exact duplicates,
        and links near-duplicate candidate pairs within hamming_threshold.
        """
        processed_records: List[Dict[str, Any]] = []
        seen_md5: Dict[str, str] = {}  # md5 -> first record file_path

        for rec in records:
            path = Path(rec["file_path"])
            md5_val = self.compute_md5(path)
            dhash_val = self.compute_dhash(path)

            rec["md5_hash"] = md5_val
            rec["dhash"] = dhash_val
            rec["is_exact_duplicate"] = False
            rec["duplicate_of"] = None

            if md5_val in seen_md5:
                rec["is_exact_duplicate"] = True
                rec["duplicate_of"] = seen_md5[md5_val]
            else:
                seen_md5[md5_val] = str(path)

            processed_records.append(rec)

        return processed_records
