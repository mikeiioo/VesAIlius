import streamlit as st
import pandas as pd

# Flask Backend URL
API_BASE_URL = "http://127.0.0.1:5000"

st.markdown("# Ves**AI**ius")
st.write("This is a test!")

st.markdown(
    "<h1>Ves<span style='color: red; font-weight: bold;'>AI</span>ius</h1>", 
    unsafe_allow_html=True
)

# Subheader with custom styling
st.markdown(
    """
    <h2>Welcome to <span style='color: green; font-size: 1.2em;'>VesAIlius</span>!</h2>
    """, 
    unsafe_allow_html=True
)

# Custom paragraph with colored text
st.markdown(
    """
    <p>This is a <span style='color: purple;'>Streamlit</span> app with 
    <span style='color: orange; font-weight: bold;'>custom</span> styling.</p>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    "<div style='text-align: center;'>This text is centered!</div>", 
    unsafe_allow_html=True
)



# Title
st.title("Interactive Table with Actions")

# Create a DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Select": [False, False, False]  # Placeholder for selection
}
df = pd.DataFrame(data)

# Display the editable DataFrame
edited_df = st.data_editor(df)

# Button to trigger an action
if st.button("Perform Action"):
    selected_names = edited_df[edited_df["Select"]]["Name"].tolist()
    if selected_names:
        for name in selected_names:
            st.success(f"Action performed for {name}!")
    else:
        st.warning("No one selected!")