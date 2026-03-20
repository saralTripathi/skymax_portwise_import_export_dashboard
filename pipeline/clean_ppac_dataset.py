import pandas as pd

file_path = r"data/processed/ppac_cleaned.csv"

df = pd.read_csv(file_path)

# 🔥 detect correct column
col_name = None

for col in df.columns:
    col_clean = col.strip().upper().replace(" ", "")
    if "IMPORT" in col_clean and "EXPORT" in col_clean:
        col_name = col
        break

if not col_name:
    raise Exception(" IMPORT/EXPORT column not found")

print(f"Using column: {col_name}")

# remove rows where product column is empty
df = df[df[col_name].notna()]

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
    df = df[~df[col_name].str.contains(p, case=False, na=False)]

# remove section headers
bad_rows = [
    "IMPORT^",
    "PRODUCTS",
    "PRODUCT IMPORT",
    "PRODUCT EXPORT",
]

df = df[~df[col_name].isin(bad_rows)]

# clean product names
df[col_name] = df[col_name].str.replace(r"[^\w\s/]", "", regex=True)

# convert month columns
months = [
"April","May","June","July","August","September",
"October","November","December","January","February","March","Total"
]

for m in months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# remove invalid rows
df = df[df["Total"].notna()]
df = df[df["Total"] > 0]

df.to_csv("data/processed/ppac_cleaned.csv", index=False)

print(" PPAC dataset cleaned successfully")