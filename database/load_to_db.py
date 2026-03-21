import pandas as pd
import os
from sqlalchemy import create_engine

print("Loading final dataset...")

# ✅ correct file path (your latest pipeline output)
file_path = os.path.join("data", "final", "port_trade_dataset_clean.csv")

# check file exists
if not os.path.exists(file_path):
    raise Exception(f"File not found: {file_path}")

df = pd.read_csv(file_path)

print("Dataset loaded successfully")
print("Rows:", len(df))

# ✅ get DATABASE_URL from environment (Render)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL not set in environment variables")

print("Connecting to database...")

# create engine
engine = create_engine(DATABASE_URL)

# 🔥 FAST upload (replaces slow loop)
df.to_sql(
    "trade_data",        # table name
    engine,
    if_exists="replace", # or "append" if needed
    index=False
)

print("Data loaded to database successfully")