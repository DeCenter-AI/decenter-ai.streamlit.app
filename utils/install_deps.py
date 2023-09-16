import concurrent.futures
import logging
import subprocess
import sys

import streamlit as st


@st.cache_resource
def install_dependencies_v1(requirements_txt):
    if not requirements_txt:
        return
    requirements = requirements_txt

    def install(package):
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', package],
        )

    # Use a ThreadPoolExecutor to install the packages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(install, requirements)


@st.cache_resource
def install_dependencies_v2(requirements_txt):
    if not requirements_txt:
        return
    requirements = requirements_txt

    def install(package):
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', package],
        )

    # Use a ThreadPoolExecutor to install the packages in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(install, requirements)

    # for package in requirements:
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", package])


@st.cache_resource
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
