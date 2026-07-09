import streamlit as st


def render_chat_message(role: str, content: str, sources: list[dict[str, object]] | None = None) -> None:
    with st.chat_message(role):
        st.write(content)
        if sources:
            with st.expander("Sources"):
                st.json(sources)
