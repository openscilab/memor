# -*- coding: utf-8 -*-
"""Prompt class."""
import enum
import datetime
from .functions import _load_prompt_from_response_obj

class Role(enum.Enum):
    """Role enum."""
    SYSTEM = 0
    USER = 1
    ASSISTANT = 2

    DEFAULT = SYSTEM


class Prompt:
    """Prompt class."""

    def __init__(
            self,
            message,
            responses=[],
            role=Role.DEFAULT,
            temperature=None,
            model=None,
            date=datetime.datetime.now(),
            response_obj=None):
        """Prompt object initiator."""
        if response_obj is not None:
            from_response = _load_prompt_from_response_obj(response_obj)
            responses = from_response["responses"]
            role = from_response["role"]
            model = from_response["model"]
        self.message = message
        self.responses = responses
        self.role = role
        self.temperature = temperature
        self.model = model
        self.date = date
    
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
        return {
            "message": self.message,
            "responses": self.responses,
            "role": self.role,
            "temperature": self.temperature,
            "model": self.model,
            "date": self.date
        }
