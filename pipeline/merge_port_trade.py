import pandas as pd

print("Loading datasets")

ppac = pd.read_csv("data\\processed\\ppac_cleaned.csv")

ports = pd.read_csv("data\\processed\\ipa_cleaned.csv")

ports = ports[["port"]]

final = ppac.merge(ports, how="cross")

final = final[
    ["Year","port","product","import_export","Month","quantity","rupees","dollars"]
]

final.to_csv(
    r"data\final\port_trade_dataset_clean.csv",
    index=False
)

print("Final dataset created")