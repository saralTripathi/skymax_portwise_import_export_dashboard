from fastapi import FastAPI
import pandas as pd
import os
from sqlalchemy import create_engine

app = FastAPI()



DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL not found. Set it in environment variables.")

engine = create_engine(DATABASE_URL)


@app.get("/")
def home():
    return {"message": "Petroleum Trade API running 🚀"}




@app.get("/trade-data")
def get_trade_data():
    try:
        query = "SELECT * FROM trade_data"
        df = pd.read_sql(query, engine)

        # ✅ Fix NaN issue (important for JSON)
        df = df.fillna(0)

        return df.to_dict(orient="records")

    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to fetch data from database"
        }