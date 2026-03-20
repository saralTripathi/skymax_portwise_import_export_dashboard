import requests
import pandas as pd
import re
import os
import time

url = "https://ppac.gov.in/AjaxController/getImportExports"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

reports = {
    "quantity": 1,
    "rupees": 2,
    "dollars": 3
}

years = [
    "2025-2026",
    "2024-2025",
    "2023-2024"
]


def clean_html(value):
    if value is None:
        return ""
    value = str(value)
    value = re.sub("<.*?>", "", value)
    return value.strip()


# RAW DATA PATH
save_dir = r"C:\Users\om\Desktop\trade_data_project\data\raw"
os.makedirs(save_dir, exist_ok=True)

year_label = f"{years[-1][:4]}-{years[0][:4]}"


def fetch_data(payload, retries=5):

    for attempt in range(retries):

        try:

            response = requests.post(
                url,
                data=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["result"]

        except Exception as e:

            print(f"Request failed (attempt {attempt+1}/{retries})")
            print(e)

            time.sleep(5)

    print("Skipping payload after multiple failures")
    return {}


for report_name, report_type in reports.items():

    all_rows = []

    for year in years:

        payload = {
            "financialYear": year,
            "reportBy": report_type,
            "pageId": "14"
        }

        data = fetch_data(payload)

        if not data:
            continue

        for key in data:

            item = data[key]

            row = {
                "Year": year,
                "IMPORT/EXPORT": clean_html(item.get("title")),
                "April": clean_html(item.get("april")),
                "May": clean_html(item.get("may")),
                "June": clean_html(item.get("june")),
                "July": clean_html(item.get("july")),
                "August": clean_html(item.get("august")),
                "September": clean_html(item.get("september")),
                "October": clean_html(item.get("october")),
                "November": clean_html(item.get("november")),
                "December": clean_html(item.get("december")),
                "January": clean_html(item.get("january")),
                "February": clean_html(item.get("february")),
                "March": clean_html(item.get("march")),
                "Total": clean_html(item.get("total"))
            }

            all_rows.append(row)

        print(f"Downloaded {year} for {report_name}")

        # Delay to avoid blocking
        time.sleep(2)

    df = pd.DataFrame(all_rows)

    filename = f"ppac_{report_name}_{year_label}.csv"
    filepath = os.path.join(save_dir, filename)

    df.to_csv(filepath, index=False)

    print(f"{filepath} saved with {len(df)} rows")


