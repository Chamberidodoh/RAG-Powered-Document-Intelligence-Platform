import streamlit as st

from frontend.api_client import query_chat

st.set_page_config(page_title="Ask Questions", layout="wide")
st.title("Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

question = st.text_input("Ask about the uploaded documents")
if st.button("Submit") and question:
    with st.spinner("Retrieving context and generating answer..."):
        response = query_chat({"question": question, "top_k": 5})
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": response["answer"], "sources": response.get("sources", [])})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                st.json(message["sources"])
