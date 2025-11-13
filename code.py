import pandas as pd
import numpy as np
from zipfile import ZipFile
from pathlib import Path

# === 1. Extract and Load Dataset ===
zip_path = "amazon.csv.zip"       # your zip file name
extract_path = "amazon_dataset_work"

with ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)

csv_path = str(next(Path(extract_path).rglob("*.csv")))
df = pd.read_csv(csv_path, low_memory=False)

print("Initial shape:", df.shape)
print("Initial columns:", df.columns.tolist())

# === 2. Clean String Columns ===
for col in df.select_dtypes(include='object'):
    df[col] = df[col].astype(str).str.strip().str.lower()
    df[col] = df[col].replace({'nan': np.nan})

# === 3. Convert Numeric-like Strings to Numbers ===
currency_cols = ['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']
for col in currency_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[$₹,%]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# === 4. Handle Missing Values ===
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        df[col].fillna(df[col].median(), inplace=True)
    else:
        mode_val = df[col].mode()
        if not mode_val.empty:
            df[col].fillna(mode_val[0], inplace=True)
        else:
            df[col].fillna('unknown', inplace=True)

# === 5. Remove Duplicates ===
before = df.shape[0]
df.drop_duplicates(inplace=True)
after = df.shape[0]
print(f"Removed {before - after} duplicate rows")

# === 6. Handle Outliers (IQR Capping) ===
for col in df.select_dtypes(include='number').columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[col] = df[col].clip(lower, upper)

# === 7. Standardize Column Names ===
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

# === 8. Save Cleaned Data ===
df.to_csv("cleaned_amazon.csv", index=False)
print("✅ Cleaned data saved to cleaned_amazon.csv")

# === 9. Summary ===
print("Final shape:", df.shape)
print("Data cleaning complete!")
