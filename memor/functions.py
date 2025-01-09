# -*- coding: utf-8 -*-
"""Memor functions."""
import os
from .params import INVALID_PATH_MESSAGE, INVALID_NONSTR_VALUE_MESSAGE
from .params import PATH_DOES_NOT_EXIST_MESSAGE
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
    if not os.path.exists(path):
        raise MemorValidationError(PATH_DOES_NOT_EXIST_MESSAGE)
    return True


def _validate_string(value, parameter_name):
    """
    Validate string.

    :param value: value
    :type value: Any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is valid
    """
    if not isinstance(value, str):
        raise MemorValidationError(INVALID_NONSTR_VALUE_MESSAGE.format(parameter_name))
    return True


def validate_template_title(title):
    """Validate title.

    :param title: title
    :type title: Any
    :return: True if title is valid
    """
    return _validate_string(title, "title")


def validate_template_content(content):
    """Validate template content.

    :param content: content
    :type content: Any
    :return: True if content is valid
    """
    return _validate_string(content, "content")
