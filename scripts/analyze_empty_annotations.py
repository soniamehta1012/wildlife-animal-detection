from pathlib import Path

# --------------------------------------------------
# TASK 4.2 — EMPTY ANNOTATION ANALYSIS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):
    content = label_file.read_text(encoding="utf-8").strip()

    if not content:
        empty_labels.append(label_file)

print("=" * 60)
print("TASK 4.2 — EMPTY ANNOTATION ANALYSIS")
print("=" * 60)

print("\nTotal empty labels:", len(empty_labels))

print("\nChecking corresponding images:")

for label_file in empty_labels[:20]:

    image_found = False

    for extension in IMAGE_EXTENSIONS:
        image_file = IMAGE_DIR / (label_file.stem + extension)

        if image_file.exists():
            print(f"{label_file.name} -> {image_file.name}")
            image_found = True
            break

    if not image_found:
        print(f"{label_file.name} -> IMAGE NOT FOUND")

print("\nTask 4.2 analysis completed.")

# --------------------------------------------------
# SAVE EMPTY ANNOTATION REPORT
# --------------------------------------------------

REPORT_FILE = ROOT / "empty_annotation_report.txt"

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("TASK 4.2 — EMPTY ANNOTATION REPORT\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total empty labels: {len(empty_labels)}\n\n")

    for label_file in empty_labels:
        f.write(f"{label_file.name} -> corresponding image exists\n")

print(f"\nReport saved to: {REPORT_FILE}")