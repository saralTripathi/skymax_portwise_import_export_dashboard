import pandas as pd

file_path = r"data\raw\ipa_ports.csv"

df = pd.read_csv(file_path)

# drop fully empty columns
df = df.dropna(axis=1, how="all")

# drop rows that are fully empty
df = df.dropna(how="all")

# reset index
df = df.reset_index(drop=True)

# remove header rows that contain text
df = df[~df.iloc[:,1].astype(str).str.contains("TRAFFIC|PORTS|TARGET|TOTAL", na=False)]

# rename columns based on position
df = df.iloc[:, [1,3]]   # port name and traffic column

df.columns = ["port", "traffic_2025"]

# remove rows with missing port
df = df.dropna()

# remove TOTAL rows if present
df = df[~df["port"].str.contains("TOTAL", case=False)]

df.to_csv("data/processed/ipa_cleaned.csv", index=False)

print("IPA dataset cleaned successfully")