from pathlib import Path
from ultralytics import YOLO
import yaml
import csv

# ============================================================
# TASK 4.2 — FINAL A/B REVIEW
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_YAML = ROOT / "data.yaml"
IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

OUTPUT_FILE = ROOT / "scripts" / "final_ab_review.csv"

# ------------------------------------------------------------
# Check paths
# ------------------------------------------------------------

if not DATA_YAML.exists():
    print("ERROR: data.yaml not found.")
    raise SystemExit(1)

if not IMAGE_DIR.exists():
    print("ERROR: Image directory not found.")
    print(IMAGE_DIR)
    raise SystemExit(1)

if not LABEL_DIR.exists():
    print("ERROR: Label directory not found.")
    print(LABEL_DIR)
    raise SystemExit(1)

# ------------------------------------------------------------
# Read dataset classes
# ------------------------------------------------------------

with open(DATA_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]

print("=" * 60)
print("TASK 4.2 — FINAL A/B REVIEW")
print("=" * 60)

print(f"Dataset classes : {len(names)}")

# ------------------------------------------------------------
# Find empty labels
# ------------------------------------------------------------

print("\nFinding empty-label files...")

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):

    if label_file.stat().st_size == 0:
        empty_labels.append(label_file)

print(f"Empty labels found : {len(empty_labels)}")

# ------------------------------------------------------------
# Find corresponding images
# ------------------------------------------------------------

images = []

for label_file in empty_labels:

    found = False

    for extension in IMAGE_EXTENSIONS:

        image_file = IMAGE_DIR / (
            label_file.stem + extension
        )

        if image_file.exists():

            images.append(image_file)
            found = True
            break

# ------------------------------------------------------------
# Load pretrained YOLO model
# ------------------------------------------------------------

print("\nLoading YOLO model...")

model = YOLO("yolov8n.pt")

# ------------------------------------------------------------
# COCO animal classes understood by YOLOv8n
# ------------------------------------------------------------

COCO_ANIMAL_CLASSES = {
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe"
}

# ------------------------------------------------------------
# Counters
# ------------------------------------------------------------

A_count = 0
B_count = 0

review_results = []

# ------------------------------------------------------------
# Analyze images
# ------------------------------------------------------------

for index, image_path in enumerate(images, start=1):

    print(
        f"Processing {index}/{len(images)}: "
        f"{image_path.name}"
    )

    result = model(
        str(image_path),
        conf=0.20,
        verbose=False
    )[0]

    detected_animals = []

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        if class_name in COCO_ANIMAL_CLASSES:

            detected_animals.append(
                f"{class_name} ({confidence:.2f})"
            )

    if detected_animals:

        B_count += 1

        review_results.append([
            image_path.name,
            "B",
            "; ".join(detected_animals)
        ])

    else:

        A_count += 1

        review_results.append([
            image_path.name,
            "A",
            "No supported animal detected"
        ])

# ------------------------------------------------------------
# Save review report
# ------------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "image",
        "category",
        "YOLO_detection"
    ])

    writer.writerows(review_results)

# ------------------------------------------------------------
# Final output
# ------------------------------------------------------------

print()
print("=" * 60)
print("TASK 4.2 — FINAL A/B REVIEW")
print("=" * 60)

print(f"Total empty-label images : {len(images)}")
print(f"A - Legitimate negative  : {A_count}")
print(f"B - Animal present       : {B_count}")

print()
print(f"Review report saved to:")
print(OUTPUT_FILE)

print("=" * 60)
print("Task 4.2 analysis completed.")
print("=" * 60)
