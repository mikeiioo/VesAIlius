from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from match_datasets import search_and_rank_datasets
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

app = Flask(__name__, template_folder="templates")
CORS(app)

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/search', methods=['GET'])
def search_datasets():
    """Search and return relevant datasets based on user query."""
    user_query = request.args.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    results = search_and_rank_datasets(user_query)

    # Format response
    formatted_results = [
        {
            "title": dataset["title"],
            "tags": dataset.get("tags", []),
            "url": dataset["url"]
        }
        for dataset in results
    ]

    return jsonify(formatted_results)

if __name__ == '__main__':
    app.run(debug=True)