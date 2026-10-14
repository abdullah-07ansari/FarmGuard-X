"""
Config Manager for FarmGuard X AI Pipeline.
Loads YAML configurations, validates invariants, and enforces fixed random seeds.
"""

import os
import random
from pathlib import Path
from typing import Dict, Any, List
import yaml
import numpy as np


class ConfigError(Exception):
    """Exception raised for invalid configurations."""
    pass


class Config:
    APPROVED_LABELS: Dict[int, str] = {
        0: "Potato___Early_blight",
        1: "Potato___Late_blight",
        2: "Potato___healthy",
        3: "Tomato___Bacterial_spot",
        4: "Tomato___Early_blight",
        5: "Tomato___Late_blight",
        6: "Tomato___Yellow_Leaf_Curl_Virus",
        7: "Tomato___healthy"
    }

    def __init__(self, raw_config: Dict[str, Any], config_path: Path):
        self.raw_config = raw_config
        self.config_path = config_path.resolve()
        self.experiment_name = raw_config.get("experiment_name", "unnamed_experiment")
        self.seed = raw_config.get("seed", 42)

        # Enforce Fixed Architectural Invariants
        invariants = raw_config.get("invariants", {})
        self.image_size = tuple(invariants.get("image_size", [224, 224]))
        self.channels = invariants.get("channels", 3)
        self.num_classes = invariants.get("num_classes", 8)
        self.normalization = invariants.get("normalization", "mobilenet_v2")
        self.labels = invariants.get("labels", self.APPROVED_LABELS)

        # Configurable Parameters
        self.data_cfg = raw_config.get("data", {})
        self.training_cfg = raw_config.get("training", {})
        self.calibration_cfg = raw_config.get("calibration", {})
        self.quantization_cfg = raw_config.get("quantization", {})

        # Resolve Data Directories portably relative to workspace root or repo root
        repo_root = self.config_path.parent.parent.parent

        def _resolve_dir(sub_path_str: str) -> Path:
            p = Path(sub_path_str)
            if p.is_absolute():
                return p
            if (Path.cwd() / p).exists():
                return (Path.cwd() / p).resolve()
            if (repo_root / p).exists():
                return (repo_root / p).resolve()
            return (repo_root / p).resolve()

        self.raw_dir = _resolve_dir(self.data_cfg.get("raw_dir", "farmguard_ai/data/01_raw"))
        self.processed_dir = _resolve_dir(self.data_cfg.get("processed_dir", "farmguard_ai/data/02_processed"))
        self.splits_dir = _resolve_dir(self.data_cfg.get("splits_dir", "farmguard_ai/data/03_splits"))
        self.experiments_dir = _resolve_dir(self.data_cfg.get("experiments_dir", "farmguard_ai/data/04_experiments"))

        self.dedup_hamming_threshold = self.data_cfg.get("dedup_hamming_threshold", 6)
        self.split_ratios = self.data_cfg.get("split_ratios", [0.70, 0.15, 0.15])

        self._validate_invariants()
        self.set_seed(self.seed)

    def _validate_invariants(self) -> None:
        """Validate fixed technical specification invariants."""
        if self.image_size != (224, 224):
            raise ConfigError(f"Invalid image_size {self.image_size}. Must be (224, 224).")
        if self.channels != 3:
            raise ConfigError(f"Invalid channels {self.channels}. Must be 3 (RGB).")
        if self.num_classes != 8:
            raise ConfigError(f"Invalid num_classes {self.num_classes}. Must be 8.")

        # Check label mapping alignment
        for idx, label_str in self.APPROVED_LABELS.items():
            if str(idx) in self.labels:
                cfg_label = self.labels[str(idx)]
            elif idx in self.labels:
                cfg_label = self.labels[idx]
            else:
                raise ConfigError(f"Missing approved label index {idx} in config.")

            if cfg_label != label_str:
                raise ConfigError(
                    f"Label mapping mismatch for index {idx}: expected '{label_str}', got '{cfg_label}'."
                )

        # Check split ratios sum to 1.0
        if not np.isclose(sum(self.split_ratios), 1.0):
            raise ConfigError(f"Split ratios {self.split_ratios} must sum to 1.0.")

    @staticmethod
    def set_seed(seed: int = 42) -> None:
        """Enforce reproducible random seeds across Python environment."""
        os.environ['PYTHONHASHSEED'] = str(seed)
        random.seed(seed)
        np.random.seed(seed)

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "Config":
        """Factory method to parse YAML configuration file."""
        path = Path(yaml_path)
        if not path.exists():
            raise ConfigError(f"Config file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw_cfg = yaml.safe_load(f)

        return cls(raw_config=raw_cfg, config_path=path)
