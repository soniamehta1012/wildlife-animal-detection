from pathlib import Path
from collections import Counter
import yaml

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_YAML = ROOT / "data.yaml"

TRAIN_LABELS = ROOT / "labels" / "train"
VAL_LABELS = ROOT / "labels" / "val"


# --------------------------------------------------
# READ DATA.YAML
# --------------------------------------------------

with open(DATA_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]


# --------------------------------------------------
# FINAL 40 CLASSES
# Original IDs from data.yaml
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
# FUNCTION TO COUNT OBJECTS
# --------------------------------------------------

def count_objects(label_folder):

    counter = Counter()

    if not label_folder.exists():
        return counter

    for label_file in label_folder.glob("*.txt"):

        with open(label_file, "r", encoding="utf-8") as f:

            for line in f:

                parts = line.strip().split()

                if len(parts) < 5:
                    continue

                try:
                    class_id = int(parts[0])
                except ValueError:
                    continue

                if class_id in SELECTED_CLASSES:
                    counter[class_id] += 1

    return counter


# --------------------------------------------------
# COUNT TRAIN AND VALIDATION
# --------------------------------------------------

train_counts = count_objects(TRAIN_LABELS)
val_counts = count_objects(VAL_LABELS)


# --------------------------------------------------
# PRINT REPORT
# --------------------------------------------------

print("\n" + "=" * 90)
print("TASK 5E — TRAIN / VALIDATION CLASS ANALYSIS")
print("=" * 90)

print(
    f"\n{'New ID':<8}"
    f"{'Class':<38}"
    f"{'Train':>10}"
    f"{'Val':>10}"
    f"{'Total':>10}"
)

print("-" * 90)

total_train = 0
total_val = 0

for new_id, (old_id, class_name) in enumerate(SELECTED_CLASSES.items()):

    train = train_counts[old_id]
    val = val_counts[old_id]
    total = train + val

    total_train += train
    total_val += val

    print(
        f"{new_id:<8}"
        f"{class_name:<38}"
        f"{train:>10}"
        f"{val:>10}"
        f"{total:>10}"
    )


print("-" * 90)

print(
    f"{'TOTAL':<46}"
    f"{total_train:>10}"
    f"{total_val:>10}"
    f"{total_train + total_val:>10}"
)

print("=" * 90)

print("\nAnalysis complete.")
print("No files were modified.")