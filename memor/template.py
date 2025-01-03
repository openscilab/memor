# -*- coding: utf-8 -*-
"""Template class."""
from enum import Enum

class PromptTemplate:
    def __init__(self, content):
        self._content = content

DEFAULT_TEMPLATE = PromptTemplate(content="{message}")


