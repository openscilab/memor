# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
import json
from .params import DATE_TIME_FORMAT
from .params import PromptRenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_PROMPT_FILE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc
from .functions import validate_path, validate_prompt_message
from .functions import validate_prompt_responses
from .functions import validate_prompt_temperature, validate_prompt_model
from .template import DEFAULT_TEMPLATE, CustomPromptTemplate


class Role(enum.Enum):
    """Role enum."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DEFAULT = USER


class Prompt:
    """Prompt class."""

    def __init__(
            self,
            message=None,
            responses=[],
            role=Role.DEFAULT,
            temperature=None,
            model=None,
            template=DEFAULT_TEMPLATE,
            date=get_time_utc(),
            file_path=None):
        """
        Prompt object initiator.

        :param message: prompt message
        :type message: str
        :param responses: prompt responses
        :type responses: list
        :param role: prompt role
        :type role: Role object
        :param temperature: prompt temperature
        :type temperature: float
        :param model: prompt model
        :type model: str
        :param template: prompt template
        :type template: CustomPromptTemplate object
        :param date: prompt date
        :type date: datetime.datetime
        :param file_path: prompt file path
        :type file_path: str
        :return: None
        """
        self._message = None
        self._temperature = None
        self._model = None
        self._role = Role.DEFAULT
        self._template = DEFAULT_TEMPLATE
        self._responses = []
        if file_path:
            self.load(file_path)
        if message:
            self.update_message(message)
        if model:
            self.update_model(model)
        if temperature:
            self.update_temperature(temperature)
        if role:
            self.update_role(role)
        if responses:
            self.update_responses(responses)
        if template:
            self.update_template(template)
        if date:
            self._date = date

    def add_response(self, response, index=None):
        """
        Add a response to the prompt object.

        :param response: response
        :type response: str
        :param index: index
        :type index: int
        :return: None
        """
        if index is None:
            self._responses.append(response)
        else:
            self._responses.insert(index, response)

    def remove_response(self, index):
        """
        Remove a response from the prompt object.

        :param index: index
        :type index: int
        :return: None
        """
        self._responses.pop(index)

    def update_responses(self, responses):
        validate_prompt_responses(responses)
        self._responses = responses

    def update_message(self, message):
        """Update the prompt message."""
        validate_prompt_message(message)
        self._message = message

    def update_role(self, role):
        if not isinstance(role, Role):
            raise MemorValidationError(INVALID_ROLE_MESSAGE)
        self._role = role

    def update_temperature(self, temperature):
        validate_prompt_temperature(temperature)
        self._temperature = temperature

    def update_model(self, model):
        validate_prompt_model(model)
        self._model = model

    def update_template(self, template):
        if not isinstance(template, CustomPromptTemplate):
            raise MemorValidationError(INVALID_TEMPLATE_MESSAGE)
        self._template = template

    def save(self, file_path):
        """
        Save method.

        :param file_path: prompt file path
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

        :param file_path: prompt file path
        :type file_path: str
        :return: result as dict
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            try:
                loaded_obj = json.loads(file.read())
                self._message = loaded_obj["message"]
                self._responses = loaded_obj["responses"]
                self._role = Role(loaded_obj["role"])
                self._temperature = loaded_obj["temperature"]
                self._model = loaded_obj["model"]
                self._date = datetime.datetime.strptime(loaded_obj["date"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_PROMPT_FILE_MESSAGE)

    def to_json(self):
        """Convert the prompt to a JSON object."""
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """Convert the prompt to a dictionary."""
        return {
            "message": self._message,
            "responses": self._responses,
            "role": str(self._role),
            "temperature": self._temperature,
            "model": self._model,
            "date": get_time_utc().strftime(DATE_TIME_FORMAT)
        }

    @property
    def message(self):
        return self._message

    @property
    def responses(self):
        return self._responses

    @property
    def role(self):
        return self._role

    @property
    def temperature(self):
        return self._temperature

    @property
    def model(self):
        return self._model

    @property
    def date(self):
        return self._date

    @property
    def template(self):
        return self._template

    def render(self, render_format=PromptRenderFormat.OpenAI):
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered prompt
        """
        try:
            format_kwargs = {
                "temperature": self._temperature,
                "role": self._role.value,
                "model": self._model,
                "message": self._message,
                "date": self._date}
            for index, response in enumerate(self._responses):
                format_kwargs.update({"response_{index}".format(index=index): response})
            if render_format == PromptRenderFormat.OpenAI:
                return [
                    {"role": self._role.value,
                     "content": self._template._content.format(**format_kwargs)}]
        except Exception:
            raise MemorRenderError(PROMPT_RENDER_ERROR_MESSAGE)
