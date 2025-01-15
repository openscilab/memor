# -*- coding: utf-8 -*-
"""Memor functions."""
import os
import datetime
from .params import INVALID_PATH_MESSAGE, INVALID_NONSTR_VALUE_MESSAGE
from .params import INVALID_NON_POSFLOAT_VALUE_MESSAGE
from .params import INVALID_LIST_OF_STR_MESSAGE
from .params import PATH_DOES_NOT_EXIST_MESSAGE
from .params import INVALID_CUSTOM_MAP_MESSAGE
from .errors import MemorValidationError


def get_time_utc():
    """
    Get time in UTC format.

    :return: UTC format time as a datetime object
    """
    return datetime.datetime.now(datetime.timezone.utc)


def _validate_string(value, parameter_name):
    """
    Validate string.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a string
    """
    if not isinstance(value, str):
        raise MemorValidationError(INVALID_NONSTR_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_pos_float(value, parameter_name):
    """
    Validate positive float.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a positive float
    """
    if not isinstance(value, float) or value < 0:
        raise MemorValidationError(INVALID_NON_POSFLOAT_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_list_of_str(value, parameter_name):
    """
    Validate list of strings.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a list of strings
    """
    if not isinstance(value, list):
        raise MemorValidationError(INVALID_LIST_OF_STR_MESSAGE.format(parameter_name))

    for x in value:
        if not isinstance(x, str):
            raise MemorValidationError(INVALID_LIST_OF_STR_MESSAGE.format(parameter_name))
    return True


def validate_path(path):
    """
    Validate path property.

    :param path: path
    :type path: any
    :return: True if path is a string and exists
    """
    if not isinstance(path, str):
        raise MemorValidationError(INVALID_PATH_MESSAGE)
    if not os.path.exists(path):
        raise FileNotFoundError(PATH_DOES_NOT_EXIST_MESSAGE.format(path))
    return True


def validate_template_title(title):
    """
    Validate title property in CustomPromptTemplate class.

    :param title: title
    :type title: any
    :return: True if title is valid
    """
    return _validate_string(title, "title")


def validate_template_content(content):
    """
    Validate content property in CustomPromptTemplate class.

    :param content: content
    :type content: any
    :return: True if content is valid
    """
    return _validate_string(content, "content")


def validate_custom_map(custom_map):
    """
    Validate custom map property in CustomPromptTemplate class.

    :param custom_map: custom map
    :type custom_map: any
    :return: True if custom map is a dictionary with keys and values that can be converted to strings
    """
    if not isinstance(custom_map, dict):
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    try:
        for k, v in custom_map.items():
            str(k), str(v)
    except Exception:
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    return True


def validate_prompt_message(message):
    """
    Validate message property in Prompt class.

    :param message: message
    :type message: any
    :return: True if message is valid
    """
    return _validate_string(message, "message")


def validate_prompt_responses(responses):
    """
    Validate responses property in Prompt class.

    :param responses: responses
    :type responses: any
    :return: True if responses is valid
    """
    return _validate_list_of_str(responses, "responses")


def validate_prompt_temperature(temperature):
    """
    Validate temperature property in Prompt class.

    :param temperature: temperature
    :type temperature: any
    :return: True if temperature is valid
    """
    return _validate_pos_float(temperature, "temperature")


def validate_prompt_model(model):
    """
    Validate model property in Prompt class.

    :param model: model
    :type model: any
    :return: True if model is valid
    """
    return _validate_string(model, "model")
