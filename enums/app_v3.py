import logging
import tempfile
from dataclasses import dataclass

import streamlit as st

from config.constants import EXECUTION_TEMPLATE


@dataclass
class App:
    version: str = "v3"
    demo: bool = True
    model_name: str = "decenter-model-linear-reg-sample_v3"
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

    def validate_model_name(self):
        if not self.model_name:
            self.model_name_changed = False
            self.model_name = "decenter-model-linear-reg-sample_v3"
            st.toast(f"model name reverted to {self.model_name}", icon="👎")
        elif not self.model_name == "decenter-model-linear-reg-sample_v3":
            self.model_name_changed = True
            st.toast(f"model name updated to {self.model_name}", icon="👌")

        logging.info(self.model_name)
