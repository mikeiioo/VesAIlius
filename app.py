from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB connection details
connection_string = "mongodb+srv://mikeiio:Vessy123@main.nazv8.mongodb.net/?retryWrites=true&w=majority&appName=Main"
database_name = "your_database_name"  # Replace with your actual database name
collection_name = "your_collection_name"  # Replace with your actual collection name

# Connect to MongoDB
client = MongoClient(connection_string)
db = client[database_name]
collection = db[collection_name]

@app.route('/')
def home():
    return "Welcome to VesAIlius!"

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