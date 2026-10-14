"""
Sprint 2A CLI Entrypoint: 02_train_model.py
Orchestrates MobileNetV2 architecture building, class weight calculation, TF dataset loading,
and two-phase transfer learning training. Includes a --smoke_test flag to verify CPU forward/backward passes.
"""

import sys
import argparse
from pathlib import Path
import numpy as np
import tensorflow as tf

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from farmguard_ai.src.config import Config
from farmguard_ai.src.data.loader import DataLoader
from farmguard_ai.src.models.class_weights import ClassWeightCalculator
from farmguard_ai.src.models.builder import ModelBuilder
from farmguard_ai.src.models.trainer import ModelTrainer


def run_smoke_test(cfg: Config) -> None:
    """
    Executes a lightweight 1-epoch CPU smoke test on synthetic tensors
    to verify model construction, loss computation, and forward/backward gradient updates.
    """
    print("\n[SMOKE TEST] Running synthetic CPU forward/backward pass verification...")
    Config.set_seed(cfg.seed)

    # 1. Build Model
    model = ModelBuilder.build_mobilenet_v2(
        input_shape=(224, 224, 3),
        num_classes=8,
        dropout_rate=0.3
    )

    # 2. Generate Synthetic Micro-Batch (Batch size = 4)
    x_synthetic = np.random.uniform(low=-1.0, high=1.0, size=(4, 224, 224, 3)).astype(np.float32)
    y_synthetic = np.eye(8)[np.random.choice(8, 4)] # One-hot encoded labels

    synth_ds = tf.data.Dataset.from_tensor_slices((x_synthetic, y_synthetic)).batch(4)

    # 3. Configure Phase 1 & Compile
    model, p1_stats = ModelBuilder.configure_phase1(model)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="categorical_crossentropy", metrics=["accuracy"])

    # 4. Single Forward/Backward Pass
    history_p1 = model.fit(synth_ds, epochs=1, verbose=1)

    # 5. Configure Phase 2 & Compile
    model, p2_stats = ModelBuilder.configure_phase2(model, unfreeze_top_n_layers=30)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001), loss="categorical_crossentropy", metrics=["accuracy"])

    # 6. Single Forward/Backward Pass
    history_p2 = model.fit(synth_ds, epochs=1, verbose=1)

    print("[OK] CPU Smoke Test Completed Successfully! Architecture and gradient passes verified.")


def main():
    parser = argparse.ArgumentParser(description="FarmGuard X - Sprint 2A MobileNetV2 Training Pipeline")
    parser.add_argument("--config", type=str, default="farmguard_ai/configs/mobilenet_v2_int8.yaml", help="Path to YAML config file")
    parser.add_argument("--smoke_test", action="store_true", help="Run 1-epoch CPU smoke test on synthetic tensors")
    parser.add_argument("--gpu_run", action="store_true", help="Execute full two-phase training run")
    args = parser.parse_args()

    config_path = Path(args.config)
    print("=== FarmGuard X MobileNetV2 Training Pipeline (Sprint 2A) ===")
    print(f"Loading config from: {config_path}")

    cfg = Config.from_yaml(config_path)
    print(f"Experiment Name: {cfg.experiment_name}")
    print(f"Random Seed Locked: {cfg.seed}")

    manifest_csv = cfg.splits_dir / "split_manifest.csv"
    if not manifest_csv.exists():
        print(f"[ERROR] Split manifest not found at {manifest_csv}. Run scripts/01_prepare_data.py first.")
        sys.exit(1)

    # Calculate Class Weights strictly from Training split
    class_weights = ClassWeightCalculator.compute_weights_from_manifest(
        manifest_csv_path=manifest_csv,
        num_classes=cfg.num_classes,
        method=cfg.training_cfg.get("class_weight_method", "inverse_frequency")
    )
    print(f"[OK] Class Weights Computed (From Training Split ONLY):")
    for c_id, w in class_weights.items():
        label_name = cfg.APPROVED_LABELS[c_id]
        print(f"   - Class {c_id} ({label_name}): weight = {w:.4f}")

    if args.smoke_test or not args.gpu_run:
        run_smoke_test(cfg)
        print("\n=== Sprint 2A Training Pipeline Setup Verified ===")
        print("To launch the real GPU training run, execute:")
        print(f"python farmguard_ai/scripts/02_train_model.py --config {args.config} --gpu_run")
        return

    # Real GPU Training Run Execution
    print("\n=== Constructing TensorFlow Datasets ===")
    train_ds = DataLoader.build_dataset(manifest_csv, "train", cfg.image_size, cfg.training_cfg.get("batch_size", 32), cfg.num_classes, is_training=True, seed=cfg.seed)
    val_ds = DataLoader.build_dataset(manifest_csv, "val", cfg.image_size, cfg.training_cfg.get("batch_size", 32), cfg.num_classes, is_training=False, seed=cfg.seed)

    print("\n=== Instantiating MobileNetV2 Model ===")
    model = ModelBuilder.build_mobilenet_v2(input_shape=(224, 224, 3), num_classes=8, dropout_rate=cfg.training_cfg.get("dropout_rate", 0.3))

    trainer = ModelTrainer(config=cfg)
    trainer.train_two_phase(
        model=model,
        train_ds=train_ds,
        val_ds=val_ds,
        class_weights=class_weights,
        epochs_phase1=cfg.training_cfg.get("phase1_epochs", 15),
        lr_phase1=cfg.training_cfg.get("phase1_lr", 0.001),
        epochs_phase2=cfg.training_cfg.get("phase2_epochs", 30),
        lr_phase2=cfg.training_cfg.get("phase2_lr", 0.00001),
        patience=cfg.training_cfg.get("early_stopping_patience", 5)
    )


if __name__ == "__main__":
    main()
