import openai
from config import MISTRAL_API_KEY

def process_query_with_mistral(user_query):
    """Extracts key topics from user query using Mistral API."""
    
    response = openai.ChatCompletion.create(
        model="mistral-tiny",
        messages=[{"role": "user", "content": f"Extract the main topics from: {user_query}"}],
        api_key=MISTRAL_API_KEY
    )
    return response["choices"][0]["message"]["content"]