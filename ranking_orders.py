import openai
from match_datasets import search_and_rank_datasets
from mistralai import Mistral
from mistralai.client import MistralClient

# Define the user query
user_query = "motor vehicle death"

# Use the search_and_rank function to get a list of datasets
datasets = search_and_rank_datasets(user_query)

datasets_filtered = []
for dataset in datasets:
    datasets_filtered.append(dataset['id'])

print(datasets_filtered)
# OpenAI API key and model details

api_key = "wzTimOUmlgj88SKZVuybjzRTDLanF8vC"
model = "ft:ministral-3b-latest:08590df2:20250222:16ee7d91"
client = Mistral(api_key=api_key)

# Format the conversation-style input
messages = [
    {"role": "system", "content": "You are an AI assistant trained to rank datasets based on relevance to a query."},
    {"role": "user", "content": f"""Rank all of the following datasets based on relevance to the query; do not format with 
     bold, do not skip lines, do not number responses, and do not add an explanation for your ranking '{user_query}':\n\n"""}
]

# Add dataset list as part of the conversation
for i, dataset in enumerate(datasets_filtered, 1):
    messages.append({"role": "user", "content": f"{i}. {dataset}"})

# Call the OpenAI API to rank the datasets
response = client.chat.complete(
    model=model,
    messages=messages,
    max_tokens=1000
)

# Print the ranked response from Mistral-3B
print(response.choices[0].message.content)
