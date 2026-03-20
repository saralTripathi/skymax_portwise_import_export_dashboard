import pandas as pd
import psycopg2

print("Loading final dataset...")

df = pd.read_csv(r"data\final\port_trade_dataset.csv")

conn = psycopg2.connect(
    database="petroleum_trade",
    user="postgres",
    password="Saral@2004",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

print("Inserting data into database...")

for _, row in df.iterrows():

    cursor.execute(
        """
        INSERT INTO trade_data (
        year,
        port,
        product,
        import_export,
        month,
        quantity,
        rupees,
        dollars
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            row["Year"],
            row["port"],
            row["product"],
            row["import_export"],
            row["Month"],
            row["quantity"],
            row["rupees"],
            row["dollars"]
        )
    )

conn.commit()

cursor.close()
conn.close()

print("Data inserted successfully")