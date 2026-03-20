import pandas as pd

print("Starting data validation...")

df = pd.read_csv("data/final/port_trade_dataset_clean.csv")

# missing values
missing = df.isnull().sum()

if missing.any():
    print("WARNING: Missing values detected")
    print(missing)
else:
    print("No missing values found")


# check negative values

if (df["quantity"] < 0).any():
    print("WARNING: Negative values found in quantity")

if (df["rupees"] < 0).any():
    print("WARNING: Negative values found in rupees")

if (df["dollars"] < 0).any():
    print("WARNING: Negative values found in dollars")


# check unique ports

ports = df["port"].unique()

print("\nPorts detected:")
print(ports)


print("\nData validation completed")
