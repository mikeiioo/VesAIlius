import logging
import internetarchive as ia
import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, CONFIG_COLLECTION, AUTO_FETCH_ON_START

##### If you want to fetch on startup, set AUTO_FETCH_ON_START to True in config.py #####

logging.basicConfig(filename="dataset_fetch.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
config_collection = db[CONFIG_COLLECTION]

def should_fetch_data():
    """Check if the dataset update flag is set to True."""
    config = config_collection.find_one({"_id": "update_flag"})
    return config and config.get("fetch", False) 

def set_fetch_flag(value):
    """Set the dataset update flag to True or False."""
    config_collection.update_one({"_id": "update_flag"}, {"$set": {"fetch": value}}, upsert=True)

def fetch_and_store_cdc_data():
    """Fetch CDC datasets from Internet Archive and store in MongoDB, only if the update flag is set."""
    if not should_fetch_data():
        logging.info("✅ Fetching skipped as update flag is not set.")
        return

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

    # Reset the fetch flag after updating
    set_fetch_flag(False)
    
if __name__ == "__main__":
    if AUTO_FETCH_ON_START:
        set_fetch_flag(True)
    fetch_and_store_cdc_data()