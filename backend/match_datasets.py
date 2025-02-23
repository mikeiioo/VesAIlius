from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def generate_query_embedding(query):
    """Generate an embedding for the user's query."""
    return model.encode(query).tolist()

def search_and_rank_datasets(user_query, num_results=10):
    """Search for the most relevant datasets using MongoDB Atlas vector search."""
    query_embedding = generate_query_embedding(user_query)

    search_results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "default",  # Replace with your actual index name
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,  # Number of candidates for search
                "limit": num_results
            }
        }
    ])

    return list(search_results)

# Example usage
if __name__ == "__main__":
    query = "I want Reproductive data"
    results = search_and_rank_datasets(query)
 
    for dataset in results:
        print(f"Title: {dataset['title']}")
        print(f"Tags: {', '.join(dataset['tags'])}")
        print(f"URL: {dataset['url']}")
        print("---")
