from pathlib import Path
import shutil
import csv
import yaml

# ============================================================
# TASK 4.3 — CREATE CLEANED FINAL DATASET
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# SOURCE DATASET
# ------------------------------------------------------------

SOURCE_ROOT = ROOT / "dataset" / "task_4_3_resolved"

SOURCE_IMAGES = SOURCE_ROOT / "images" / "train"
SOURCE_LABELS = SOURCE_ROOT / "labels" / "train"

# ------------------------------------------------------------
# 152 UNRESOLVED B REVIEW FILE
# ------------------------------------------------------------

REVIEW_FILE = ROOT / "scripts" / "task_4_3_152_B_manual_review.csv"

# ------------------------------------------------------------
# FINAL DATASET
# ------------------------------------------------------------

FINAL_ROOT = ROOT / "dataset" / "cleaned_final"

FINAL_IMAGES = FINAL_ROOT / "images" / "train"
FINAL_LABELS = FINAL_ROOT / "labels" / "train"

FINAL_YAML = FINAL_ROOT / "data.yaml"

# ------------------------------------------------------------
# IMAGE EXTENSIONS
# ------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

print("=" * 60)
print("TASK 4.3 — CREATE CLEANED FINAL DATASET")
print("=" * 60)

# ------------------------------------------------------------
# CHECK SOURCE
# ------------------------------------------------------------

if not SOURCE_IMAGES.exists():
    print("ERROR: Source image directory not found:")
    print(SOURCE_IMAGES)
    raise SystemExit(1)

if not SOURCE_LABELS.exists():
    print("ERROR: Source label directory not found:")
    print(SOURCE_LABELS)
    raise SystemExit(1)

if not REVIEW_FILE.exists():
    print("ERROR: 152-image review file not found:")
    print(REVIEW_FILE)
    raise SystemExit(1)

# ------------------------------------------------------------
# READ 152 IMAGES TO EXCLUDE
# ------------------------------------------------------------

exclude_images = set()

with open(
    REVIEW_FILE,
    "r",
    encoding="utf-8",
    newline=""
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        image_name = row["image"].strip()

        if image_name:
            exclude_images.add(image_name)

print(f"Images marked for exclusion : {len(exclude_images)}")

# ------------------------------------------------------------
# SAFETY CHECK
# ------------------------------------------------------------

if len(exclude_images) != 152:

    print()
    print("WARNING:")
    print(f"Expected 152 images to exclude,")
    print(f"but found {len(exclude_images)}.")

    answer = input("Continue anyway? (yes/no): ").strip().lower()

    if answer != "yes":
        print("Operation cancelled.")
        raise SystemExit(0)

# ------------------------------------------------------------
# CREATE FINAL DIRECTORIES
# ------------------------------------------------------------

if FINAL_ROOT.exists():

    print()
    print("Existing cleaned_final dataset found.")
    print("Removing old cleaned_final dataset...")

    shutil.rmtree(FINAL_ROOT)

FINAL_IMAGES.mkdir(
    parents=True,
    exist_ok=True
)

FINAL_LABELS.mkdir(
    parents=True,
    exist_ok=True
)

# ------------------------------------------------------------
# FIND ALL SOURCE IMAGES
# ------------------------------------------------------------

source_images = []

for image_path in SOURCE_IMAGES.iterdir():

    if not image_path.is_file():
        continue

    if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
        continue

    source_images.append(image_path)

# ------------------------------------------------------------
# COPY DATASET EXCEPT 152 UNRESOLVED IMAGES
# ------------------------------------------------------------

copied_images = 0
copied_labels = 0
excluded_images = 0
missing_labels = 0

for image_path in source_images:

    # Exclude unresolved B image
    if image_path.name in exclude_images:

        excluded_images += 1
        continue

    # Copy image
    destination_image = FINAL_IMAGES / image_path.name

    shutil.copy2(
        image_path,
        destination_image
    )

    copied_images += 1

    # Corresponding YOLO label
    label_path = SOURCE_LABELS / (
        image_path.stem + ".txt"
    )

    if label_path.exists():

        destination_label = FINAL_LABELS / (
            image_path.stem + ".txt"
        )

        shutil.copy2(
            label_path,
            destination_label
        )

        copied_labels += 1

    else:

        missing_labels += 1

# ------------------------------------------------------------
# CREATE DATA.YAML
# ------------------------------------------------------------

SOURCE_YAML = ROOT / "data.yaml"

if SOURCE_YAML.exists():

    with open(
        SOURCE_YAML,
        "r",
        encoding="utf-8"
    ) as f:

        original_yaml = yaml.safe_load(f)

    # Preserve dataset class names
    names = original_yaml.get("names", [])

else:

    print()
    print("WARNING: Root data.yaml not found.")

    names = []

# Create YAML using final dataset paths
final_yaml_data = {
    "path": str(FINAL_ROOT),
    "train": "images/train",
    "val": "images/train",
    "nc": len(names),
    "names": names
}

with open(
    FINAL_YAML,
    "w",
    encoding="utf-8"
) as f:

    yaml.safe_dump(
        final_yaml_data,
        f,
        sort_keys=False,
        allow_unicode=True
    )

# ------------------------------------------------------------
# FINAL COUNTS
# ------------------------------------------------------------

final_image_count = len(
    list(FINAL_IMAGES.iterdir())
)

final_label_count = len(
    list(FINAL_LABELS.glob("*.txt"))
)

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print()
print("=" * 60)
print("CLEANED FINAL DATASET CREATED")
print("=" * 60)

print(f"Source images             : {len(source_images)}")
print(f"Excluded 152 images       : {excluded_images}")
print(f"Final images              : {final_image_count}")
print(f"Final labels              : {final_label_count}")
print(f"Missing labels            : {missing_labels}")
print(f"Dataset classes           : {len(names)}")

print()
print("FINAL DATASET:")
print(FINAL_ROOT)

print()
print("IMAGES:")
print(FINAL_IMAGES)

print()
print("LABELS:")
print(FINAL_LABELS)

print()
print("DATA YAML:")
print(FINAL_YAML)

print()
print("=" * 60)
print("TASK 4.3 CLEANED FINAL DATASET COMPLETED")
print("=" * 60)
