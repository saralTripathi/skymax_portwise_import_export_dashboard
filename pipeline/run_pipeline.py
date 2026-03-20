import subprocess

print("===== PIPELINE STARTED =====")

def run_step(script_name):
    print(f"\n Running: {script_name}")
    
    result = subprocess.run(["python3", script_name])
    
    if result.returncode != 0:
        raise Exception(f" {script_name} failed. Stopping pipeline.")
    
    print(f"✅ Completed: {script_name}")


# 1 PPAC scraping
run_step("scraper/ppac_import_export_scraper.py")

# 2 IPA scraping
run_step("scraper/ipa_scraper.py")

# 3 Merge PPAC datasets
run_step("pipeline/merge_ppac.py")

# 4 Clean PPAC dataset
run_step("pipeline/clean_ppac_dataset.py")

# 5 Clean IPA dataset
run_step("pipeline/clean_ipa_data.py")

# 6 Merge port + trade data
run_step("pipeline/merge_port_trade.py")

# 7 Create final dataset
run_step("pipeline/create_final_dataset.py")

# 8 Clean final dataset
run_step("pipeline/clean_final_dataset.py")

# 9 Validation
run_step("pipeline/data_validation.py")

# 10 Load to PostgreSQL
run_step("database/load_to_db.py")

print("\n ===== PIPELINE COMPLETED SUCCESSFULLY =====")