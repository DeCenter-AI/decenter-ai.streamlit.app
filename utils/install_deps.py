import concurrent.futures
import subprocess
import sys

import streamlit as st


@st.cache_resource
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
