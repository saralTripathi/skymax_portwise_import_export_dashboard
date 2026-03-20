import pandas as pd

file_path = r"data/processed/ppac_cleaned.csv"

df = pd.read_csv(file_path)

# remove rows where product column is empty
df = df[df["IMPORT/EXPORT"].notna()]

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
    df = df[~df["IMPORT/EXPORT"].str.contains(p, case=False, na=False)]

# remove section headers
bad_rows = [
    "IMPORT^",
    "PRODUCTS",
    "PRODUCT IMPORT",
    "PRODUCT EXPORT",
]

df = df[~df["IMPORT/EXPORT"].isin(bad_rows)]

# clean product names (remove special symbols)
df["IMPORT/EXPORT"] = df["IMPORT/EXPORT"].str.replace(r"[^\w\s/]", "", regex=True)

# convert month columns to numeric
months = [
"April","May","June","July","August","September",
"October","November","December","January","February","March","Total"
]

for m in months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# remove rows where total is 0 or NaN
df = df[df["Total"].notna()]
df = df[df["Total"] > 0]

df.to_csv("data/processed/ppac_cleaned.csv", index=False)

print("PPAC dataset cleaned successfully")