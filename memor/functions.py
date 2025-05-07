# -*- coding: utf-8 -*-
"""Memor functions."""
from typing import Any, Type
import os
import datetime
import uuid
from .params import INVALID_DATETIME_MESSAGE
from .params import INVALID_PATH_MESSAGE, INVALID_STR_VALUE_MESSAGE
from .params import INVALID_PROB_VALUE_MESSAGE, INVALID_MESSAGE_STATUS_LEN_MESSAGE
from .params import INVALID_POSFLOAT_VALUE_MESSAGE
from .params import INVALID_POSINT_VALUE_MESSAGE
from .params import INVALID_CUSTOM_MAP_MESSAGE
from .params import INVALID_BOOL_VALUE_MESSAGE
from .params import INVALID_LIST_OF_X_MESSAGE
from .params import INVALID_ID_MESSAGE
from .errors import MemorValidationError


def generate_message_id() -> str:
    """Generate message ID."""
    return str(uuid.uuid4())


def _validate_message_id(message_id: str) -> bool:
    """
    Validate message ID.

    :param message_id: message ID
    """
    try:
        _ = uuid.UUID(message_id, version=4)
    except ValueError:
        raise MemorValidationError(INVALID_ID_MESSAGE)
    return True


def get_time_utc() -> datetime.datetime:
    """
    Get time in UTC format.

    :return: UTC format time as a datetime object
    """
    return datetime.datetime.now(datetime.timezone.utc)


def _validate_string(value: Any, parameter_name: str) -> bool:
    """
    Validate string.

    :param value: value
    :param parameter_name: parameter name
    """
    if not isinstance(value, str):
        raise MemorValidationError(INVALID_STR_VALUE_MESSAGE.format(parameter_name=parameter_name))
    return True


def _validate_bool(value: Any, parameter_name: str) -> bool:
    """
    Validate boolean.

    :param value: value
    :param parameter_name: parameter name
    """
    if not isinstance(value, bool):
        raise MemorValidationError(INVALID_BOOL_VALUE_MESSAGE.format(parameter_name=parameter_name))
    return True


def _can_convert_to_string(value: Any) -> bool:
    """
    Check if value can be converted to string.

    :param value: value
    """
    try:
        str(value)
    except Exception:
        return False
    return True


def _validate_pos_int(value: Any, parameter_name: str) -> bool:
    """
    Validate positive integer.

    :param value: value
    :param parameter_name: parameter name
    """
    if not isinstance(value, int) or value < 0:
        raise MemorValidationError(INVALID_POSINT_VALUE_MESSAGE.format(parameter_name=parameter_name))
    return True


def _validate_pos_float(value: Any, parameter_name: str) -> bool:
    """
    Validate positive float.

    :param value: value
    :param parameter_name: parameter name
    """
    if not isinstance(value, float) or value < 0:
        raise MemorValidationError(INVALID_POSFLOAT_VALUE_MESSAGE.format(parameter_name=parameter_name))
    return True


def _validate_probability(value: Any, parameter_name: str) -> bool:
    """
    Validate probability (a float between 0 and 1).

    :param value: value
    :param parameter_name: parameter name
    """
    if not isinstance(value, float) or value < 0 or value > 1:
        raise MemorValidationError(INVALID_PROB_VALUE_MESSAGE.format(parameter_name=parameter_name))
    return True


def _validate_list_of(value: Any, parameter_name: str, type_: Type, type_name: str) -> bool:
    """
    Validate list of values.

    :param value: value
    :param parameter_name: parameter name
    :param type_: type
    :param type_name: type name
    """
    if not isinstance(value, list):
        raise MemorValidationError(INVALID_LIST_OF_X_MESSAGE.format(parameter_name=parameter_name, type_name=type_name))

    if not all(isinstance(x, type_) for x in value):
        raise MemorValidationError(INVALID_LIST_OF_X_MESSAGE.format(parameter_name=parameter_name, type_name=type_name))
    return True


def _validate_date_time(date_time: Any, parameter_name: str) -> bool:
    """
    Validate date time.

    :param date_time: date time
    :param parameter_name: parameter name
    """
    if not isinstance(date_time, datetime.datetime) or date_time.tzinfo is None:
        raise MemorValidationError(INVALID_DATETIME_MESSAGE.format(parameter_name=parameter_name))
    return True


def _validate_status(status: Any, messages: Any) -> bool:
    """
    Validate status.

    :param status: status
    :param messages: messages
    """
    _validate_list_of(status, "status", bool, "booleans")
    if len(status) != len(messages):
        raise MemorValidationError(INVALID_MESSAGE_STATUS_LEN_MESSAGE)
    return True


def _validate_path(path: Any) -> bool:
    """
    Validate path property.

    :param path: path
    """
    if not isinstance(path, str) or not os.path.exists(path):
        raise FileNotFoundError(INVALID_PATH_MESSAGE.format(path=path))
    return True


def _validate_custom_map(custom_map: Any) -> bool:
    """
    Validate custom map a dictionary with keys and values that can be converted to strings.

    :param custom_map: custom map
    """
    if not isinstance(custom_map, dict):
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    if not all(_can_convert_to_string(k) and _can_convert_to_string(v) for k, v in custom_map.items()):
        raise MemorValidationError(INVALID_CUSTOM_MAP_MESSAGE)
    return True
