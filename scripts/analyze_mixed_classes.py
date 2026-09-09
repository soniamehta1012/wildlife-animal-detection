from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL_DIRS = [
    ROOT / "labels" / "train",
    ROOT / "labels" / "val"
]

# Original IDs of the 40 selected classes
SELECTED_CLASSES = {
    10, 15, 20, 4, 6, 13, 9, 17, 8, 51,
    3, 53, 12, 22, 60, 72, 5, 34, 23, 11,
    1, 63, 71, 27, 39, 65, 62, 59, 50, 47,
    31, 54, 2, 7, 14, 19, 41, 58, 70, 73
}

only_selected = 0
only_discarded = 0
mixed = 0
empty = 0

for label_dir in LABEL_DIRS:

    if not label_dir.exists():
        continue

    for label_file in label_dir.glob("*.txt"):

        class_ids = set()

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                parts = line.strip().split()

                if len(parts) < 5:
                    continue

                try:
                    class_id = int(parts[0])
                    class_ids.add(class_id)
                except ValueError:
                    continue

        if not class_ids:
            empty += 1

        elif class_ids.issubset(SELECTED_CLASSES):
            only_selected += 1

        elif class_ids.isdisjoint(SELECTED_CLASSES):
            only_discarded += 1

        else:
            mixed += 1


print("\n" + "=" * 60)
print("TASK 5G — MIXED CLASS ANALYSIS")
print("=" * 60)

print(f"\nOnly selected classes     : {only_selected}")
print(f"Only discarded classes    : {only_discarded}")
print(f"Mixed selected/discarded  : {mixed}")
print(f"Empty label files         : {empty}")

print("\n" + "=" * 60)
print("NO FILES WERE MODIFIED")
print("=" * 60)