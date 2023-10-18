import logging

import streamlit as st
from streamlit.commands.page_config import (
    REPORT_A_BUG_KEY,
    ABOUT_KEY,
    GET_HELP_KEY,
)

import public


def head():
    with open("static/_style.css") as f:
        logging.info("reading _style.css")
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


def head_v3():
    st.set_page_config(
        page_title="Decenter AI",
        page_icon="static/favicon.ico",
        layout="centered",
        menu_items={
            REPORT_A_BUG_KEY: "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/issues/new/choose",
            ABOUT_KEY: "https://app.pitch.com/app/dashboard/0ba0eb40-0ffc-4970-91a5-64cec23d3457",
            GET_HELP_KEY: "https://github.com/DeCenter-AI/decenter-ai.streamlit.app/issues/new/choose",
        },
    )
    st.sidebar.header("v3")

    st.markdown(public.button_styles_css, unsafe_allow_html=True)

    st.sidebar.markdown(
        public.report_request_buttons_html,
        unsafe_allow_html=True,
    )

    st.write(public.index_css, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(
            "static/stand.png",
            caption="AI Infrastructure for Model training",
        )
        st.toast("Welcome to Decenter", icon="🙏")

    col2.image(public.logo, width=400)

    st.sidebar.success("Load complete")


def head_v4():
    # to be tested
    st.markdown(
        """
        <link rel="stylesheet" type="text/css" href="app/static/index.css">
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(
            "static/stand.png",
            caption="AI Infrastructure for Model training",
        )
        st.toast("Welcome to Decenter", icon="🙏")

    col2.image(public.logo, width=400)

    st.sidebar.success("Load complete")
