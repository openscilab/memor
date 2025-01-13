# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.1"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

INVALID_PATH_MESSAGE = "Invalid path. Path must be a string."
PATH_DOES_NOT_EXIST_MESSAGE = "Path {0} does not exist."
INVALID_NONSTR_VALUE_MESSAGE = "Invalid value. `{0}` must be a string."
INVALID_NON_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{0}` must be a positive float."
INVALID_LIST_OF_STR_MESSAGE = "Invalid value. `{0}` must be a list of strings."
INVALID_TEMPLATE_MESSAGE = "Invalid template. It must be an instance of `CustomPromptTemplate` object."
INVALID_COSUTOM_MAP_MESSAGE = "Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."
INVALID_ROLE_MESSAGE = "Invalid role. It must be an instance of Role enum."
INVALID_TEMPLATE_FILE_MESSAGE = "Invalid template file. It should be a JSON file with proper fields."
INVALID_PROMPT_FILE_MESSAGE = "Invalid prompt file. It should be a JSON file with proper fields."
INVALID_RENDER_FORMAT_MESSAGE = "Invalid render format. It must be an instance of PromptRenderFormat enum."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."


class PromptRenderFormat(Enum):
    """Prompt render format."""

    STRING = "STRING"
    AISUITE = "AISUITE"
    DICTIONARY = "DICTIONARY"
    ITEMS = "ITEMS"
    DEFAULT = STRING
