import streamlit as st

st.set_page_config(page_title="RAG Document Intelligence", page_icon="📄", layout="wide")
st.title("RAG-Powered Document Intelligence Platform")
st.write("Upload internal documents, index them with embeddings, and ask grounded questions using retrieval-augmented generation.")

st.metric("System Status", "Healthy")
st.metric("Uploaded Documents", "0")
st.metric("Indexed Chunks", "0")

st.header("Quick Navigation")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/1_Upload_Documents.py", label="Upload Documents")
with col2:
    st.page_link("pages/2_Ask_Questions.py", label="Ask Questions")
with col3:
    st.page_link("pages/3_Manage_Documents.py", label="Manage Documents")
with col4:
    st.page_link("pages/4_Settings.py", label="Settings")
