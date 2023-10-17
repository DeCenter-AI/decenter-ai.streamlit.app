import logging
import os
import platform
import sys
import tempfile
import venv
from dataclasses import dataclass

import streamlit as st
from dataclasses_json import dataclass_json, LetterCase
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config.constants import EXECUTION_TEMPLATE
from utils.archive import archive_directory


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(slots=True)
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

    python_repl: str = sys.executable
    venv_dir: str = None
    exit_code: bool = True

    _input_archive: UploadedFile | str = None

    @property
    def input_archive(self):
        return self._input_archive

    @input_archive.setter
    def input_archive(self, input_archive: UploadedFile | str):
        if not self._input_archive:
            logging.debug("input_archive: not found")
            self._input_archive = "samples/sample_v3"
            self.work_dir = "samples/sample_v3"
            self.demo = True
            return
        self.demo = False
        self._input_archive = input_archive
        logging.info(f"set input_archive: {input_archive}")

    @property
    def work_dir(self):
        return self._work_dir

    @work_dir.setter
    def work_dir(self, _work_dir: str):
        if not _work_dir:
            logging.warning("no work_dir found")
            return
        self._work_dir = _work_dir

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

    def create_venv(self, venv_dir=".venv"):
        venv_dir = os.path.join(self.work_dir, venv_dir)
        self.venv_dir = venv_dir

        venv.create(
            venv_dir,
            system_site_packages=True,
            with_pip=True,
            symlinks=True,  # TODO: disable in the future
        )

        logging.info("created venv dir")

        match platform.system():
            case "Windows":
                python_repl = os.path.join(venv_dir, "Scripts", "python.exe")
            case _:
                python_repl = os.path.join(venv_dir, "bin", "python3")

        self.python_repl = python_repl

    def export_working_dir(self) -> str:
        zipfile_ = archive_directory(
            f"{self.models_archive_dir}/{self.model_name}",
            self.work_dir,
        )
        # zipfile_ = archive_directory_in_memory(app.work_dir)
        return zipfile_
