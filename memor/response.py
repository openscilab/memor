# -*- coding: utf-8 -*-
"""Response class."""
import enum
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import PromptRenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_PROMPT_FILE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc
from .functions import _validate_string, _validate_pos_float, _validate_list_of_str
from .functions import _validate_date_time
from .functions import validate_path
from .template import CustomPromptTemplate, PresetPromptTemplate


class Response:
    """
    Response class.
    """

    def __init__(
            self,
            message=None,
            temperature=None,
            model=None,
            date=get_time_utc(),
            file_path=None):
        """
        Response object initiator.

        :param message: response message
        :type message: str
        :param temperature: temperature
        :type temperature: float
        :param model: agent model
        :type model: str
        :param date: response date
        :type date: datetime.datetime
        :param file_path: response file path
        :type file_path: str
        :return: None
        """
        self._message = None
        self._temperature = None
        self._model = None
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if message:
                self.update_message(message)
            if model:
                self.update_model(model)
            if temperature:
                self.update_temperature(temperature)
            if date:
                _validate_date_time(date, "date")
                self._date_created = date

    def __str__(self):
        """Return string representation of Response."""
        return self._message

    def __repr__(self):
        """Return string representation of Response."""
        return "Response(message={message})".format(message=self._message)

    def __copy__(self):
        """
        Return a copy of the Response object.
        
        :return: a copy of Response object
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result
    
    def copy(self):
        """
        Return a copy of the Response object.
        
        :return: a copy of Response object
        """
        return self.__copy__()


    def update_message(self, message):
        """
        Update the response message.

        :param message: message
        :type message: str
        :return: None
        """
        _validate_string(message, "message")
        self._message = message
        self._date_modified = get_time_utc()


    def update_temperature(self, temperature):
        """
        Update the temperature.

        :param temperature: temperature
        :type temperature: float
        :return: None
        """
        _validate_pos_float(temperature, "temperature")
        self._temperature = temperature
        self._date_modified = get_time_utc()

    def update_model(self, model):
        """
        Update the agent model.

        :param model: model
        :type model: str
        :return: None
        """
        _validate_string(model, "model")
        self._model = model
        self._date_modified = get_time_utc()

    def save(self, file_path):
        """
        Save method.

        :param file_path: response file path
        :type file_path: str
        :return: result as dict
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                data = self.to_dict()
                file.write(json.dumps(data, indent=4))
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def load(self, file_path):
        """
        Load method.

        :param file_path: response file path
        :type file_path: str
        :return: None
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            try:
                loaded_obj = json.loads(file.read())
                self._message = loaded_obj["message"]
                self._temperature = loaded_obj["temperature"]
                self._model = loaded_obj["model"]
                self._memor_version = loaded_obj["memor_version"]
                self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
                self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_PROMPT_FILE_MESSAGE)

    def to_json(self):
        """
        Convert the response to a JSON object.

        :return: JSON object
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """
        Convert the response to a dictionary.

        :return: dict
        """
        return {
            "message": self._message,
            "temperature": self._temperature,
            "model": self._model,
            "memor_version": MEMOR_VERSION,
            "date_created": datetime.datetime.strftime(self._date_created, DATE_TIME_FORMAT),
            "date_modified": datetime.datetime.strftime(self._date_modified, DATE_TIME_FORMAT),
        }

    @property
    def message(self):
        """
        Get the response message.

        :return: response message
        """
        return self._message


    @property
    def temperature(self):
        """
        Get the temperature.

        :return: temperature
        """
        return self._temperature

    @property
    def model(self):
        """
        Get the agent model.

        :return: agent model
        """
        return self._model

    @property
    def date_created(self):
        """
        Get the response creation date.

        :return: response creation date
        """
        return self._date_created

    @property
    def date_modified(self):
        """
        Get the response object modification date.

        :return: response object modification date
        """
        return self._date_modified
