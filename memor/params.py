# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.3"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"

INVALID_PATH_MESSAGE = "Invalid path. Path must be a string."
PATH_DOES_NOT_EXIST_MESSAGE = "Path {0} does not exist."
INVALID_STR_VALUE_MESSAGE = "Invalid value. `{0}` must be a string."
INVALID_BOOL_VALUE_MESSAGE = "Invalid value. `{0}` must be a boolean."
INVALID_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{0}` must be a positive float."
INVALID_POSINT_VALUE_MESSAGE = "Invalid value. `{0}` must be a positive integer."
INVALID_PROB_VALUE_MESSAGE = "Invalid value. `{0}` must be a value between 0 and 1."
INVALID_LIST_OF_X_MESSAGE = "Invalid value. `{0}` must be a list of {1}."
INVALID_DATETIME_MESSAGE = "Invalid value. `{0}` must be a datetime object that includes timezone information."
INVALID_TEMPLATE_MESSAGE = "Invalid template. It must be an instance of `PromptTemplate` or `PresetPromptTemplate`."
INVALID_RESPONSE_MESSAGE = "Invalid response. It must be an instance of `Response`."
INVALID_MESSAGE = "Invalid message. It must be an instance of `Prompt` or `Response`."
INVALID_MESSAGE_STATUS_LEN_MESSAGE = "Invalid message status length. It must be equal to the number of messages."
INVALID_CUSTOM_MAP_MESSAGE = "Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."
INVALID_ROLE_MESSAGE = "Invalid role. It must be an instance of Role enum."
INVALID_TEMPLATE_STRUCTURE_MESSAGE = "Invalid template structure. It should be a JSON object with proper fields."
INVALID_PROMPT_STRUCTURE_MESSAGE = "Invalid prompt structure. It should be a JSON object with proper fields."
INVALID_RESPONSE_STRUCTURE_MESSAGE = "Invalid response structure. It should be a JSON object with proper fields."
INVALID_RENDER_FORMAT_MESSAGE = "Invalid render format. It must be an instance of RenderFormat enum."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
UNSUPPORTED_OPERAND_ERROR_MESSAGE = "Unsupported operand type(s) for {0}: `{1}` and `{2}`"
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."


class Role(Enum):
    """Role enum."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DEFAULT = USER


class RenderFormat(Enum):
    """Render format."""

    STRING = "STRING"
    OPENAI = "OPENAI"
    DICTIONARY = "DICTIONARY"
    ITEMS = "ITEMS"
    DEFAULT = STRING
