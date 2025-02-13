# -*- coding: utf-8 -*-
"""Session class."""
from .params import MEMOR_VERSION
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

    def add_prompt(self, prompt, index=None):
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

    def update_prompts(self, prompts):
        """Update the session prompts."""
        pass

    def update_instruction(self, instruction):
        """Update the session instruction."""
        pass

    def save(self, file_path, save_template=True):
        """Save method."""
        pass

    def load(self, file_path):
        """Load method."""
        pass

    def from_json(self, json_doc):
        """
        Load attributes from the JSON document.

        :param json_doc: JSON document
        :type json_doc: str
        :return: None
        """
        pass

    def to_json(self):
        """
        Convert the session to a JSON object.

        :return: JSON object
        """
        pass

    def to_dict(self):
        """
        Convert the session to a dictionary.

        :return: dict
        """
        pass

    def render(self):
        """Render method."""
        pass
