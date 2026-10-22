from pathlib import Path
import pandas as pd
#==========================
#PROJECT CONFIGURATION
#==========================

BASE_DIR=Path(__file__).resolve().parent
SOURCE_DIR=BASE_DIR/"data"/"source"

# ==========================
# LOAD DATASETS
# ===========================

def load_dataset(filename):
    path=SOURCE_DIR/filename
    if not path.exists():
        print(f"WARNING: Missing file: {filename}")
        return None
    if filename.endswith(".csv"):
        return pd.read_csv(path)
    if filename.endswith(".json"):
        return pd.read_json(path,lines=True)
    raise ValueError(f"Unsupported file format:{filename}"  )

# ================================
# PROFIL A DATASET
# ================================

def profile_dataset(filename):
    df=load_dataset(filename)
    if df is None:
        return
    print("\n"+ "=" * 70)
    print(f"DATASET:{filename}")
    print("=" * 70)

    #1. Row and column count
    print("\n1. DATASET SIZE")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    #2. Column names and data types
    print("\n2. COLUMN DATA TYPES")
    print(df.dtypes)

    #3. Missing values
    print("\n3. MISSING VALUES")
    print(df.isnull().sum())

    #4. Duplicate complete rows
    print("\n4. DUPLICATE ROWS")
    print("Duplicate rows:",df.duplicated().sum())

    #5. Unique values
    print("\n5. UNIQUE VALUES PER COLUMN")
    print(df.nunique(dropna=True))

    #6. Numeric statistics
    print("\n6. NUMERIC COLUMN STATISTICS")
    print(df.describe().to_string())

    #7. Sample records
    print("\n7. SAMPLE RECORDS")
    print(df.head(5).to_string(index=False))

    # ===========================================
    # MAIN WORKFLOW
    # ===========================================

def main():
    datasets=[
        "customer.csv",
        "products.csv",
        "orders.csv",
        "order_items.csv",
        "payments.csv",
        "returns.csv",
        "website_events.json",
    ]
    for filename in datasets:
        profile_dataset(filename)
if __name__=="__main__":
    main()
