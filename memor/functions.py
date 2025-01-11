# -*- coding: utf-8 -*-
"""Memor functions."""
import os
import datetime
from .params import INVALID_PATH_MESSAGE, INVALID_NONSTR_VALUE_MESSAGE
from .params import INVALID_NONFLOAT_VALUE_MESSAGE
from .params import INVALID_NONLIST_VALUE_MESSAGE
from .params import PATH_DOES_NOT_EXIST_MESSAGE
from .errors import MemorValidationError


def get_time_utc():
    """
    Get time in UTC format.
    
    :return: time in UTC format in datetime object
    """
    return datetime.datetime.now(datetime.timezone.utc)


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


def _validate_list(value, parameter_name):
    """
    Validate list.

    :param value: value
    :type value: Any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is valid
    """
    if not isinstance(value, list):
        raise MemorValidationError(INVALID_NONLIST_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_float(value, parameter_name):
    """
    Validate float.

    :param value: value
    :type value: Any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is valid
    """
    if not isinstance(value, float):
        raise MemorValidationError(INVALID_NONFLOAT_VALUE_MESSAGE.format(parameter_name))
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


def validate_prompt_message(message):
    """Validate prompt message.

    :param message: message
    :type message: Any
    :return: True if message is valid
    """
    return _validate_string(message, "message")


def validate_prompt_responses(responses): #TODO: Here we need to check that all of the list items are str or not.
    """Validate prompt responses.

    :param responses: responses
    :type responses: Any
    :return: True if responses is valid
    """
    return _validate_list(responses, "responses")


def validate_prompt_temperature(temperature): #TODO: Temperature >= 0
    """Validate prompt temperature.

    :param temperature: temperature
    :type temperature: Any
    :return: True if temperature is valid
    """
    return _validate_float(temperature, "temperature")


def validate_prompt_model(model):
    """Validate prompt model.

    :param model: model
    :type model: Any
    :return: True if model is valid
    """
    return _validate_string(model, "model")
