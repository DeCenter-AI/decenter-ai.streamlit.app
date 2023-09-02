import datetime
import os
import random
import uuid
from dataclasses import dataclass
from pprint import pprint
from typing import Final
import joblib

import cachetools
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


@st.cache(allow_output_mutation=True)
def load_model(model_file):
    return joblib.load(model_file)


# Review = namedtuple('Review', ['text', 'date', 'sentiment', 'votes'])

# c = cachetools.Cache(maxsize=100)
#
# if 'history' not in st.session_state:
#     print('history not found')
#     st.session_state.history = c
#     c['models'] = []
# else:
#     c = st.session_state.history

# models = c['models']
st.title("Decenter- Decentralized AI Infrastructure for Model training")

new_review_text = st.text_input("Enter a model name: ", value=f"new-{uuid.uuid1()}")
# if st.button("Add Model") and new_review_text.strip() != "":
# models.append(r)


python_code: str

with open('examples/linear-regression.py', 'r') as f1:
    python_code = f1.read()

dataset: str = 'examples/canada_per_capita_income.csv'

# with open('examples/income.csv') as f1:
#     dataset = f1.read()

# python_code = st.file_uploader("Upload Python Code", type=["py"])
pretrained_model = st.file_uploader("Upload Pretrained Model", type=["sav"])
# dataset = st.file_uploader("Upload Dataset", type=["csv"])

if st.button('Train'):
    # Load dataset
    if dataset:

        if pretrained_model:
            model = load_model(pretrained_model)
            st.write("Loaded pretrained model.")
        elif python_code:
            train_model = lambda dataset: {}
            # exec(python_code.getvalue())
            exec(python_code) #FIXME:
            model = train_model(dataset)
            joblib.dump(model, "trained_model.sav")

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
