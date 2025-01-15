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


class PresetPromptTemplate(Enum):
    """Preset prompt template enum."""

    # With Instruction
    IMESSAGE = CustomPromptTemplate(
        content="### Instruction: This is a message prompt loaded for memory initialization.\n{message}",
        title="IMessage"
    )
    IRESPONSE = CustomPromptTemplate(
        content="### Instruction: This is a response prompt loaded for memory initialization.\n{response_0}",
        title="IResponse"
    )
    IMR = CustomPromptTemplate(
        content="### Instruction: This is a message and response prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}",
        title="IMR")
    IMRM = CustomPromptTemplate(
        content="### Instruction: This is a message, response, and model prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}",
        title="IMRM"
    )
    IMRMT = CustomPromptTemplate(
        content="### Instruction: This is a message, response, model, and temperature prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}",
        title="IMRMT"
    )
    IMRD = CustomPromptTemplate(
        content="### Instruction: This is a message, response, and date prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nDate: {date}",
        title="IMRD")
    IMRMD = CustomPromptTemplate(
        content="### Instruction: This is a message, response, model, and date prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nDate: {date}",
        title="IMRMD"
    )
    IMRMTD = CustomPromptTemplate(
        content="### Instruction: This is a message, response, model, temperature, and date prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}",
        title="IMRMTD"
    )
    IMRMTR = CustomPromptTemplate(
        content="### Instruction: This is a message, response, model, temperature, and role prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nRole: {role}",
        title="IMRMTR"
    )
    IMRMTDR = CustomPromptTemplate(
        content="### Instruction: This is a message, response, model, temperature, date, and role prompt loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}\nRole: {role}",
        title="IMRMTDR"
    )
    IMT = CustomPromptTemplate(
        content="### Instruction: This is a message and temperature prompt loaded for memory initialization.\nMessage: {message}\nTemperature: {temperature}",
        title="IMT")
    IRT = CustomPromptTemplate(
        content="### Instruction: This is a response and temperature prompt loaded for memory initialization.\nResponse: {response_0}\nTemperature: {temperature}",
        title="IRT")
    IMDR = CustomPromptTemplate(
        content="### Instruction: This is a message, date, and role prompt loaded for memory initialization.\nMessage: {message}\nDate: {date}\nRole: {role}",
        title="IMDR")
    IALL = CustomPromptTemplate(
        content="### Instruction: This is a complete prompt with all parameters loaded for memory initialization.\nMessage: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}\nRole: {role}",
        title="IALL"
    )

    # Without Instruction
    MESSAGE = CustomPromptTemplate(
        content="{message}",
        title="Message"
    )
    RESPONSE = CustomPromptTemplate(
        content="{response_0}",
        title="Response"
    )
    MR = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}",
        title="MR"
    )
    MRM = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}",
        title="MRM"
    )
    MRMT = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}",
        title="MRMT"
    )
    MRD = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nDate: {date}",
        title="MRD"
    )
    MRMD = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nDate: {date}",
        title="MRMD"
    )
    MRMTD = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}",
        title="MRMTD"
    )
    MRMTR = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nRole: {role}",
        title="MRMTR"
    )
    MRMTDR = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}\nRole: {role}",
        title="MRMTDR")
    MT = CustomPromptTemplate(
        content="Message: {message}\nTemperature: {temperature}",
        title="MT"
    )
    RT = CustomPromptTemplate(
        content="Response: {response_0}\nTemperature: {temperature}",
        title="RT"
    )
    MDR = CustomPromptTemplate(
        content="Message: {message}\nDate: {date}\nRole: {role}",
        title="MDR"
    )
    ALL = CustomPromptTemplate(
        content="Message: {message}\nResponse: {response_0}\nModel: {model}\nTemperature: {temperature}\nDate: {date}\nRole: {role}",
        title="ALL")
