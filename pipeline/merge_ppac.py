import pandas as pd
import os

print("Loading PPAC raw datasets...")

# -------------------------------
# LOAD RAW FILES
# -------------------------------
qty = pd.read_csv("data/raw/ppac_quantity_2023-2025.csv")
rs = pd.read_csv("data/raw/ppac_rupees_2023-2025.csv")
usd = pd.read_csv("data/raw/ppac_dollars_2023-2025.csv")

# Add metric column
qty["metric"] = "quantity"
rs["metric"] = "rupees"
usd["metric"] = "dollars"

# Combine all
df = pd.concat([qty, rs, usd], ignore_index=True)

print("Raw datasets combined")

# -------------------------------
# RENAME COLUMN (SAFE FIX)
# -------------------------------
# handle different possible names
for col in df.columns:
    col_clean = col.strip().upper().replace(" ", "")
    if "IMPORT" in col_clean and "EXPORT" in col_clean:
        df = df.rename(columns={col: "product"})
        break

# -------------------------------
# CREATE import_export COLUMN
# -------------------------------
mode = "Import"
trade_type = []

for val in df["product"]:
    val = str(val).upper()

    if "EXPORT" in val:
        mode = "Export"
        trade_type.append(None)

    elif "IMPORT" in val:
        mode = "Import"
        trade_type.append(None)

    else:
        trade_type.append(mode)

df["import_export"] = trade_type

# remove unwanted rows
df = df[df["import_export"].notna()]
df = df[~df["product"].str.contains("TOTAL|NET", case=False, na=False)]

# -------------------------------
# MONTH PROCESSING (SAFE)
# -------------------------------
months = [
    "April","May","June","July","August","September",
    "October","November","December","January","February","March"
]

# keep only existing columns
available_months = [m for m in months if m in df.columns]

print("Available month columns:", available_months)

for m in available_months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# -------------------------------
# WIDE → LONG
# -------------------------------
df_long = df.melt(
    id_vars=["Year", "product", "import_export", "metric"],
    value_vars=available_months,
    var_name="Month",
    value_name="Value"
)

df_long = df_long.dropna(subset=["Value"])

# -------------------------------
# FINAL PIVOT
# -------------------------------
df_final = df_long.pivot_table(
    index=["Year", "product", "import_export", "Month"],
    columns="metric",
    values="Value",
    aggfunc="sum"
).reset_index()

df_final.columns.name = None

# -------------------------------
# SAVE FILE
# -------------------------------
os.makedirs("data/processed", exist_ok=True)

df_final.to_csv("data/processed/ppac_combined.csv", index=False)

print("PPAC combined dataset created")
print("Rows:", len(df_final))