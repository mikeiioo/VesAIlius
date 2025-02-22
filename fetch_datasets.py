from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from config import BASE_URL

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cdc_database"]
collection = db["datasets"]

def fetch_cdc_datasets():
    """Scrapes dataset filenames, stores in MongoDB, and returns dataset list."""
    
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    files = soup.find_all("a")

    datasets = []
    for file in files:
        filename = file.get("href")
        if filename and filename.endswith(".csv"):
            dataset = {
                "id": filename,
                "title": filename.replace("_", " ").replace(".csv", ""),
                "url": f"{BASE_URL}{filename}",
                "description": f"CDC dataset file: {filename}"
            }
            datasets.append(dataset)

            # Store in MongoDB (avoid duplicates)
            collection.update_one({"id": filename}, {"$set": dataset}, upsert=True)
    
    return datasets[:100]  # Return only top 100 datasets
