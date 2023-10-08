import logging
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile
from typing import List

import streamlit as st
from pychroot import Chroot
from streamlit.commands.page_config import (
    REPORT_A_BUG_KEY,
    ABOUT_KEY,
    GET_HELP_KEY,
)

from config.constants import *
from config.log import setup_log
from enums.app_v3 import App
from public import report_request_buttons_html, button_styles_css
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

app: App = st.session_state.get("app")
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

app.model_name = st.text_input(
    "Model Name",
    max_chars=50,
    placeholder="decenter-model",
    key="model_name",
    value=app.model_name,
)

input_archive = st.file_uploader(
    "Upload working directory of notebook",
    type=["zip"],
)

if not app.model_name_changed and input_archive:
    app.model_name = (
        "decenter-model-"
        + os.path.splitext(os.path.basename(input_archive.name))[0]
    )
    print("streamlit rerun")
    st.experimental_rerun()
    print("dead code: won't run")  # know this

app.demo = input_archive is None
# app.demo = st.checkbox('demo') #TODO: wip

if app.demo:
    st.warning("input archive not found: demo:on")
    app.model_name = "decenter-model-linear-reg-sample_v3"
    input_archive = "samples/sample_v3"
    app.work_dir = "samples/sample_v3"
else:
    app.temp_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix=app.model_name,
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
    print("temp_dir contains", temp_dir_contents)

    app.create_venv()

driver_scripts = find_driver_scripts(app.work_dir)
app.starter_script = st.selectbox("Training Script:", driver_scripts)
training_cmd: List[str] = []

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
                        app.python_repl,
                        app.requirements_path,
                        cwd=app.work_dir,
                    )

            training_cmd = [app.python_repl, app.starter_script]

        case ".ipynb":
            app.exec_mode = TRAINER_PYTHON_NB

            training_cmd = get_notebook_cmd(
                app.starter_script,
                app.python_repl,
            )

        case _:
            raise Exception(f"invalid script-{script_ext}")

if not training_cmd:
    st.stop()

if st.button("Train"):
    print(app.starter_script)

    st.snow()

    with st.spinner("Training in progress"):
        if platform.system() == "Linux":
            if app.python_repl is not sys.executable:
                python_repl = os.path.relpath(
                    app.python_repl,
                    app.work_dir,
                )

                training_cmd[0] = python_repl

            mountpoints = {
                os.path.dirname(sys.executable): {
                    "create": True,
                },
                os.path.dirname(app.work_dir) : {
                    "create":True
                }
            }
            shutil.copyfile(sys.executable,f'{app.work_dir}/python3' )

            python_executable_permissions = os.stat(sys.executable).st_mode

            # Set the permissions of the copied Python executable file to the same permissions as the original file
            os.chmod(f'{app.work_dir}/python3', python_executable_permissions)
            
            # def preexec_fn():
            #     os.chroot("/tmp/chroot")
            #     os.mount("--bind", "/dev", "/dev")
            #     os.mount("--bind", "/proc", "/proc")
            # subprocess.run(["python3"], preexec_fn=preexec_fn)

            
            with Chroot(
                app.work_dir,
                logging.getLogger(),
                mountpoints=mountpoints,
                skip_chdir=True,
            ):
                print("chroot:", os.getcwd())
                print("training_cmd:", training_cmd)
                print("ls:", os.listdir())

                result = subprocess.run(
                    ['pwd'],
                    # cwd=app.work_dir,
                    capture_output=True,
                    encoding="UTF-8",
                )
                print('res')
                print(result.stderr)
                print(result.stdout)
        else:
            result = subprocess.run(
                training_cmd,
                cwd=app.work_dir,
                capture_output=True,
                encoding="UTF-8",
            )

        logging.info(result.stdout)
        logging.info(result.stderr)

        with open(os.path.join(app.work_dir, "stdout"), "w") as stdout, open(
            os.path.join(app.work_dir, "stderr"),
            "w",
        ) as stderr:
            stdout.write(result.stdout)
            stderr.write(result.stderr)

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
                app.exit_code = False
                st.error("notebook: execution failed")
                print("notebook:", "execution failed")

    if app.exit_code:
        venv_dir = app.venv_dir
        if venv_dir:
            shutil.rmtree(venv_dir)

        zipfile_ = app.export_working_dir()

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
