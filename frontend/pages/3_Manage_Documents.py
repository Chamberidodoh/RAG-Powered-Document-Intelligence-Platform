import streamlit as st

from frontend.api_client import delete_document, list_documents

st.set_page_config(page_title="Manage Documents", layout="wide")
st.title("Manage Documents")

try:
    documents = list_documents()
    for document in documents:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{document.get('filename', 'Unknown')}**")
                st.write(f"Type: {document.get('file_type', 'unknown')}")
                st.write(f"Chunks: {document.get('chunk_count', 0)}")
            with col2:
                if st.button("Delete", key=document.get("document_id")):
                    delete_document(document["document_id"])
                    st.rerun()
except Exception as exc:
    st.error(f"Could not load documents: {exc}")
