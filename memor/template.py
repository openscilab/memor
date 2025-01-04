# -*- coding: utf-8 -*-
"""Template class."""
from enum import Enum


class CustomPromptTemplate:
    """Prompt template."""

    def __init__(self, content):
        """
        Template object initiator.

        :param content: template content
        :type content: str
        """
        self._content = content


DEFAULT_TEMPLATE = CustomPromptTemplate(content="{message}")
