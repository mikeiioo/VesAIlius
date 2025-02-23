import pandas as pd
import io
import internetarchive as ia
from internetarchive import get_item
from mistralai import Mistral
from mistralai.client import MistralClient
import requests

temp = "Impaired_Driving_Death_Rate_by_Age_and_Gender_2012_2014_Region_10_Seattle.csv"
def summarize_data(file):

    item_id = "20250128-cdc-datasets"
    file_name = file

    file_url = f"https://archive.org/download/{item_id}/{file_name}"
    response = requests.get(file_url, stream=True)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    headers = df.columns.tolist()
    sample_data = df.head().to_dict()

    api_key = "qmkFbpB1AT6chW0KTfLh16L2dainN8bN"
    model = "ft:ministral-3b-latest:08590df2:20250222:16ee7d91"
    client = Mistral(api_key=api_key)

    messages = [
        {"role": "system", "content": "You are an AI assistant trained to read and summarize datasets."},
        {"role": "user", "content": f"""Based on the following pandas dataframe headers and sample data, summarize
        the data in this dataset in 3-4 sentences. Specify timeframe and location, if available and applicable. '{headers}' '{sample_data}':\n\n"""}
    ]

    response = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=300
    )

    return response.choices[0].message.content

summarize_data(temp)