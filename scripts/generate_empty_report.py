from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"
REPORT_FILE = ROOT / "empty_annotation_report.txt"

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):
    if not label_file.read_text(encoding="utf-8").strip():
        empty_labels.append(label_file)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("TASK 4.2 - EMPTY ANNOTATION REPORT\n")
    f.write("=" * 60 + "\n")
    f.write(f"Total empty labels: {len(empty_labels)}\n\n")

    for label_file in empty_labels:
        f.write(label_file.name + "\n")

print("Report generated successfully.")
print("Total empty labels:", len(empty_labels))
print("Report:", REPORT_FILE)