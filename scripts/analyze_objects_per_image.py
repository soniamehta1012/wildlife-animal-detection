from pathlib import Path
from collections import Counter

# Use the project directory from which the script is run
ROOT = Path.cwd()

TRAIN_LABELS = ROOT / "labels" / "train"
VAL_LABELS = ROOT / "labels" / "val"

# Original class IDs of our final 40 selected classes
SELECTED_OLD_IDS = {
    10, 15, 20, 4, 6, 13, 9, 17,
    8, 51, 3, 53, 12, 22, 60, 72,
    5, 34, 23, 11, 1, 63, 71, 27,
    39, 65, 62, 59, 50, 47, 31, 54,
    2, 7, 14, 19, 41, 58, 70, 73
}

print("ROOT:", ROOT)
print("TRAIN LABELS:", TRAIN_LABELS)
print("VAL LABELS:", VAL_LABELS)

# Check paths
if not TRAIN_LABELS.exists():
    print("ERROR: labels/train does not exist.")
    exit()

if not VAL_LABELS.exists():
    print("ERROR: labels/val does not exist.")
    exit()

object_counts = []

for label_dir in [TRAIN_LABELS, VAL_LABELS]:

    print(f"\nReading: {label_dir}")

    label_files = list(label_dir.glob("*.txt"))

    print("Label files found:", len(label_files))

    for label_file in label_files:

        selected_objects = 0

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) < 5:
                    continue

                class_id = int(parts[0])

                if class_id in SELECTED_OLD_IDS:
                    selected_objects += 1

        # Only count images that contain at least
        # one of our selected 40 classes
        if selected_objects > 0:
            object_counts.append(selected_objects)


# Distribution
distribution = Counter(object_counts)

print("\n======================================")
print("       OBJECTS PER IMAGE ANALYSIS")
print("======================================")

total_images_with_animals = len(object_counts)

print("\nImages containing selected animals:",
      total_images_with_animals)

print("\nDistribution:")

print("1 animal  :", distribution[1])
print("2 animals :", distribution[2])
print("3 animals :", distribution[3])
print("4 animals :", distribution[4])
print("5 animals :", distribution[5])

six_or_more = sum(
    count for objects, count in distribution.items()
    if objects >= 6
)

print("6+ animals:", six_or_more)

two_or_more = sum(
    count for objects, count in distribution.items()
    if objects >= 2
)

three_or_more = sum(
    count for objects, count in distribution.items()
    if objects >= 3
)

print("\n---------- GROUP IMAGES ----------")

print("Images with 2+ animals:", two_or_more)
print("Images with 3+ animals:", three_or_more)

if object_counts:
    print(
        "Maximum animals in one image:",
        max(object_counts)
    )

print("\n======================================")