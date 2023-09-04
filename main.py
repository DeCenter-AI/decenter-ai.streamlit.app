import importlib.util
import io
import time

import joblib
import streamlit as st
from colorama import Fore
from dotenv import load_dotenv

from enums.model_trainer import ModelTrainer
from models.model import c, getModelTrainer
from utils.install_deps import install_dependencies
from views.head import head

load_dotenv()

head()

model_name = st.text_input("Enter a model name: ", value=f"model")

m1: ModelTrainer = getModelTrainer(model_name)

# with open('examples/linear-regression.py', 'r') as f1:
#     python_code = f1.read()
# dataset: str = dataset or 'examples/canada_per_capita_income.csv'

python_code = st.file_uploader("Upload Python Code", type=["py"])
dataset = st.file_uploader("Upload Dataset", type=["csv"])
requirements_txt = st.file_uploader("Upload requirements.txt", type=["txt"])

install_dependencies(requirements_txt)

loaded_model = None

if python_code and dataset:
    module_name = '__temp_module__'
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    # spec.loader.load_module() #FIXME: install and inject deps to the module only
    # Compile and execute the code within the module
    exec(python_code.getvalue(), module.__dict__)

    m1: ModelTrainer = module.__dict__["ModelTrainer"](dataset, loaded_model)

    c[model_name] = m1
    # train_model: Callable[[UploadedFile, UploadedFile], any] = module.__dict__["train_model"]

    pretrained_model = st.file_uploader("Upload Pretrained Model", type=["sav"])

    if pretrained_model:
        loaded_model = joblib.load(pretrained_model)
        st.write("Loaded pretrained model.")

        if st.button('Score: Pretrained Model'):
            score = m1.calculate_score(loaded_model, m1.X, m1.y)
            st.write(f"Pretrained-Model Score: {score * 100:0.3f}%")

if st.button('Train'):
    # if not dataset:
    #     st.write("Please upload a dataset.")
    #
    # if not python_code:
    #     st.write("Please upload Python code to train the model.")

    # if python_code and dataset:
    start_time = time.time()
    model = m1.train_model()
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"{Fore.CYAN} Elapsed time: {elapsed_time:.6f} sec {Fore.RESET}")

    fName = f"trained-{model_name}-{elapsed_time:.6f}s.sav"

    model_bytes = io.BytesIO()
    joblib.dump(m1.trained_model, model_bytes)
    model_bytes.seek(0)

    # st.write("Trained a new model")

    score = m1.calculate_score()

    st.write(f"Training Duration: {elapsed_time:.6f}s")
    st.write(f"Trained Model Score: {score * 100:0.3f}%")

    # if st.button('Score: Trained Model'):
    #     score = m1.calculate_score(m1.trained_model, m1.X, m1.y)
    #     st.write(f"Trained Model Score: {score * 100:0.3f}")

    st.download_button(
        label="Download trained model",
        data=model_bytes,
        file_name=fName,
    )
