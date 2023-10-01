import streamlit as st

import public


def head():
    st.write(f"{public.index_css}", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(
            "static/stand.png", caption="AI Infrastructure for Model training"
        )
        st.toast("Welcome to Decenter", icon="🙏")

    col2.image(public.logo, width=400)
