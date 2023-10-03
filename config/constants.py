import os
from typing import Final, TypeAlias, Literal

from dotenv import load_dotenv

load_dotenv()

PRODUCTION: Final[str] = "production"
DEVELOPMENT: Final[str] = "development"
TESTING: Final[str] = "testing"
MODE: Final[str] = os.getenv("mode", DEVELOPMENT)

#
# OPENAI_API_KEY: Final[str] = environ['OPENAI_API_KEY'].strip()
# OPENAI_ORGANIZATION_ID: Final[str] = environ.get(
#     'OPENAI_ORGANIZATION_ID', '',
# ).strip()
# OPENAI_EMBEDDINGS_LLM: Final[str] = os.getenv(
#     'OPENAI_EMBEDDINGS_LLM', 'text-embedding-ada-002',
# ).strip()
# OPENAI_CHAT_MODEL: Final[str] = os.getenv(
#     'OPENAI_CHAT_MODEL', 'gpt-3.5-turbo',
# ).strip()

TRAINER_PYTHON: Final[str] = ".py"
TRAINER_PYTHON_NB: Final[str] = ".pynb"


EXECUTION_TEMPLATE: TypeAlias = Literal[TRAINER_PYTHON, TRAINER_PYTHON_NB]
