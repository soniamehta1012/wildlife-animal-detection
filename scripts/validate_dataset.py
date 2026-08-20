from pathlib import Path
import yaml

# --------------------------------------------------
# DATASET VALIDATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

IMAGE_DIRS = [
    ROOT / "images" / "train",
    ROOT / "images" / "val"
]

LABEL_DIRS = [
    ROOT / "labels" / "train",
    ROOT / "labels" / "val"
]


def get_images(folder):
    return {
        file.stem: file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    }


def get_labels(folder):
    return {
        file.stem: file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".txt"
    }


# --------------------------------------------------
# READ DATA.YAML
# --------------------------------------------------

print("=" * 60)
print("WILDLIFE DATASET VALIDATION")
print("=" * 60)

yaml_path = ROOT / "data.yaml"

with open(yaml_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

names = data["names"]

print("\nNumber of classes:", len(names))

print("\nClasses:")
for class_id, class_name in enumerate(names):
    print(f"{class_id} -> {class_name}")


# --------------------------------------------------
# CHECK EACH SPLIT
# --------------------------------------------------

total_missing_labels = 0
total_extra_labels = 0
total_empty_labels = 0
total_invalid_labels = 0
total_invalid_classes = 0
total_invalid_boxes = 0


for split in ["train", "val"]:

    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    print("\n" + "-" * 60)
    print(f"CHECKING {split.upper()} DATA")
    print("-" * 60)

    images = get_images(image_dir)
    labels = get_labels(label_dir)

    print("Images:", len(images))
    print("Labels:", len(labels))

    # ----------------------------------------------
    # Images without labels
    # ----------------------------------------------

    missing_labels = set(images.keys()) - set(labels.keys())

    print("\nImages without labels:", len(missing_labels))

    if missing_labels:
        print("First 10 examples:")
        for name in list(missing_labels)[:10]:
            print("  ", images[name].name)

    total_missing_labels += len(missing_labels)

    # ----------------------------------------------
    # Labels without images
    # ----------------------------------------------

    extra_labels = set(labels.keys()) - set(images.keys())

    print("\nLabels without images:", len(extra_labels))

    if extra_labels:
        print("First 10 examples:")
        for name in list(extra_labels)[:10]:
            print("  ", labels[name].name)

    total_extra_labels += len(extra_labels)

    # ----------------------------------------------
    # Validate label contents
    # ----------------------------------------------

    empty_labels = 0
    invalid_labels = 0
    invalid_classes = 0
    invalid_boxes = 0

    for label_file in labels.values():

        try:
            content = label_file.read_text(encoding="utf-8").strip()

            # Empty label file
            if not content:
                empty_labels += 1
                continue

            for line_number, line in enumerate(content.splitlines(), start=1):

                parts = line.split()

                # YOLO format should have 5 values
                if len(parts) != 5:
                    invalid_labels += 1
                    continue

                try:
                    class_id = int(parts[0])
                    x, y, width, height = map(float, parts[1:])
                except ValueError:
                    invalid_labels += 1
                    continue

                # Class ID check
                if class_id < 0 or class_id >= len(names):
                    invalid_classes += 1

                # Bounding box range check
                if not (
                    0 <= x <= 1
                    and 0 <= y <= 1
                    and 0 <= width <= 1
                    and 0 <= height <= 1
                ):
                    invalid_boxes += 1

        except Exception:
            invalid_labels += 1

    print("\nEmpty label files:", empty_labels)
    print("Malformed label entries:", invalid_labels)
    print("Invalid class IDs:", invalid_classes)
    print("Invalid bounding boxes:", invalid_boxes)

    total_empty_labels += empty_labels
    total_invalid_labels += invalid_labels
    total_invalid_classes += invalid_classes
    total_invalid_boxes += invalid_boxes


# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL VALIDATION SUMMARY")
print("=" * 60)

print("Images without labels :", total_missing_labels)
print("Labels without images :", total_extra_labels)
print("Empty label files     :", total_empty_labels)
print("Malformed labels      :", total_invalid_labels)
print("Invalid class IDs     :", total_invalid_classes)
print("Invalid bounding boxes:", total_invalid_boxes)

print("\nDataset validation completed.")