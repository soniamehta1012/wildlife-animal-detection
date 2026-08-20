from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def get_images(folder):
    return {
        file.stem: file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS
    }


def get_labels(folder):
    return {
        file.stem
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() == ".txt"
    }


def check_split(split):
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    images = get_images(image_dir)
    labels = get_labels(label_dir)

    missing = set(images.keys()) - labels

    print(f"\n{split.upper()}")
    print("-" * 50)
    print(f"Images : {len(images)}")
    print(f"Labels : {len(labels)}")
    print(f"Missing labels : {len(missing)}")

    if missing:
        print("\nFirst 20 images without labels:")

        for name in sorted(missing)[:20]:
            print(images[name].name)

    # Save a report instead of changing the dataset
    report_file = ROOT / f"missing_labels_{split}.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        for name in sorted(missing):
            file.write(str(images[name]) + "\n")

    print(f"\nReport saved to: {report_file}")

def main():
    print("=" * 60)
    print("MISSING LABEL ANALYSIS")
    print("=" * 60)

    check_split("train")
    check_split("val")

    print("\nAnalysis completed.")
    print("No images or labels were modified.")


if __name__ == "__main__":
    main()