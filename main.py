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


python_code = st.file_uploader("Upload Python Code", type=["py"])
pretrained_model = st.file_uploader("Upload Pretrained Model", type=["sav"])
dataset = st.file_uploader("Upload Dataset", type=["csv"])

if python_code is not None and pretrained_model is not None and dataset is not None:
    exec(python_code.getvalue())
    model = joblib.load(pretrained_model)
    data = pd.read_csv(dataset)

    # save the model to disk
    joblib.dump(model, "trained_model.sav")

    # create download button
    st.download_button(
        label="Download trained model",
        data="trained_model.sav",
        file_name="trained_model.sav",
    )
