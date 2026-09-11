from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEANED_YAML = ROOT / "dataset" / "cleaned" / "data.yaml"

BEFORE = {
    "Classes": 74,
    "Train Images": 9764,
    "Validation Images": 1778,
    "Train Labels": 9764,
    "Validation Labels": 1778,
    "Empty Labels": 528,
    "Total Annotations": 16659,
}

AFTER = {
    "Classes": 40,
    "Train Images": 6636,
    "Validation Images": 1135,
    "Train Labels": 6636,
    "Validation Labels": 1135,
    "Empty Labels": 0,
    "Total Annotations": 11616,
}

def print_comparison():
    print()
    print("=" * 70)
    print("          DATASET CLEANING — BEFORE vs AFTER")
    print("=" * 70)
    print()
    print(f"{'Metric':<30} {'BEFORE':>15} {'AFTER':>15}")
    print("-" * 70)

    for metric in BEFORE:
        print(f"{metric:<30} {BEFORE[metric]:>15,} {AFTER[metric]:>15,}")

    print("-" * 70)
    print()
    print("Cleaning Result:")
    print(f"  Classes:       {BEFORE['Classes']}  ->  {AFTER['Classes']}")
    print(f"  Empty labels:  {BEFORE['Empty Labels']}  ->  {AFTER['Empty Labels']}")
    print(f"  Annotations:   {BEFORE['Total Annotations']}  ->  {AFTER['Total Annotations']}")

    print(f"  Final data.yaml: {'FOUND' if CLEANED_YAML.exists() else 'NOT FOUND'}")

    print()
    print("=" * 70)
    print("          BEFORE/AFTER COMPARISON COMPLETED")
    print("=" * 70)
    print()

if __name__ == "__main__":
    print_comparison()