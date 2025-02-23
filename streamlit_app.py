import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Flask Backend URL
API_BASE_URL = "http://127.0.0.1:5000"

st.title("📊 VesAIlius - CDC Dataset Search")

# User input for search query
query = st.text_input("🔍 Enter a search query (e.g., 'Covid Cases'):")

if query:
    response = requests.get(f"{API_BASE_URL}/search", params={"query": query})

    if response.status_code == 200:
        datasets = response.json()

        if datasets:
            st.write(f"### 🔎 {len(datasets)} datasets found:")
            for dataset in datasets:
                with st.expander(f"📂 {dataset['title']}"):
                    st.write(f"**Description:** {dataset['description']}")
                    st.write(f"[🔗 Download Dataset]({dataset['url']})")
                    
                    # Fetch and visualize dataset
                    if st.button(f"📊 Visualize {dataset['title']}", key=dataset["id"]):
                        df = pd.read_csv(dataset["url"])
                        st.write(df.head())

                        if "state" in df.columns and "cases" in df.columns:
                            fig, ax = plt.subplots()
                            df.groupby("state")["cases"].sum().plot(kind="bar", ax=ax)
                            st.pyplot(fig)
        else:
            st.warning("⚠ No datasets found.")
    else:
        st.error("❌ Error fetching datasets.")