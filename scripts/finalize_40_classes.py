from pathlib import Path
import shutil

# ============================================================
# TASK 5 — FINALIZE 40 ANIMAL CLASSES
# ============================================================
# This script:
# 1. Reads the original 74-class dataset
# 2. Keeps only the selected 40 classes
# 3. Remaps original class IDs to new IDs 0–39
# 4. Creates a separate cleaned dataset
# 5. Creates the final data.yaml
#
# IMPORTANT:
# The original images/ and labels/ folders are NEVER modified.
# ============================================================


# ============================================================
# 1. PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

# Original dataset
ORIGINAL_IMAGES = ROOT / "images"
ORIGINAL_LABELS = ROOT / "labels"

# New cleaned dataset
CLEANED_ROOT = ROOT / "dataset" / "cleaned"
CLEANED_IMAGES = CLEANED_ROOT / "images"
CLEANED_LABELS = CLEANED_ROOT / "labels"


# ============================================================
# 2. ORIGINAL CLASS ID → NEW CLASS ID
# ============================================================

CLASS_MAPPING = {
    10: 0,    # lion
    15: 1,    # tiger
    20: 2,    # bear
    4: 3,     # elephant
    6: 4,     # giraffe
    13: 5,    # rhinoceros
    9: 6,     # hippopotamus
    17: 7,    # zebra
    8: 8,     # gorilla
    51: 9,    # monkey
    3: 10,    # deer
    53: 11,   # mule_deer
    12: 12,   # moose
    22: 13,   # bison
    60: 14,   # pronghorn
    72: 15,   # wild_boar
    5: 16,    # fox
    34: 17,   # coyote
    23: 18,   # bobcat
    11: 19,   # mongoose
    1: 20,    # alligator
    63: 21,   # rattlesnake
    71: 22,   # western_diamondback_rattlesnake
    27: 23,   # california_sea_lion
    39: 24,   # elephant_seal
    65: 25,   # river_otter
    62: 26,   # raccoon
    59: 27,   # porcupine
    50: 28,   # marten
    47: 29,   # jackrabbit
    31: 30,   # chipmunk
    54: 31,   # muskrat
    2: 32,    # crow
    7: 33,    # goldfinch
    14: 34,   # sparrow
    19: 35,   # bald_eagle
    41: 36,   # golden_eagle
    58: 37,   # peacock
    70: 38,   # turkey_vulture
    73: 39,   # wild_turkey
}


# ============================================================
# 3. FINAL CLASS NAMES
# ============================================================

CLASS_NAMES = [
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


# ============================================================
# 4. IMAGE EXTENSIONS
# ============================================================

IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
]


# ============================================================
# 5. CREATE CLEANED DATASET DIRECTORIES
# ============================================================

for split in ["train", "val"]:
    (CLEANED_IMAGES / split).mkdir(parents=True, exist_ok=True)
    (CLEANED_LABELS / split).mkdir(parents=True, exist_ok=True)


# ============================================================
# 6. STATISTICS
# ============================================================

stats = {
    "train": {
        "label_files": 0,
        "selected_images": 0,
        "discarded_images": 0,
        "original_annotations": 0,
        "selected_annotations": 0,
        "missing_images": 0,
    },
    "val": {
        "label_files": 0,
        "selected_images": 0,
        "discarded_images": 0,
        "original_annotations": 0,
        "selected_annotations": 0,
        "missing_images": 0,
    },
}


# ============================================================
# 7. FIND CORRESPONDING IMAGE
# ============================================================

def find_image(image_dir, stem):
    """
    Find the image corresponding to a label file.
    """

    for extension in IMAGE_EXTENSIONS:
        image_path = image_dir / f"{stem}{extension}"

        if image_path.exists():
            return image_path

    return None


# ============================================================
# 8. PROCESS TRAIN AND VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("TASK 5 — FINALIZING 40-CLASS DATASET")
print("=" * 70)

print("\nOriginal dataset:")
print(ORIGINAL_IMAGES)
print(ORIGINAL_LABELS)

print("\nCleaned dataset:")
print(CLEANED_ROOT)

print("\nProcessing...")


for split in ["train", "val"]:

    print("\n" + "-" * 70)
    print(f"PROCESSING {split.upper()}")
    print("-" * 70)

    image_dir = ORIGINAL_IMAGES / split
    label_dir = ORIGINAL_LABELS / split

    output_image_dir = CLEANED_IMAGES / split
    output_label_dir = CLEANED_LABELS / split

    if not image_dir.exists():
        print(f"ERROR: Image directory not found: {image_dir}")
        continue

    if not label_dir.exists():
        print(f"ERROR: Label directory not found: {label_dir}")
        continue

    label_files = list(label_dir.glob("*.txt"))

    print(f"Label files found: {len(label_files)}")

    for label_file in label_files:

        stats[split]["label_files"] += 1

        selected_lines = []

        # ----------------------------------------------------
        # READ LABEL FILE
        # ----------------------------------------------------

        with open(label_file, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                parts = line.split()

                # YOLO format:
                # class_id x_center y_center width height

                if len(parts) < 5:
                    continue

                try:
                    original_class_id = int(parts[0])
                except ValueError:
                    continue

                stats[split]["original_annotations"] += 1

                # ------------------------------------------------
                # KEEP ONLY SELECTED CLASSES
                # ------------------------------------------------

                if original_class_id not in CLASS_MAPPING:
                    continue

                # ------------------------------------------------
                # REMAP CLASS ID
                # ------------------------------------------------

                new_class_id = CLASS_MAPPING[original_class_id]

                parts[0] = str(new_class_id)

                selected_lines.append(" ".join(parts))

                stats[split]["selected_annotations"] += 1

        # ----------------------------------------------------
        # DISCARD IMAGE IF NO SELECTED CLASS EXISTS
        # ----------------------------------------------------

        if not selected_lines:

            stats[split]["discarded_images"] += 1

            continue

        # ----------------------------------------------------
        # FIND CORRESPONDING IMAGE
        # ----------------------------------------------------

        image_file = find_image(
            image_dir,
            label_file.stem
        )

        if image_file is None:

            stats[split]["missing_images"] += 1

            print(
                f"WARNING: Image not found for "
                f"{label_file.name}"
            )

            continue

        # ----------------------------------------------------
        # COPY IMAGE
        # ----------------------------------------------------

        destination_image = (
            output_image_dir / image_file.name
        )

        shutil.copy2(
            image_file,
            destination_image
        )

        # ----------------------------------------------------
        # WRITE REMAPPED LABEL
        # ----------------------------------------------------

        destination_label = (
            output_label_dir / label_file.name
        )

        with open(
            destination_label,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n".join(selected_lines)
                + "\n"
            )

        stats[split]["selected_images"] += 1


# ============================================================
# 9. CREATE FINAL DATA.YAML
# ============================================================

DATA_YAML = CLEANED_ROOT / "data.yaml"

with open(
    DATA_YAML,
    "w",
    encoding="utf-8"
) as file:

    file.write("path: .\n")
    file.write("train: images/train\n")
    file.write("val: images/val\n")
    file.write("nc: 40\n")
    file.write("names:\n")

    for class_name in CLASS_NAMES:
        file.write(f"  - {class_name}\n")


# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("TASK 5 — FINALIZATION SUMMARY")
print("=" * 70)

for split in ["train", "val"]:

    print("\n" + split.upper())

    print(
        f"Label files processed : "
        f"{stats[split]['label_files']}"
    )

    print(
        f"Images selected       : "
        f"{stats[split]['selected_images']}"
    )

    print(
        f"Images discarded      : "
        f"{stats[split]['discarded_images']}"
    )

    print(
        f"Original annotations  : "
        f"{stats[split]['original_annotations']}"
    )

    print(
        f"Selected annotations  : "
        f"{stats[split]['selected_annotations']}"
    )

    print(
        f"Missing images        : "
        f"{stats[split]['missing_images']}"
    )


# ============================================================
# 11. TOTALS
# ============================================================

total_selected_images = (
    stats["train"]["selected_images"]
    + stats["val"]["selected_images"]
)

total_selected_annotations = (
    stats["train"]["selected_annotations"]
    + stats["val"]["selected_annotations"]
)

total_discarded_images = (
    stats["train"]["discarded_images"]
    + stats["val"]["discarded_images"]
)

total_missing_images = (
    stats["train"]["missing_images"]
    + stats["val"]["missing_images"]
)


print("\n" + "-" * 70)
print("TOTAL")
print("-" * 70)

print(
    f"Selected images       : "
    f"{total_selected_images}"
)

print(
    f"Discarded images      : "
    f"{total_discarded_images}"
)

print(
    f"Selected annotations  : "
    f"{total_selected_annotations}"
)

print(
    f"Missing images        : "
    f"{total_missing_images}"
)

print(
    f"Final number of classes: 40"
)

print(
    f"\nCleaned dataset saved at:"
)
print(CLEANED_ROOT)

print(
    f"\nFinal data.yaml:"
)
print(DATA_YAML)

print("\nOriginal dataset was NOT modified.")

print("\n" + "=" * 70)
print("TASK 5 — 40 CLASS DATASET FINALIZATION COMPLETE")
print("=" * 70)