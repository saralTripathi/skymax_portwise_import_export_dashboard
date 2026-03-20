import pandas as pd

print(" Cleaning PPAC dataset...")

# -------------------------------
# LOAD DATA
# -------------------------------
file_path = "data/processed/ppac_combined.csv"
df = pd.read_csv(file_path)

print("Columns BEFORE cleaning:", list(df.columns))

# -------------------------------
# STEP 1: CLEAN COLUMN NAMES (SAFE)
# -------------------------------
df.columns = df.columns.str.strip()

# -------------------------------
# STEP 2: DETECT IMPORT/EXPORT COLUMN
# -------------------------------
product_col = None

for col in df.columns:
    col_clean = col.upper().replace(" ", "")
    if "IMPORT" in col_clean and "EXPORT" in col_clean:
        product_col = col
        break

if not product_col:
    raise Exception("❌ IMPORT/EXPORT column not found")

print(f" Using column: {product_col}")

# -------------------------------
# STEP 3: REMOVE INVALID ROWS
# -------------------------------
df = df[df[product_col].notna()]

remove_patterns = ["Source", "Notes", "RIL", "LNG", "include", "export data"]

for p in remove_patterns:
    df = df[~df[product_col].str.contains(p, case=False, na=False)]

bad_rows = ["IMPORT^", "PRODUCTS", "PRODUCT IMPORT", "PRODUCT EXPORT"]
df = df[~df[product_col].isin(bad_rows)]

# clean text
df[product_col] = df[product_col].str.replace(r"[^\w\s/]", "", regex=True)

# -------------------------------
# STEP 4: STANDARDIZE MONTH COLUMNS (CONTROLLED)
# -------------------------------
month_map = {
    "APR": "April",
    "APRIL": "April",
    "MAY": "May",
    "JUN": "June",
    "JUNE": "June",
    "JUL": "July",
    "JULY": "July",
    "AUG": "August",
    "AUGUST": "August",
    "SEP": "September",
    "SEPT": "September",
    "SEPTEMBER": "September",
    "OCT": "October",
    "OCTOBER": "October",
    "NOV": "November",
    "NOVEMBER": "November",
    "DEC": "December",
    "DECEMBER": "December",
    "JAN": "January",
    "JANUARY": "January",
    "FEB": "February",
    "FEBRUARY": "February",
    "MAR": "March",
    "MARCH": "March",
    "TOTAL": "Total"
}

rename_dict = {}

for col in df.columns:
    col_upper = col.upper().strip()
    if col_upper in month_map:
        rename_dict[col] = month_map[col_upper]

df = df.rename(columns=rename_dict)

print("Columns AFTER standardization:", list(df.columns))

# -------------------------------
# STEP 5: ENSURE REQUIRED MONTHS EXIST
# -------------------------------
required_months = [
    "April","May","June","July","August","September",
    "October","November","December","January","February","March","Total"
]

for m in required_months:
    if m not in df.columns:
        print(f"⚠️ Missing column: {m} → filling with 0")
        df[m] = 0

# -------------------------------
# STEP 6: CONVERT TO NUMERIC
# -------------------------------
for m in required_months:
    df[m] = pd.to_numeric(df[m], errors="coerce")

# -------------------------------
# STEP 7: REMOVE INVALID DATA
# -------------------------------
df = df[df["Total"].notna()]
df = df[df["Total"] > 0]

# -------------------------------
# SAVE OUTPUT
# -------------------------------
df.to_csv("data/processed/ppac_cleaned.csv", index=False)

print("✅ PPAC dataset cleaned successfully")
print("Rows:", len(df))