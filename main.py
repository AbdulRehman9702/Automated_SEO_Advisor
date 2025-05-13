import torch
print(torch.__version__)

import streamlit as st
from new import main  # Importing your main function from the `new` module
import json  # Importing json to handle JSON serialization

# --- Page Config ---
st.set_page_config(
    page_title="Automated SEO Advisor",
    page_icon="💬",
    layout="centered"
)

# --- Title and Header ---
st.title("🤖 Automated SEO Advisor")
st.markdown("""
Welcome to the Automated SEO Advisor! 🤗
""")

# --- User Input ---
st.subheader("📝 Submit Your Query")
user_query = st.text_area(
    "Enter your query here:",
    placeholder="Type something you'd like to ask the Bot... ⌨️"
)

# --- Process the Query ---
if st.button("🚀 Process Query"):
    st.info("Processing your query... ⏳")
    try:
        # Call the main function with the user query
        response = main(user_query)
        
        # Convert the response to a JSON-formatted string
        response_str = json.dumps(response, indent=2)
        
        # Display the result
        st.subheader("📋 Results")
        st.text_area("Response", value=response_str, height=300)
        
    except Exception as e:
        st.error(f"An error occurred while processing the query: {e}")
