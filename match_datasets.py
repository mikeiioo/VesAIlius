from pymongo import MongoClient
from process_query import process_query_with_mistral
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
import openai

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def search_and_rank_datasets(user_query):
    """Search MongoDB datasets and rank them using Mistral AI."""
    
    query_filter = {"$text": {"$search": user_query}}
    initial_results = list(collection.find(query_filter, {"_id": 0}).limit(10))

    if not initial_results:
        return []

    dataset_text = "\n".join([f"{d['title']}: {d['description']}" for d in initial_results])

    response = openai.ChatCompletion.create(
        model="mistral-tiny",
        messages=[
            {"role": "system", "content": "Rank the following datasets based on query relevance."},
            {"role": "user", "content": f"Query: {user_query}\n\nAvailable Datasets:\n{dataset_text}\n\nRank the top 5."}
        ],
        api_key=MISTRAL_API_KEY
    )

    return response["choices"][0]["message"]["content"]
