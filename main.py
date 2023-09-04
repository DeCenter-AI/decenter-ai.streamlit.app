import datetime
import importlib
import io
import os
import random
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pprint import pprint
from typing import Final, TextIO, Callable
import joblib
import concurrent.futures
import importlib.util

import cachetools
import pandas as pd
import streamlit as st
from colorama import Fore
from dotenv import load_dotenv
from streamlit.runtime.uploaded_file_manager import UploadedFile

from enums.model_trainer import ModelTrainer

load_dotenv()

with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def load_model(model_object: str | io.BytesIO):
    return joblib.load(model_object)


col1, col2, col3 = st.columns([1, 2, 1])
col2.image("static/logo.png", width=300)

# st.image("static/stand.png")
st.title("AI Infrastructure for Model training")

model_name = st.text_input("Enter a model name: ", value=f"model")

python_code: str

# with open('examples/linear-regression.py', 'r') as f1:
#     python_code = f1.read()
# dataset: str = dataset or 'examples/canada_per_capita_income.csv'

python_code = st.file_uploader("Upload Python Code", type=["py"])
pretrained_model = st.file_uploader("Upload Pretrained Model", type=["sav"])
dataset = st.file_uploader("Upload Dataset", type=["csv"])
requirements_txt = st.file_uploader("Upload requirements.txt", type=["txt"])


def install_dependencies(requirements_txt):
    if not requirements_txt:
        return
    requirements = requirements_txt.getvalue().decode().split('\n')

    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Use a ThreadPoolExecutor to install the packages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(install, requirements)

    # for package in requirements:
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if st.button('Train'):
    install_dependencies(requirements_txt)

    loaded_model = None

    if pretrained_model:
        loaded_model = load_model(pretrained_model)
        st.write("Loaded pretrained model.")
    # Load dataset
    if not dataset:
        st.write("Please upload a dataset.")

    if python_code and dataset:
        module_name = '__temp_module__'
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        # spec.loader.load_module() #FIXME: install and inject deps to the module only
        # Compile and execute the code within the module
        exec(python_code.getvalue(), module.__dict__)

        m1: ModelTrainer = module.__dict__["ModelTrainer"](dataset, pretrained_model)
        # train_model: Callable[[UploadedFile, UploadedFile], any] = module.__dict__["train_model"]

        start_time = time.time()
        model = m1.train_model()
        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"{Fore.GREEN} Elapsed time: {elapsed_time:.6f} seconds")

        fName = f"trained-{model_name}-{str(datetime.datetime.now())}-{elapsed_time:.6f}s.sav"

        model_bytes = io.BytesIO()
        joblib.dump(m1.trained_model, model_bytes)
        model_bytes.seek(0)

        st.write("Trained a new model")

        score = m1.calculate_score()
        st.write(f"Model Score: {score * 100:0.3f}")

        st.download_button(
            label="Download trained model",
            data=model_bytes,
            file_name=fName,
        )
    else:
        st.write("Please upload Python code to train the model.")
