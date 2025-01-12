# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.1"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

INVALID_PATH_MESSAGE = "Invalid path. Path must be a string."
PATH_DOES_NOT_EXIST_MESSAGE = "Path does not exist."
INVALID_NONSTR_VALUE_MESSAGE = "Invalid value. `{0}` must be a string."
INVALID_NON_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{0}` must be a positive float."
INVALID_LIST_OF_STR_MESSAGE = "Invalid value. `{0}` must be a list of strings."
INVALID_TEMPLATE_MESSAGE = "Invalid template. It must be an instance of `CustomPromptTemplate` object."
INVALID_ROLE_MESSAGE = "Invalid role. It must be an instance of Role enum."
INVALID_TEMPLATE_FILE_MESSAGE = "Invalid template file. It should be a JSON file with proper fields."
INVALID_PROMPT_FILE_MESSAGE = "Invalid prompt file. It should be a JSON file with proper fields."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."


class PromptRenderFormat(Enum):
    """Prompt render format."""

    OpenAI = "OpenAI"
