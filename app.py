import datetime as dt
import logging
import os.path
import subprocess
import tempfile
import zipfile

import streamlit as st
import venv
from dotenv import load_dotenv

from utils.archive import archive_directory
from views.head import head

st.set_page_config(
    page_title='Decenter AI',
    page_icon='static/favicon.ico',
)

st.sidebar.header('v3-beta')

load_dotenv()

head()

# @st.cache_data
# def get_python_code(filename: str, label: str):
#     return


model_name = st.text_input(
    'Enter the model name: ',
    value=f'decenter-model-{dt.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")}',
)

input_archive = st.file_uploader(
    'Upload working directory of notebook', type=['zip'],
)

starter_script: str  # notebook or python_script

temp_dir: str | tempfile.TemporaryDirectory

if not input_archive:
    st.warning('input archive not found: using sample')
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
    import os
    extracted_files = os.listdir(temp_dir_path)
    print('extracted:', extracted_files)


def find_notebooks(path):
    notebooks = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.ipynb'):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                notebooks.append(rel_path)
                # notebooks.append(os.path.join(root, file))
    return notebooks


def find_notebook_scripts(path):
    driver_codes = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.ipynb') or file.endswith('.py'):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                driver_codes.append(rel_path)
                # notebooks.append(os.path.join(root, file))
    return driver_codes


if temp_dir:
    print('temp_dir is ', temp_dir)
    temp_dir_contents = os.listdir(temp_dir_path)
    print('temp_dir contains', temp_dir_contents)  # FIXME error
    # notebooks = [f for f in os.listdir(temp_dir) if f.endswith('.ipynb')]
    driver_scripts = find_notebook_scripts(temp_dir_path)

    starter_script = st.selectbox('Select a notebook:', driver_scripts)


def run_notebook():
    # It will save executed notebook to your-notebook.nbconvert.ipynb file. You can specify the custom output name and custom output director
    cmd_string = 'jupyter nbconvert --execute --to notebook --output custom-name --output-dir /custom/path/ your-notebook.ipynb'

    cmd_string = 'jupyter nbconvert --execute --to notebook --allow-errors your-notebook.ipynb'
    #  You can execute the notebook and save output into PDF or HTML format. Additionally, you can hide code in the final notebook. The example command that will execute notebook and save it as HTML file with code hidden.
    cmd_string = f'jupyter nbconvert --execute --to html --no-input {starter_script}'
    cmd_string = f'jupyter nbconvert --execute --to html  {starter_script}'

    # cmd_string = f'jupyter nbconvert --execute --to notebook {starter_notebook}'
    command = cmd_string.split(' ')

    return command


def run_python_script(python_interpreter='python3'):
    command = [python_interpreter, starter_script]
    return command


def find_requirements_txt_files(root_directory):
    requirements_files = []

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.txt') and file.startswith('requirements'):
                rel_path = os.path.relpath(
                    os.path.join(root, file), root_directory,
                )
                requirements_files.append(rel_path)

    logging.info('requirements', requirements_files)

    return requirements_files


execution_modes = {
    '.py': run_python_script,
    '.ipynb': run_notebook,
}


def install_dependencies(python_repl='python3', requirements_path=None):

    if not requirements_path:
        logging.warning('requirements not found')
        return
    logging.info('installing deps')
    command = [python_repl, '-m', 'pip', 'install', '-r', requirements_path]
    result = subprocess.run(command, capture_output=True, encoding='UTF-8')

    logging.debug(result.stdout)
    logging.debug(result.stderr)
    return result


if starter_script:
    script_ext = os.path.splitext(starter_script)[1]

    match script_ext:
        case '.py':
            available_requirement_files = find_requirements_txt_files(
                temp_dir_path,
            )
            requirements = st.selectbox(
                'Select dependencies to install', available_requirement_files,
            )

            venv_dir: str = None

            python_repl = 'python3'

            if requirements:
                with st.spinner('Installing dependencies in progress'):
                    venv_dir = os.path.join(temp_dir_path, 'venv')
                    venv.create(venv_dir, with_pip=True)
                    python_repl = f'venv/bin/python3'

                    print('venv contains', os.listdir(venv_dir))

                    requirements_path = os.path.join(
                        temp_dir_path, requirements,
                    )
                    install_dependencies(python_repl, requirements_path)

            command = run_python_script(python_interpreter=python_repl)

        case '.ipynb':
            command = run_notebook()

        case _:
            raise Exception(f'invalid script-{script_ext}')


if command and st.button('Execute'):

    # TODO: revive python script, requirements.txt from v1

    logging.info('starter-script', starter_script)

    st.snow()

    # command = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{temp_dir}/{starter_notebook}', '--no-browser', '--notebook-dir', temp_dir]
    with st.spinner():
        result = subprocess.run(command, capture_output=True, encoding='UTF-8')

    # print(result.stdout) #TODO: logs trace
    # print(result.stderr)

    zipfile_ = archive_directory(model_name, temp_dir_path)

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
