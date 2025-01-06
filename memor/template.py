# -*- coding: utf-8 -*-
"""Template class."""
import json
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import MEMOR_VERSION


class CustomPromptTemplate:
    """Prompt template."""

    def __init__(self, content=None, file_path=None, title="unknown"):
        """
        Template object initiator.

        :param content: template content
        :type content: str
        :param file_path: template file path
        :type file_path: str
        :param title: template title
        :type title: str
        """
        memor_version = MEMOR_VERSION
        if file_path:
            with open(file_path, "r") as file:
                loaded_obj = json.loads(file.read())
                content = loaded_obj["content"]
                title = loaded_obj["title"]
                memor_version = loaded_obj["memor_version"]
        self._title = title
        self._content = content
        self._memor_version = memor_version


    def __str__(self):
        return self._content
    

    def save(self, file_path):
        """
        Save method.

        :param file_path: template file path
        :type file_path: str
        :return: result as dict
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                file.write(self.to_json())
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    def to_json(self):
        """Convert to json."""
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        "Convert to dict."
        return {
            "title": self._title,
            "content": self._content,
            "memor_version": MEMOR_VERSION
        }


DEFAULT_TEMPLATE_CONTENT = "{message}"
DEFAULT_TEMPLATE = CustomPromptTemplate(content=DEFAULT_TEMPLATE_CONTENT)
