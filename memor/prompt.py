# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
import json
from .params import PromptRenderFormat
from .template import DEFAULT_TEMPLATE


class Role(enum.Enum):
    """Role enum."""
    
    SYSTEM = 0
    USER = 1
    ASSISTANT = 2

    DEFAULT = USER


class Prompt:
    """Prompt class."""

    def __init__(
            self,
            message,
            responses=[],
            role=Role.DEFAULT,
            temperature=None,
            model=None,
            template=DEFAULT_TEMPLATE,
            date=datetime.datetime.now()):
        """Prompt object initiator."""
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

    def get_message(self):
        """Get the prompt message."""
        return self.message

    def to_json(self):
        """Convert the prompt to a JSON object."""
        data = {
            "message": self.message,
            "responses": self.responses,
            "role": str(self.role),
            "temperature": self.temperature,
            "model": self.model,
            "date": str(self.date)
        }
        return json.dumps(data, indent=4)

    def render(self, render_format=PromptRenderFormat.OpenAI):
        """
        Render method.

        :param render_format: render format
        :type render_format: PromptRenderFormat object
        :return: rendered prompt
        """
        if format == PromptRenderFormat.OpenAI:
            return [{"role": self.role, "content": self.template.format(message=self.message)}]


