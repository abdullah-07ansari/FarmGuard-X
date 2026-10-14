"""
Two-Phase Transfer Learning Trainer for FarmGuard X.
Orchestrates Phase 1 (Feature Extractor) and Phase 2 (Fine-Tuning) training loops,
validation checkpointing, class weighting, and training history logging.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import tensorflow as tf
from farmguard_ai.src.models.builder import ModelBuilder
from farmguard_ai.src.config import Config


class TrainerError(Exception):
    """Exception raised during training execution."""
    pass


class ModelTrainer:
    def __init__(self, config: Config):
        self.config = config
        self.checkpoint_dir = config.experiments_dir / "checkpoints"
        self.metrics_dir = config.experiments_dir / "metrics"

        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def train_two_phase(
        self,
        model: tf.keras.Model,
        train_ds: tf.data.Dataset,
        val_ds: tf.data.Dataset,
        class_weights: Dict[int, float],
        epochs_phase1: int = 15,
        lr_phase1: float = 0.001,
        epochs_phase2: int = 30,
        lr_phase2: float = 0.00001,
        unfreeze_top_n: int = 30,
        patience: int = 5
    ) -> Dict[str, Any]:
        """
        Executes two-phase transfer learning training architecture.
        Phase 1: Frozen backbone, high learning rate (0.001).
        Phase 2: Fine-tune top N backbone layers, low learning rate (0.00001) with early stopping.
        """
        best_checkpoint_path = self.checkpoint_dir / "best_model.h5"
        csv_log_path = self.metrics_dir / "training_history.csv"

        # --- PHASE 1: Feature Extractor Training ---
        print("\n=== STARTING PHASE 1: Feature Extractor Training (Frozen Backbone) ===")
        model, p1_stats = ModelBuilder.configure_phase1(model)

        optimizer_p1 = tf.keras.optimizers.Adam(learning_rate=lr_phase1)
        model.compile(
            optimizer=optimizer_p1,
            loss="categorical_crossentropy",
            metrics=["accuracy", tf.keras.metrics.MacroAverageF1Score(num_classes=8, name="macro_f1") if hasattr(tf.keras.metrics, "MacroAverageF1Score") else "categorical_accuracy"]
        )

        callbacks_p1 = [
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(best_checkpoint_path),
                monitor="val_loss",
                save_best_only=True,
                verbose=1
            ),
            tf.keras.callbacks.CSVLogger(filename=str(csv_log_path), append=False)
        ]

        history_p1 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs_phase1,
            class_weight=class_weights,
            callbacks=callbacks_p1,
            verbose=1
        )

        # --- PHASE 2: Controlled Fine-Tuning ---
        print("\n=== STARTING PHASE 2: Controlled Fine-Tuning (Unfreezing Top Backbone Layers) ===")
        model, p2_stats = ModelBuilder.configure_phase2(model, unfreeze_top_n_layers=unfreeze_top_n)

        optimizer_p2 = tf.keras.optimizers.Adam(learning_rate=lr_phase2)
        model.compile(
            optimizer=optimizer_p2,
            loss="categorical_crossentropy",
            metrics=["accuracy", tf.keras.metrics.MacroAverageF1Score(num_classes=8, name="macro_f1") if hasattr(tf.keras.metrics, "MacroAverageF1Score") else "categorical_accuracy"]
        )

        callbacks_p2 = [
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(best_checkpoint_path),
                monitor="val_loss",
                save_best_only=True,
                verbose=1
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=patience,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.CSVLogger(filename=str(csv_log_path), append=True)
        ]

        history_p2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs_phase1 + epochs_phase2,
            initial_epoch=epochs_phase1,
            class_weight=class_weights,
            callbacks=callbacks_p2,
            verbose=1
        )

        # Record training metadata
        summary_metadata = {
            "experiment_name": self.config.experiment_name,
            "seed": self.config.seed,
            "best_checkpoint_path": str(best_checkpoint_path),
            "csv_log_path": str(csv_log_path),
            "phase1_stats": p1_stats,
            "phase2_stats": p2_stats,
            "phase1_epochs_completed": len(history_p1.history["loss"]),
            "phase2_epochs_completed": len(history_p2.history["loss"]),
            "class_weights_used": class_weights
        }

        metadata_path = self.metrics_dir / "training_summary.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(summary_metadata, f, indent=2)

        return summary_metadata
