import datetime as dt
import os.path

import streamlit as st
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
    value=f'model-${dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}',
)

input_archive = st.file_uploader('Upload Archive', type=['zip'])

starter_notebook: str


if not input_archive:
    st.warning('input archive not found: using sample')
    input_archive = 'examples/sample_v3'
    temp_dir = 'examples/sample_v3'
    notebook_name = 'linear-regression.ipynb'


def find_notebooks(path):
    notebooks = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.ipynb'):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                notebooks.append(rel_path)
                # notebooks.append(os.path.join(root, file))
    return notebooks


if temp_dir:
    # notebooks = [f for f in os.listdir(temp_dir) if f.endswith('.ipynb')]
    notebooks = find_notebooks(temp_dir)

    starter_notebook = st.selectbox('Select a notebook:', notebooks)

if starter_notebook:
    pass
    # command = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{temp_dir}/{notebook_name}', '--no-browser', '--notebook-dir', temp_dir]
    #
    # result = subprocess.run(command, capture_output=True, encoding='UTF-8')
    #
    # print(result.stdout)
    # print(result.stderr)

    # with tempfile.TemporaryDirectory() as temp_dir:
    #     shutil.copy(notebook_path, temp_dir)

if st.button('Execute'):
    st.snow()

    # temp_dir = '' #FIXME:

    zipfile_ = archive_directory(model_name, temp_dir)

    st.toast('executed the notebook successfully')

    st.balloons()

    with open(zipfile_, 'rb') as f1:
        st.download_button(
            label='download working directory',
            data=f1, file_name=os.path.basename(zipfile_),
        )
