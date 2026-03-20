import pandas as pd

df = pd.read_csv(r"data/final/port_trade_dataset.csv")

# remove rows where port is numeric
df = df[~df["port"].astype(str).str.isnumeric()]

# fill missing values
df["quantity"] = df["quantity"].fillna(0)
df["rupees"] = df["rupees"].fillna(0)
df["dollars"] = df["dollars"].fillna(0)

# remove duplicates
df = df.drop_duplicates()

df.to_csv(r"data/final/port_trade_dataset_clean.csv", index=False)

print("Dataset cleaned")