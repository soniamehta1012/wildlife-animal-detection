from pathlib import Path
import csv
from ultralytics import YOLO
import yaml
import shutil

# ============================================================
# TASK 4.3 — APPLY B YOLO ANNOTATIONS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_YAML = ROOT / "data.yaml"
IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"
REVIEW_FILE = ROOT / "scripts" / "final_ab_review.csv"

BACKUP_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train_backup_before_task_4_3"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}

# ------------------------------------------------------------
# CHECK PATHS
# ------------------------------------------------------------

if not DATA_YAML.exists():
    print("ERROR: data.yaml not found.")
    raise SystemExit(1)

if not IMAGE_DIR.exists():
    print("ERROR: image directory not found.")
    print(IMAGE_DIR)
    raise SystemExit(1)

if not LABEL_DIR.exists():
    print("ERROR: label directory not found.")
    print(LABEL_DIR)
    raise SystemExit(1)

if not REVIEW_FILE.exists():
    print("ERROR: final_ab_review.csv not found.")
    print(REVIEW_FILE)
    raise SystemExit(1)

# ------------------------------------------------------------
# READ DATASET CLASSES
# ------------------------------------------------------------

with open(DATA_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]

class_to_id = {
    str(name).lower(): index
    for index, name in enumerate(names)
}

# ------------------------------------------------------------
# SUPPORTED COCO ANIMAL CLASSES
# ------------------------------------------------------------

SUPPORTED_ANIMALS = {
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
# READ B IMAGES
# ------------------------------------------------------------

b_images = []

with open(REVIEW_FILE, "r", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        if row["category"].strip().upper() == "B":
            b_images.append(row["image"])

print("=" * 60)
print("TASK 4.3 — APPLY B YOLO ANNOTATIONS")
print("=" * 60)

print(f"B images to process : {len(b_images)}")

# ------------------------------------------------------------
# CREATE BACKUP
# ------------------------------------------------------------

if BACKUP_DIR.exists():
    print("\nBackup directory already exists.")
else:
    BACKUP_DIR.mkdir(parents=True)

for image_name in b_images:

    label_file = LABEL_DIR / (Path(image_name).stem + ".txt")

    if label_file.exists():

        backup_file = BACKUP_DIR / label_file.name

        if not backup_file.exists():
            shutil.copy2(label_file, backup_file)

print(f"Backup created at:")
print(BACKUP_DIR)

# ------------------------------------------------------------
# LOAD YOLO
# ------------------------------------------------------------

print("\nLoading YOLO model...")

model = YOLO("yolov8n.pt")

# ------------------------------------------------------------
# PROCESS B IMAGES
# ------------------------------------------------------------

annotated = 0
no_detection = 0
total_boxes = 0

for index, image_name in enumerate(b_images, start=1):

    image_path = None

    for extension in IMAGE_EXTENSIONS:

        candidate = IMAGE_DIR / (
            Path(image_name).stem + extension
        )

        if candidate.exists():
            image_path = candidate
            break

    if image_path is None:
        print(f"WARNING: Image not found: {image_name}")
        continue

    print(
        f"Processing {index}/{len(b_images)}: "
        f"{image_name}"
    )

    result = model(
        str(image_path),
        conf=0.20,
        verbose=False
    )[0]

    annotation_lines = []

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = str(model.names[class_id]).lower()

        # Only supported animal detections
        if class_name not in SUPPORTED_ANIMALS:
            continue

        # Dataset must contain this class
        if class_name not in class_to_id:
            print(
                f"  Skipping {class_name}: "
                f"not present in dataset classes"
            )
            continue

        dataset_class_id = class_to_id[class_name]

        # YOLO normalized coordinates
        x_center, y_center, width, height = (
            box.xywhn[0].tolist()
        )

        annotation_lines.append(
            f"{dataset_class_id} "
            f"{x_center:.6f} "
            f"{y_center:.6f} "
            f"{width:.6f} "
            f"{height:.6f}"
        )

    label_path = LABEL_DIR / (
        Path(image_name).stem + ".txt"
    )

    if annotation_lines:

        with open(
            label_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(annotation_lines) + "\n"
            )

        annotated += 1
        total_boxes += len(annotation_lines)

    else:

        no_detection += 1

print()
print("=" * 60)
print("TASK 4.3 — B ANNOTATION RESULTS")
print("=" * 60)

print(f"B images processed     : {len(b_images)}")
print(f"Images annotated       : {annotated}")
print(f"Images with no boxes   : {no_detection}")
print(f"Total YOLO boxes       : {total_boxes}")

print()
print(f"Original labels backed up to:")
print(BACKUP_DIR)

print("=" * 60)
print("Task 4.3 B annotation step completed.")
print("=" * 60)
