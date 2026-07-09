import streamlit as st


def render_document_card(document: dict[str, object]) -> None:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{document.get('filename', 'Unknown')}**")
            st.write(f"Type: {document.get('file_type', 'unknown')}")
            st.write(f"Chunks: {document.get('chunk_count', 0)}")
        with col2:
            if st.button("Delete", key=str(document.get("document_id"))):
                st.session_state["delete_document_id"] = document.get("document_id")
