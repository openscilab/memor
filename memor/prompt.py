# -*- coding: utf-8 -*-
"""Prompt class."""
from typing import List, Dict, Union, Tuple, Any
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import RenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import Role
from .tokens_estimator import TokensEstimator
from .params import INVALID_PROMPT_STRUCTURE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE, INVALID_RESPONSE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc, generate_message_id
from .functions import _validate_string, _validate_pos_int, _validate_list_of
from .functions import _validate_path, _validate_message_id
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
            message: str = "",
            responses: List[Response] = [],
            role: Role = Role.DEFAULT,
            tokens: int = None,
            template: Union[PresetPromptTemplate, PromptTemplate] = PresetPromptTemplate.DEFAULT,
            file_path: str = None,
            init_check: bool = True) -> None:
        """
        Prompt object initiator.

        :param message: prompt message
        :param responses: prompt responses
        :param role: prompt role
        :param tokens: tokens
        :param template: prompt template
        :param file_path: prompt file path
        :param init_check: initial check flag
        """
        self._message = ""
        self._tokens = None
        self._role = Role.DEFAULT
        self._template = PresetPromptTemplate.DEFAULT.value
        self._responses = []
        self._date_created = get_time_utc()
        self._mark_modified()
        self._memor_version = MEMOR_VERSION
        self._selected_response_index = 0
        self._selected_response = None
        self._id = None
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
            self._id = generate_message_id()
        _validate_message_id(self._id)
        if init_check:
            _ = self.render()

    def _mark_modified(self) -> None:
        """Mark modification."""
        self._date_modified = get_time_utc()

    def __eq__(self, other_prompt: "Prompt") -> bool:
        """
        Check prompts equality.

        :param other_prompt: another prompt
        """
        if isinstance(other_prompt, Prompt):
            return self._message == other_prompt._message and self._responses == other_prompt._responses and \
                self._role == other_prompt._role and self._template == other_prompt._template and \
                self._tokens == other_prompt._tokens
        return False

    def __str__(self) -> str:
        """Return string representation of Prompt."""
        return self.render(render_format=RenderFormat.STRING)

    def __repr__(self) -> str:
        """Return string representation of Prompt."""
        return "Prompt(message={message})".format(message=self._message)

    def __len__(self) -> int:
        """Return the length of the Prompt object."""
        try:
            return len(self.render(render_format=RenderFormat.STRING))
        except Exception:
            return 0

    def __copy__(self) -> "Prompt":
        """
        Return a copy of the Prompt object.

        :return: a copy of Prompt object
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        result.regenerate_id()
        return result

    def copy(self) -> "Prompt":
        """
        Return a copy of the Prompt object.

        :return: a copy of Prompt object
        """
        return self.__copy__()

    def add_response(self, response: Response, index: int = None) -> None:
        """
        Add a response to the prompt object.

        :param response: response
        :param index: index
        """
        if not isinstance(response, Response):
            raise MemorValidationError(INVALID_RESPONSE_MESSAGE)
        if index is None:
            self._responses.append(response)
        else:
            self._responses.insert(index, response)
        self._mark_modified()

    def remove_response(self, index: int) -> None:
        """
        Remove a response from the prompt object.

        :param index: index
        """
        self._responses.pop(index)
        self._mark_modified()

    def select_response(self, index: int) -> None:
        """
        Select a response as selected response.

        :param index: index
        """
        if len(self._responses) > 0:
            self._selected_response_index = index
            self._selected_response = self._responses[index]
            self._mark_modified()

    def update_responses(self, responses: List[Response]) -> None:
        """
        Update the prompt responses.

        :param responses: responses
        """
        _validate_list_of(responses, "responses", Response, "`Response`")
        self._responses = responses
        self._mark_modified()

    def update_message(self, message: str) -> None:
        """
        Update the prompt message.

        :param message: message
        """
        _validate_string(message, "message")
        self._message = message
        self._mark_modified()

    def update_role(self, role: Role) -> None:
        """
        Update the prompt role.

        :param role: role
        """
        if not isinstance(role, Role):
            raise MemorValidationError(INVALID_ROLE_MESSAGE)
        self._role = role
        self._mark_modified()

    def update_tokens(self, tokens: int) -> None:
        """
        Update the tokens.

        :param tokens: tokens
        """
        _validate_pos_int(tokens, "tokens")
        self._tokens = tokens
        self._mark_modified()

    def update_template(self, template: PromptTemplate) -> None:
        """
        Update the prompt template.

        :param template: template
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
        self._mark_modified()

    def save(self, file_path: str, save_template: bool = True) -> Dict[str, Any]:
        """
        Save method.

        :param file_path: prompt file path
        :param save_template: save template flag
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

    def load(self, file_path: str) -> None:
        """
        Load method.

        :param file_path: prompt file path
        """
        _validate_path(file_path)
        with open(file_path, "r") as file:
            self.from_json(file.read())

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        try:
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            self._message = loaded_obj["message"]
            self._tokens = loaded_obj.get("tokens", None)
            self._id = loaded_obj.get("id", generate_message_id())
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

    def to_json(self, save_template: bool = True) -> Dict[str, Any]:
        """
        Convert the prompt to a JSON object.

        :param save_template: save template flag
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

    def to_dict(self, save_template: bool = True) -> Dict[str, Any]:
        """
        Convert the prompt to a dictionary.

        :param save_template: save template flag
        """
        data = {
            "type": "Prompt",
            "message": self._message,
            "responses": self._responses.copy(),
            "selected_response_index": self._selected_response_index,
            "tokens": self._tokens,
            "role": self._role,
            "id": self._id,
            "template": self._template,
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }
        if not save_template:
            del data["template"]
        return data

    def regenerate_id(self) -> None:
        """Regenerate ID."""
        new_id = self._id
        while new_id == self.id:
            new_id = generate_message_id()
        self._id = new_id

    @property
    def message(self) -> str:
        """Get the prompt message."""
        return self._message

    @property
    def responses(self) -> List[Response]:
        """Get the prompt responses."""
        return self._responses

    @property
    def role(self) -> Role:
        """Get the prompt role."""
        return self._role

    @property
    def tokens(self) -> int:
        """Get the prompt tokens."""
        return self._tokens

    @property
    def date_created(self) -> datetime.datetime:
        """Get the prompt creation date."""
        return self._date_created

    @property
    def date_modified(self) -> datetime.datetime:
        """Get the prompt object modification date."""
        return self._date_modified

    @property
    def template(self) -> PromptTemplate:
        """Get the prompt template."""
        return self._template

    @property
    def id(self) -> str:
        """Get the prompt ID."""
        return self._id

    @property
    def selected_response(self) -> Response:
        """Get the prompt selected response."""
        return self._selected_response

    def render(self, render_format: RenderFormat = RenderFormat.DEFAULT) -> Union[str,
                                                                                  Dict[str, Any],
                                                                                  List[Tuple[str, Any]]]:
        """
        Render method.

        :param render_format: render format
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
            if render_format == RenderFormat.AI_STUDIO:
                return {"role": self._role.value, "parts": [{"text": content}]}
            if render_format == RenderFormat.STRING:
                return content
            if render_format == RenderFormat.DICTIONARY:
                return prompt_dict
            if render_format == RenderFormat.ITEMS:
                return list(prompt_dict.items())
        except Exception:
            raise MemorRenderError(PROMPT_RENDER_ERROR_MESSAGE)

    def check_render(self) -> bool:
        """Check render."""
        try:
            _ = self.render()
            return True
        except Exception:
            return False

    def estimate_tokens(self, method: TokensEstimator = TokensEstimator.DEFAULT) -> int:
        """
        Estimate the number of tokens in the prompt message.

        :param method: token estimator method
        """
        return method(self.render(render_format=RenderFormat.STRING))
