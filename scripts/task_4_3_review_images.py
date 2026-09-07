from pathlib import Path
import shutil
import csv

# ============================================================
# TASK 4.3 — VISUAL REVIEW BATCH CREATION
# ============================================================

ROOT = Path(__file__).resolve().parent

IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
MANIFEST = ROOT / "scripts" / "task_4_3_review_manifest.csv"

OUTPUT_DIR = ROOT / "empty_annotation_batches"

BATCH_SIZE = 50

# ------------------------------------------------------------
# Check required files
# ------------------------------------------------------------

if not IMAGE_DIR.exists():
    print("ERROR: Image directory not found.")
    print(IMAGE_DIR)
    raise SystemExit(1)

if not MANIFEST.exists():
    print("ERROR: Review manifest not found.")
    print(MANIFEST)
    raise SystemExit(1)

# ------------------------------------------------------------
# Read manifest
# ------------------------------------------------------------

with open(MANIFEST, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("=" * 60)
print("TASK 4.3 — VISUAL REVIEW BATCH CREATION")
print("=" * 60)

print(f"Images to review : {len(rows)}")

# ------------------------------------------------------------
# Create output directory
# ------------------------------------------------------------

OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Create batches
# ------------------------------------------------------------

batch_number = 1

for start in range(0, len(rows), BATCH_SIZE):

    batch_rows = rows[start:start + BATCH_SIZE]

    batch_dir = OUTPUT_DIR / f"batch_{batch_number:02d}"

    batch_dir.mkdir(exist_ok=True)

    for row in batch_rows:

        image_name = row["image"]

        source = IMAGE_DIR / image_name

        if source.exists():

            destination = batch_dir / image_name

            shutil.copy2(source, destination)

    batch_number += 1

# ------------------------------------------------------------
# Final output
# ------------------------------------------------------------

total_batches = batch_number - 1

print()
print(f"Review batches created : {total_batches}")
print(f"Images per batch       : {BATCH_SIZE}")

print()
print("Review directory:")
print(OUTPUT_DIR)

print()
print("Original dataset was NOT modified.")

print("=" * 60)
print("Task 4.3 visual review preparation completed.")
print("=" * 60)
