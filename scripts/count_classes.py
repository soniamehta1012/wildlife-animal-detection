from pathlib import Path
from collections import Counter
import yaml
import re

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_YAML = ROOT / "data.yaml"
LABEL_DIR = ROOT / "labels" / "train"


# --------------------------------------------------
# READ CLASS NAMES
# --------------------------------------------------

with open(DATA_YAML, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]


# --------------------------------------------------
# COUNT ANNOTATED OBJECTS
# --------------------------------------------------

counter = Counter()
empty_labels = []


for label_file in LABEL_DIR.glob("*.txt"):

    with open(label_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Empty label file
    if not content:
        empty_labels.append(label_file.stem)
        continue

    # Count annotated objects
    for line in content.splitlines():

        parts = line.strip().split()

        if len(parts) < 5:
            continue

        try:
            class_id = int(parts[0])
            counter[class_id] += 1

        except ValueError:
            continue


# --------------------------------------------------
# ANIMAL CLASS DISTRIBUTION
# --------------------------------------------------

print()
print("ANIMAL CLASS DISTRIBUTION")
print("-" * 50)

total = 0

for class_id, class_name in enumerate(names):

    count = counter[class_id]
    total += count

    if count > 0:
        print(f"{class_name:<40} {count:5}")


print("-" * 50)
print(f"Total annotated objects : {total}")


# --------------------------------------------------
# EMPTY LABEL DISTRIBUTION
# --------------------------------------------------

empty_counter = Counter()

# Sort class names by length so that names such as
# "american_black_bear" are matched before shorter names.
sorted_names = sorted(names, key=len, reverse=True)


for filename in empty_labels:

    matched = False

    for class_name in sorted_names:

        # Empty label filenames generally look like:
        # animal_123
        #
        # Example:
        # american_black_bear_103

        pattern = rf"^{re.escape(class_name)}_\d+$"

        if re.match(pattern, filename):
            empty_counter[class_name] += 1
            matched = True
            break

    if not matched:
        empty_counter["UNKNOWN"] += 1


# --------------------------------------------------
# PRINT EMPTY LABEL DISTRIBUTION
# --------------------------------------------------

print()
print("EMPTY LABEL DISTRIBUTION")
print("-" * 50)

for class_name, count in empty_counter.most_common():
    print(f"{class_name:<40} {count:5}")

print("-" * 50)
print(f"Total empty label files : {len(empty_labels)}")
print()