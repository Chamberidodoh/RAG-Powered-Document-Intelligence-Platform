import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")
st.title("Settings")

st.number_input("Retrieved chunks", min_value=1, max_value=10, value=5, key="top_k")
st.number_input("Chunk size", min_value=200, max_value=4000, value=1000, key="chunk_size")
st.number_input("Chunk overlap", min_value=0, max_value=1000, value=200, key="chunk_overlap")
st.text_input("Chat model", value="gpt-4.1-mini")
st.text_input("Embedding model", value="text-embedding-3-small")
st.slider("Response temperature", min_value=0.0, max_value=1.0, value=0.1)
