# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import PromptRenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import Role
from .params import INVALID_PROMPT_FILE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE, INVALID_RESPONSE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE, INVALID_RESPONSES_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc
from .functions import _validate_string, _validate_pos_float, _validate_list_of_str
from .functions import _validate_date_time
from .functions import validate_path
from .template import CustomPromptTemplate, PresetPromptTemplate
from .response import Response


class Prompt:
    """
    Prompt class.

    >>> from memor import Prompt, Role
    >>> prompt = Prompt(message="Hello, how are you?", responses=["I am fine."], role=Role.USER)
    >>> prompt.message
    'Hello, how are you?'
    """

    def __init__(
            self,
            message=None,
            responses=[],
            role=Role.DEFAULT,
            template=PresetPromptTemplate.DEFAULT,
            file_path=None):
        """
        Prompt object initiator.

        :param message: prompt message
        :type message: str
        :param responses: prompt responses
        :type responses: list
        :param role: prompt role
        :type role: Role object
        :param template: prompt template
        :type template: CustomPromptTemplate/PresetPromptTemplate object
        :param file_path: prompt file path
        :type file_path: str
        :return: None
        """
        self._message = None
        self._role = Role.DEFAULT
        self._template = PresetPromptTemplate.DEFAULT.value
        self._responses = []
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if message:
                self.update_message(message)
            if role:
                self.update_role(role)
            if responses:
                self.update_responses(responses)
            if template:
                self.update_template(template)

    def __str__(self):
        """Return string representation of Prompt."""
        return self._message

    def __repr__(self):
        """Return string representation of Prompt."""
        return "Prompt(message={message})".format(message=self._message)

    def __copy__(self):
        """
        Return a copy of the Prompt object.

        :return: a copy of Prompt object
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self):
        """
        Return a copy of the Prompt object.

        :return: a copy of Prompt object
        """
        return self.__copy__()

    def add_response(self, response, index=None):
        """
        Add a response to the prompt object.

        :param response: response
        :type response: str
        :param index: index
        :type index: int
        :return: None
        """
        if not isinstance(response, Response):
            raise MemorValidationError(INVALID_RESPONSE_MESSAGE)
        if index is None:
            self._responses.append(response)
        else:
            self._responses.insert(index, response)
        self._date_modified = get_time_utc()

    def remove_response(self, index):
        """
        Remove a response from the prompt object.

        :param index: index
        :type index: int
        :return: None
        """
        self._responses.pop(index)
        self._date_modified = get_time_utc()

    def update_responses(self, responses):
        """
        Update the prompt responses.

        :param responses: responses
        :type responses: list
        :return: None
        """
        if not isinstance(responses, list):
            raise MemorValidationError(INVALID_RESPONSES_MESSAGE)
        if not all(isinstance(x, Response) for x in responses):
            raise MemorValidationError(INVALID_RESPONSES_MESSAGE)
        self._responses = responses
        self._date_modified = get_time_utc()

    def update_message(self, message):
        """
        Update the prompt message.

        :param message: message
        :type message: str
        :return: None
        """
        _validate_string(message, "message")
        self._message = message
        self._date_modified = get_time_utc()

    def update_role(self, role):
        """
        Update the prompt role.

        :param role: role
        :type role: Role object
        :return: None
        """
        if not isinstance(role, Role):
            raise MemorValidationError(INVALID_ROLE_MESSAGE)
        self._role = role
        self._date_modified = get_time_utc()

    def update_template(self, template):
        """
        Update the prompt template.

        :param template: template
        :type template: CustomPromptTemplate/PresetPromptTemplate object
        :return: None
        """
        if not isinstance(template, (CustomPromptTemplate, PresetPromptTemplate)):
            raise MemorValidationError(INVALID_TEMPLATE_MESSAGE)
        if isinstance(template, CustomPromptTemplate):
            self._template = template
        if isinstance(template, PresetPromptTemplate):
            self._template = template.value
        self._date_modified = get_time_utc()

    def save(self, file_path, save_template=True):
        """
        Save method.

        :param file_path: prompt file path
        :type file_path: str
        :param save_template: save template flag
        :type save_template: bool
        :return: result as dict
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                data = self.to_dict()
                if not save_template:
                    del data["template"]
                file.write(json.dumps(data, indent=4))
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def load(self, file_path):
        """
        Load method.

        :param file_path: prompt file path
        :type file_path: str
        :return: None
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            try:
                loaded_obj = json.loads(file.read())
                self._message = loaded_obj["message"]
                self._responses = loaded_obj["responses"]
                self._role = Role(loaded_obj["role"])
                self._template = PresetPromptTemplate.DEFAULT.value
                if "template" in loaded_obj:
                    self._template = CustomPromptTemplate(**loaded_obj["template"])
                self._memor_version = loaded_obj["memor_version"]
                self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
                self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_PROMPT_FILE_MESSAGE)

    def to_json(self):
        """
        Convert the prompt to a JSON object.

        :return: JSON object
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """
        Convert the prompt to a dictionary.

        :return: dict
        """
        return {
            "message": self._message,
            "responses": self._responses,
            "role": str(self._role),
            "template": self._template.to_dict(),
            "memor_version": MEMOR_VERSION,
            "date_created": datetime.datetime.strftime(self._date_created, DATE_TIME_FORMAT),
            "date_modified": datetime.datetime.strftime(self._date_modified, DATE_TIME_FORMAT),
        }

    @property
    def message(self):
        """
        Get the prompt message.

        :return: prompt message
        """
        return self._message

    @property
    def responses(self):
        """
        Get the prompt responses.

        :return: prompt responses
        """
        return self._responses

    @property
    def role(self):
        """
        Get the prompt role.

        :return: prompt role
        """
        return self._role

    @property
    def date_created(self):
        """
        Get the prompt creation date.

        :return: prompt creation date
        """
        return self._date_created

    @property
    def date_modified(self):
        """
        Get the prompt object modification date.

        :return: prompt object modification date
        """
        return self._date_modified

    @property
    def template(self):
        """
        Get the prompt template.

        :return: prompt template
        """
        return self._template

    def render(self, render_format=PromptRenderFormat.DEFAULT):
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered prompt
        """
        if not isinstance(render_format, PromptRenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        try:
            format_kwargs = {
                "role": self._role.value,
                "message": self._message,
                "date": datetime.datetime.strftime(self._date_created, DATE_TIME_FORMAT)}
            for index, response in enumerate(self._responses):
                format_kwargs.update({"response_{index}".format(index=index): response})
            custom_map = self._template._custom_map
            if custom_map is not None:
                format_kwargs.update(custom_map)
            content = self._template._content.format(**format_kwargs)
            prompt_dict = self.to_dict()
            prompt_dict["content"] = content
            if render_format == PromptRenderFormat.AISUITE:
                return [
                    {"role": self._role.value,
                     "content": content}]
            if render_format == PromptRenderFormat.STRING:
                return content
            if render_format == PromptRenderFormat.DICTIONARY:
                return prompt_dict
            if render_format == PromptRenderFormat.ITEMS:
                return list(prompt_dict.items())
        except Exception:
            raise MemorRenderError(PROMPT_RENDER_ERROR_MESSAGE)
