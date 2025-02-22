import logging
import internetarchive as ia
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, CONFIG_COLLECTION, AUTO_FETCH_ON_START
import os

LOG_FILE = "dataset_fetch.log"
MAX_LOG_LINES = 1000  # Maximum lines before truncation

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def truncate_log():
    """Remove the oldest 1000 lines from the log file if it exceeds the limit."""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log_file:
                lines = log_file.readlines()

            if len(lines) > MAX_LOG_LINES:
                with open(LOG_FILE, "w") as log_file:
                    log_file.writelines(lines[-MAX_LOG_LINES:])  # Keep only the last MAX_LOG_LINES
                logging.info("🔄 Log file truncated: Removed oldest lines.")
    except Exception as e:
        print(f"⚠️ Error truncating log file: {e}")

def fetch_and_store_cdc_data():
    """Fetch CDC datasets from Internet Archive and store in MongoDB only if AUTO_FETCH_ON_START is True."""
    
    # ✅ Stop execution if auto-fetch is disabled
    if not AUTO_FETCH_ON_START:
        logging.info("🚫 Auto-fetch is disabled in config. Skipping dataset fetch.")
        return

    truncate_log()  # Ensure log truncation happens before writing new entries

    COLLECTION_ID = "20250128-cdc-datasets"
    logging.info("🔄 Fetching dataset file list from Internet Archive...")

    search_results = ia.get_item(COLLECTION_ID)
    dataset_count = 0

    for file in search_results.files:
        filename = file["name"]
        if filename.endswith(".csv") and "-meta.csv" not in filename:
            dataset = {
                "id": filename,
                "title": filename.replace("_", " "),
                "description": f"CDC dataset file: {filename}",
                "url": f"https://archive.org/download/{COLLECTION_ID}/{filename}"
            }
            collection.update_one({"id": dataset["id"]}, {"$set": dataset}, upsert=True)
            dataset_count += 1
            logging.info(f"✅ Stored dataset: {dataset['title']}")

    collection.create_index([("title", "text"), ("description", "text")])
    logging.info(f"🎉 {dataset_count} datasets successfully stored in MongoDB.")

if __name__ == "__main__":
    # ✅ Auto-fetch only runs if explicitly enabled
    if AUTO_FETCH_ON_START:
        fetch_and_store_cdc_data()