import pandas as pd

file_path = "data/processed/ppac_combined.csv"

df = pd.read_csv(file_path)

# remove rows where product column is empty
df = df[df["import_export"].notna()]

# remove rows containing text / notes
remove_patterns = [
    "Source",
    "Notes",
    "RIL",
    "LNG",
    "include",
    "export data",
]

for p in remove_patterns:
    df = df[~df["product"].str.contains(p, case=False, na=False)]

# remove section headers
bad_rows = [
    "IMPORT^",
    "PRODUCTS",
    "PRODUCT IMPORT",
    "PRODUCT EXPORT",
]

df = df[~df["product"].isin(bad_rows)]

# clean product names
df["product"] = df["product"].str.replace(r"[^\w\s/]", "", regex=True)

# convert numeric columns
for col in ["quantity", "rupees", "dollars"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# remove rows where all values are NaN
df = df.dropna(subset=["quantity", "rupees", "dollars"], how="all")

# save cleaned file
df.to_csv("data/processed/ppac_cleaned.csv", index=False)

print("PPAC dataset cleaned successfully")
print("Rows:", len(df))