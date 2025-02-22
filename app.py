from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import openai  # Import OpenAI for LLM-based ranking
import internetarchive as ia
import os

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Connect to MongoDB (Edit connection string if needed)
# client = MongoClient("mongodb+srv://mikeiio:Vessy123@main.nazv8.mongodb.net/?retryWrites=true&w=majority&appName=Main")
client = MongoClient("mongodb://localhost:27017/")  # Change if using MongoDB Atlas

# Database and collection names (Edit these if needed)
db = client["put_in_database_here"] # Database name
collection = db["put_in_collection_here"] # Collection storing dataset metadata

# Mistral API Key (Replace with your actual API key)
MISTRAL_API_KEY = "your_api_key_here"

# Function to fetch and store CDC datasets from Internet Archive
def fetch_and_store_cdc_data():
    COLLECTION_ID = "20250128-cdc-datasets"
    search_results = ia.search_items(f"collection:{COLLECTION_ID}", fields=["identifier", "title", "description"])
    
    for item in search_results:
        dataset = {
            "id": item.get("identifier"),
            "title": item.get("title", "No Title"),
            "description": item.get("description", "No Description"),
            "url": f"https://archive.org/details/{item.get('identifier')}"
        }
        collection.update_one({"id": dataset["id"]}, {"$set": dataset}, upsert=True)  # Store in MongoDB
    
    # Ensure text index exists
    collection.create_index([("title", "text"), ("description", "text")])
    
    print("✅ CDC datasets imported into MongoDB!")


# Fetch and store CDC datasets on startup
fetch_and_store_cdc_data()

# Function to process user query using Mistral AI
def process_query_with_mistral(user_query):
    """Extracts key topics from user query using Mistral AI."""
    response = openai.ChatCompletion.create(
        model="mistral-tiny",
        messages=[
            {"role": "system", "content": "Extract the main topics from the query."},
            {"role": "user", "content": user_query}
        ],
        api_key=MISTRAL_API_KEY
    )
    return response["choices"][0]["message"]["content"]

# Function to search MongoDB and rank results using Mistral AI
def search_and_rank_datasets(user_query):
    """Search datasets in MongoDB and rank them using Mistral AI."""
    
    # Step 1: Use MongoDB text search to get initial matches
    query_filter = {"$text": {"$search": user_query}}
    initial_results = list(collection.find(query_filter, {"_id": 0}).limit(10))
    
    if not initial_results:
        return []  # Return empty list if no matches found
    
    # Step 2: Use Mistral AI to refine ranking
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

# Function to generate a text summary for a dataset using Mistral AI
def generate_dataset_summary(dataset_id):
    """Generates a summary for a given dataset using Mistral AI."""
    dataset = collection.find_one({"id": dataset_id}, {"_id": 0})
    
    if not dataset:
        return "Dataset not found."
    
    dataset_text = f"Title: {dataset['title']}\nDescription: {dataset['description']}\nURL: {dataset['url']}"
    
    response = openai.ChatCompletion.create(
        model="mistral-tiny",
        messages=[
            {"role": "system", "content": "Summarize the following dataset in a clear and concise way."},
            {"role": "user", "content": dataset_text}
        ],
        api_key=MISTRAL_API_KEY
    )
    
    return response["choices"][0]["message"]["content"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search_datasets():
    user_query = request.args.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    results = search_and_rank_datasets(user_query)
    return jsonify(results)

@app.route('/generate_summary', methods=['GET'])
def generate_summary():
    dataset_id = request.args.get("dataset_id", "")
    if not dataset_id:
        return jsonify({"error": "No dataset ID provided"}), 400
    
    summary = generate_dataset_summary(dataset_id)
    return jsonify({"summary": summary})
    
if __name__ == '__main__':
    app.run(debug=True)

######## CODE BELOW IS NOT NECESSARY FOR NOW ########


# @app.route('/data', methods=['GET'])
# def get_data():
#     # Fetch all documents from the collection
#     data = list(collection.find())
#     return dumps(data)

# @app.route('/data/<id>', methods=['GET'])
# def get_single_data(id):
#     # Fetch a single document by ID
#     data = collection.find_one({"_id": ObjectId(id)})
#     if data:
#         return dumps(data)
#     else:
#         return jsonify({"error": "Data not found"}), 404

# @app.route('/data', methods=['POST'])
# def add_data():
#     # Insert a new document into the collection
#     new_data = request.json
#     if not new_data:
#         return jsonify({"error": "No data provided"}), 400
#     result = collection.insert_one(new_data)
#     return jsonify({"inserted_id": str(result.inserted_id)}), 201

# @app.route('/data/<id>', methods=['PUT'])
# def update_data(id):
#     # Update a document by ID
#     update_data = request.json
#     if not update_data:
#         return jsonify({"error": "No data provided"}), 400
#     result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
#     if result.matched_count:
#         return jsonify({"message": "Data updated successfully"})
#     else:
#         return jsonify({"error": "Data not found"}), 404

# @app.route('/data/<id>', methods=['DELETE'])
# def delete_data(id):
#     # Delete a document by ID
#     result = collection.delete_one({"_id": ObjectId(id)})
#     if result.deleted_count:
#         return jsonify({"message": "Data deleted successfully"})
#     else:
#         return jsonify({"error": "Data not found"}), 404