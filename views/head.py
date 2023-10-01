import streamlit as st

import public


def head():
    st.markdown(f"{public.index_css}", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    col2.image(public.logo, width=300)

    st.toast("Welcome to Decenter", icon="🙏")

    # st.image("static/stand.png")
    st.title("AI Infrastructure for Model training")
