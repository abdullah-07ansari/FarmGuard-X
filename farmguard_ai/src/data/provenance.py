"""
Dataset Provenance & Licensing Metadata Module.
Manages dataset licensing verification, source tracking, and provenance metadata logging.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class ProvenanceError(Exception):
    """Exception raised for provenance or licensing failures."""
    pass


class ProvenanceManager:
    ALLOWED_LICENSES: List[str] = [
        "CC0 1.0",
        "CC0 1.0 Universal",
        "Public Domain",
        "CC BY 4.0",
        "Creative Commons Attribution 4.0 International",
        "MIT"
    ]

    @classmethod
    def verify_and_log(
        cls,
        dataset_name: str,
        source_url: str,
        license_name: str,
        dataset_dir: Path,
        output_manifest_path: Path
    ) -> Dict[str, Any]:
        """
        Verifies license compliance and records dataset provenance metadata.
        """
        is_compliant = any(
            allowed.lower() in license_name.lower() for allowed in cls.ALLOWED_LICENSES
        )
        if not is_compliant:
            raise ProvenanceError(
                f"License '{license_name}' for dataset '{dataset_name}' is not in allowed open-source licenses list."
            )

        provenance_record = {
            "dataset_name": dataset_name,
            "source_url": source_url,
            "license": license_name,
            "dataset_directory": str(dataset_dir.resolve()),
            "license_compliant": True,
            "verification_status": "APPROVED"
        }

        output_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_manifest_path, "w", encoding="utf-8") as f:
            json.dump(provenance_record, f, indent=2)

        return provenance_record
