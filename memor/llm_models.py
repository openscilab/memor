# -*- coding: utf-8 -*-
"""Memor LLM model registry."""

from enum import Enum

class _OpenAI(Enum):
    pass

class _Anthropic(Enum):
    pass

class _Google(Enum):
    pass

class _Meta(Enum):
    pass

class _Mistral(Enum):
    pass

class _DeepSeek(Enum):
    pass

class _Qwen(Enum):
    pass

class _Microsoft(Enum):
    pass

class _XAI(Enum):
    pass

class _ZeroOneAI(Enum):
    pass

class _LGAI(Enum):
    pass

class _Other(Enum):
    pass


class LLMModel:
    """LLM model registry."""

    OpenAI = _OpenAI
    Anthropic = _Anthropic
    Google = _Google
    Meta = _Meta
    Mistral = _Mistral
    DeepSeek = _DeepSeek
    Qwen = _Qwen
    Microsoft = _Microsoft
    XAI = _XAI
    ZeroOneAI = _ZeroOneAI
    LGAI = _LGAI
    Other = _Other
    DEFAULT = "unknown"


