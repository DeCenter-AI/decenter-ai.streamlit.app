import datetime
import io
import os
import random
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pprint import pprint
from typing import Final
import joblib
import concurrent.futures

import cachetools
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache(allow_output_mutation=True)
def load_model(model_file):
    return joblib.load(model_file)


st.title("Decenter- Decentralized AI Infrastructure for Model training")

model_name = st.text_input("Enter a model name: ", value=f"model-{uuid.uuid1()}")

python_code: str


# with open('examples/linear-regression.py', 'r') as f1:
#     python_code = f1.read()


python_code = st.file_uploader("Upload Python Code", type=["py"])
pretrained_model = st.file_uploader("Upload Pretrained Model", type=["sav"])
dataset = st.file_uploader("Upload Dataset", type=["csv"])
requirements_txt = st.file_uploader("Upload requirements.txt", type=["txt"])

# dataset: str = dataset or 'examples/canada_per_capita_income.csv'


if st.button('Train'):

    if requirements_txt:
        requirements = requirements_txt.getvalue().decode().split('\n')


        def install(package):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

        # Use a ThreadPoolExecutor to install the packages in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(install, requirements)

        # for package in requirements:
        #     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Load dataset
    if dataset:

        if pretrained_model:
            model = load_model(pretrained_model)
            st.write("Loaded pretrained model.")
        elif python_code:
            train_model = lambda dataset: {}
            exec(python_code.getvalue())
            # exec(python_code) #FIXME:
            model = train_model(dataset)
            joblib.dump(model, f"trained-{model_name}-{str(datetime.datetime.now())}.sav")

            st.download_button(
                label="Download trained model",
                data="trained_model.sav",
                file_name="trained_model.sav",
            )
            st.write("Trained a new model.")
        else:
            st.write("Please upload a pretrained model or Python code to train a new model.")
    else:
        st.write("Please upload a dataset.")

# if python_code is not None and pretrained_model is not None and dataset is not None:
#     exec(python_code.getvalue())
#     model = joblib.load(pretrained_model)
#     data = pd.read_csv(dataset)
#
#     # save the model to disk
#     joblib.dump(model, "trained_model.sav")
#
#     # create download button
#     st.download_button(
#         label="Download trained model",
#         data="trained_model.sav",
#         file_name="trained_model.sav",
#
#
#
#     )
