import streamlit as st


def render_source_citation(source: dict[str, object]) -> None:
    with st.expander(f"{source.get('filename', 'Source')}"):
        st.json(source)
