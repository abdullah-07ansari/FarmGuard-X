import unittest
from farmguard_ai.src.data.leakage_checker import LeakageChecker, DataLeakageError


class TestLeakageChecker(unittest.TestCase):
    def test_zero_leakage_passes(self):
        records = [
            {"file_path": "/p1", "group_id": "g1", "group_provenance": "unassigned_unique", "md5_hash": "m1", "split_assignment": "train"},
            {"file_path": "/p2", "group_id": "g2", "group_provenance": "unassigned_unique", "md5_hash": "m2", "split_assignment": "val"},
            {"file_path": "/p3", "group_id": "g3", "group_provenance": "unassigned_unique", "md5_hash": "m3", "split_assignment": "test"},
        ]
        result = LeakageChecker.verify_records(records)
        self.assertEqual(result["status"], "PASSED_ZERO_LEAKAGE")

    def test_group_leakage_triggers_error(self):
        records = [
            {"file_path": "/p1", "group_id": "g1", "group_provenance": "unassigned_unique", "md5_hash": "m1", "split_assignment": "train"},
            {"file_path": "/p2", "group_id": "g1", "group_provenance": "unassigned_unique", "md5_hash": "m2", "split_assignment": "test"}, # Forced group leak!
        ]
        with self.assertRaises(DataLeakageError):
            LeakageChecker.verify_records(records)

    def test_md5_leakage_triggers_error(self):
        records = [
            {"file_path": "/p1", "group_id": "g1", "group_provenance": "unassigned_unique", "md5_hash": "m1", "split_assignment": "train"},
            {"file_path": "/p2", "group_id": "g2", "group_provenance": "unassigned_unique", "md5_hash": "m1", "split_assignment": "test"}, # Forced MD5 leak!
        ]
        with self.assertRaises(DataLeakageError):
            LeakageChecker.verify_records(records)

    def test_near_duplicate_cluster_cross_split_triggers_error(self):
        records = [
            {"file_path": "/p1", "group_id": "inferred_cluster_0001", "group_provenance": "inferred_dhash", "md5_hash": "m1", "split_assignment": "train"},
            {"file_path": "/p2", "group_id": "inferred_cluster_0001", "group_provenance": "inferred_dhash", "md5_hash": "m2", "split_assignment": "val"}, # Cluster crossing split!
        ]
        with self.assertRaises(DataLeakageError):
            LeakageChecker.verify_records(records)


if __name__ == "__main__":
    unittest.main()
