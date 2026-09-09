from pathlib import Path
from collections import Counter
from datetime import datetime

ROOT = Path.cwd()

TRAIN_LABELS = ROOT / "labels" / "train"
VAL_LABELS = ROOT / "labels" / "val"
REPORT_DIR = ROOT / "reports"
REPORT_FILE = REPORT_DIR / "dataset_report.md"

# Final 40 selected classes.
# These are the ORIGINAL class IDs from data.yaml.
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

train_counts = Counter()
val_counts = Counter()

train_images = 0
val_images = 0

train_empty = 0
val_empty = 0

train_object_counts_per_image = []
val_object_counts_per_image = []


def analyze_directory(label_dir, class_counter, object_counts):
    """
    Analyze one label directory.
    Returns:
        total label files,
        images containing selected classes,
        empty/no-selected-object images
    """

    total_files = 0
    images_with_selected = 0
    empty_images = 0

    if not label_dir.exists():
        return 0, 0, 0

    for label_file in label_dir.glob("*.txt"):

        total_files += 1
        selected_objects = 0

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) < 5:
                    continue

                try:
                    class_id = int(parts[0])
                except ValueError:
                    continue

                if class_id in SELECTED_CLASSES:
                    class_counter[class_id] += 1
                    selected_objects += 1

        if selected_objects > 0:
            images_with_selected += 1
            object_counts.append(selected_objects)
        else:
            empty_images += 1

    return total_files, images_with_selected, empty_images


# Analyze train
train_total, train_images, train_empty = analyze_directory(
    TRAIN_LABELS,
    train_counts,
    train_object_counts_per_image
)

# Analyze validation
val_total, val_images, val_empty = analyze_directory(
    VAL_LABELS,
    val_counts,
    val_object_counts_per_image
)


# Combine counts
total_counts = Counter()

for class_id in SELECTED_CLASSES:
    total_counts[class_id] = (
        train_counts[class_id] +
        val_counts[class_id]
    )


total_annotations = sum(total_counts.values())

train_annotations = sum(train_counts.values())
val_annotations = sum(val_counts.values())

all_object_counts = (
    train_object_counts_per_image +
    val_object_counts_per_image
)

distribution = Counter(all_object_counts)

images_with_selected = len(all_object_counts)

multi_animal_images = sum(
    count for objects, count in distribution.items()
    if objects >= 2
)

three_plus_images = sum(
    count for objects, count in distribution.items()
    if objects >= 3
)

maximum_objects = (
    max(all_object_counts)
    if all_object_counts
    else 0
)


# Create reports directory
REPORT_DIR.mkdir(exist_ok=True)


# Build Markdown report
report = []

report.append("# Wildlife Dataset Report\n")

report.append(
    f"**Last generated:** "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
)

report.append("## 1. Dataset Overview\n")

report.append("| Metric | Value |")
report.append("|---|---:|")
report.append(f"| Training label files | {train_total:,} |")
report.append(f"| Validation label files | {val_total:,} |")
report.append("| Final selected classes | 40 |")
report.append(f"| Training annotations | {train_annotations:,} |")
report.append(f"| Validation annotations | {val_annotations:,} |")
report.append(f"| Total selected annotations | {total_annotations:,} |")
report.append(
    f"| Images containing selected animals | "
    f"{images_with_selected:,} |"
)
report.append(
    f"| Images with 2+ animals | "
    f"{multi_animal_images:,} |"
)
report.append(
    f"| Images with 3+ animals | "
    f"{three_plus_images:,} |"
)
report.append(
    f"| Maximum annotated animals in one image | "
    f"{maximum_objects} |"
)

report.append("\n## 2. Objects Per Image\n")

report.append("| Objects in image | Number of images |")
report.append("|---|---:|")

for number in range(1, 6):
    report.append(
        f"| {number} | {distribution[number]:,} |"
    )

six_plus = sum(
    count for objects, count in distribution.items()
    if objects >= 6
)

report.append(f"| 6+ | {six_plus:,} |")


report.append("\n## 3. Final 40 Classes\n")

report.append("| New ID | Class | Train | Validation | Total |")
report.append("|---:|---|---:|---:|---:|")

# New IDs are assigned according to the order of the selected classes
# from Task 5.
selected_in_order = [
    "lion",
    "tiger",
    "bear",
    "elephant",
    "giraffe",
    "rhinoceros",
    "hippopotamus",
    "zebra",
    "gorilla",
    "monkey",
    "deer",
    "mule_deer",
    "moose",
    "bison",
    "pronghorn",
    "wild_boar",
    "fox",
    "coyote",
    "bobcat",
    "mongoose",
    "alligator",
    "rattlesnake",
    "western_diamondback_rattlesnake",
    "california_sea_lion",
    "elephant_seal",
    "river_otter",
    "raccoon",
    "porcupine",
    "marten",
    "jackrabbit",
    "chipmunk",
    "muskrat",
    "crow",
    "goldfinch",
    "sparrow",
    "bald_eagle",
    "golden_eagle",
    "peacock",
    "turkey_vulture",
    "wild_turkey",
]

name_to_old_id = {
    name: class_id
    for class_id, name in SELECTED_CLASSES.items()
}

for new_id, name in enumerate(selected_in_order):

    old_id = name_to_old_id[name]

    train = train_counts[old_id]
    val = val_counts[old_id]
    total = train + val

    report.append(
        f"| {new_id} | {name} | "
        f"{train:,} | {val:,} | {total:,} |"
    )


report.append("\n## 4. Dataset Validation Status\n")

report.append(
    "- Train images and labels were previously verified to match."
)
report.append(
    "- Validation images and labels were previously verified to match."
)
report.append(
    "- No malformed YOLO annotation entries were found."
)
report.append(
    "- No invalid class IDs were found."
)
report.append(
    "- No invalid bounding boxes were found."
)
report.append(
    "- 528 empty label files were identified during validation."
)
report.append(
    "- Empty-label images require review before final cleaning."
)


report.append("\n## 5. Multi-Animal Analysis\n")

report.append(
    f"The current dataset contains **{multi_animal_images:,} "
    f"images with two or more selected animals**."
)

report.append(
    f"There are **{three_plus_images:,} images with three or more "
    f"selected animals**."
)

report.append(
    "Therefore, the current dataset already contains a substantial "
    "amount of multi-animal training data. Replacing the dataset "
    "solely to obtain group-animal images is not currently justified."
)


report.append("\n## 6. Current Task 5 Status\n")

report.append("- Final target: 40 wildlife classes")
report.append("- Class names standardized")
report.append("- Original dataset preserved")
report.append("- Class-selection dry run completed")
report.append("- Train/validation class analysis completed")
report.append("- Multi-animal image analysis completed")
report.append(
    "- Next step: inspect highly crowded images and then create "
    "the cleaned 40-class dataset."
)


# Write report
REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print("======================================")
print("DATASET REPORT GENERATED")
print("======================================")
print(f"Report: {REPORT_FILE}")
print(f"Total selected annotations: {total_annotations:,}")
print(f"Images with selected animals: {images_with_selected:,}")
print(f"Images with 2+ animals: {multi_animal_images:,}")
print(f"Images with 3+ animals: {three_plus_images:,}")
print(f"Maximum objects in one image: {maximum_objects}")
print("======================================")