# -*- coding: utf-8 -*-
"""Memor functions."""
import os
import datetime
from .params import INVALID_DATETIME_MESSAGE
from .params import INVALID_PATH_MESSAGE, INVALID_STR_VALUE_MESSAGE
from .params import INVALID_PROB_VALUE_MESSAGE
from .params import INVALID_POSFLOAT_VALUE_MESSAGE
from .params import INVALID_POSINT_VALUE_MESSAGE
from .params import PATH_DOES_NOT_EXIST_MESSAGE
from .params import INVALID_CUSTOM_MAP_MESSAGE
from .params import INVALID_BOOL_VALUE_MESSAGE
from .params import INVALID_LIST_OF_X_MESSAGE
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
        raise MemorValidationError(INVALID_STR_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_bool(value, parameter_name):
    """
    Validate boolean.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a boolean
    """
    if not isinstance(value, bool):
        raise MemorValidationError(INVALID_BOOL_VALUE_MESSAGE.format(parameter_name))
    return True


def _can_convert_to_string(value):
    """
    Check if value can be converted to string.

    :param value: value
    :type value: any
    :return: True if value can be converted to string
    """
    try:
        str(value)
    except Exception:
        return False
    return True


def _validate_pos_int(value, parameter_name):
    """
    Validate positive integer.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a positive integer
    """
    if not isinstance(value, int) or value < 0:
        raise MemorValidationError(INVALID_POSINT_VALUE_MESSAGE.format(parameter_name))
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
        raise MemorValidationError(INVALID_POSFLOAT_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_probability(value, parameter_name):
    """
    Validate probability.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if value is a float between 0 and 1
    """
    if not isinstance(value, float) or value < 0 or value > 1:
        raise MemorValidationError(INVALID_PROB_VALUE_MESSAGE.format(parameter_name))
    return True


def _validate_list_of(value, parameter_name, type_, type_name):
    """
    Validate list of values.

    :param value: value
    :type value: any
    :param parameter_name: parameter name
    :type parameter_name: str
    :param type_: type
    :type type_: type
    :param type_name: type name
    :type type_name: str
    :return: True if value is a list of type_
    """
    if not isinstance(value, list):
        raise MemorValidationError(INVALID_LIST_OF_X_MESSAGE.format(parameter_name, type_name))

    if not all(isinstance(x, type_) for x in value):
        raise MemorValidationError(INVALID_LIST_OF_X_MESSAGE.format(parameter_name, type_name))
    return True


def _validate_date_time(date_time, parameter_name):
    """
    Validate date time.

    :param date_time: date time
    :type date_time: datetime.datetime
    :param parameter_name: parameter name
    :type parameter_name: str
    :return: True if date time is a datetime object
    """
    if not isinstance(date_time, datetime.datetime) or date_time.tzinfo is None:
        raise MemorValidationError(INVALID_DATETIME_MESSAGE.format(parameter_name))
    return True


def _validate_path(path):
    """
    Validate path property.

    :param path: path
    :type path: any
    :return: True if path is a string and exists
    """
    if not isinstance(path, str):  # TODO: We should combine these two errors.
        raise MemorValidationError(INVALID_PATH_MESSAGE)
    if not os.path.exists(path):
        raise FileNotFoundError(PATH_DOES_NOT_EXIST_MESSAGE.format(path))
    return True


def _validate_custom_map(custom_map):
    """
    Validate custom map property in PromptTemplate class.

    :param custom_map: custom map
    :type custom_map: any
    :return: True if custom map is a dictionary with keys and values that can be converted to strings
    """
    if not isinstance(custom_map, dict):
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    if not all(_can_convert_to_string(k) and _can_convert_to_string(v) for k, v in custom_map.items()):
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    return True
