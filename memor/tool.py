# -*- coding: utf-8 -*-
"""Tool class."""
from typing import List, Dict, Union, Tuple, Any, Optional
import datetime
import json
import warnings
from .message import Message
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import RenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .params import Role
from .params import INVALID_PROMPT_STRUCTURE_MESSAGE, INVALID_TEMPLATE_MESSAGE
from .params import INVALID_RESPONSE_MESSAGE
from .params import PROMPT_RENDER_ERROR_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .params import AI_STUDIO_SYSTEM_WARNING
from .errors import MemorValidationError, MemorRenderError
from .functions import generate_message_id
from .functions import _validate_string, _validate_pos_int, _validate_list_of
from .functions import _validate_message_id, _validate_warnings, get_time_utc
from .functions import _validate_arguments
from .template import PromptTemplate, PresetPromptTemplate
from .template import _BasicPresetPromptTemplate, _Instruction1PresetPromptTemplate, _Instruction2PresetPromptTemplate, _Instruction3PresetPromptTemplate
from .response import Response


class ToolCall(Message):
    """
    ToolCall class.

    Represents a tool/function call requested by the assistant.
    """

    def __init__(
            self,
            name: str,
            arguments: Dict[str, Any],
            message: str = "",
            call_id: Optional[str] = None,
            role: Role = Role.ASSISTANT,
            date: datetime.datetime = get_time_utc(),
            file_path: Optional[str] = None
    ) -> None:
        """
        ToolCall object initiator.

        :param name: tool/function name
        :param arguments: tool/function arguments
        :param message: tool message
        :param call_id: tool call id
        :param role: message role
        :param date: creation date
        :param file_path: tool call file path
        """
        super().__init__()
        self._name = None
        self._arguments = None
        self._call_id = None
        self._role = Role.ASSISTANT

        if file_path is not None:
            self.load(file_path)
        else:
            self.update_name(name)
            self.update_arguments(arguments)
            self.update_role(role)
            self.update_message(message)

            if call_id is not None:
                self.update_call_id(call_id)

            if date:
                _validate_date_time(date, "date")
                self._date_created = date

            self._id = generate_message_id()

        _validate_message_id(self._id)


    def __eq__(self, other: "ToolCall") -> bool:
        if isinstance(other, ToolCall):
            return (
                self._name == other._name and
                self._arguments == other._arguments and
                self._call_id == other._call_id and
                self._role == other._role
            )
        return False

    def __repr__(self) -> str:
        return "ToolCall(name={name}, arguments={arguments})".format(name=self._name, arguments=self._arguments)

    def update_name(self, name: str) -> None:
        """Update tool name."""
        if _validate_string(name, "name"):
            self._name = name
            self._mark_modified()

    def update_arguments(self, arguments: Dict[str, Any]) -> None:
        """Update tool arguments."""
        if _validate_arguments(arguments):
            self._arguments = arguments
            self._mark_modified()

    def update_call_id(self, call_id: str) -> None:
        """Update tool call id."""
        if _validate_string(call_id, "call_id"):
            self._call_id = call_id
            self._mark_modified()

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool call to dictionary."""
        return {
            "type": "ToolCall",
            "name": self._name,
            "arguments": self._arguments,
            "call_id": self._call_id,
            "role": self._role,
            "id": self._id,
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }

    def to_json(self) -> Dict[str, Any]:
        """Convert tool call to JSON."""
        data = self.to_dict().copy()
        data["role"] = data["role"].value
        data["date_created"] = datetime.datetime.strftime(
            data["date_created"], DATE_TIME_FORMAT
        )
        data["date_modified"] = datetime.datetime.strftime(
            data["date_modified"], DATE_TIME_FORMAT
        )
        return data

    def render(
            self,
            render_format: RenderFormat = RenderFormat.DEFAULT,
            show_warning: bool = True
    ) -> Union[Dict[str, Any], str]:
        """
        Render the tool call.

        :param render_format: render format
        :param show_warning: show warning flag
        """
        if not isinstance(render_format, RenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)

        if render_format == RenderFormat.OPENAI:
            role_str = self._role.value
            if self._role == Role.ASSISTANT:
                role_str = "model"
            return {
                "role": role_str,
                "tool_calls": [
                    {
                        "id": self._call_id,
                        "type": "function",
                        "function": {
                            "name": self._name,
                            "arguments": json.dumps(self._arguments),
                        }
                    }
                ]
            }

        elif render_format == RenderFormat.AI_STUDIO:
            return {
                "role": self._role.value,
                "parts": [
                    {
                        "functionCall": {
                            "name": self._name,
                            "args": self._arguments
                        }
                    }
                ]
            }

        elif render_format == RenderFormat.DICTIONARY:
            return self.to_dict()

        elif render_format == RenderFormat.ITEMS:
            return self.to_dict().items()

        return self.to_dict()


    @property
    def name(self) -> str:
        return self._name

    @property
    def arguments(self) -> Dict[str, Any]:
        return self._arguments

    @property
    def call_id(self) -> str:
        return self._call_id
