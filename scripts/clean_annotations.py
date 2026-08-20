from pathlib import Path

# --------------------------------------------------
# TASK 4 — ANNOTATION VALIDATION & CLEANING
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):
    content = label_file.read_text(encoding="utf-8").strip()

    if not content:
        empty_labels.append(label_file)

print("=" * 60)
print("TASK 4 — ANNOTATION CLEANING")
print("=" * 60)

print("\nTraining label directory:")
print(LABEL_DIR)

print("\nEmpty label files:", len(empty_labels))

print("\nFirst 20 empty labels:")
for label_file in empty_labels[:20]:
    print(label_file.name)

print("\nAnalysis completed.")
