import pandas as pd
import os

print("Loading datasets")

# Load datasets
ppac = pd.read_csv("data/processed/ppac_cleaned.csv")
ports = pd.read_csv("data/processed/ipa_cleaned.csv")

# 🔥 Clean column names (avoid hidden bugs)
ppac.columns = ppac.columns.str.strip()
ports.columns = ports.columns.str.strip()

# 🔥 Ensure required column exists
if "port" not in ports.columns:
    raise Exception("Column 'port' not found in IPA dataset")

# Keep only port column
ports = ports[["port"]].drop_duplicates()

print("Creating cross join...")

# Cross join
final = ppac.merge(ports, how="cross")

print("Cross join completed")
print("Rows:", len(final))

# 🔥 Ensure required columns exist in PPAC
required_cols = ["Year","product","import_export","Month","quantity","rupees","dollars"]

for col in required_cols:
    if col not in final.columns:
        raise Exception(f"Missing column in dataset: {col}")

# Reorder columns
final = final[
    ["Year","port","product","import_export","Month","quantity","rupees","dollars"]
]

# 🔥 CRITICAL FIX (your error)
os.makedirs("data/final", exist_ok=True)

# Save dataset
output_path = "data/final/port_trade_dataset_clean.csv"
final.to_csv(output_path, index=False)

print(f"Final dataset created successfully at {output_path}")