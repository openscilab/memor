# -*- coding: utf-8 -*-
"""Prompt class."""
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import RenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import Role
from .params import INVALID_PROMPT_STRUCTURE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE, INVALID_RESPONSE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc
from .functions import _validate_string, _validate_pos_int, _validate_list_of
from .functions import _validate_path
from .template import PromptTemplate, PresetPromptTemplate
from .template import _BasicPresetPromptTemplate, _Instruction1PresetPromptTemplate, _Instruction2PresetPromptTemplate, _Instruction3PresetPromptTemplate
from .response import Response


class Prompt:
    """
    Prompt class.

    >>> from memor import Prompt, Role, Response
    >>> responses = [Response(message="I am fine."), Response(message="I am not fine."), Response(message="I am okay.")]
    >>> prompt = Prompt(message="Hello, how are you?", responses=responses)
    >>> prompt.message
    'Hello, how are you?'
    >>> prompt.responses[1].message
    'I am not fine.'
    """

    def __init__(
            self,
            message=None,
            responses=[],
            role=Role.DEFAULT,
            tokens=None,
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
        :param tokens: tokens
        :type tokens: int
        :param template: prompt template
        :type template: PromptTemplate/PresetPromptTemplate object
        :param file_path: prompt file path
        :type file_path: str
        :return: None
        """
        self._message = None
        self._tokens = None
        self._role = Role.DEFAULT
        self._template = PresetPromptTemplate.DEFAULT.value
        self._responses = []
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        self._selected_response_index = 0
        self._selected_response = None
        if file_path:
            self.load(file_path)
        else:
            if message:
                self.update_message(message)
            if role:
                self.update_role(role)
            if tokens:
                self.update_tokens(tokens)
            if responses:
                self.update_responses(responses)
            if template:
                self.update_template(template)
            self.select_response(index=self._selected_response_index)

    def __eq__(self, other_prompt):
        """
        Check prompts equality.

        :param other_prompt: another prompt
        :type other_prompt: Prompt
        :return: result as bool
        """
        if isinstance(other_prompt, Prompt):
            return self._message == other_prompt._message and self._responses == other_prompt._responses and \
                self._role == other_prompt._role and self._template == other_prompt._template and \
                self._tokens == other_prompt._tokens
        return False

    def __str__(self):
        """Return string representation of Prompt."""
        return self.render(render_format=RenderFormat.STRING)

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

    def select_response(self, index):
        """
        Select a response as selected response.

        :param index: index
        :type index: int
        :return: None
        """
        if len(self._responses) > 0:
            self._selected_response_index = index
            self._selected_response = self._responses[index]
            self._date_modified = get_time_utc()

    def update_responses(self, responses):
        """
        Update the prompt responses.

        :param responses: responses
        :type responses: list
        :return: None
        """
        _validate_list_of(responses, "responses", Response, "`Response`")
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

    def update_tokens(self, tokens):
        """
        Update the tokens.

        :param tokens: tokens
        :type tokens: int
        :return: None
        """
        _validate_pos_int(tokens, "tokens")
        self._tokens = tokens
        self._date_modified = get_time_utc()

    def update_template(self, template):
        """
        Update the prompt template.

        :param template: template
        :type template: PromptTemplate/PresetPromptTemplate object
        :return: None
        """
        if not isinstance(
            template,
            (PromptTemplate,
             _BasicPresetPromptTemplate,
             _Instruction1PresetPromptTemplate,
             _Instruction2PresetPromptTemplate,
             _Instruction3PresetPromptTemplate)):
            raise MemorValidationError(INVALID_TEMPLATE_MESSAGE)
        if isinstance(template, PromptTemplate):
            self._template = template
        if isinstance(
            template,
            (_BasicPresetPromptTemplate,
             _Instruction1PresetPromptTemplate,
             _Instruction2PresetPromptTemplate,
             _Instruction3PresetPromptTemplate)):
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
                data = self.to_json(save_template=save_template)
                json.dump(data, file)
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
        _validate_path(file_path)
        with open(file_path, "r") as file:
            self.from_json(file.read())

    def from_json(self, json_object):
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        :type json_object: str or dict
        :return: None
        """
        try:
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            self._message = loaded_obj["message"]
            self._tokens = loaded_obj.get("tokens", None)
            responses = []
            for response in loaded_obj["responses"]:
                response_obj = Response()
                response_obj.from_json(response)
                responses.append(response_obj)
            self._responses = responses
            self._role = Role(loaded_obj["role"])
            self._template = PresetPromptTemplate.DEFAULT.value
            if "template" in loaded_obj:
                template_obj = PromptTemplate()
                template_obj.from_json(loaded_obj["template"])
                self._template = template_obj
            self._memor_version = loaded_obj["memor_version"]
            self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            self._selected_response_index = loaded_obj["selected_response_index"]
            self.select_response(index=self._selected_response_index)
        except Exception:
            raise MemorValidationError(INVALID_PROMPT_STRUCTURE_MESSAGE)

    def to_json(self, save_template=True):
        """
        Convert the prompt to a JSON object.

        :param save_template: save template flag
        :type save_template: bool
        :return: JSON object as dict
        """
        data = self.to_dict(save_template=save_template).copy()
        for index, response in enumerate(data["responses"]):
            data["responses"][index] = response.to_json()
        if "template" in data:
            data["template"] = data["template"].to_json()
        data["role"] = data["role"].value
        data["date_created"] = datetime.datetime.strftime(data["date_created"], DATE_TIME_FORMAT)
        data["date_modified"] = datetime.datetime.strftime(data["date_modified"], DATE_TIME_FORMAT)
        return data

    def to_dict(self, save_template=True):
        """
        Convert the prompt to a dictionary.

        :param save_template: save template flag
        :type save_template: bool
        :return: dict
        """
        data = {
            "type": "Prompt",
            "message": self._message,
            "responses": self._responses.copy(),
            "selected_response_index": self._selected_response_index,
            "tokens": self._tokens,
            "role": self._role,
            "template": self._template,
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }
        if not save_template:
            del data["template"]
        return data

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
    def tokens(self):
        """
        Get the prompt tokens.

        :return: prompt tokens
        """
        return self._tokens

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

    @property
    def selected_response(self):
        """
        Get the prompt selected response.

        :return: selected response as Response object
        """
        return self._selected_response

    def render(self, render_format=RenderFormat.DEFAULT):
        """
        Render method.

        :param render_format: render format
        :type render_format: RenderFormat object
        :return: rendered prompt
        """
        if not isinstance(render_format, RenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        try:
            format_kwargs = {"prompt": self.to_json(save_template=False)}
            if isinstance(self._selected_response, Response):
                format_kwargs.update({"response": self._selected_response.to_json()})
            responses_dicts = []
            for _, response in enumerate(self._responses):
                responses_dicts.append(response.to_json())
            format_kwargs.update({"responses": responses_dicts})
            custom_map = self._template._custom_map
            if custom_map is not None:
                format_kwargs.update(custom_map)
            content = self._template._content.format(**format_kwargs)
            prompt_dict = self.to_dict()
            prompt_dict["content"] = content
            if render_format == RenderFormat.OPENAI:
                return {"role": self._role.value, "content": content}
            if render_format == RenderFormat.STRING:
                return content
            if render_format == RenderFormat.DICTIONARY:
                return prompt_dict
            if render_format == RenderFormat.ITEMS:
                return list(prompt_dict.items())
        except Exception:
            raise MemorRenderError(PROMPT_RENDER_ERROR_MESSAGE)
