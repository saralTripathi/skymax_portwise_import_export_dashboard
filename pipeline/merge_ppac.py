import pandas as pd

print("Loading PPAC dataset...")

df = pd.read_csv("data\\processed\\ppac_combined.csv")

# rename column
df = df.rename(columns={"IMPORT/EXPORT": "product"})

# detect import/export sections
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

# remove header rows
df = df[df["import_export"].notna()]

# remove TOTAL rows
df = df[~df["product"].str.contains("TOTAL|NET", case=False, na=False)]

months = [
"April","May","June","July","August","September",
"October","November","December","January","February","March"
]

# convert months to numeric
for m in months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# convert wide → long
df_long = df.melt(
    id_vars=["Year","product","import_export","metric"],
    value_vars=months,
    var_name="Month",
    value_name="Value"
)

df_long = df_long.dropna(subset=["Value"])

# pivot metrics
df_final = df_long.pivot_table(
    index=["Year","product","import_export","Month"],
    columns="metric",
    values="Value",
    aggfunc="sum"
).reset_index()

df_final.columns.name = None

df_final.to_csv(
    "data/processed/ppac_clean.csv",
    index=False
)

print("PPAC cleaned dataset created")
print("Rows:", len(df_final))