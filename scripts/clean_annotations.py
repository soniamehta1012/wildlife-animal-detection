from pathlib import Path

# ============================================================
# TASK 4 — EMPTY ANNOTATION INVESTIGATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"
REPORT_FILE = ROOT / "scripts" / "empty_annotation_report.txt"

if not LABEL_DIR.exists():
    print("ERROR: Label directory not found.")
    print(LABEL_DIR)
    raise SystemExit(1)

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):

    if label_file.stat().st_size == 0:
        empty_labels.append(label_file)

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("TASK 4 — EMPTY ANNOTATION INVESTIGATION\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        f"Total empty annotation files: "
        f"{len(empty_labels)}\n\n"
    )

    f.write("Empty annotation files:\n")

    for label_file in empty_labels:
        f.write(f"{label_file.name}\n")

print("=" * 60)
print("TASK 4 — EMPTY ANNOTATION INVESTIGATION")
print("=" * 60)

print(f"Empty label files : {len(empty_labels)}")
print(f"Report saved to   : {REPORT_FILE}")

print("\nInvestigation completed.")


