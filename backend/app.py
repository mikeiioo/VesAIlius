from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from match_datasets import search_and_rank_datasets
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from ranking_orders import ranked_query
import requests

app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/search', methods=['GET'])
def search_datasets():
    """Search and return relevant datasets based on user query."""
    user_query = request.args.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    results = ranked_query(user_query)

    # Format response
    formatted_results = [
        {
            "title": dataset["title"],
            "url": dataset["url"],
            "id": dataset["id"],
        }
        for dataset in results
    ]

    return jsonify(formatted_results)

@app.route('/dataset/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    """Fetch and return dataset details by ID."""
    dataset = collection.find_one({"id": dataset_id})

    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404

    return jsonify({
        "id": dataset["id"],
        "title": dataset["title"],
        "summary": dataset.get("summary", "No summary available."),
        "url": dataset["url"],
        "url-meta": dataset["url-meta"]
    })

@app.route('/fetch_csv', methods=['GET'])
def fetch_csv():
    """Fetch CSV data from the provided URL."""
    print("CSV URL COMPUTING!")
    csv_url = request.args.get("url")
    if not csv_url:
        return jsonify({"error": "No URL provided"}), 400

    response = requests.get(csv_url)
    print("RESPONSE DONE", response)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch CSV data"}), response.status_code
    
    return Response(response.content, mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
