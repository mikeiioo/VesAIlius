from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import pandas as pd

model = "meta-llama/Llama-2-7B-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model)
generator = pipeline("text-generation", model=model)

response = generator("What are the benefits of AI?", max_length=200)
print(response)
# Load your dataframe
df = pd.read_csv('/path/to/your/data.csv')

# Extract headers and some contents
headers = df.columns.tolist()
sample_data = df.head().to_dict()

# Prepare the prompt for the model
prompt = f"The dataset has the following columns: {headers}. Here are some sample rows: {sample_data}. Summarize what this data is about."

# Generate the summary
response = generator(prompt, max_length=200)
print(response)