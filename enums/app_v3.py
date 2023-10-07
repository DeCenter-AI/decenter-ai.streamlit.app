import logging
import tempfile
from dataclasses import dataclass

import streamlit as st

from config.constants import EXECUTION_TEMPLATE


@dataclass
class App:
    version: str = "v3"
    demo: bool = True
    _model_name: str = "decenter-model-linear-reg-sample_v3"
    model_name_changed: bool = False

    exec_mode: EXECUTION_TEMPLATE = None
    starter_script: str = None
    requirements_path: str = None
    _work_dir: str = None
    temp_dir: tempfile.TemporaryDirectory = None
    models_archive_dir = tempfile.TemporaryDirectory(
        prefix="decenter-ai-",
        suffix="-models-zip-dir",
    ).name

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, _work_dir: str):
        if not _work_dir:
            logging.warning("no work_dir found")
            return
        self._work_dir = _work_dir

    def set_model_name(self, model_name: str):
        self.model_name = model_name
        self.model_name_changed = True

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, model_name: str):
        if not model_name:
            st.toast("model name not changed")
            logging.debug("model_name: invalid")
            return

        self.model_name_changed = (
            model_name != "decenter-model-linear-reg-sample_v3"
        )

        if self.model_name_changed:
            self._model_name = model_name
            st.toast(f"model name updated to {model_name}", icon="👌")
