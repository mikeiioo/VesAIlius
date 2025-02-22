import logging
import internetarchive as ia
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, AUTO_FETCH_ON_START
import os
import csv
import requests
from sentence_transformers import SentenceTransformer
import numpy as np

LOG_FILE = "dataset_fetch.log"
MAX_LOG_LINES = 1000  # Maximum lines before truncation

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional embeddings

def generate_embedding(title, tags):
    """Generate an embedding based on title and tags."""
    combined_text = f"{title} {' '.join(tags)}"
    return model.encode(combined_text).tolist()  # Convert to list for MongoDB storage

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

def extract_tags_from_meta_file(meta_url):
    """Extract 'Tags' field from a meta file on Internet Archive."""    
    try:
        # ✅ Download the meta CSV file
        response = requests.get(meta_url)
        response.raise_for_status()  # Raise an error if the request fails
        
        # ✅ Read CSV content
        lines = response.text.splitlines()
        reader = csv.reader(lines)
        
        for row in reader:
            if row and row[0].strip().lower() == "tags":  # Look for "Tags" field
                return [tag.strip() for tag in row[1].split(",")]  # Convert to list

    except Exception as e:
        logging.error(f"❌ Failed to extract tags from {meta_url}: {e}")

    return []  # Return an empty list if no tags were found

from sentence_transformers import SentenceTransformer
import numpy as np

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional embeddings

def generate_embedding(title, tags):
    """Generate an embedding based on title and tags."""
    combined_text = f"{title} {' '.join(tags)}"
    return model.encode(combined_text).tolist()  # Convert to list for MongoDB storage

# if you want to limit how many files are used for testing purposes
# maxIterations = math.inf
maxIterations = 10
def fetch_and_store_cdc_data():
    """Fetch CDC datasets, process metadata, and store in MongoDB with embeddings."""
    if not AUTO_FETCH_ON_START:
        logging.info("🚫 Auto-fetch is disabled in config. Skipping dataset fetch.")
        return

    truncate_log()
    COLLECTION_ID = "20250128-cdc-datasets"
    logging.info("🔄 Fetching dataset file list from Internet Archive...")

    search_results = ia.get_item(COLLECTION_ID)
    file_list = {file["name"]: file for file in search_results.files}    

    collection.delete_many({})

    iterations = 0
    for filename in file_list:
        if iterations > maxIterations:
            break  # Limit entries for testing
        iterations += 1

        if filename.endswith(".csv") and "-meta.csv" not in filename:
            meta_filename = filename.replace(".csv", "-meta.csv")

            if meta_filename not in file_list:
                logging.info(f"⚠️ Skipping {filename} (No meta file found)")
                continue

            meta_url = f"https://archive.org/download/{COLLECTION_ID}/{meta_filename}"
            tags = extract_tags_from_meta_file(meta_url)

            # ✅ Generate embedding
            embedding = generate_embedding(filename.replace("_", " "), tags)

            dataset = {
                "id": filename,
                "title": filename.replace("_", " ").replace(".csv", ""),
                "url": f"https://archive.org/download/{COLLECTION_ID}/{filename}",
                "url-meta": meta_url,
                "tags": tags,
                "embedding": embedding  # Store vector embedding
            }
            collection.update_one({"id": dataset["id"]}, {"$set": dataset}, upsert=True)
            logging.info(f"✅ Stored dataset: {dataset['title']} with Tags: {tags}")

    logging.info("🎉 All datasets successfully stored in MongoDB.")
    print("----- FINISHED FETCHING ----")

if __name__ == "__main__":
    # ✅ Auto-fetch only runs if explicitly enabled
    if AUTO_FETCH_ON_START:
        fetch_and_store_cdc_data()