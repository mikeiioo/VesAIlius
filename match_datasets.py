from pymongo import MongoClient
from process_query import process_query_with_mistral

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cdc_database"]
collection = db["datasets"]

def match_datasets(user_query):
    """Matches user query with MongoDB datasets instead of scraping every time."""

    # Extract key topics using Mistral AI
    keywords = process_query_with_mistral(user_query).lower().split()
    
    # Perform MongoDB full-text search
    query_filter = {"$text": {"$search": " ".join(keywords)}}
    results = list(collection.find(query_filter, {"_id": 0}).limit(5))

    return results