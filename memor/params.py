# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.1"

INVALID_PATH_MESSAGE = "Invalid path. Path must be a string."
PATH_DOES_NOT_EXIST_MESSAGE = "Path does not exist."
INVALID_NONSTR_VALUE_MESSAGE = "Invalid value. `{0}` must be a string.."
INVALID_TEMPLATE_FILE_MESSAGE = "Invalid template file. It should be a JSON file with proper fields."
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."


class PromptRenderFormat(Enum):
    """Prompt render format."""

    OpenAI = "OpenAI"
