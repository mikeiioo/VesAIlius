import pandas as pd
from flask import Flask, request, send_file
from internetarchive import get_item
from internetarchive import download
import requests
import io
import os

app = Flask(__name__)

item_id = "20250128-cdc-datasets"

def filter_data(file, op_code):
    file_name = file
    item = get_item(item_id)

    file_url = f"https://archive.org/download/{item_id}/{file_name}"
    response = requests.get(file_url, stream=True)

    if op_code == 0:
        download_first_hundred(file_url)
    elif op_code == 1:
        download_full_file(file_url, response)
    elif op_code == 2:
        download_all_exclude_columns(file_url, response, exclude_columns=[])
    

def download_first_hundred(file_url, download_dir=None):
    # If no download directory is provided, default to user's Downloads folder
    if download_dir is None:
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    response = requests.get(file_url, stream=True)  # Enable streaming
    
    if response.status_code == 200:
        os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

        file_name = file_url.split("/")[-1]  # Extract filename from URL
        file_path = os.path.join(download_dir, file_name)  # Full path

        with open(file_path, "wb") as f:
            line_count = 0
            for line in response.iter_lines():  # Read file line by line
                f.write(line + b"\n")  # Write each line to file
                line_count += 1
                if line_count >= 100:  # Stop after 100 lines
                    break

def download_full_file(file_url, response, download_dir="downloads"):
    if response.status_code == 200:
        with open(f"{download_dir}/{file_url.split('/')[-1]}", "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)

def download_all_exclude_columns(file_url, response, download_dir="downloads", exclude_columns=[]):
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        df = df.drop(exclude_columns, axis=1)
        reduced_csv = df.to_csv(index=False)
        with open(f"{download_dir}/reduced.csv", "w") as f:
            for chunk in reduced_csv.iter_content(chunk_size=128):
                f.write(chunk)

if __name__ == "__main__":
    app.run(debug=True)