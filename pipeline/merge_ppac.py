import pandas as pd
import os

print(" Loading PPAC raw datasets...")

# -------------------------------
# LOAD RAW FILES (FIXED)
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

print(" Raw datasets combined")

# -------------------------------
# CLEANING
# -------------------------------

# rename column safely
df = df.rename(columns={"IMPORT/EXPORT": "product"})

# detect import/export
mode = "Import"
trade_type = []

for val in df["product"]:
    val = str(val)

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
# MONTH PROCESSING
# -------------------------------
months = [
    "April","May","June","July","August","September",
    "October","November","December","January","February","March"
]

for m in months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# -------------------------------
# WIDE → LONG
# -------------------------------
df_long = df.melt(
    id_vars=["Year","product","import_export","metric"],
    value_vars=months,
    var_name="Month",
    value_name="Value"
)

df_long = df_long.dropna(subset=["Value"])

# -------------------------------
# FINAL PIVOT
# -------------------------------
df_final = df_long.pivot_table(
    index=["Year","product","import_export","Month"],
    columns="metric",
    values="Value",
    aggfunc="sum"
).reset_index()

df_final.columns.name = None

# -------------------------------
# SAVE FILE (IMPORTANT FIX)
# -------------------------------
os.makedirs("data/processed", exist_ok=True)

df_final.to_csv(
    "data/processed/ppac_combined.csv",   # 🔥 IMPORTANT NAME FIX
    index=False
)

print(" PPAC combined dataset created")
print("Rows:", len(df_final))