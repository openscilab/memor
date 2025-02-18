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
            prompts=[],
            file_path=None):
        """
        Session object initiator.

        :param instruction: instruction
        :type instruction: str
        :param prompts: prompts
        :type prompts: list
        :param file_path: file path
        :type file_path: str
        :return: None
        """
        self._instruction = None
        self._prompts = []
        self._prompts_status = []
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        if file_path:
            self.load(file_path)
        else:
            if instruction:
                self.update_instruction(instruction)
            if prompts:
                self.update_prompts(prompts)

    def __eq__(self, other_session):
        """
        Check sessions equality.

        :param other_session: other session
        :type other_session: Session
        :return: bool
        """
        return self._instruction == other_session._instruction and self._prompts == other_session._prompts

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

    def add_prompt(self, prompt, status=True, index=None):
        """
        Add a prompt to the session object.

        :param prompt: prompt
        :type prompt: Prompt
        :param status: status
        :type status: bool
        :param index: index
        :type index: int
        :return: None
        """
        if not isinstance(prompt, Prompt):
            raise MemorValidationError(INVALID_PROMPT_MESSAGE)
        _validate_bool(status, "status")
        if index is None:
            self._prompts.append(prompt)
            self._prompts_status.append(status)
        else:
            self._prompts.insert(index, prompt)
            self._prompts_status.insert(index, status)
        self._date_modified = get_time_utc()

    def remove_prompt(self, index):
        """
        Remove a prompt from the session object.

        :param index: index
        :type index: int
        :return: None
        """
        self._prompts.pop(index)
        self._prompts_status.pop(index)
        self._date_modified = get_time_utc()

    def enable_prompt(self, index):
        """
        Enable a prompt.

        :param index: index
        :type index: int
        :return: None
        """
        self._prompts_status[index] = True

    def disable_prompt(self, index):
        """
        Disable a prompt.

        :param index: index
        :type index: int
        :return: None
        """
        self._prompts_status[index] = False

    def update_prompts(self, prompts, status=None):
        """
        Update the session prompts.

        :param prompts: prompts
        :type prompts: list
        :param status: status
        :type status: list
        :return: None
        """
        _validate_list_of(prompts, "prompts", Prompt, "`Prompt`")
        self._prompts = prompts
        if status:
            self.update_prompts_status(status)
        self._date_modified = get_time_utc()

    def update_prompts_status(self, status):
        """
        Update the session prompts status.

        :param status: status
        :type status: list
        :return: None
        """
        _validate_list_of(status, "status", bool, "booleans")
        if len(status) != len(self._prompts):
            raise MemorValidationError(INVALID_PROMPT_STATUS_LEN_MESSAGE)
        self._prompts_status = status

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
        self._prompts_status = loaded_obj["prompts_status"]
        prompts = []
        for prompt in loaded_obj["prompts"]:
            prompt_obj = Prompt()
            prompt_obj.from_json(prompt)
            prompts.append(prompt_obj)
        self._prompts = prompts
        self._memor_version = loaded_obj["memor_version"]
        self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
        self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)

    def to_json(self):
        """
        Convert the session to a JSON object.

        :return: JSON object
        """
        data = self.to_dict()
        for index, prompt in enumerate(data["prompts"]):
            data["prompts"][index] = prompt.to_json()
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
            "prompts": self._prompts.copy(),
            "prompts_status": self._prompts_status.copy(),
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
            for prompt in self._prompts:
                result.extend(prompt.render(render_format=PromptRenderFormat.OPENAI))
            return result
        content = ""
        if self._instruction is not None:
            content = self._instruction + "\n"
        session_dict = self.to_dict()
        for prompt in self._prompts:
            content += prompt.render(render_format=PromptRenderFormat.STRING) + "\n"
        session_dict["content"] = content
        if render_format == PromptRenderFormat.STRING:
            return content
        if render_format == PromptRenderFormat.DICTIONARY:
            return session_dict
        if render_format == PromptRenderFormat.ITEMS:
            return list(session_dict.items())


# TODO: Properties
