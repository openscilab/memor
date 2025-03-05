# -*- coding: utf-8 -*-
"""Template class."""
import json
import datetime
from enum import Enum
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_TEMPLATE_STRUCTURE_MESSAGE
from .params import MEMOR_VERSION
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import _validate_path, _validate_custom_map
from .functions import _validate_string


class PromptTemplate:
    r"""
    Prompt template.

    >>> template = PromptTemplate(content="Take a deep breath\n{prompt_message}!", title="Greeting")
    >>> template.title
    'Greeting'
    """

    def __init__(
            self,
            content=None,
            file_path=None,
            title=None,
            custom_map=None):
        """
        Prompt template object initiator.

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

    def __eq__(self, other_template):
        """
        Check templates equality.

        :param other_template: another template
        :type other_template: PromptTemplate
        :return: result as bool
        """
        if isinstance(other_template, PromptTemplate):
            return self._content == other_template._content and self._title == other_template._title and self._custom_map == other_template._custom_map
        return False

    def __str__(self):
        """Return string representation of PromptTemplate."""
        return self._content

    def __repr__(self):
        """Return string representation of PromptTemplate."""
        return "PromptTemplate(content={content})".format(content=self._content)

    def __copy__(self):
        """
        Return a copy of the PromptTemplate object.

        :return: a copy of PromptTemplate object
        """
        _class = self.__class__
        result = _class.__new__(_class)
        result.__dict__.update(self.__dict__)
        return result

    def copy(self):
        """
        Return a copy of the PromptTemplate object.

        :return: a copy of PromptTemplate object
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
        _validate_custom_map(custom_map)
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
                json.dump(self.to_json(), file)
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
        _validate_path(file_path)
        with open(file_path, "r") as file:
            self.from_json(file.read())

    def from_json(self, json_object):
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        :type json_object: str or dict
        :return: None
        """
        try:
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            self._content = loaded_obj["content"]
            self._title = loaded_obj["title"]
            self._memor_version = loaded_obj["memor_version"]
            self._custom_map = loaded_obj["custom_map"]
            self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            self._date_modified = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
        except Exception:
            raise MemorValidationError(INVALID_TEMPLATE_STRUCTURE_MESSAGE)

    def to_json(self):
        """
        Convert PromptTemplate to json.

        :return: JSON structure as dict
        """
        data = self.to_dict().copy()
        data["date_created"] = datetime.datetime.strftime(data["date_created"], DATE_TIME_FORMAT)
        data["date_modified"] = datetime.datetime.strftime(data["date_modified"], DATE_TIME_FORMAT)
        return data

    def to_dict(self):
        """
        Convert PromptTemplate to dict.

        :return: dict
        """
        return {
            "title": self._title,
            "content": self._content,
            "memor_version": MEMOR_VERSION,
            "custom_map": self._custom_map.copy(),
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }

    @property
    def content(self):
        """
        Get the PromptTemplate content.

        :return: content
        """
        return self._content

    @property
    def title(self):
        """
        Get the PromptTemplate title.

        :return: title
        """
        return self._title

    @property
    def date_created(self):
        """
        Get the PromptTemplate creation date.

        :return: template creation date
        """
        return self._date_created

    @property
    def date_modified(self):
        """
        Get the PromptTemplate modification date.

        :return: template modification date
        """
        return self._date_modified

    @property
    def custom_map(self):
        """
        Get the PromptTemplate custom map.

        :return: custom map
        """
        return self._custom_map


PROMPT_INSTRUCTION1 = "I'm providing you with a history of a previous conversation. Please consider this context when responding to my new question.\n"
PROMPT_INSTRUCTION2 = "Here is the context from a prior conversation. Please learn from this information and use it to provide a thoughtful and context-aware response to my next questions.\n"
PROMPT_INSTRUCTION3 = "I am sharing a record of a previous discussion. Use this information to provide a consistent and relevant answer to my next query.\n"

BASIC_PROMPT_CONTENT = "{instruction}{prompt[message]}"
BASIC_RESPONSE_CONTENT = "{instruction}{response[message]}"
BASIC_RESPONSE0_CONTENT = "{instruction}{responses[0][message]}"
BASIC_RESPONSE1_CONTENT = "{instruction}{responses[1][message]}"
BASIC_RESPONSE2_CONTENT = "{instruction}{responses[2][message]}"
BASIC_RESPONSE3_CONTENT = "{instruction}{responses[3][message]}"
BASIC_PROMPT_CONTENT_LABEL = "{instruction}Prompt: {prompt[message]}"
BASIC_RESPONSE_CONTENT_LABEL = "{instruction}Response: {response[message]}"
BASIC_RESPONSE0_CONTENT_LABEL = "{instruction}Response: {responses[0][message]}"
BASIC_RESPONSE1_CONTENT_LABEL = "{instruction}Response: {responses[1][message]}"
BASIC_RESPONSE2_CONTENT_LABEL = "{instruction}Response: {responses[2][message]}"
BASIC_RESPONSE3_CONTENT_LABEL = "{instruction}Response: {responses[3][message]}"
BASIC_PROMPT_RESPONSE_STANDARD_CONTENT = "{instruction}Prompt: {prompt[message]}\nResponse: {response[message]}"
BASIC_PROMPT_RESPONSE_FULL_CONTENT = """{instruction}
Prompt:
    Message: {prompt[message]}
    Role: {prompt[role]}
    Tokens: {prompt[tokens]}
    Date: {prompt[date]}
Response:
    Message: {response[message]}
    Role: {response[role]}
    Temperature: {response[temperature]}
    Model: {response[model]}
    Score: {response[score]}
    Tokens: {response[tokens]}
    Date: {response[date]}"""


class _BasicPresetPromptTemplate(Enum):
    """Preset basic-prompt templates."""

    PROMPT = PromptTemplate(content=BASIC_PROMPT_CONTENT, title="Basic/Prompt", custom_map={"instruction": ""})
    RESPONSE = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT,
        title="Basic/Response",
        custom_map={
            "instruction": ""})
    RESPONSE0 = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT,
        title="Basic/Response0",
        custom_map={
            "instruction": ""})
    RESPONSE1 = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT,
        title="Basic/Response1",
        custom_map={
            "instruction": ""})
    RESPONSE2 = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT,
        title="Basic/Response2",
        custom_map={
            "instruction": ""})
    RESPONSE3 = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT,
        title="Basic/Response3",
        custom_map={
            "instruction": ""})
    PROMPT_WITH_LABEL = PromptTemplate(
        content=BASIC_PROMPT_CONTENT_LABEL,
        title="Basic/Prompt With Label",
        custom_map={
            "instruction": ""})
    RESPONSE_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT_LABEL,
        title="Basic/Response With Label",
        custom_map={
            "instruction": ""})
    RESPONSE0_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT_LABEL,
        title="Basic/Response0 With Label",
        custom_map={
            "instruction": ""})
    RESPONSE1_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT_LABEL,
        title="Basic/Response1 With Label",
        custom_map={
            "instruction": ""})
    RESPONSE2_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT_LABEL,
        title="Basic/Response2 With Label",
        custom_map={
            "instruction": ""})
    RESPONSE3_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT_LABEL,
        title="Basic/Response3 With Label",
        custom_map={
            "instruction": ""})
    PROMPT_RESPONSE_STANDARD = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_STANDARD_CONTENT,
        title="Basic/Prompt-Response Standard",
        custom_map={
            "instruction": ""})
    PROMPT_RESPONSE_FULL = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_FULL_CONTENT,
        title="Basic/Prompt-Response Full",
        custom_map={
            "instruction": ""})


class _Instruction1PresetPromptTemplate(Enum):
    """Preset instruction1-prompt templates."""

    PROMPT = PromptTemplate(
        content=BASIC_PROMPT_CONTENT,
        title="Instruction1/Prompt",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT,
        title="Instruction1/Response",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE0 = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT,
        title="Instruction1/Response0",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE1 = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT,
        title="Instruction1/Response1",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE2 = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT,
        title="Instruction1/Response2",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE3 = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT,
        title="Instruction1/Response3",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    PROMPT_WITH_LABEL = PromptTemplate(
        content=BASIC_PROMPT_CONTENT_LABEL,
        title="Instruction1/Prompt With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT_LABEL,
        title="Instruction1/Response With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE0_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT_LABEL,
        title="Instruction1/Response0 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE1_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT_LABEL,
        title="Instruction1/Response1 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE2_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT_LABEL,
        title="Instruction1/Response2 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    RESPONSE3_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT_LABEL,
        title="Instruction1/Response3 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    PROMPT_RESPONSE_STANDARD = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_STANDARD_CONTENT,
        title="Instruction1/Prompt-Response Standard",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})
    PROMPT_RESPONSE_FULL = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_FULL_CONTENT,
        title="Instruction1/Prompt-Response Full",
        custom_map={
            "instruction": PROMPT_INSTRUCTION1})


class _Instruction2PresetPromptTemplate(Enum):
    """Preset instruction2-prompt templates."""

    PROMPT = PromptTemplate(
        content=BASIC_PROMPT_CONTENT,
        title="Instruction2/Prompt",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT,
        title="Instruction2/Response",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE0 = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT,
        title="Instruction2/Response0",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE1 = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT,
        title="Instruction2/Response1",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE2 = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT,
        title="Instruction2/Response2",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE3 = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT,
        title="Instruction2/Response3",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    PROMPT_WITH_LABEL = PromptTemplate(
        content=BASIC_PROMPT_CONTENT_LABEL,
        title="Instruction2/Prompt With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT_LABEL,
        title="Instruction2/Response With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE0_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT_LABEL,
        title="Instruction2/Response0 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE1_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT_LABEL,
        title="Instruction2/Response1 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE2_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT_LABEL,
        title="Instruction2/Response2 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    RESPONSE3_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT_LABEL,
        title="Instruction2/Response3 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    PROMPT_RESPONSE_STANDARD = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_STANDARD_CONTENT,
        title="Instruction2/Prompt-Response Standard",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})
    PROMPT_RESPONSE_FULL = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_FULL_CONTENT,
        title="Instruction2/Prompt-Response Full",
        custom_map={
            "instruction": PROMPT_INSTRUCTION2})


class _Instruction3PresetPromptTemplate(Enum):
    """Preset instruction3-prompt templates."""

    PROMPT = PromptTemplate(
        content=BASIC_PROMPT_CONTENT,
        title="Instruction3/Prompt",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT,
        title="Instruction3/Response",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE0 = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT,
        title="Instruction3/Response0",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE1 = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT,
        title="Instruction3/Response1",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE2 = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT,
        title="Instruction3/Response2",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE3 = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT,
        title="Instruction3/Response3",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    PROMPT_WITH_LABEL = PromptTemplate(
        content=BASIC_PROMPT_CONTENT_LABEL,
        title="Instruction3/Prompt With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE_CONTENT_LABEL,
        title="Instruction3/Response With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE0_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE0_CONTENT_LABEL,
        title="Instruction3/Response0 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE1_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE1_CONTENT_LABEL,
        title="Instruction3/Response1 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE2_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE2_CONTENT_LABEL,
        title="Instruction3/Response2 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    RESPONSE3_WITH_LABEL = PromptTemplate(
        content=BASIC_RESPONSE3_CONTENT_LABEL,
        title="Instruction3/Response3 With Label",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    PROMPT_RESPONSE_STANDARD = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_STANDARD_CONTENT,
        title="Instruction3/Prompt-Response Standard",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})
    PROMPT_RESPONSE_FULL = PromptTemplate(
        content=BASIC_PROMPT_RESPONSE_FULL_CONTENT,
        title="Instruction3/Prompt-Response Full",
        custom_map={
            "instruction": PROMPT_INSTRUCTION3})


class PresetPromptTemplate:
    """Preset prompt templates."""

    BASIC = _BasicPresetPromptTemplate
    INSTRUCTION1 = _Instruction1PresetPromptTemplate
    INSTRUCTION2 = _Instruction2PresetPromptTemplate
    INSTRUCTION3 = _Instruction3PresetPromptTemplate
    DEFAULT = BASIC.PROMPT
