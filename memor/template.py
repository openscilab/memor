# -*- coding: utf-8 -*-
"""Template class."""


class CustomPromptTemplate:
    """Prompt template."""

    def __init__(self, content, file_path=None):
        """
        Template object initiator.

        :param content: template content
        :type content: str
        :param file_path: template file path
        :type file_path: str
        """
        self._content = content

    def save(self, file_path):
        """
        Save method.

        :param file_path: template file path
        :type file_path: str
        :return: result as dict
        """
        pass

    def to_json(self):
        """Convert to json."""
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        "Convert to dict."
        return {
            "content": self._content,
        }


DEFAULT_TEMPLATE = CustomPromptTemplate(content="{message}")
