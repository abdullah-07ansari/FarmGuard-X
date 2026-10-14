import unittest
from farmguard_ai.src.data.grouper import SpecimenGrouper


class TestGrouper(unittest.TestCase):
    def test_metadata_extraction(self):
        path1 = "/data/raw/Potato___healthy/leaf_042_frame1.jpg"
        path2 = "/data/raw/Potato___healthy/sample_image.jpg"

        id1 = SpecimenGrouper.extract_metadata_group_id(path1)
        id2 = SpecimenGrouper.extract_metadata_group_id(path2)

        self.assertEqual(id1, "leaf_042")
        self.assertEqual(id2, "")

    def test_group_assignment(self):
        grouper = SpecimenGrouper(hamming_threshold=6)
        records = [
            {
                "file_path": "/data/Potato___healthy/leaf_001_v1.jpg",
                "class_id": 2,
                "class_name": "Potato___healthy",
                "md5_hash": "hash1",
                "dhash": "0000000000000000",
                "is_exact_duplicate": False
            },
            {
                "file_path": "/data/Potato___healthy/leaf_001_v2.jpg",
                "class_id": 2,
                "class_name": "Potato___healthy",
                "md5_hash": "hash2",
                "dhash": "0000000000000000",
                "is_exact_duplicate": False
            }
        ]

        grouped = grouper.assign_groups(records)
        self.assertEqual(grouped[0]["group_id"], "verified_leaf_001")
        self.assertEqual(grouped[1]["group_id"], "verified_leaf_001")
        self.assertEqual(grouped[0]["group_provenance"], "verified_metadata")


if __name__ == "__main__":
    unittest.main()
