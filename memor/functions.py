# -*- coding: utf-8 -*-
"""Memor functions."""

from .params import INVALID_PATH_MESSAGE, INVALID_NONSTR_VALUE_MESSAGE
from .errors import MemorValidationError


def validate_path(path):
    """
    Validate path.
    
    :param path: path
    :type path: Any
    :return: True if path is valid
    """
    if not isinstance(path, str):
        raise MemorValidationError(INVALID_PATH_MESSAGE)
    return True


def _validate_string(value):
    """
    Validate string.
    
    :param value: value
    :type value: Any
    :return: True if value is valid
    """
    if not isinstance(value, str):
        raise MemorValidationError(INVALID_NONSTR_VALUE_MESSAGE)
    return True


def validate_template_title(title):
    """Validate title.
    
    :param title: title
    :type title: Any
    :return: True if title is valid
    """
    return _validate_string(title)

def validate_template_content(content):
    """Validate template content.
    
    :param content: content
    :type content: Any
    :return: True if content is valid
    """
    return _validate_string(content)
