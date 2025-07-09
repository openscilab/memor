# -*- coding: utf-8 -*-
"""Memor parameters and constants."""
from enum import Enum
MEMOR_VERSION = "0.7"

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"

INVALID_PATH_MESSAGE = "Invalid path: must be a string and refer to an existing location. Given path: {path}"
INVALID_STR_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a string."
INVALID_BOOL_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a boolean."
INVALID_POSFLOAT_VALUE_MESSAGE = "Invalid value. `{parameter_name}` must be a positive float."
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
INVALID_MODEL_MESSAGE = "Invalid model. It must be an instance of LLMModel enum or a string."
INVALID_TEMPLATE_STRUCTURE_MESSAGE = "Invalid template structure. It should be a JSON object with proper fields."
INVALID_PROMPT_STRUCTURE_MESSAGE = "Invalid prompt structure. It should be a JSON object with proper fields."
INVALID_RESPONSE_STRUCTURE_MESSAGE = "Invalid response structure. It should be a JSON object with proper fields."
INVALID_SESSION_STRUCTURE_MESSAGE = "Invalid session structure. It should be a JSON object with proper fields."
INVALID_RENDER_FORMAT_MESSAGE = "Invalid render format. It must be an instance of RenderFormat enum."
PROMPT_RENDER_ERROR_MESSAGE = "Prompt template and properties are incompatible."
UNSUPPORTED_OPERAND_ERROR_MESSAGE = "Unsupported operand type(s) for {operator}: `{operand1}` and `{operand2}`"
AI_STUDIO_SYSTEM_WARNING = "Google AI Studio models may not support content with a system role."
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
    AI_STUDIO = "AI STUDIO"
    DICTIONARY = "DICTIONARY"
    ITEMS = "ITEMS"
    DEFAULT = STRING


class LLMModel(Enum):
    """LLM model enum."""

    GPT_O1 = "gpt-o1"
    GPT_O1_MINI = "gpt-o1-mini"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_4_VISION = "gpt-4-vision"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    DAVINCI = "davinci"
    BABBAGE = "babbage"

    CLAUDE_3_5_SONNET = "claude-3.5-sonnet"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_HAIKU = "claude-3-haiku"
    CLAUDE_2 = "claude-2"
    CLAUDE_INSTANT = "claude-instant"

    LLAMA3_70B = "llama3-70b"
    LLAMA3_8B = "llama3-8b"
    LLAMA_GUARD_3_8B = "llama-guard-3-8b"

    MISTRAL_7B = "mistral-7b"
    MIXTRAL_8X7B = "mixtral-8x7b"
    MIXTRAL_8X22B = "mixtral-8x22b"
    MISTRAL_NEMO = "mistral-nemo"
    MISTRAL_TINY = "mistral-tiny"
    MISTRAL_SMALL = "mistral-small"
    MISTRAL_MEDIUM = "mistral-medium"
    MISTRAL_LARGE = "mistral-large"
    CODESTRAL = "codestral"
    PIXTRAL = "pixtral-12b"

    GEMMA_7B = "gemma-7b"
    GEMMA2_9B = "gemma2-9b"
    GEMINI_1_PRO = "gemini-1-pro"
    GEMINI_1_ULTRA = "gemini-1-ultra"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_ULTRA = "gemini-1.5-ultra"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_FLASH = "gemini-2-flash"
    GEMINI_2_PRO = "gemini-2-pro"

    DEEPSEEK_V3 = "deepseek-v3"
    DEEPSEEK_R1 = "deepseek-r1"
    DEEPSEEK_CODER = "deepseek-coder"

    PHI_2 = "phi-2"
    PHI_4 = "phi-4"

    QWEN_1_8B = "qwen-1.8b"
    QWEN_7B = "qwen-7b"
    QWEN_14B = "qwen-14b"
    QWEN_72B = "qwen-72b"

    YI_6B = "yi-6b"
    YI_9B = "yi-9b"
    YI_34B = "yi-34b"

    DEFAULT = "unknown"
