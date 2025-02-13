# -*- coding: utf-8 -*-
"""Session class."""
import datetime
import json
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .prompt import Prompt
from .functions import get_time_utc

class Session:
    """Session class."""

    def __init__(
            self,
            instruction=None,
            prompts=[],
            file_path=None):
        """Session object initiator."""
        self._instruction = None
        self._prompts = []
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
        """Check sessions equality."""
        return self._instruction == other_session._instruction and self._prompts == other_session._prompts

    def __str__(self):
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

    def add_prompt(self, prompt, index=None): #TODO: Need validation
        """Add a prompt to the session object."""
        if index is None:
            self._prompts.append(prompt)
        else:
            self._prompts.insert(index, prompt)
        self._date_modified = get_time_utc()

    def remove_prompt(self, index):
        """Remove a prompt from the session object."""
        self._prompts.pop(index)
        self._date_modified = get_time_utc()

    def enable_prompt(self, index):
        """
        Enable a prompt.

        :param index: index
        :type index: int
        :return: None
        """
        pass

    def disable_prompt(self, index):
        """
        Disable a prompt.

        :param index: index
        :type index: int
        :return: None
        """
        pass

    def update_prompts(self, prompts): #TODO: Need validation
        """Update the session prompts."""
        self._prompts = prompts
        self._date_modified = get_time_utc()

    def update_instruction(self, instruction): #TODO: Need validation
        """Update the session instruction."""
        self._instruction = instruction
        self._date_modified = get_time_utc()

    def save(self, file_path):
        """Save method."""
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                data = self.to_json()
                file.write(data)
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def load(self, file_path): #TODO: Need validation
        """Load method."""
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
        pass

    def render(self):
        """Render method."""
        pass
