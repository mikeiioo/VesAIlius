from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from match_datasets import search_and_rank_datasets
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from ranking_orders import ranked_query
import requests
from summarize_data import summarize_data
from lines import get_x_lines
import math
import os
from io import BytesIO
import pandas as pd  # Add this with other imports at the top

ITEM_ID = "20250128-cdc-datasets"

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

    # Add this line to extract filename from URL
    file_name = dataset["url"].split("/")[-1]

    return jsonify({
        "id": dataset["id"],
        "title": dataset["title"],
        "url": dataset["url"],
        "url-meta": dataset["url-meta"],
        "file_name": file_name  # <-- Add this line
    })

@app.route('/summary/<dataset_id>', methods=['GET'])
def get_summary(dataset_id):
    """Fetch and return dataset details by ID."""
    dataset = collection.find_one({"id": dataset_id})

    if not dataset:
        return jsonify({"error": "Dataset not found"}), 404

    return jsonify({
        "summary": dataset.get("summary", summarize_data(dataset_id)),
    })

@app.route('/fetch_csv', methods=['GET'])
def fetch_csv():
    """Fetch CSV data from the provided URL."""
    csv_url = request.args.get("url")

    print("CSV URL COMPUTING!", csv_url)
    if not csv_url:
        return jsonify({"error": "No URL provided"}), 400

    response = get_x_lines(csv_url, 500)
    
    return Response(response, mimetype='text/csv')

@app.route('/download_first_hundred')
def download_first_hundred():
    """Stream first 100 rows of a CSV dataset"""
    file_name = request.args.get('file_name')
    csv_url = f"https://archive.org/download/{ITEM_ID}/{file_name}"
    
    # Stream the CSV content
    response = requests.get(csv_url, stream=True)
    response.raise_for_status()

    def generate():
        line_count = 0
        for line in response.iter_lines():
            if line_count >= 100:
                break
            yield line + b'\n'
            line_count += 1

    return Response(
        generate(),
        headers={
            'Content-Disposition': f'attachment; filename=first_100_{file_name}',
            'Content-Type': 'text/csv'
        }
    )

@app.route('/download_all_exclude_columns')
def download_all_exclude_columns():
    """Download full dataset excluding specified columns"""
    try:
        file_name = request.args.get('file_name')
        if not file_name:
            return jsonify({"error": "Missing file_name parameter"}), 400

        exclude_columns = request.args.get('exclude_columns', '')
        exclude_list = [col.strip() for col in exclude_columns.split(',') if col.strip()]
        
        csv_url = f"https://archive.org/download/{ITEM_ID}/{file_name}"
        
        # Stream the CSV content
        response = requests.get(csv_url, stream=True)
        response.raise_for_status()

        # Process in chunks
        def generate():
            chunk_size = 1024 * 1024  # 1MB chunks
            buffer = BytesIO()
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                buffer.write(chunk)
                buffer.seek(0)
                
                # Process CSV in chunks
                df = pd.read_csv(buffer)
                
                # Remove columns if they exist
                cols_to_drop = [col for col in exclude_list if col in df.columns]
                if cols_to_drop:
                    df = df.drop(columns=cols_to_drop, errors='ignore')
                
                output = df.to_csv(index=False)
                buffer.truncate(0)
                buffer.seek(0)
                
                yield output

        return Response(
            generate(),
            headers={
                'Content-Disposition': f'attachment; filename=filtered_{file_name}',
                'Content-Type': 'text/csv'
            }
        )
        
    except Exception as e:
        app.logger.error(f"Error processing filtered download: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)