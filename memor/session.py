# -*- coding: utf-8 -*-
"""Session class."""
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_PROMPT_MESSAGE
from .params import INVALID_PROMPT_STATUS_LEN_MESSAGE
from .params import INVALID_RENDER_FORMAT_MESSAGE
from .params import PromptRenderFormat
from .prompt import Prompt
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import validate_path
from .functions import _validate_bool, _validate_string
from .functions import _validate_list_of


class Session:
    """Session class."""

    def __init__(
            self,
            instruction=None,
            messages=[],
            file_path=None):
        """
        Session object initiator.

        :param instruction: instruction
        :type instruction: str
        :param messages: messages
        :type messages: list
        :param file_path: file path
        :type file_path: str
        :return: None
        """
        self._instruction = None
        self._messages = []
        self._messages_status = []
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if instruction:
                self.update_instruction(instruction)
            if messages:
                self.update_messages(messages)

    def __eq__(self, other_session):
        """
        Check sessions equality.

        :param other_session: other session
        :type other_session: Session
        :return: bool
        """
        return self._instruction == other_session._instruction and self._messages == other_session._messages

    def __str__(self):  # TODO: Need discussion
        """Return string representation of Session."""
        pass

    def __repr__(self):
        """Return string representation of Session."""
        return "Session(instruction={instruction})".format(instruction=self._instruction)

    def __copy__(self):
        """
        Return a copy of the Session object.

        :return: a copy of Session object
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self):
        """
        Return a copy of the Session object.

        :return: a copy of Session object
        """
        return self.__copy__()

    def add_message(self, message, status=True, index=None):
        """
        Add a message to the session object.

        :param message: message
        :type message: message
        :param status: status
        :type status: bool
        :param index: index
        :type index: int
        :return: None
        """
        if not isinstance(message, Prompt):
            raise MemorValidationError(INVALID_PROMPT_MESSAGE)
        _validate_bool(status, "status")
        if index is None:
            self._messages.append(message)
            self._messages_status.append(status)
        else:
            self._messages.insert(index, message)
            self._messages_status.insert(index, status)
        self._date_modified = get_time_utc()

    def remove_message(self, index):
        """
        Remove a message from the session object.

        :param index: index
        :type index: int
        :return: None
        """
        self._messages.pop(index)
        self._messages_status.pop(index)
        self._date_modified = get_time_utc()

    def enable_message(self, index):
        """
        Enable a message.

        :param index: index
        :type index: int
        :return: None
        """
        self._messages_status[index] = True

    def disable_message(self, index):
        """
        Disable a message.

        :param index: index
        :type index: int
        :return: None
        """
        self._messages_status[index] = False

    def update_messages(self, messages, status=None):
        """
        Update the session messages.

        :param messages: messages
        :type messages: list
        :param status: status
        :type status: list
        :return: None
        """
        _validate_list_of(messages, "messages", Prompt, "`Prompt`")
        self._messages = messages
        if status:
            self.update_messages_status(status)
        self._date_modified = get_time_utc()

    def update_messages_status(self, status):
        """
        Update the session messages status.

        :param status: status
        :type status: list
        :return: None
        """
        _validate_list_of(status, "status", bool, "booleans")
        if len(status) != len(self._messages):
            raise MemorValidationError(INVALID_PROMPT_STATUS_LEN_MESSAGE)
        self._messages_status = status

    def update_instruction(self, instruction):
        """
        Update the session instruction.

        :param instruction: instruction
        :type instruction: str
        :return: None
        """
        _validate_string(instruction, "instruction")
        self._instruction = instruction
        self._date_modified = get_time_utc()

    def save(self, file_path):
        """
        Save method.

        :param file_path: session file path
        :type file_path: str
        :return: result as dict
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                data = self.to_json()
                file.write(data)
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def load(self, file_path):
        """
        Load method.

        :param file_path: session file path
        :type file_path: str
        :return: None
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            self.from_json(file.read())

    def from_json(self, json_doc):
        """
        Load attributes from the JSON document.

        :param json_doc: JSON document
        :type json_doc: str
        :return: None
        """
        loaded_obj = json.loads(json_doc)
        self._instruction = loaded_obj["instruction"]
        self._messages_status = loaded_obj["messages_status"]
        messages = []
        for message in loaded_obj["messages"]:
            message_obj = Prompt()
            message_obj.from_json(message)
            messages.append(message_obj)
        self._messages = messages
        self._memor_version = loaded_obj["memor_version"]
        self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
        self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)

    def to_json(self):
        """
        Convert the session to a JSON object.

        :return: JSON object
        """
        data = self.to_dict()
        for index, message in enumerate(data["messages"]):
            data["messages"][index] = message.to_json()
        data["date_created"] = datetime.datetime.strftime(data["date_created"], DATE_TIME_FORMAT)
        data["date_modified"] = datetime.datetime.strftime(data["date_modified"], DATE_TIME_FORMAT)
        return json.dumps(data, indent=4)

    def to_dict(self):
        """
        Convert the session to a dictionary.

        :return: dict
        """
        data = {
            "instruction": self._instruction,
            "messages": self._messages.copy(),
            "messages_status": self._messages_status.copy(),
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }
        return data

    def render(self, render_format=PromptRenderFormat.DEFAULT):  # TODO: Need validation
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered session
        """
        if not isinstance(render_format, PromptRenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        if render_format == PromptRenderFormat.OPENAI:
            result = []
            if self._instruction is not None:
                # TODO: I think we can remove instruction (need discussion)
                result = [{"role": "user", "content": self._instruction}]
            for message in self._messages:
                result.extend(message.render(render_format=PromptRenderFormat.OPENAI))
            return result
        content = ""
        if self._instruction is not None:
            content = self._instruction + "\n"
        session_dict = self.to_dict()
        for message in self._messages:
            content += message.render(render_format=PromptRenderFormat.STRING) + "\n"
        session_dict["content"] = content
        if render_format == PromptRenderFormat.STRING:
            return content
        if render_format == PromptRenderFormat.DICTIONARY:
            return session_dict
        if render_format == PromptRenderFormat.ITEMS:
            return list(session_dict.items())


# TODO: Properties
