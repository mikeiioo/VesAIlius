from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from match_datasets import match_datasets
from transformers import AutoModelForCausalLM, AutoTokenizer
import internetarchive as ia
import torch
from bson.json_util import dumps
import os

if __name__ == "__main__":
    app.run(debug=True)

app = Flask(__name__, template_folder="templates")

# MongoDB connection details
# connection_string = "mongodb+srv://mikeiio:Vessy123@main.nazv8.mongodb.net/?retryWrites=true&w=majority&appName=Main"
connection_string = "mongodb://localhost:27017/"
db = "put_in_database_here"  # Replace with your actual database name
query_collection = "put_in_collection_here"  # Replace with your actual collection name

# Connect to MongoDB
client = MongoClient(connection_string)
db = client[db]
collection = db[query_collection]

@app.route("/search", methods=["GET"])
def search():
    user_query = request.args.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Store user query in MongoDB
    query_collection.insert_one({"query": user_query})

    results = match_datasets(user_query)
    return jsonify(results)

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
        collection.update_one({"id": dataset["id"]}, {"$set": dataset}, upsert=True)
    
    print("✅ CDC datasets imported into MongoDB!")

# Fetch and store CDC datasets on startup
fetch_and_store_cdc_data()

# Load Fine-Tuned Phi-2 Model
# MODEL_NAME = "microsoft/phi-2"
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained("./phi2_finetuned", torch_dtype=torch.float16, device_map="auto")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search_datasets():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Search MongoDB for relevant datasets
    results = list(collection.find({"$text": {"$search": query}}, {"_id": 0}))
    return jsonify(results)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    inputs = tokenizer(query, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({"generated_text": response})

@app.route('/data', methods=['GET'])
def get_data():
    # Fetch all documents from the collection
    data = list(collection.find())
    return dumps(data)

@app.route('/data/<id>', methods=['GET'])
def get_single_data(id):
    # Fetch a single document by ID
    data = collection.find_one({"_id": ObjectId(id)})
    if data:
        return dumps(data)
    else:
        return jsonify({"error": "Data not found"}), 404

@app.route('/data', methods=['POST'])
def add_data():
    # Insert a new document into the collection
    new_data = request.json
    if not new_data:
        return jsonify({"error": "No data provided"}), 400
    result = collection.insert_one(new_data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    # Update a document by ID
    update_data = request.json
    if not update_data:
        return jsonify({"error": "No data provided"}), 400
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count:
        return jsonify({"message": "Data updated successfully"})
    else:
        return jsonify({"error": "Data not found"}), 404

@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    # Delete a document by ID
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Data deleted successfully"})
    else:
        return jsonify({"error": "Data not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)