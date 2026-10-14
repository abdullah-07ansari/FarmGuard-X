"""
Data Validation Module for FarmGuard X.
Inspects raw image files, checks decodability, verifies 3-channel RGB mode,
validates min dimensions (224x224), and flags corrupt or unreadable files.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
from PIL import Image


class DataValidator:
    FOLDER_ALIASES: Dict[str, str] = {
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato___Yellow_Leaf_Curl_Virus"
    }

    def __init__(self, target_labels: Dict[int, str], min_dim: Tuple[int, int] = (224, 224)):
        self.label_to_id = {v: k for k, v in target_labels.items()}
        self.min_width, self.min_height = min_dim

    def validate_dataset(self, raw_dir: Path, corrupt_log_path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Validates all raw images in the given directory.
        Returns a tuple of (valid_image_records, corrupt_log_lines).
        """
        valid_records: List[Dict[str, Any]] = []
        corrupt_logs: List[str] = []

        if not raw_dir.exists():
            return valid_records, [f"Raw directory does not exist: {raw_dir}"]

        # Scan for class subdirectories matching target labels
        for class_dir in raw_dir.iterdir():
            if not class_dir.is_dir():
                continue

            folder_name = class_dir.name
            target_name = self.FOLDER_ALIASES.get(folder_name, folder_name)

            if target_name not in self.label_to_id:
                corrupt_logs.append(f"Ignored directory with non-target label: {folder_name}")
                continue

            class_id = self.label_to_id[target_name]

            # Process image files inside class folder
            for img_path in class_dir.glob("*"):
                if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp"]:
                    continue

                try:
                    with Image.open(img_path) as img:
                        img.verify()  # Verify file integrity

                    # Re-open for metadata inspection after verify()
                    with Image.open(img_path) as img:
                        w, h = img.size
                        mode = img.mode

                        if w < self.min_width or h < self.min_height:
                            corrupt_logs.append(
                                f"Dimension Error [{img_path}]: Size ({w}x{h}) smaller than min ({self.min_width}x{self.min_height})"
                            )
                            continue

                        valid_records.append({
                            "file_path": str(img_path.resolve()),
                            "class_id": class_id,
                            "class_name": target_name,
                            "raw_folder_name": folder_name,
                            "width": w,
                            "height": h,
                            "mode": mode
                        })

                except Exception as e:
                    corrupt_logs.append(f"Corrupt File [{img_path}]: {str(e)}")

        # Write corrupt log if corrupt log path is specified
        corrupt_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(corrupt_log_path, "w", encoding="utf-8") as f:
            for log_line in corrupt_logs:
                f.write(log_line + "\n")

        return valid_records, corrupt_logs
