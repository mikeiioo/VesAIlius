from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from fetch_datasets import fetch_and_store_cdc_data, set_fetch_flag
from match_datasets import search_and_rank_datasets
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
import openai

app = Flask(__name__, template_folder="templates")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

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

@app.route('/update_datasets', methods=['POST'])
def update_datasets():
    """Manually trigger dataset fetching by setting the update flag."""
    set_fetch_flag(False) # Set to True to fetch data
    fetch_and_store_cdc_data()
    return jsonify({"message": "Dataset update triggered."})

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