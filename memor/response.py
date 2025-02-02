# -*- coding: utf-8 -*-
"""Response class."""
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_RESPONSE_FILE_MESSAGE
from .params import INVALID_ROLE_MESSAGE
from .params import Role
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import _validate_string, _validate_pos_float
from .functions import _validate_date_time, _validate_probability
from .functions import validate_path


class Response:
    """
    Response class.

    >>> from memor import Response, Role
    >>> response = Response(message="Hello!", score=0.9, role=Role.ASSISTANT, temperature=0.5, model="gpt-3.5")
    >>> response.message
    'Hello!'
    """

    def __init__(
            self,
            message=None,
            score=None,
            role=Role.ASSISTANT,
            temperature=None,
            model=None,
            date=get_time_utc(),
            file_path=None):
        """
        Response object initiator.

        :param message: response message
        :type message: str
        :param score: response score
        :type score: float
        :param role: response role
        :type role: Role object
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
        self._score = None
        self._role = Role.ASSISTANT
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
            if score:
                self.update_score(score)
            if role:
                self.update_role(role)
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

    def update_score(self, score):
        """
        Update the response score.

        :param score: score
        :type score: float
        :return: None
        """
        _validate_probability(score, "score")
        self._score = score
        self._date_modified = get_time_utc()

    def update_role(self, role):
        """
        Update the response role.

        :param role: role
        :type role: Role object
        :return: None
        """
        if not isinstance(role, Role):
            raise MemorValidationError(INVALID_ROLE_MESSAGE)
        self._role = role
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
                file.write(self.to_json())
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
                self._score = loaded_obj["score"]
                self._temperature = loaded_obj["temperature"]
                self._model = loaded_obj["model"]
                self._memor_version = loaded_obj["memor_version"]
                self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
                self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_RESPONSE_FILE_MESSAGE)

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
            "score": self._score,
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
    def score(self):
        """
        Get the response score.

        :return: response score
        """
        return self._score

    @property
    def temperature(self):
        """
        Get the temperature.

        :return: temperature
        """
        return self._temperature

    @property
    def role(self):
        """
        Get the response role.

        :return: response role
        """
        return self._role

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
