from fastapi import FastAPI
import psycopg2
import pandas as pd
import numpy as np

app = FastAPI()


def get_connection():

    conn = psycopg2.connect(
        database="petroleum_trade",
        user="postgres",
        password="Saral@2004",
        host="localhost",
        port="5432"
    )

    return conn


@app.get("/")
def home():
    return {"message": "Petroleum Trade API running"}


@app.get("/trade-data")
def get_trade_data():

    conn = get_connection()

    query = "SELECT * FROM trade_data"

    df = pd.read_sql(query, conn)

    conn.close()

    # FIX NaN values
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")
