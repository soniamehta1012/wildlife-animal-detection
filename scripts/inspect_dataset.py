from pathlib import Path
import yaml

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset directories
IMAGES_DIR = PROJECT_ROOT / "images"
LABELS_DIR = PROJECT_ROOT / "labels"
DATA_YAML = PROJECT_ROOT / "data.yaml"


def count_files(folder, extensions):
    """Count files with the given extensions inside a folder."""
    if not folder.exists():
        return 0

    return sum(
        1
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    )


def main():
    print("=" * 60)
    print("WILDLIFE DATASET INSPECTION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Check important directories/files
    # ---------------------------------------------------------

    print("\n[1] Checking dataset structure...")

    print(f"Images directory : {IMAGES_DIR}")
    print(f"Labels directory : {LABELS_DIR}")
    print(f"data.yaml        : {DATA_YAML}")

    print("\nImages folder exists:", IMAGES_DIR.exists())
    print("Labels folder exists:", LABELS_DIR.exists())
    print("data.yaml exists   :", DATA_YAML.exists())

    # ---------------------------------------------------------
    # 2. Read class names from data.yaml
    # ---------------------------------------------------------

    print("\n[2] Reading class information...")

    with open(DATA_YAML, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    class_names = data.get("names", [])

    print(f"Number of classes: {len(class_names)}")

    print("\nClass IDs and names:")

    for class_id, class_name in enumerate(class_names):
        print(f"{class_id:3d} -> {class_name}")

    # ---------------------------------------------------------
    # 3. Count images
    # ---------------------------------------------------------

    print("\n[3] Counting images...")

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    train_images = count_files(
        IMAGES_DIR / "train",
        image_extensions
    )

    val_images = count_files(
        IMAGES_DIR / "val",
        image_extensions
    )

    print("Training images  :", train_images)
    print("Validation images:", val_images)
    print("Total images     :", train_images + val_images)

    # ---------------------------------------------------------
    # 4. Count label files
    # ---------------------------------------------------------

    print("\n[4] Counting label files...")

    label_extensions = {".txt"}

    train_labels = count_files(
        LABELS_DIR / "train",
        label_extensions
    )

    val_labels = count_files(
        LABELS_DIR / "val",
        label_extensions
    )

    print("Training labels  :", train_labels)
    print("Validation labels:", val_labels)
    print("Total labels     :", train_labels + val_labels)

    # ---------------------------------------------------------
    # 5. Final message
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("DATASET INSPECTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()