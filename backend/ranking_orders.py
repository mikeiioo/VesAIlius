from match_datasets import search_and_rank_datasets
from mistralai import Mistral
from mistralai.client import MistralClient
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Define the user query
api_key = "wzTimOUmlgj88SKZVuybjzRTDLanF8vC"
model = "ft:ministral-3b-latest:08590df2:20250222:16ee7d91"
client = Mistral(api_key=api_key)

def ranked_query(user_query):
    datasets = search_and_rank_datasets(user_query)

    datasets_filtered = []
    for dataset in datasets:
        datasets_filtered.append(dataset['id'])

    # Format the conversation-style input
    messages = [
        {"role": "system", "content": "You are an AI assistant trained to rank datasets based on relevance to a query."},
        {"role": "user", "content": f"""Rank all of the following datasets based on relevance to the query; do not format with 
        bold, do not skip lines, do not number responses, and do not add an explanation for your ranking '{user_query}':\n\n"""}
    ]

    # Add dataset list as part of the conversation
    for i, dataset in enumerate(datasets_filtered, 1):
        messages.append({"role": "user", "content": f"{i}. {dataset}"})

    # Call the OpenAI API to rank the datasets
    response = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=1000
    )

    ranked_response = response.choices[0].message.content.strip().split('\n')
    ranked_datasets = []
    for line in ranked_response:
        parts = line.split('. ', 1)
        if len(parts) == 2:
            id = parts[1].strip()
            dataset = collection.find_one({"id": id})
            dataset["embedding"] = None
            ranked_datasets.append(dataset)

    return ranked_datasets

if __name__ == "__main__":
    print("GOT HERE")
    user_query = "covid"
    print(ranked_query(user_query, collection))
    print("FUNISHED")