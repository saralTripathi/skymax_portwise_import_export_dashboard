import pandas as pd

print("Creating final dataset...")

# load datasets
ppac = pd.read_csv(r"data/processed/ppac_cleaned.csv")
ports = pd.read_csv(r"data/processed/ipa_cleaned.csv")

# calculate port share
total_traffic = ports["traffic_2025"].sum()
ports["port_share"] = ports["traffic_2025"] / total_traffic

# months
months = [
"April","May","June","July","August","September",
"October","November","December","January","February","March"
]

rows = []

for _, p in ppac.iterrows():

    metric = p["metric"]   # quantity / rupees / dollars
    
    for _, port in ports.iterrows():

        for m in months:

            value = p[m]

            if pd.isna(value):
                continue

            distributed_value = float(value) * port["port_share"]

            row = {
                "Year": p["Year"],
                "port": port["port"],
                "product": p["IMPORT/EXPORT"],
                "import_export": "IMPORT" if "IMPORT" in p["IMPORT/EXPORT"] else "EXPORT",
                "Month": m,
                "quantity": 0,
                "rupees": 0,
                "dollars": 0
            }

            if metric == "quantity":
                row["quantity"] = distributed_value
            elif metric == "rupees":
                row["rupees"] = distributed_value
            elif metric == "dollars":
                row["dollars"] = distributed_value

            rows.append(row)

final_df = pd.DataFrame(rows)

# aggregate duplicates
final_df = final_df.groupby(
    ["Year","port","product","import_export","Month"],
    as_index=False
).sum()

final_df.to_csv("data/final/port_trade_dataset.csv", index=False)

print("Final merged dataset created")
print("Rows:", len(final_df))
