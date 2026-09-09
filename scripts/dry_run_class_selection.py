from pathlib import Path
from collections import Counter

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LABEL_DIRS = [
    BASE_DIR / "labels" / "train",
    BASE_DIR / "labels" / "val"
]

# --------------------------------------------------
# SELECTED 40 CLASSES
# Original class IDs from data.yaml
# --------------------------------------------------

SELECTED_CLASSES = {
    10: "lion",
    15: "tiger",
    20: "bear",
    4: "elephant",
    6: "giraffe",
    13: "rhinoceros",
    9: "hippopotamus",
    17: "zebra",
    8: "gorilla",
    51: "monkey",
    3: "deer",
    53: "mule_deer",
    12: "moose",
    22: "bison",
    60: "pronghorn",
    72: "wild_boar",
    5: "fox",
    34: "coyote",
    23: "bobcat",
    11: "mongoose",
    1: "alligator",
    63: "rattlesnake",
    71: "western_diamondback_rattlesnake",
    27: "california_sea_lion",
    39: "elephant_seal",
    65: "river_otter",
    62: "raccoon",
    59: "porcupine",
    50: "marten",
    47: "jackrabbit",
    31: "chipmunk",
    54: "muskrat",
    2: "crow",
    7: "goldfinch",
    14: "sparrow",
    19: "bald_eagle",
    41: "golden_eagle",
    58: "peacock",
    70: "turkey_vulture",
    73: "wild_turkey",
}

# --------------------------------------------------
# COUNTERS
# --------------------------------------------------

total_annotations = 0
selected_annotations = 0
discarded_annotations = 0

selected_class_counts = Counter()
discarded_class_counts = Counter()

selected_images = 0
images_with_discarded_classes = 0

# --------------------------------------------------
# PROCESS LABEL FILES
# --------------------------------------------------

for label_dir in LABEL_DIRS:

    if not label_dir.exists():
        print(f"WARNING: Folder not found: {label_dir}")
        continue

    for label_file in label_dir.glob("*.txt"):

        has_selected = False
        has_discarded = False

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                # YOLO format:
                # class_id x_center y_center width height

                try:
                    class_id = int(parts[0])
                except (ValueError, IndexError):
                    continue

                total_annotations += 1

                if class_id in SELECTED_CLASSES:

                    selected_annotations += 1
                    selected_class_counts[class_id] += 1
                    has_selected = True

                else:

                    discarded_annotations += 1
                    discarded_class_counts[class_id] += 1
                    has_discarded = True

        if has_selected:
            selected_images += 1

        if has_discarded:
            images_with_discarded_classes += 1


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("TASK 5D — DRY RUN CLASS SELECTION")
print("=" * 60)

print(f"\nTotal original annotations : {total_annotations}")
print(f"Selected annotations       : {selected_annotations}")
print(f"Annotations to discard     : {discarded_annotations}")

print(f"\nImages containing selected classes : {selected_images}")
print(f"Images containing discarded classes: {images_with_discarded_classes}")

print("\n" + "-" * 60)
print("SELECTED CLASS COUNTS")
print("-" * 60)

for class_id, name in sorted(
    SELECTED_CLASSES.items(),
    key=lambda x: x[1]
):
    print(
        f"{class_id:2d} -> {name:<35} "
        f"{selected_class_counts[class_id]}"
    )

print("\n" + "-" * 60)
print("DISCARDED CLASS COUNTS")
print("-" * 60)

for class_id, count in sorted(discarded_class_counts.items()):
    print(
        f"{class_id:2d} -> {count}"
    )

print("\n" + "=" * 60)
print("DRY RUN COMPLETE — NO FILES WERE MODIFIED")
print("=" * 60)