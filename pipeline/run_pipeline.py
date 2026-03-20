import os

print("===== PIPELINE STARTED =====")

# 1 PPAC scraping
print("Running PPAC scraper...")
os.system("python scraper/ppac_import_export_scraper.py")

# 2 IPA scraping
print("Running IPA scraper...")
os.system("python scraper/ipa_scraper.py")

# 3 Merge PPAC datasets
print("Merging PPAC datasets...")
os.system("python pipeline/merge_ppac.py")

# 4 Clean PPAC dataset
print("Cleaning PPAC dataset...")
os.system("python pipeline/clean_ppac_dataset.py")

# 5 Clean IPA dataset
print("Cleaning IPA dataset...")
os.system("python pipeline/clean_ipa_data.py")

# 6 Merge port + trade data
print("Merging port trade...")
os.system("python pipeline/merge_port_trade.py")

# 7 Create final dataset
print("Creating final dataset...")
os.system("python pipeline/create_final_dataset.py")

# 8 Clean final dataset
print("Cleaning final dataset...")
os.system("python pipeline/clean_final_dataset.py")

# validation step
os.system("python pipeline/data_validation.py")

# 9 Load to PostgreSQL
print("Loading data to PostgreSQL...")
os.system("python database/load_to_db.py")

print("API is ready to serve data at http://localhost:8000")
os.system("uvicorn api.app:app --reload")

print("===== PIPELINE COMPLETED SUCCESSFULLY =====")
