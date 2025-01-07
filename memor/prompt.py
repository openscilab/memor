# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
import json
from .params import PromptRenderFormat, DATA_SAVE_SUCCESS_MESSAGE
from .template import DEFAULT_TEMPLATE


class Role(enum.Enum):
    """Role enum."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DEFAULT = USER


class Prompt:
    """Prompt class."""

    def __init__(
            self,
            message=None,
            responses=[],
            role=Role.DEFAULT,
            temperature=None,
            model=None,
            template=DEFAULT_TEMPLATE,
            date=datetime.datetime.now(),
            file_path=None):
        """Prompt object initiator."""
        if file_path:
            with open(file_path, "r") as file:
                loaded_obj = json.loads(file.read())
                message = loaded_obj["message"]
                responses = loaded_obj["responses"]
                role = Role(loaded_obj["role"])
                temperature = loaded_obj["temperature"]
                model = loaded_obj["model"]
                date = datetime.datetime.strptime(loaded_obj["date"], "%Y-%m-%d %H:%M:%S.%f")
        self.message = message
        self.responses = responses
        self.role = role
        self.temperature = temperature
        self.model = model
        self.date = date
        self.template = template

    def add_response(self, response, index=None):
        """Add a response to the prompt object."""
        if index is None:
            self.responses.append(response)
        else:
            self.responses.insert(index, response)

    def remove_response(self, index):
        """Remove a response from the prompt object."""
        self.responses.pop(index)

    def update_message(self, message):
        """Update the prompt message."""
        self.message = message

    def update_role(self, role):
        self.role = role

    def update_temperature(self, temperature):
        self.temperature = temperature

    def get_message(self):
        """Get the prompt message."""
        return self.message
    
    def save(self, file_path):
        """
        Save method.

        :param file_path: prompt file path
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
        """Convert the prompt to a JSON object."""
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """Convert the prompt to a dictionary."""
        return {
            "message": self.message,
            "responses": self.responses,
            "role": str(self.role),
            "temperature": self.temperature,
            "model": self.model,
            "date": str(self.date)
        }

    def render(self, render_format=PromptRenderFormat.OpenAI):
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered prompt
        """
        if render_format == PromptRenderFormat.OpenAI:
            return [
                {"role": self.role.value,
                 "content": self.template._content.format(message=self.message)}]
