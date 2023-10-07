import app as streamlit_app

from enums.app_v3 import App


def test_app():
    assert isinstance(streamlit_app.app, App)

    app: App = streamlit_app.app  # st.session_state.get("app")
    assert isinstance(streamlit_app.app, App)
    assert isinstance(app.model_name, str) is True
    assert app.model_name == "decenter-model-linear-reg-sample_v3"
    assert app.demo is True
