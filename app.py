import datetime as dt
import logging
import os.path
import subprocess

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


if starter_notebook and st.button('Execute'):

    logging.info('starter-notebook', starter_notebook)

    st.snow()

    # It will save executed notebook to your-notebook.nbconvert.ipynb file. You can specify the custom output name and custom output director
    cmd_string = 'jupyter nbconvert --execute --to notebook --output custom-name --output-dir /custom/path/ your-notebook.ipynb'

    cmd_string = 'jupyter nbconvert --execute --to notebook --allow-errors your-notebook.ipynb'
    #  You can execute the notebook and save output into PDF or HTML format. Additionally, you can hide code in the final notebook. The example command that will execute notebook and save it as HTML file with code hidden.
    cmd_string = 'jupyter nbconvert --execute --to html --no-input your-notebook.ipynb'

    cmd_string = f'jupyter nbconvert --execute --to notebook {starter_notebook}'
    command = cmd_string.split(' ')
    # command = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{temp_dir}/{starter_notebook}', '--no-browser', '--notebook-dir', temp_dir]
    with st.spinner():
        result = subprocess.run(command, capture_output=True, encoding='UTF-8')

    # print(result.stdout) #TODO: logs trace
    # print(result.stderr)

    zipfile_ = archive_directory(model_name, temp_dir)

    st.toast('executed the notebook successfully')

    st.balloons()

    with open(zipfile_, 'rb') as f1:
        st.download_button(
            label='download working directory',
            data=f1, file_name=os.path.basename(zipfile_),
        )
