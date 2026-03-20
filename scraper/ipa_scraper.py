import requests
import pandas as pd
import os

# IPA dataset link
url = "https://www.ipa.nic.in/WriteReadData/Links/Major%20Ports%20Traffic%20for%20April%20to%20March%2020259e57b7d3-36b9-4462-874f-da2431e33413.xlsx"

# raw folder
save_dir = r"data\raw"
os.makedirs(save_dir, exist_ok=True)

excel_path = os.path.join(save_dir, "ipa_ports.xlsx")
csv_path = os.path.join(save_dir, "ipa_ports.csv")

print("Downloading IPA port data...")

response = requests.get(url)

with open(excel_path, "wb") as f:
    f.write(response.content)

print("Excel downloaded")

# Excel read
df = pd.read_excel(excel_path)

# column clean
df.columns = df.columns.str.strip()

# CSV save
df.to_csv(csv_path, index=False)

print("CSV saved:", csv_path)