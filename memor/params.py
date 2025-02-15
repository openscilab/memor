# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.1"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"

# TODO: error message uniformity (NONX -> X)
INVALID_PATH_MESSAGE = "Invalid path. Path must be a string."
PATH_DOES_NOT_EXIST_MESSAGE = "Path {0} does not exist."
INVALID_NONSTR_VALUE_MESSAGE = "Invalid value. `{0}` must be a string."
INVALID_NOBOOL_VALUE_MESSAGE = "Invalid value. `{0}` must be a boolean."
INVALID_NON_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{0}` must be a positive float."
INVALID_NON_PROB_VALUE_MESSAGE = "Invalid value. `{0}` must be a value between 0 and 1."
INVALID_LIST_OF_STR_MESSAGE = "Invalid value. `{0}` must be a list of strings."
INVALID_LIST_OF_BOOL_MESSAGE = "Invalid value. `{0}` must be a list of booleans."
INVALID_DATETIME_MESSAGE = "Invalid value. `{0}` must be a datetime object."
INVALID_TEMPLATE_MESSAGE = "Invalid template. It must be an instance of `PromptTemplate` or `PresetPromptTemplate` objects."
INVALID_RESPONSE_MESSAGE = "Invalid response. It must be an instance of `Response` object."
INVALID_PROMPT_MESSAGE = "Invalid prompt. It must be an instance of `Prompt` object."
INVALID_PROMPTS_MESSAGE = "Invalid prompts. It must be a list of `Prompt` objects."
INVALID_RESPONSES_MESSAGE = "Invalid responses. It must be a list of `Response` objects."
INVALID_CUSTOM_MAP_MESSAGE = "Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."
INVALID_ROLE_MESSAGE = "Invalid role. It must be an instance of Role enum."
INVALID_TEMPLATE_STRUCTURE_MESSAGE = "Invalid template structure. It should be a JSON object with proper fields."
INVALID_PROMPT_STRUCTURE_MESSAGE = "Invalid prompt structure. It should be a JSON object with proper fields."
INVALID_RESPONSE_STRUCTURE_MESSAGE = "Invalid response structure. It should be a JSON object with proper fields."
INVALID_RENDER_FORMAT_MESSAGE = "Invalid render format. It must be an instance of PromptRenderFormat enum."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."


class Role(Enum):
    """Role enum."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DEFAULT = USER


class PromptRenderFormat(Enum):
    """Prompt render format."""

    STRING = "STRING"
    OPENAI = "OPENAI"
    DICTIONARY = "DICTIONARY"
    ITEMS = "ITEMS"
    DEFAULT = STRING
