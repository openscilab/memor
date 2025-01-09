# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
import json
from .params import PromptRenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_PROMPT_FILE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .errors import MemorValidationError
from .functions import validate_path, validate_prompt_message
from .functions import validate_prompt_responses, validate_prompt_role
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
            date=datetime.datetime.now(),
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
            self.responses.append(response)
        else:
            self.responses.insert(index, response)

    def remove_response(self, index):
        """
        Remove a response from the prompt object.
        
        :param index: index
        :type index: int
        :return: None
        """
        self.responses.pop(index)

    def update_responses(self, responses):
        validate_prompt_responses(responses)
        self.responses = responses

    def update_message(self, message):
        """Update the prompt message."""
        validate_prompt_message(message)
        self.message = message

    def update_role(self, role):
        validate_prompt_role(role)
        self.role = role

    def update_temperature(self, temperature):
        validate_prompt_temperature(temperature)
        self.temperature = temperature

    def update_model(self, model):
        validate_prompt_model(model)
        self.model = model

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
                self._date = datetime.datetime.strptime(loaded_obj["date"], "%Y-%m-%d %H:%M:%S.%f")
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
            "date": str(self._date)
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

    def render(self, render_format=PromptRenderFormat.OpenAI):
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered prompt
        """
        if render_format == PromptRenderFormat.OpenAI:
            return [
                {"role": self._role.value,
                 "content": self.template._content.format(message=self._message)}]
