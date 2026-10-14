"""
Sprint 1.5 CLI Entrypoint: 01_prepare_data.py
Executes real dataset acquisition, class mapping verification, validation, deduplication,
specimen grouping, grouped 70/15/15 splitting, zero-leakage verification, and audit report generation.
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from farmguard_ai.src.config import Config
from farmguard_ai.src.data.acquisition import DatasetAcquisition, AcquisitionError
from farmguard_ai.src.data.validator import DataValidator
from farmguard_ai.src.data.deduplicator import Deduplicator
from farmguard_ai.src.data.grouper import SpecimenGrouper
from farmguard_ai.src.data.splitter import DatasetSplitter
from farmguard_ai.src.data.leakage_checker import LeakageChecker
from farmguard_ai.src.data.auditor import DatasetAuditor


def main():
    parser = argparse.ArgumentParser(description="FarmGuard X - Sprint 1.5 Real Dataset Acquisition & Audit")
    parser.add_argument("--config", type=str, default="farmguard_ai/configs/mobilenet_v2_int8.yaml", help="Path to YAML config file")
    args = parser.parse_args()

    config_path = Path(args.config)
    print("=== FarmGuard X Real Dataset Acquisition & Audit (Sprint 1.5) ===")
    print(f"Loading config from: {config_path}")

    cfg = Config.from_yaml(config_path)
    print(f"Experiment Name: {cfg.experiment_name}")
    print(f"Random Seed Locked: {cfg.seed}")

    # 1. Real Dataset Acquisition & Class Mapping Check
    acquisitor = DatasetAcquisition(raw_dir=cfg.raw_dir, target_labels=cfg.APPROVED_LABELS)

    # Check for git repo checkout location or raw_dir location
    color_dir = cfg.raw_dir / "plantvillage_repo" / "raw" / "color"
    if not color_dir.exists():
        color_dir = cfg.raw_dir

    try:
        mapped_dirs, missing_classes, unexpected_classes = acquisitor.verify_and_map_classes(color_dir)
        print(f"[OK] Source Image Directory: {color_dir}")
        print(f"[OK] Target Classes Mapped: {len(mapped_dirs)} / 8")
        if missing_classes:
            print(f"[WARN] Missing Target Classes: {missing_classes}")
        if unexpected_classes:
            print(f"[INFO] Unexpected Class Folders Ignored: {len(unexpected_classes)} folders")
    except AcquisitionError as e:
        print(f"[ERROR] Acquisition Failure: {str(e)}")
        sys.exit(1)

    # Record Provenance Metadata
    provenance_path = cfg.processed_dir / "provenance_manifest.json"
    commit_hash = DatasetAcquisition.get_git_commit_hash(cfg.raw_dir / "plantvillage_repo")
    provenance_record = acquisitor.record_provenance(
        output_manifest_path=provenance_path,
        mapped_count=len(mapped_dirs),
        commit_hash=commit_hash
    )
    print(f"[OK] Provenance Recorded: {provenance_record['license']} (Commit: {commit_hash[:8]})")

    # 2. Data Validation
    validator = DataValidator(target_labels=cfg.APPROVED_LABELS, min_dim=cfg.image_size)
    corrupt_log_path = cfg.processed_dir / "corrupt_log.txt"
    valid_records, corrupt_logs = validator.validate_dataset(color_dir, corrupt_log_path)
    print(f"[OK] Data Validation Complete: {len(valid_records)} valid images, {len(corrupt_logs)} issues logged.")

    if not valid_records:
        print(f"[WARN] No valid raw images found in {color_dir}. Audit complete.")
        return

    # 3. Deduplication (MD5 & dhash)
    deduplicator = Deduplicator()
    processed_records = deduplicator.process_records(valid_records, hamming_threshold=cfg.dedup_hamming_threshold)
    exact_dupes = sum(1 for r in processed_records if r.get("is_exact_duplicate"))
    print(f"[OK] Deduplication Complete: {exact_dupes} exact duplicates flagged.")

    # 4. Specimen Grouping
    grouper = SpecimenGrouper(hamming_threshold=cfg.dedup_hamming_threshold)
    grouped_records = grouper.assign_groups(processed_records)
    unique_groups = len(set(r["group_id"] for r in grouped_records))
    print(f"[OK] Specimen Grouping Complete: Assigned {len(grouped_records)} images to {unique_groups} unique specimen groups.")

    # 5. Grouped Stratified 70/15/15 Split
    splitter = DatasetSplitter(split_ratios=cfg.split_ratios, seed=cfg.seed)
    split_records, summary = splitter.split_records(grouped_records)
    print(f"[OK] Grouped Stratified Split Complete:")
    print(f"   - Train Images: {summary['train_images']}")
    print(f"   - Val Images:   {summary['val_images']}")
    print(f"   - Test Images:  {summary['test_images']}")

    # 6. Export Split Manifest
    manifest_csv = cfg.splits_dir / "split_manifest.csv"
    DatasetSplitter.export_manifest(split_records, manifest_csv)
    print(f"[OK] Split Manifest Exported: {manifest_csv}")

    # 7. Zero-Leakage Verification Assertions
    leakage_result = LeakageChecker.verify_manifest_file(manifest_csv)
    print(f"[OK] Zero-Leakage Verification Status: {leakage_result['status']}")

    # 8. Generate Auditable Dataset Audit Report
    audit_json = cfg.processed_dir / "dataset_audit_report.json"
    audit_md = cfg.processed_dir / "dataset_audit_report.md"
    audit_report = DatasetAuditor.generate_audit_report(
        provenance_info=provenance_record,
        valid_records=valid_records,
        corrupt_logs=corrupt_logs,
        split_records=split_records,
        split_summary=summary,
        leakage_status=leakage_result,
        output_json_path=audit_json,
        output_md_path=audit_md
    )
    print(f"[OK] Dataset Audit Reports Exported:")
    print(f"   - JSON Report: {audit_json}")
    print(f"   - Markdown Report: {audit_md}")
    print("=== Pipeline Complete: Real Dataset Audit & Split Manifest Ready ===")


if __name__ == "__main__":
    main()
