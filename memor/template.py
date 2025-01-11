# -*- coding: utf-8 -*-
"""Template class."""
import json
import datetime
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_TEMPLATE_FILE_MESSAGE
from .params import MEMOR_VERSION
from .errors import MemorValidationError
from .functions import get_time_utc
from .functions import validate_path
from .functions import validate_template_content, validate_template_title


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
        self._date_created = get_time_utc
        self._date_modified = get_time_utc()
        self._memor_version = memor_version
        if file_path:
            self.load(file_path)
        if title:
            self.update_title(title)
        if content:
            self.update_content(content)

    def __str__(self):
        return self._content

    def update_title(self, title):
        validate_template_title(title)
        self._title = title
        self._date_modified = get_time_utc()

    def update_content(self, content):
        validate_template_content(content)
        self._content = content
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
        :return: result as dict
        """
        validate_path(file_path)
        with open(file_path, "r") as file:
            try:
                loaded_obj = json.loads(file.read())
                self._content = loaded_obj["content"]
                self._title = loaded_obj["title"]
                self._memor_version = loaded_obj["memor_version"]
                self._date_created = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            except Exception:
                raise MemorValidationError(INVALID_TEMPLATE_FILE_MESSAGE)

    def to_json(self):
        """Convert to json."""
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        "Convert to dict."
        return {
            "title": self._title,
            "content": self._content,
            "memor_version": MEMOR_VERSION,
            "date_created": datetime.datetime.strftime(self._date_created, DATE_TIME_FORMAT),
            "date_modified": datetime.datetime.strftime(self._date_modified, DATE_TIME_FORMAT),
        }

    @property
    def content(self):
        return self._content

    @property
    def title(self):
        return self._title

    @property
    def date_created(self):
        return self._date_created

    @property
    def date_modified(self):
        return self._date_modified


DEFAULT_TEMPLATE_CONTENT = "{message}"
DEFAULT_TEMPLATE = CustomPromptTemplate(content=DEFAULT_TEMPLATE_CONTENT)
