# -*- coding: utf-8 -*-
"""Prompt class."""
from typing import List, Dict, Union, Tuple, Any, Optional
import datetime
import json
import warnings
from .message import Message
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import RenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import Role
from .tokens_estimator import TokensEstimator
from .params import INVALID_PROMPT_STRUCTURE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_ROLE_MESSAGE, INVALID_RESPONSE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .params import AI_STUDIO_SYSTEM_WARNING
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc, generate_message_id
from .functions import _validate_string, _validate_pos_int, _validate_list_of
from .functions import _validate_path, _validate_message_id
from .template import PromptTemplate, PresetPromptTemplate
from .template import _BasicPresetPromptTemplate, _Instruction1PresetPromptTemplate, _Instruction2PresetPromptTemplate, _Instruction3PresetPromptTemplate
from .response import Response


class Prompt(Message):
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
        super().__init__()
        self._role = Role.USER
        self._template = PresetPromptTemplate.DEFAULT.value
        self._responses = []
        self._selected_response_index = 0
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
            self._id = generate_message_id()
        _validate_message_id(self._id)
        if init_check:
            _ = self.render()

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

    def __repr__(self) -> str:
        """Return string representation of Prompt."""
        return "Prompt(message={message})".format(message=self._message)

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

    def select_response(self, index: int) -> Optional[Response]:
        """
        Select a response as selected response.

        :param index: index
        """
        _validate_pos_int(index, "index")
        self._selected_response_index = index
        self._mark_modified()
        if index < len(self._responses):
            return self._responses[index]

    def update_responses(self, responses: List[Response]) -> None:
        """
        Update the prompt responses.

        :param responses: responses
        """
        _validate_list_of(responses, "responses", Response, "`Response`")
        self._responses = responses
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

    @staticmethod
    def _validate_extract_json(json_object: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate and extract JSON object.

        :param json_object: JSON object
        """
        try:
            result = dict()
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            result["message"] = loaded_obj["message"]
            result["tokens"] = loaded_obj.get("tokens", None)
            result["id"] = loaded_obj.get("id", generate_message_id())
            result["responses"] = []
            for response in loaded_obj["responses"]:
                response_obj = Response()
                response_obj.from_json(response)
                result["responses"].append(response_obj)
            result["role"] = Role(loaded_obj["role"])
            result["template"] = PresetPromptTemplate.DEFAULT.value
            if "template" in loaded_obj:
                template = PromptTemplate()
                template.from_json(loaded_obj["template"])
                result["template"] = template
            result["memor_version"] = loaded_obj["memor_version"]
            result["date_created"] = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            result["date_modified"] = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            result["selected_response_index"] = loaded_obj["selected_response_index"]
        except Exception:
            raise MemorValidationError(INVALID_PROMPT_STRUCTURE_MESSAGE)
        _validate_string(result["message"], "message")
        if result["tokens"] is not None:
            _validate_pos_int(result["tokens"], "tokens")
        _validate_message_id(result["id"])
        _validate_string(result["memor_version"], "memor_version")
        _validate_pos_int(result["selected_response_index"], "selected_response_index")
        return result

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        data = self._validate_extract_json(json_object)
        self._message = data["message"]
        self._tokens = data["tokens"]
        self._id = data["id"]
        self._responses = data["responses"]
        self._role = data["role"]
        self._template = data["template"]
        self._memor_version = data["memor_version"]
        self._date_created = data["date_created"]
        self._date_modified = data["date_modified"]
        self.select_response(data["selected_response_index"])

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

    @property
    def responses(self) -> List[Response]:
        """Get the prompt responses."""
        return self._responses

    @property
    def template(self) -> PromptTemplate:
        """Get the prompt template."""
        return self._template

    @property
    def selected_response(self) -> Response:
        """Get the prompt selected response."""
        if 0 <= self._selected_response_index < len(self._responses):
            return self._responses[self._selected_response_index]
        return None

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
            if isinstance(self.selected_response, Response):
                format_kwargs.update({"response": self.selected_response.to_json()})
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
                if self._role == Role.SYSTEM:
                    warnings.warn(AI_STUDIO_SYSTEM_WARNING, UserWarning)
                return {"role": self._role.value, "parts": [{"text": content}]}
            if render_format == RenderFormat.STRING:
                return content
            if render_format == RenderFormat.DICTIONARY:
                return prompt_dict
            if render_format == RenderFormat.ITEMS:
                return list(prompt_dict.items())
        except Exception:
            raise MemorRenderError(PROMPT_RENDER_ERROR_MESSAGE)
