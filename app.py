import logging
import shutil
import subprocess
import sys
import zipfile
from typing import List

import streamlit as st

from config import DEMO_DIR
from config.constants import *
from config.log import setup_log
from enums.app_v3 import App
from utils.exec_commands import get_notebook_cmd
from utils.helper_find import (
    find_requirements_txt_files,
    find_driver_scripts,
    find_demos,
)
from utils.install_deps import install_dependencies
from views.head import head_v3

setup_log()

load_dotenv()

head_v3()

app: App = st.session_state.get("app")
app = None if MODE == DEVELOPMENT else app  # FIXME: DEV: when testing

if not app:
    app = App()
    logging.info("creating new app instance")
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

# TODO: checkbox-button for "demo" , if enabled then show the selectbox that's what is app.demo

app.selected_demo = st.selectbox(
    "Demo",
    find_demos(),
    help="enabled when no input archive is uploaded",
    disabled=not app.demo,
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

if app.demo and input_archive:
    app._prev_model_name = None
    app.demo = False
    print("streamlit rerun: app.demo and input_archive")
    st.experimental_rerun()
elif not app.demo and not input_archive:
    app._prev_model_name = None
    app.demo = True
    print("streamlit rerun: app.demo")
    st.experimental_rerun()

# app.demo = st.checkbox('demo') #TODO: wip

if not app.model_name_changed and input_archive:
    app.model_name = os.path.splitext(os.path.basename(input_archive.name))[0]
    print("streamlit rerun: input_archive")
    st.experimental_rerun()
    print("dead code: won't run")


app.create_temporary_dir()

if app.demo:
    st.warning("input archive not found: demo:on")

    if not app.selected_demo:
        st.error("demo: not found")
        logging.critical("demo: not found")
        st.stop()
    cur_model_name = app.model_name
    app.model_name = os.path.splitext(os.path.basename(app.selected_demo))[0]
    print("demo model_name", app.model_name)

    if cur_model_name != app.model_name:
        print("streamlit: rerun: model_name_updated")
        st.experimental_rerun()

    temp_file_path = os.path.join(DEMO_DIR, app.selected_demo)

    with zipfile.ZipFile(temp_file_path, "r") as zip_ref:
        zip_ref.extractall(app.work_dir)

    app.python_repl = sys.executable

else:
    app.selected_demo = None

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
                file_name=f"decenter-model-{app.model_name}",
            )

        st.balloons()
        app.recycle_temp_dir()
