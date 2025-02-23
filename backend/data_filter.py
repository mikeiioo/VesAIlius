import pandas as pd
from internetarchive import get_item
from internetarchive import download
import requests
import io

item_id = "20250128-cdc-datasets"

def filter_data(file, op_code):
    file_name = file
    item = get_item(item_id)

    file_url = f"https://archive.org/download/{item_id}/{file_name}"
    response = requests.get(file_url, stream=True)

    if op_code == 0:
        download_first_hundred(file_url, response)
    elif op_code == 1:
        download_full_file(file_url, response)
    elif op_code == 2:
        download_all_exclude_columns(file_url, response, exclude_columns=[])
    

def download_first_hundred(file_url, response, download_dir="downloads"):
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        reduced_csv = df.head(100).to_csv(index=False)
        with open(f"{download_dir}/first_hundred.csv", "w") as f:
            f.write(reduced_csv)

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


