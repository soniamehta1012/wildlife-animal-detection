from pathlib import Path
from ultralytics import YOLO

# ============================================================
# TASK 4.2 — FINAL A/B REVIEW
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

# ------------------------------------------------------------
# Find empty labels
# ------------------------------------------------------------

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):

    content = label_file.read_text(
        encoding="utf-8"
    ).strip()

    if not content:
        empty_labels.append(label_file)


# ------------------------------------------------------------
# Find corresponding images
# ------------------------------------------------------------

images = []

for label_file in empty_labels:

    for extension in IMAGE_EXTENSIONS:

        image_file = IMAGE_DIR / (
            label_file.stem + extension
        )

        if image_file.exists():

            images.append(image_file)
            break


# ------------------------------------------------------------
# Load YOLO model
# ------------------------------------------------------------

print("Loading YOLO model...")

model = YOLO("yolov8n.pt")


# ------------------------------------------------------------
# Animal classes
# ------------------------------------------------------------

ANIMAL_CLASSES = {
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
# Classification
# ------------------------------------------------------------

A_count = 0
B_count = 0

for image_path in images:

    result = model(
        str(image_path),
        conf=0.20,
        verbose=False
    )[0]

    animal_found = False

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name in ANIMAL_CLASSES:

            animal_found = True
            break

    if animal_found:

        B_count += 1

    else:

        A_count += 1


# ------------------------------------------------------------
# FINAL OUTPUT
# ------------------------------------------------------------

print()
print("=" * 50)
print("TASK 4.2 — FINAL A/B REVIEW")
print("=" * 50)

print(f"Total empty-label images : {len(images)}")
print(f"A - Legitimate negative  : {A_count}")
print(f"B - Animal present       : {B_count}")

print("=" * 50)
print("Task 4.2 analysis completed.")