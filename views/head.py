import streamlit as st


def head():
    with open('static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    col2.image("static/logo.png", width=300)

    # st.image("static/stand.png")
    st.title("AI Infrastructure for Model training")
