# -*- coding: utf-8 -*-
"""Session class."""
from typing import List, Dict, Tuple, Any, Union, Generator
import datetime
import json
import re
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT, DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_MESSAGE
from .params import INVALID_SESSION_STRUCTURE_MESSAGE, INVALID_RENDER_FORMAT_MESSAGE
from .params import INVALID_INT_OR_STR_MESSAGE, INVALID_INT_OR_STR_SLICE_MESSAGE
from .params import UNSUPPORTED_OPERAND_ERROR_MESSAGE
from .params import RenderFormat
from .tokens_estimator import TokensEstimator
from .prompt import Prompt
from .response import Response
from .errors import MemorValidationError, MemorRenderError
from .functions import get_time_utc
from .functions import _validate_bool, _validate_path
from .functions import _validate_list_of, _validate_string
from .functions import _validate_status, _validate_pos_int


class Session:
    """Session class."""

    def __init__(
            self,
            title: str = None,
            messages: List[Union[Prompt, Response]] = [],
            file_path: str = None,
            init_check: bool = True) -> None:
        """
        Session object initiator.

        :param title: title
        :param messages: messages
        :param file_path: file path
        :param init_check: initial check flag
        """
        self._title = None
        self._render_counter = 0
        self._messages = []
        self._messages_status = []
        self._date_created = get_time_utc()
        self._mark_modified()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if title:
                self.update_title(title)
            if messages:
                self.update_messages(messages)
        if init_check:
            _ = self.render(enable_counter=False)

    def _mark_modified(self) -> None:
        """Mark modification."""
        self._date_modified = get_time_utc()

    def __eq__(self, other_session: "Session") -> bool:
        """
        Check sessions equality.

        :param other_session: other session
        """
        if isinstance(other_session, Session):
            return self._title == other_session._title and self._messages == other_session._messages
        return False

    def __str__(self) -> str:
        """Return string representation of Session."""
        return self.render(render_format=RenderFormat.STRING, enable_counter=False)

    def __repr__(self) -> str:
        """Return string representation of Session."""
        return "Session(title={title})".format(title=self._title)

    def __len__(self) -> int:
        """Return the length of the Session object."""
        return len(self._messages)

    def __iter__(self) -> Generator[Union[Prompt, Response], None, None]:
        """Iterate through the Session object."""
        yield from self._messages

    def __add__(self, other_object: Union["Session", Response, Prompt]) -> "Session":
        """
        Addition method.

        :param other_object: other object
        """
        if isinstance(other_object, (Response, Prompt)):
            new_messages = self._messages + [other_object]
            return Session(title=self.title, messages=new_messages)
        if isinstance(other_object, Session):
            new_messages = self._messages + other_object._messages
            return Session(messages=new_messages)
        raise TypeError(
            UNSUPPORTED_OPERAND_ERROR_MESSAGE.format(
                operator="+",
                operand1="Session",
                operand2=type(other_object).__name__))

    def __radd__(self, other_object: Union["Session", Response, Prompt]) -> "Session":
        """
        Reverse addition method.

        :param other_object: other object
        """
        if isinstance(other_object, (Response, Prompt)):
            new_messages = [other_object] + self._messages
            return Session(title=self.title, messages=new_messages)
        raise TypeError(
            UNSUPPORTED_OPERAND_ERROR_MESSAGE.format(
                operator="+",
                operand1="Session",
                operand2=type(other_object).__name__))

    def __contains__(self, message: Union[Prompt, Response]) -> bool:
        """
        Check if the Session contains the given message.

        :param message: message
        """
        return message in self._messages

    def __getitem__(self, identifier: Union[int, slice, str]) -> Union[Prompt, Response]:
        """
        Get a message from the session object.

        :param identifier: message identifier (index/slice or id)
        """
        return self.get_message(identifier=identifier)

    def __copy__(self) -> "Session":
        """Return a copy of the Session object."""
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self) -> "Session":
        """Return a copy of the Session object."""
        return self.__copy__()

    def search(self, query: str, use_regex: bool = False, case_sensitive: bool = False) -> List[int]:
        """
        Search messages for a keyword or regex pattern, returning indices.

        :param query: input query
        :param use_regex: regex flag
        :param case_sensitive: case sensitivity flag
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        if not use_regex:
            query = re.escape(query)
        pattern = re.compile(query, flags)
        result = []
        for index, message in enumerate(self.messages):
            if isinstance(message, (Prompt, Response)):
                try:
                    searchable_str = message.render(render_format=RenderFormat.STRING)
                    if pattern.search(searchable_str):
                        result.append(index)
                except MemorRenderError:
                    continue
        return result

    def add_message(self,
                    message: Union[Prompt, Response],
                    status: bool = True,
                    index: int = None) -> None:
        """
        Add a message to the session object.

        :param message: message
        :param status: status
        :param index: index
        """
        if not isinstance(message, (Prompt, Response)):
            raise MemorValidationError(INVALID_MESSAGE)
        _validate_bool(status, "status")
        if index is None:
            self._messages.append(message)
            self._messages_status.append(status)
        else:
            self._messages.insert(index, message)
            self._messages_status.insert(index, status)
        self._mark_modified()

    def get_message_by_index(self, index: Union[int, slice]) -> Union[Prompt, Response]:
        """
        Get a message from the session object by index/slice.

        :param index: index
        """
        return self._messages[index]

    def get_message_by_id(self, message_id: str) -> Union[Prompt, Response]:
        """
        Get a message from the session object by message id.

        :param message_id: message id
        """
        for index, message in enumerate(self._messages):
            if message.id == message_id:
                return self.get_message_by_index(index=index)

    def get_message(self, identifier: Union[int, slice, str]) -> Union[Prompt, Response]:
        """
        Get a message from the session object.

        :param identifier: message identifier (index/slice or id)
        """
        if isinstance(identifier, (int, slice)):
            return self.get_message_by_index(index=identifier)
        elif isinstance(identifier, str):
            return self.get_message_by_id(message_id=identifier)
        else:
            raise MemorValidationError(INVALID_INT_OR_STR_SLICE_MESSAGE.format(parameter_name="identifier"))

    def remove_message_by_index(self, index: int) -> None:
        """
        Remove a message from the session object by index.

        :param index: index
        """
        self._messages.pop(index)
        self._messages_status.pop(index)
        self._mark_modified()

    def remove_message_by_id(self, message_id: str) -> None:
        """
        Remove a message from the session object by message id.

        :param message_id: message id
        """
        for index, message in enumerate(self._messages):
            if message.id == message_id:
                self.remove_message_by_index(index=index)
                break

    def remove_message(self, identifier: Union[int, str]) -> None:
        """
        Remove a message from the session object.

        :param identifier: message identifier (index or id)
        """
        if isinstance(identifier, int):
            self.remove_message_by_index(index=identifier)
        elif isinstance(identifier, str):
            self.remove_message_by_id(message_id=identifier)
        else:
            raise MemorValidationError(INVALID_INT_OR_STR_MESSAGE.format(parameter_name="identifier"))

    def clear_messages(self) -> None:
        """Remove all messages."""
        self._messages = []
        self._messages_status = []
        self._mark_modified()

    def enable_message(self, index: int) -> None:
        """
        Enable a message.

        :param index: index
        """
        self._messages_status[index] = True

    def disable_message(self, index: int) -> None:
        """
        Disable a message.

        :param index: index
        """
        self._messages_status[index] = False

    def mask_message(self, index: int) -> None:
        """
        Mask a message.

        :param index: index
        """
        self.disable_message(index)

    def unmask_message(self, index: int) -> None:
        """
        Unmask a message.

        :param index: index
        """
        self.enable_message(index)

    def update_title(self, title: str) -> None:
        """
        Update the session title.

        :param title: title
        """
        _validate_string(title, "title")
        self._title = title
        self._mark_modified()

    def update_messages(self,
                        messages: List[Union[Prompt, Response]],
                        status: List[bool] = None) -> None:
        """
        Update the session messages.

        :param messages: messages
        :param status: status
        """
        _validate_list_of(messages, "messages", (Prompt, Response), "`Prompt` or `Response`")
        if not status:
            status = len(messages) * [True]
        _validate_status(status, messages)
        self._messages_status = status
        self._messages = messages
        self._mark_modified()

    def update_messages_status(self, status: List[bool]) -> None:
        """
        Update the session messages status.

        :param status: status
        """
        self.update_messages(messages=self._messages, status=status)

    def save(self, file_path: str) -> Dict[str, Any]:
        """
        Save method.

        :param file_path: session file path
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                data = self.to_json()
                json.dump(data, file)
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def load(self, file_path: str) -> None:
        """
        Load method.

        :param file_path: session file path
        """
        _validate_path(file_path)
        with open(file_path, "r") as file:
            self.from_json(file.read())

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
            result["title"] = loaded_obj["title"]
            result["render_counter"] = loaded_obj.get("render_counter", 0)
            result["messages_status"] = loaded_obj["messages_status"]
            result["messages"] = []
            for message in loaded_obj["messages"]:
                if message["type"] == "Prompt":
                    message_obj = Prompt()
                elif message["type"] == "Response":
                    message_obj = Response()
                message_obj.from_json(message)
                result["messages"].append(message_obj)
            result["memor_version"] = loaded_obj["memor_version"]
            result["date_created"] = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            result["date_modified"] = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
        except Exception:
            raise MemorValidationError(INVALID_SESSION_STRUCTURE_MESSAGE)
        if result["title"] is not None:
            _validate_string(result["title"], "title")
        _validate_pos_int(result["render_counter"], "render_counter")
        _validate_status(result["messages_status"], result["messages"])
        _validate_string(result["memor_version"], "memor_version")
        return result

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        data = self._validate_extract_json(json_object=json_object)
        self._title = data["title"]
        self._render_counter = data["render_counter"]
        self._messages = data["messages"]
        self._messages_status = data["messages_status"]
        self._memor_version = data["memor_version"]
        self._date_created = data["date_created"]
        self._date_modified = data["date_modified"]

    def to_json(self) -> Dict[str, Any]:
        """Convert the session to a JSON object."""
        data = self.to_dict().copy()
        for index, message in enumerate(data["messages"]):
            data["messages"][index] = message.to_json()
        data["date_created"] = datetime.datetime.strftime(data["date_created"], DATE_TIME_FORMAT)
        data["date_modified"] = datetime.datetime.strftime(data["date_modified"], DATE_TIME_FORMAT)
        return data

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the session to a dictionary.

        :return: dict
        """
        data = {
            "type": "Session",
            "title": self._title,
            "render_counter": self._render_counter,
            "messages": self._messages.copy(),
            "messages_status": self._messages_status.copy(),
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }
        return data

    def get_size(self) -> int:
        """Get the size of the session in bytes."""
        json_str = json.dumps(self.to_json())
        return len(json_str.encode())

    def render(self, render_format: RenderFormat = RenderFormat.DEFAULT,
               enable_counter: bool = True) -> Union[str, Dict[str, Any], List[Tuple[str, Any]]]:
        """
        Render method.

        :param render_format: render format
        :param enable_counter: render counter flag
        """
        if not isinstance(render_format, RenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        result = None
        if render_format in [RenderFormat.OPENAI, RenderFormat.AI_STUDIO]:
            result = []
            for index, message in enumerate(self._messages):
                if self.messages_status[index]:
                    if isinstance(message, Session):
                        result.extend(message.render(render_format=render_format))
                    else:
                        result.append(message.render(render_format=render_format))
        else:
            content = ""
            session_dict = self.to_dict()
            for index, message in enumerate(self._messages):
                if self.messages_status[index]:
                    content += message.render(render_format=RenderFormat.STRING) + "\n"
            session_dict["content"] = content
            if render_format == RenderFormat.STRING:
                result = content
            if render_format == RenderFormat.DICTIONARY:
                result = session_dict
            if render_format == RenderFormat.ITEMS:
                result = list(session_dict.items())
        if enable_counter:
            self._render_counter += 1
            self._mark_modified()
        return result

    def check_render(self) -> bool:
        """Check render."""
        try:
            _ = self.render(enable_counter=False)
            return True
        except Exception:
            return False

    def estimate_tokens(self, method: TokensEstimator = TokensEstimator.DEFAULT) -> int:
        """
        Estimate the number of tokens in the session.

        :param method: token estimator method
        """
        return method(self.render(render_format=RenderFormat.STRING, enable_counter=False))

    @property
    def date_created(self) -> datetime.datetime:
        """Get the session creation date."""
        return self._date_created

    @property
    def date_modified(self) -> datetime.datetime:
        """Get the session object modification date."""
        return self._date_modified

    @property
    def title(self) -> str:
        """Get the session title."""
        return self._title

    @property
    def render_counter(self) -> int:
        """Get the render counter."""
        return self._render_counter

    @property
    def messages(self) -> List[Union[Prompt, Response]]:
        """Get the session messages."""
        return self._messages

    @property
    def messages_status(self) -> List[bool]:
        """Get the session messages status."""
        return self._messages_status

    @property
    def masks(self) -> List[bool]:
        """Get the session masks."""
        return [not x for x in self._messages_status]

    @property
    def size(self) -> int:
        """Get the session size in bytes."""
        return self.get_size()
