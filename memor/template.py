# -*- coding: utf-8 -*-
"""Template class."""
import json
import datetime
from enum import Enum
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_TEMPLATE_FILE_MESSAGE
from .params import MEMOR_VERSION
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import validate_path, validate_custom_map
from .functions import _validate_string


class CustomPromptTemplate:
    r"""
    Prompt template.

    >>> template = CustomPromptTemplate(content="Take a deep breath\n{message}!", title="Greeting")
    >>> template.title
    'Greeting'
    """

    def __init__(
            self,
            content=None,
            file_path=None,
            title="unknown",
            custom_map=None):
        """
        Template object initiator.

        :param content: template content
        :type content: str
        :param file_path: template file path
        :type file_path: str
        :param title: template title
        :type title: str
        :param custom_map: custom map
        :type custom_map: dict
        :return: None
        """
        self._content = None
        self._title = None
        self._date_created = get_time_utc()
        self._date_modified = get_time_utc()
        self._memor_version = MEMOR_VERSION
        self._custom_map = None
        if file_path:
            self.load(file_path)
        else:
            if title:
                self.update_title(title)
            if content:
                self.update_content(content)
            if custom_map:
                self.update_map(custom_map)

    def __str__(self):
        """Return string representation of CustomPromptTemplate."""
        return self._content

    def __repr__(self):
        """Return string representation of CustomPromptTemplate."""
        return "CustomPromptTemplate(content={content})".format(content=self._content)

    def __copy__(self):
        """
        Return a copy of the CustomPromptTemplate object.

        :return: a copy of CustomPromptTemplate object"""
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self):
        """
        Return a copy of the CustomPromptTemplate object.

        :return: a copy of CustomPromptTemplate object
        """
        return self.__copy__()

    def update_title(self, title):
        """
        Update title.

        :param title: title
        :type title: str
        :return: None
        """
        _validate_string(title, "title")
        self._title = title
        self._date_modified = get_time_utc()

    def update_content(self, content):
        """
        Update content.

        :param content: content
        :type content: str
        :return: None
        """
        _validate_string(content, "content")
        self._content = content
        self._date_modified = get_time_utc()

    def update_map(self, custom_map):
        """
        Update custom map.

        :param custom_map: custom map
        :type custom_map: dict
        :return: None
        """
        validate_custom_map(custom_map)
        self._custom_map = custom_map
        self._date_modified = get_time_utc()

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

    def load(self, file_path):
        """
        Load method.

        :param file_path: template file path
        :type file_path: str
        :return: None
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            try:
                loaded_obj = json.loads(file.read())
                self._content = loaded_obj["content"]
                self._title = loaded_obj["title"]
                self._memor_version = loaded_obj["memor_version"]
                self._custom_map = loaded_obj["custom_map"]
                self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
                self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_TEMPLATE_FILE_MESSAGE)

    def to_json(self):
        """
        Convert CustomPromptTemplate to json.

        :return: JSON object
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """
        Convert CustomPromptTemplate to dict.

        :return: dict
        """
        return {
            "title": self._title,
            "content": self._content,
            "memor_version": MEMOR_VERSION,
            "custom_map": self._custom_map,
            "date_created": datetime.datetime.strftime(self._date_created, DATE_TIME_FORMAT),
            "date_modified": datetime.datetime.strftime(self._date_modified, DATE_TIME_FORMAT),
        }

    @property
    def content(self):
        """
        Get the CustomPromptTemplate content.

        :return: content
        """
        return self._content

    @property
    def title(self):
        """
        Get the CustomPromptTemplate title.

        :return: title
        """
        return self._title

    @property
    def date_created(self):
        """
        Get the CustomPromptTemplate creation date.

        :return: template creation date
        """
        return self._date_created

    @property
    def date_modified(self):
        """
        Get the CustomPromptTemplate modification date.

        :return: template modification date
        """
        return self._date_modified

    @property
    def custom_map(self):
        """
        Get the CustomPromptTemplate custom map.

        :return: custom map
        """
        return self._custom_map

BASIC_PROMPT_CONTENT = "{prompt_message}"
BASIC_RESPONSE0_CONTENT = "{response_0_message}"
BASIC_RESPONSE1_CONTENT = "{response_1_message}"
BASIC_RESPONSE2_CONTENT = "{response_2_message}"
BASIC_RESPONSE3_CONTENT = "{response_3_message}"
BASIC_PROMPT_RESPONSE_STANDARD_CONTENT = "Prompt: {prompt_message}\nResponse: {response_0_message}"
BASIC_PROMPT_RESPONSE_FULL_CONTENT = """Prompt:
    Message: {prompt_message}
    Role: {prompt_role}
    Date: {prompt_date}
Response:
    Message: {response_0_message}
    Role: {response_0_role}
    Temperature: {response_0_temperature}
    Model: {response_0_model}
    Score: {response_0_score}
    Date: {response_0_date}"""

class _BasicPresetPromptTemplate(Enum):
    PROMPT = CustomPromptTemplate(content=BASIC_PROMPT_CONTENT, title="Prompt")
    RESPONSE0 = CustomPromptTemplate(content=BASIC_RESPONSE0_CONTENT, title="Response0")
    RESPONSE1 = CustomPromptTemplate(content=BASIC_RESPONSE1_CONTENT, title="Response1")
    RESPONSE2 = CustomPromptTemplate(content=BASIC_RESPONSE2_CONTENT, title="Response2")
    RESPONSE3 = CustomPromptTemplate(content=BASIC_RESPONSE3_CONTENT, title="Response3")
    PROMPT_RESPONSE_STANDARD = CustomPromptTemplate(content=BASIC_PROMPT_RESPONSE_STANDARD_CONTENT, title="Prompt-Response Standard")
    PROMPT_RESPONSE_FULL = CustomPromptTemplate(content=BASIC_PROMPT_RESPONSE_FULL_CONTENT, title="Prompt-Response Standard")

class PresetPromptTemplate:
    """Preset prompt templates."""

    BASIC = _BasicPresetPromptTemplate

    DEFAULT = BASIC.PROMPT
