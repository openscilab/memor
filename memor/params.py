# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "1.2"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"

INVALID_PATH_MESSAGE = "Invalid path: must be a string and refer to an existing location. Given path: {path}"
INVALID_STR_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a string."
INVALID_BOOL_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a boolean."
INVALID_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a positive number."
INVALID_POSINT_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a positive integer."
INVALID_PROB_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a value between 0 and 1."
INVALID_LIST_OF_X_MESSAGE = "Invalid value. `{parameter_name}` must be a list of {type_name}."
INVALID_INT_OR_STR_MESSAGE = "Invalid value. `{parameter_name}` must be an integer or a string."
INVALID_INT_OR_STR_SLICE_MESSAGE = "Invalid value. `{parameter_name}` must be an integer, string or a slice."
INVALID_DATETIME_MESSAGE = "Invalid value. `{parameter_name}` must be a datetime object that includes timezone information."
INVALID_TEMPLATE_MESSAGE = "Invalid template. It must be an instance of `PromptTemplate` or `PresetPromptTemplate`."
INVALID_RESPONSE_MESSAGE = "Invalid response. It must be an instance of `Response`."
INVALID_MESSAGE = "Invalid message. It must be an instance of `Prompt` or `Response`."
INVALID_MESSAGE_STATUS_LEN_MESSAGE = "Invalid message status length. It must be equal to the number of messages."
INVALID_CUSTOM_MAP_MESSAGE = "Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."
INVALID_ROLE_MESSAGE = "Invalid role. It must be an instance of Role enum."
INVALID_ID_MESSAGE = "Invalid message ID. It must be a valid UUIDv4."
INVALID_MODEL_MESSAGE = "Invalid model. It must be an instance of LLMModel.<provider> enum or a string."
INVALID_TEMPLATE_STRUCTURE_MESSAGE = "Invalid template structure. It should be a JSON object with proper fields."
INVALID_PROMPT_STRUCTURE_MESSAGE = "Invalid prompt structure. It should be a JSON object with proper fields."
INVALID_RESPONSE_STRUCTURE_MESSAGE = "Invalid response structure. It should be a JSON object with proper fields."
INVALID_SESSION_STRUCTURE_MESSAGE = "Invalid session structure. It should be a JSON object with proper fields."
INVALID_RENDER_FORMAT_MESSAGE = "Invalid render format. It must be an instance of RenderFormat enum."
INVALID_TEMPLATE_ENGINE_MESSAGE = "Invalid template engine. It must be an instance of TemplateEngine enum."
INVALID_WARNINGS_STRUCTURE_MESSAGE = "Invalid `warnings` structure. It must be a valid dictionary."
INVALID_XML_TREE_MESSAGE = "Invalid XML tree structure."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
TEMPLATE_RENDER_ERROR_MESSAGE = "Template and context are incompatible."
UNSUPPORTED_OPERAND_ERROR_MESSAGE = "Unsupported operand type(s) for {operator}: `{operand1}` and `{operand2}`"
AI_STUDIO_SYSTEM_WARNING = "Google AI Studio models may not support content with a system role."
DATA_SAVE_SUCCESS_MESSAGE = "Everything seems good."
MESSAGE_SIZE_WARNING = "Message {message_id} exceeded size threshold ({current_size} > {threshold})."
SESSION_SIZE_WARNING = "Session exceeded size threshold ({current_size} > {threshold})."

XML_PATTERN = r"<([a-zA-Z_][\w\-\.]*)(\s[^<>]*?)?>.*?</\1\s*>|<([a-zA-Z_][\w\-\.]*)(\s[^<>]*?)?/?>"
JINJA_VARIABLES_PATTERN = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)"

DATAFRAME_MAIN_COLUMNS = ["type", "message", "role", "id", "date_created", "date_modified"]


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
    AI_STUDIO = "AI STUDIO"
    DICTIONARY = "DICTIONARY"
    ITEMS = "ITEMS"
    DEFAULT = STRING


class TemplateEngine(Enum):
    """Template engine."""

    FORMAT = "format"
    JINJA = "jinja"
    DEFAULT = FORMAT
