import logging
import platform
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from dataclasses import dataclass
from typing import List

import streamlit as st
from streamlit.commands.page_config import (
    REPORT_A_BUG_KEY,
    ABOUT_KEY,
    GET_HELP_KEY,
)

from config.constants import *
from config.log import setup_log
from public import report_request_buttons_html, button_styles_css
from utils.archive import archive_directory
from utils.exec_commands import get_notebook_cmd
from utils.helper_find import find_requirements_txt_files, find_driver_scripts
from utils.install_deps import install_dependencies
from views.head import head_v3

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


@st.cache_resource
def get_temp_zip_dir():
    temp_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix="-models-zip-dir",
    )
    return temp_dir.name


setup_log()

st.sidebar.header("v3")

st.markdown(button_styles_css, unsafe_allow_html=True)

st.sidebar.markdown(report_request_buttons_html, unsafe_allow_html=True)

load_dotenv()

head_v3()


@dataclass
class App:
    version: str = "v3"
    demo: bool = True
    model_name: str = "decenter-model-linear-reg-sample_v3"
    model_name_changed: bool = False

    exec_mode: EXECUTION_TEMPLATE = None
    starter_script: str = None
    requirements_path: str = None
    _work_dir: str = None
    temp_dir: tempfile.TemporaryDirectory = None
    models_archive_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix="-models-zip-dir",
    ).name

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, _work_dir: str):
        if not _work_dir:
            logging.warning("no work_dir found")
            return
        self._work_dir = _work_dir

    def set_model_name(self, model_name: str):
        app.model_name = model_name
        app.model_name_changed = True

    def validate_model_name(self):
        if not self.model_name:
            self.model_name_changed = False
            self.model_name = "decenter-model-linear-reg-sample_v3"
            st.toast(f"model name reverted to {self.model_name}", icon="👎")
        elif not self.model_name == "decenter-model-linear-reg-sample_v3":
            self.model_name_changed = True
            st.toast(f"model name updated to {self.model_name}", icon="👌")

        logging.info(self.model_name)


app = st.session_state.get("app")
# app = None if MODE == DEVELOPMENT else app  # DEV: when testing
if not app:
    app = App()
    st.session_state.app = app

option = st.selectbox(
    "App Version",
    ("v3", "v2", "v1"),
)

if option != app.version:  # don't redirect if in the same page
    st.markdown(
        f'<meta http-equiv="refresh" content="0;URL=/{option}">',
        unsafe_allow_html=True,
    )


def setDemoMode(val: bool = False):
    app.demo = val


app.model_name = st.text_input(
    "Model Name",
    max_chars=50,
    placeholder="decenter-model",
    key="model_name",
    value=app.model_name,
    on_change=app.validate_model_name,
    # on_change=app.set_model_name,
    # args=(),
    # kwargs=(),
    # value=f'decenter-model-{dt.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")}',
)
app.validate_model_name()
logging.info(f"model-name:{app.model_name}")

model_name = app.model_name

input_archive = st.file_uploader(
    "Upload working directory of notebook",
    type=["zip"],
    on_change=lambda: setDemoMode(False),
)

if not app.model_name_changed and input_archive:
    model_name = (
        "decenter-model-"
        + os.path.splitext(os.path.basename(input_archive.name))[0]
    )
    app.set_model_name(model_name)
    print("streamlit rerun")
    st.experimental_rerun()
    print("rerun complete")  # know this
starter_script: str  # notebook or python_script

app.temp_dir: str | tempfile.TemporaryDirectory

venv_dir: str = None

python_repl: str = sys.executable

app.demo = input_archive is None

# app.demo = st.checkbox('demo') #TODO: wip

if app.demo:
    st.warning("input archive not found: demo:on")
    model_name = "decenter-model-linear-reg-sample_v3"
    input_archive = "samples/sample_v3"
    app.work_dir = "samples/sample_v3"
else:
    app.temp_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix=model_name,
    )

    app.work_dir = app.temp_dir.name
    temp_file_path = f"{app.work_dir}/input_archive.zip"

    print("temp file path", temp_file_path)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(input_archive.read())

    # Extract the contents of the archive to the temporary directory
    with zipfile.ZipFile(temp_file_path, "r") as zip_ref:
        zip_ref.extractall(app.work_dir)

    # At this point, the contents of the archive are extracted to the temporary directory
    # You can access the extracted files using the 'temp_dir' path

    # Example: Print the list of extracted files
    extracted_files = os.listdir(app.work_dir)
    print("extracted:", extracted_files)

    print("temp_dir is ", app.temp_dir)
    temp_dir_contents = os.listdir(app.work_dir)
    print("temp_dir contains", temp_dir_contents)  # FIXME error

    venv_dir = os.path.join(app.work_dir, ".venv")
    venv.create(
        venv_dir,
        system_site_packages=True,
        with_pip=True,
        symlinks=True,
    )

    logging.info("created venv dir")

    match platform.system():
        case "Windows":
            python_repl = os.path.join(venv_dir, "Scripts", "python.exe")
        case _:
            python_repl = os.path.join(venv_dir, "bin", "python3")

driver_scripts = find_driver_scripts(app.work_dir)
app.starter_script = st.selectbox("Training Script:", driver_scripts)
training_cmd: List[str] = None

if app.starter_script:
    script_ext = os.path.splitext(app.starter_script)[1]

    match script_ext:
        case ".py":
            app.exec_mode = TRAINER_PYTHON

            available_requirement_files = find_requirements_txt_files(
                app.work_dir,
            )
            requirements = st.selectbox(
                "Select dependencies to install",
                available_requirement_files,
            )

            if requirements:
                with st.spinner("Installing dependencies in progress"):
                    app.requirements_path = os.path.join(
                        app.work_dir,
                        requirements,
                    )
                    install_dependencies(
                        python_repl,
                        app.requirements_path,
                        cwd=app.work_dir,
                    )

            training_cmd = [python_repl, app.starter_script]

        case ".ipynb":
            app.exec_mode = TRAINER_PYTHON_NB
            # install_deps(
            #     python_repl, requirements="""
            #     """.strip().split(' '), cwd=app.work_dir,
            # )
            # if not app.demo and MODE != DEVELOPMENT:
            #     logging.info("installing  deps venv for nb")
            #     install_dependencies(
            #         python_repl,
            #        "./requirements-ml.txt",
            # )
            # python_repl = sys.executable  # FIXME: remove once stable

            training_cmd = get_notebook_cmd(app.starter_script, python_repl)

        case _:
            raise Exception(f"invalid script-{script_ext}")

if training_cmd and st.button("Train"):
    print(app.starter_script)

    st.snow()

    EXECUTION_SUCCESS = True

    with st.spinner("Training in progress"):
        result = subprocess.run(
            training_cmd,
            cwd=app.work_dir,
            capture_output=True,
            encoding="UTF-8",
        )

        logging.info(result.stdout)  # TODO: logs trace
        logging.info(result.stderr)

        if result.stdout:
            st.info(result.stdout)

        if result.stderr:
            st.warning(result.stderr)

        if app.exec_mode is TRAINER_PYTHON_NB:
            out = f"{app.starter_script}.html"
            if os.path.exists(
                os.path.join(app.work_dir, f"{app.starter_script}.html"),
            ):
                st.info(f"notebook: output generated at {out}")
                print(f"notebook: output generated at {out}")
            else:
                EXECUTION_SUCCESS = False
                st.error("notebook: execution failed")
                print("notebook:", "execution failed")

    if EXECUTION_SUCCESS:
        if venv_dir:
            shutil.rmtree(venv_dir)

        zipfile_ = archive_directory(
            f"{app.models_archive_dir}/{model_name}",
            app.work_dir,
        )
        # zipfile_ = archive_directory_in_memory(app.work_dir)

        st.toast("Executed the notebook successfully", icon="🧤")

        st.success("Execution completed successfully!", icon="✅")

        st.balloons()

        with open(zipfile_, "rb") as f1:
            st.download_button(
                label="Download Working Directory",
                data=f1,
                file_name=f"{os.path.basename(zipfile_)}",
            )

        st.balloons()
        if isinstance(app.temp_dir, tempfile.TemporaryDirectory):
            st.toast("cleaning up the temp directory")
            app.temp_dir.cleanup()
