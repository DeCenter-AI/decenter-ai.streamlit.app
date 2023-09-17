import datetime as dt
import logging
import subprocess
import sys
import tempfile
import venv
import zipfile
import shutil

import streamlit as st

from config.constants import *
from config.log import setup_log
from utils.archive import archive_directory
from utils.exec_commands import get_notebook_cmd, get_python_cmd
from utils.helper_find import find_requirements_txt_files, find_driver_scripts
from utils.install_deps import install_dependencies
from views.head import head

st.set_page_config(
    page_title='Decenter AI',
    page_icon='static/favicon.ico',
)


@st.cache_resource
def get_temp_zip_dir():
    temp_dir = tempfile.TemporaryDirectory()
    return temp_dir.name


setup_log()

st.sidebar.header('v3-beta')

load_dotenv()

head()

model_name = st.text_input(
    'Enter the model name: ',
    value=f'decenter-model-{dt.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")}',
)

input_archive = st.file_uploader(
    'Upload working directory of notebook', type=['zip'],
)

starter_script: str  # notebook or python_script

temp_dir: str | tempfile.TemporaryDirectory

temp_zip_dir = get_temp_zip_dir()

python_repl: str = sys.executable

DEMO_MODE: bool = input_archive is None


# DEMO_MODE = st.checkbox('DEMO_MODE') #TODO: wip

if DEMO_MODE:
    st.warning('input archive not found: DEMO_MODE:on')
    input_archive = 'examples/sample_v3'
    temp_dir = 'examples/sample_v3'
    temp_dir_path = temp_dir
else:
    temp_dir = tempfile.TemporaryDirectory()

    temp_dir_path = temp_dir.name

    print('temp dir', temp_dir_path)

    temp_file_path = f'{temp_dir.name}/input_archive.zip'

    print('temp file path', temp_file_path)

    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(input_archive.read())

    # Extract the contents of the archive to the temporary directory
    with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir_path)

    # At this point, the contents of the archive are extracted to the temporary directory
    # You can access the extracted files using the 'temp_dir' path

    # Example: Print the list of extracted files
    extracted_files = os.listdir(temp_dir_path)
    print('extracted:', extracted_files)

    print('temp_dir is ', temp_dir)
    temp_dir_contents = os.listdir(temp_dir_path)
    print('temp_dir contains', temp_dir_contents)  # FIXME error

    venv_dir = os.path.join(temp_dir_path, '.venv')
    venv.create(
        venv_dir, system_site_packages=True,
        with_pip=True, symlinks=True,
    )

    logging.info('created venv dir')

    python_repl = os.path.join(venv_dir, 'bin/python3')


driver_scripts = find_driver_scripts(temp_dir_path)
starter_script = st.selectbox('Training Script:', driver_scripts)

if starter_script:
    script_ext = os.path.splitext(starter_script)[1]

    match script_ext:
        case '.py':
            EXECUTION_LANG: str = TRAINER_PYTHON

            available_requirement_files = find_requirements_txt_files(
                temp_dir_path,
            )
            requirements = st.selectbox(
                'Select dependencies to install', available_requirement_files,
            )
            if not requirements and not DEMO_MODE:
                requirements = os.path.join(os.getcwd(), 'requirements-ml.txt')

            if requirements:
                with st.spinner('Installing dependencies in progress'):

                    requirements_path = os.path.join(
                        temp_dir_path, requirements,
                    )
                    install_dependencies(
                        python_repl, requirements_path, cwd=temp_dir_path,
                    )

            training_cmd = get_python_cmd(
                starter_script, python_interpreter=python_repl,
            )

        case '.ipynb':
            EXECUTION_LANG: str = TRAINER_PYTHON_NB
            # install_deps(
            #     python_repl, requirements="""
            #     """.strip().split(' '), cwd=temp_dir_path,
            # )
            if not DEMO_MODE and MODE != DEVELOPMENT:
                logging.info('installing  deps venv for nb')
                install_dependencies(
                    python_repl, './requirements-ml.txt',
                )
            python_repl = sys.executable  # FIXME:

            training_cmd = get_notebook_cmd(starter_script, python_repl)

        case _:
            raise Exception(f'invalid script-{script_ext}')

if training_cmd and st.button('Train'):

    print(starter_script)

    st.snow()

    EXECUTION_SUCCESS = True
    # command = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{temp_dir}/{starter_notebook}', '--no-browser', '--notebook-dir', temp_dir]
    with st.spinner():
        result = subprocess.run(
            training_cmd, cwd=temp_dir_path, capture_output=True, encoding='UTF-8',
        )

        logging.info(result.stdout)  # TODO: logs trace
        logging.info(result.stderr)

        if result.stdout:
            st.info(result.stdout)

        if result.stderr:
            st.warning(result.stderr)

        if EXECUTION_LANG is TRAINER_PYTHON_NB:
            out = f'{starter_script}.html'
            if os.path.exists(os.path.join(temp_dir_path, f'{starter_script}.html')):
                st.info(f'notebook: output generated at {out}')
                print(f'notebook: output generated at {out}')
            else:
                EXECUTION_SUCCESS = False
                st.error('notebook: execution failed')
                print('notebook:', 'execution failed')

    if EXECUTION_SUCCESS:
        shutil.rmtree(venv_dir)

        zipfile_ = archive_directory(
            f'{temp_zip_dir}/{model_name}', temp_dir_path,
        )
        # zipfile_ = archive_directory_in_memory(temp_dir_path)

        st.toast('executed the notebook successfully')

        st.balloons()

        with open(zipfile_, 'rb') as f1:
            st.download_button(
                label='Download Working Directory',
                data=f1, file_name=f'decenter-{os.path.basename(zipfile_)}',
            )

    if hasattr(temp_dir, 'cleanup'):
        print('cleaning up the temp dirctory')
        temp_dir.cleanup()
