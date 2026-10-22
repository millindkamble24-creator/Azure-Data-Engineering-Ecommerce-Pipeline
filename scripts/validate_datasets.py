from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "data" / "source"

files = {
    "customer.csv": 10_000,
    "products.csv": 1_000,
    "orders.csv": 50_000,
    "order_items.csv": 100_000,
    "payments.csv": 50_000,
    "returns.csv": 5_000,
    "website_events.json": 100_000
}

print("\nDATASET VALIDATION")
print("=" * 55)

for filename, expected_rows in files.items():
    path = SOURCE_DIR / filename

    if not path.exists():
        print(f"FAILED: Missing file: {filename}")
        continue

    if filename.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_json(path, lines=True)

    actual_rows = len(df)

    print(f"\nFile: {filename}")
    print(f"Expected rows: {expected_rows:,}")
    print(f"Actual rows:   {actual_rows:,}")
    print(f"Columns:       {list(df.columns)}")

    if actual_rows == expected_rows:
        print("Status: PASS")
    else:
        print("Status: FAIL")

print("\nValidation completed.")
