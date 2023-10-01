import logging

import streamlit as st


def head():
    with open("static/style.css") as f:
        logging.info("reading style.css")
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    col2.image("static/logo.png", width=300)

    st.toast("Welcome to Decenter", icon="🙏")

    # st.image("static/stand.png")
    st.title("AI Infrastructure for Model training")

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
