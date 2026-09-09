from pathlib import Path
from PIL import Image, ImageDraw
import math

ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "dataset" / "cleaned" / "images" / "train"
LABEL_DIR = ROOT / "dataset" / "cleaned" / "labels" / "train"

OUTPUT_DIR = ROOT / "empty_annotation_batches"
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

empty_labels = []

for label_file in LABEL_DIR.glob("*.txt"):
    if not label_file.read_text(encoding="utf-8").strip():
        empty_labels.append(label_file)

images = []

for label_file in empty_labels:
    for ext in IMAGE_EXTENSIONS:
        image_file = IMAGE_DIR / (label_file.stem + ext)
        if image_file.exists():
            images.append(image_file)
            break

print("Total empty-label images:", len(images))

# Create batches of 20
BATCH_SIZE = 20

for batch_no in range(math.ceil(len(images) / BATCH_SIZE)):

    batch = images[
        batch_no * BATCH_SIZE:
        (batch_no + 1) * BATCH_SIZE
    ]

    thumb_w = 250
    thumb_h = 180

    cols = 4
    rows = math.ceil(len(batch) / cols)

    sheet = Image.new(
        "RGB",
        (cols * thumb_w, rows * (thumb_h + 30)),
        "white"
    )

    draw = ImageDraw.Draw(sheet)

    for i, image_path in enumerate(batch):

        img = Image.open(image_path).convert("RGB")
        img.thumbnail((thumb_w - 10, thumb_h - 10))

        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + 30)

        sheet.paste(
            img,
            (
                x + (thumb_w - img.width) // 2,
                y
            )
        )

        draw.text(
            (x + 5, y + thumb_h),
            f"{i + 1}. {image_path.stem}",
            fill="black"
        )

    output_file = OUTPUT_DIR / f"batch_{batch_no + 1:02d}.jpg"
    sheet.save(output_file, quality=85)

    print(f"Created: {output_file}")

print("\nAll batches created.")