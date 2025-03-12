# -*- coding: utf-8 -*-
"""Session class."""
from typing import List, Dict, Tuple, Any, Union, Generator
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_MESSAGE
from .params import INVALID_MESSAGE_STATUS_LEN_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .params import UNSUPPORTED_OPERAND_ERROR_MESSAGE
from .params import RenderFormat
from .prompt import Prompt
from .response import Response
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import _validate_bool, _validate_path
from .functions import _validate_list_of, _validate_string


class Session:
    """Session class."""

    def __init__(
            self,
            title: str = None,
            messages: List[Union[Prompt, Response]] = [],
            file_path: str = None) -> None:
        """
        Session object initiator.

        :param title: title
        :param messages: messages
        :param file_path: file path
        """
        self._title: str = None
        self._messages = []
        self._messages_status = []
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if title:
                self.update_title(title)
            if messages:
                self.update_messages(messages)

    def __eq__(self, other_session: Any) -> bool:
        """
        Check sessions equality.

        :param other_session: other session
        """
        if isinstance(other_session, Session):
            return self._title == other_session._title and self._messages == other_session._messages
        return False

    def __str__(self) -> str:
        """Return string representation of Session."""
        return self.render(render_format=RenderFormat.STRING)

    def __repr__(self) -> str:
        """Return string representation of Session."""
        return "Session(title={title})".format(title=self._title)

    def __len__(self) -> int:
        """
        Return the length of the Session object.
        """
        return len(self._messages)


    def __iter__(self) -> Generator[Union[Prompt, Response], None, None]:
        """
        Iterate through the Session object.
        """
        yield from self._messages

    def __add__(self, other_object: Any) -> Any:
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
        raise TypeError(UNSUPPORTED_OPERAND_ERROR_MESSAGE.format("+", "Session", type(other_object).__name__))

    def __radd__(self, other_object: Any) -> Any:
        """
        Reverse addition method.

        :param other_object: other object
        """
        if isinstance(other_object, (Response, Prompt)):
            new_messages = [other_object] + self._messages
            return Session(title=self.title, messages=new_messages)
        raise TypeError(UNSUPPORTED_OPERAND_ERROR_MESSAGE.format("+", "Session", type(other_object).__name__))

    def __contains__(self, message: Union[Prompt, Response]) -> bool:
        """
        Check if the Session contains the given message.

        :param message: message
        """
        return message in self._messages

    def __getitem__(self, index: int) -> Union[Prompt, Response]:
        """
        Return the Session message(s).

        :param index: index
        """
        return self._messages[index]

    def __copy__(self) -> Any:
        """
        Return a copy of the Session object.
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self) -> Any:
        """
        Return a copy of the Session object.
        """
        return self.__copy__()

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
        self._date_modified = get_time_utc()

    def remove_message(self, index: int) -> None:
        """
        Remove a message from the session object.

        :param index: index
        """
        self._messages.pop(index)
        self._messages_status.pop(index)
        self._date_modified = get_time_utc()

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
        self._date_modified = get_time_utc()

    def update_messages(self,
                        messages: List[Union[Prompt, Response]],
                        status: List[bool] = None) -> None:
        """
        Update the session messages.

        :param messages: messages
        :param status: status
        """
        _validate_list_of(messages, "messages", (Prompt, Response), "`Prompt` or `Response`")
        self._messages = messages
        if status:
            self.update_messages_status(status)
        else:
            self.update_messages_status(len(messages) * [True])  # TODO: Need discussion
        self._date_modified = get_time_utc()

    def update_messages_status(self, status: List[bool]) -> None:
        """
        Update the session messages status.

        :param status: status
        """
        _validate_list_of(status, "status", bool, "booleans")
        if len(status) != len(self._messages):
            raise MemorValidationError(INVALID_MESSAGE_STATUS_LEN_MESSAGE)
        self._messages_status = status

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

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        if isinstance(json_object, str):
            loaded_obj = json.loads(json_object)
        else:
            loaded_obj = json_object.copy()
        self._title = loaded_obj["title"]
        self._messages_status = loaded_obj["messages_status"]
        messages = []
        for message in loaded_obj["messages"]:
            if message["type"] == "Prompt":
                message_obj = Prompt()
            elif message["type"] == "Response":
                message_obj = Response()
            message_obj.from_json(message)
            messages.append(message_obj)
        self._messages = messages
        self._memor_version = loaded_obj["memor_version"]
        self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
        self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the session to a JSON object.
        """
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
            "messages": self._messages.copy(),
            "messages_status": self._messages_status.copy(),
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }
        return data

    def render(self, render_format: RenderFormat = RenderFormat.DEFAULT) -> Union[str,
                                                                                  Dict[str, Any],
                                                                                  List[Tuple[str, Any]]]:
        """
        Render method.

        :param render_format: render format
        """
        if not isinstance(render_format, RenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        if render_format == RenderFormat.OPENAI:
            result = []
            for message in self._messages:
                if isinstance(message, Session):
                    result.extend(message.render(render_format=RenderFormat.OPENAI))
                else:
                    result.append(message.render(render_format=RenderFormat.OPENAI))
            return result
        content = ""
        session_dict = self.to_dict()
        for message in self._messages:
            content += message.render(render_format=RenderFormat.STRING) + "\n"
        session_dict["content"] = content
        if render_format == RenderFormat.STRING:
            return content
        if render_format == RenderFormat.DICTIONARY:
            return session_dict
        if render_format == RenderFormat.ITEMS:
            return list(session_dict.items())

    @property
    def date_created(self) -> datetime.datetime:
        """
        Get the session creation date.
        """
        return self._date_created

    @property
    def date_modified(self) -> datetime.datetime:
        """
        Get the session object modification date.
        """
        return self._date_modified

    @property
    def title(self) -> str:
        """
        Get the session title.
        """
        return self._title

    @property
    def messages(self) -> List[Union[Prompt, Response]]:
        """
        Get the session messages.
        """
        return self._messages

    @property
    def messages_status(self) -> List[bool]:
        """
        Get the session messages status.
        """
        return self._messages_status

    @property
    def masks(self) -> List[bool]:
        """
        Get the session masks.
        """
        return [not x for x in self._messages_status]
