import unittest
from farmguard_ai.src.data.splitter import DatasetSplitter


class TestSplitter(unittest.TestCase):
    def test_grouped_split(self):
        splitter = DatasetSplitter(split_ratios=(0.70, 0.15, 0.15), seed=42)

        # 10 distinct groups across class 0
        records = []
        for i in range(10):
            records.append({
                "file_path": f"/data/class0/group_{i}_img1.jpg",
                "class_id": 0,
                "class_name": "Potato___Early_blight",
                "group_id": f"group_{i}",
                "group_provenance": "verified_metadata",
                "md5_hash": f"md5_{i}_1",
                "dhash": "0000",
                "is_exact_duplicate": False
            })
            records.append({
                "file_path": f"/data/class0/group_{i}_img2.jpg",
                "class_id": 0,
                "class_name": "Potato___Early_blight",
                "group_id": f"group_{i}",
                "group_provenance": "verified_metadata",
                "md5_hash": f"md5_{i}_2",
                "dhash": "0000",
                "is_exact_duplicate": False
            })

        split_recs, summary = splitter.split_records(records)
        self.assertEqual(summary["total_images"], 20)

        # Verify that all images of group_i have the exact same split assignment
        group_split_map = {}
        for r in split_recs:
            g_id = r["group_id"]
            split = r["split_assignment"]
            if g_id in group_split_map:
                self.assertEqual(group_split_map[g_id], split, f"Group {g_id} fragmented across splits!")
            else:
                group_split_map[g_id] = split


if __name__ == "__main__":
    unittest.main()
