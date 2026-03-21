import pandas as pd
import os

print("Creating final dataset...")

# load datasets
ppac = pd.read_csv("data/processed/ppac_cleaned.csv")
ports = pd.read_csv("data/processed/ipa_cleaned.csv")

# clean column names
ppac.columns = ppac.columns.str.strip()
ports.columns = ports.columns.str.strip()

# calculate port share
total_traffic = ports["traffic_2025"].sum()
ports["port_share"] = ports["traffic_2025"] / total_traffic

rows = []

for _, p in ppac.iterrows():

    for _, port in ports.iterrows():

        row = {
            "Year": p["Year"],
            "port": port["port"],
            "product": p["product"],
            "import_export": p["import_export"],
            "Month": p["Month"],
            "quantity": float(p["quantity"]) * port["port_share"] if not pd.isna(p["quantity"]) else 0,
            "rupees": float(p["rupees"]) * port["port_share"] if not pd.isna(p["rupees"]) else 0,
            "dollars": float(p["dollars"]) * port["port_share"] if not pd.isna(p["dollars"]) else 0
        }

        rows.append(row)

final_df = pd.DataFrame(rows)

# aggregate (important if duplicates)
final_df = final_df.groupby(
    ["Year","port","product","import_export","Month"],
    as_index=False
).sum()

#  ensure folder exists (render fix)
os.makedirs("data/final", exist_ok=True)

# save file
final_df.to_csv("data/final/port_trade_dataset.csv", index=False)

print("Final dataset created successfully")
print("Rows:", len(final_df))