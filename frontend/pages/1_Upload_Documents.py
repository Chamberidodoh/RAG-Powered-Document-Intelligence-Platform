import streamlit as st

from frontend.api_client import upload_documents

st.set_page_config(page_title="Upload Documents", layout="wide")
st.title("Upload Documents")

uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt", "md", "csv", "xlsx"], accept_multiple_files=True)
if st.button("Upload and Process") and uploaded_files:
    with st.spinner("Processing files..."):
        try:
            results = upload_documents(list(uploaded_files))
            st.success("Upload completed")
            st.json(results)
        except Exception as exc:
            st.error(f"Upload failed: {exc}")
