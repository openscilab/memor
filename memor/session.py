# -*- coding: utf-8 -*-
"""Session class."""


class Session:
    """Session class."""

    def __init__(
            self,
            instruction=None,
            prompts=[],
            file_path=None):
        """Session object initiator."""
        pass

    def __eq__(self, other_session):
        """Check sessions equality."""
        pass

    def __str__(self):
        """Return string representation of Session."""
        pass

    def __repr__(self):
        """Return string representation of Session."""
        pass

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
        pass

    def remove_prompt(self, index):
        """Remove a prompt from the session object."""
        pass

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
