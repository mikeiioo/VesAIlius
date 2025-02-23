from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from match_datasets import search_and_rank_datasets
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from ranking_orders import ranked_query

app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def home():
    return render_template("index.html")

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

if __name__ == '__main__':
    app.run(debug=True)
