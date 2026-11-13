# -*- coding: utf-8 -*-
"""Reasoning class."""
from typing import List, Dict, Union, Any, Optional
import json
from .params import INVALID_REASONING_STRUCTURE_MESSAGE
from .errors import MemorValidationError
from .functions import _validate_string, _validate_list_of


class ReasoningSegment:
    """
    Reasoning segment class.

    >>> from memor import ReasoningSegment
    >>> segment = ReasoningSegment(text="Let me think.")
    >>> segment.text
    'Let me think.'
    """

    def __init__(self, text: str = "") -> None:
        """
        Reasoning segment object initiator.

        :param text: segment text
        """
        self._text = ""
        self.update_text(text)

    def __eq__(self, other_segment: "ReasoningSegment") -> bool:
        """
        Check reasoning segments equality.

        :param other_segment: another reasoning segment
        """
        if isinstance(other_segment, ReasoningSegment):
            return self._text == other_segment._text
        return False

    def __repr__(self) -> str:
        """Return string representation of ReasoningSegment."""
        return "ReasoningSegment(text={text})".format(text=self._text)

    def update_text(self, text: str) -> None:
        """
        Update the segment text.

        :param text: segment text
        """
        _validate_string(text, "text")
        self._text = text

    def to_dict(self) -> Dict[str, Any]:
        """Convert the reasoning segment to a dictionary."""
        return {
            "type": "ReasoningSegment",
            "text": self._text,
        }

    def to_json(self) -> Dict[str, Any]:
        """Convert the reasoning segment to a JSON object."""
        return self.to_dict()

    @property
    def text(self) -> str:
        """Get the segment text."""
        return self._text


class Reasoning:
    r"""
    Reasoning class.

    >>> from memor import Reasoning, ReasoningSegment
    >>> reasoning = Reasoning(segments=[ReasoningSegment(text="Step 1."), ReasoningSegment(text="Step 2.")])
    >>> reasoning.text
    'Step 1.\nStep 2.'
    """

    def __init__(self, segments: Optional[List[ReasoningSegment]] = None) -> None:
        """
        Reasoning object initiator.

        :param segments: reasoning segments
        """
        self._segments = []
        if segments is not None:
            self.update_segments(segments)

    def __eq__(self, other_reasoning: "Reasoning") -> bool:
        """
        Check reasoning equality.

        :param other_reasoning: another reasoning
        """
        if isinstance(other_reasoning, Reasoning):
            return self._segments == other_reasoning._segments
        return False

    def __str__(self) -> str:
        """Return string representation of Reasoning."""
        return self.text

    def __repr__(self) -> str:
        """Return string representation of Reasoning."""
        return "Reasoning(text={text})".format(text=self.text)

    def update_segments(self, segments: List[ReasoningSegment]) -> None:
        """
        Update the reasoning segments.

        :param segments: reasoning segments
        """
        _validate_list_of(segments, "segments", ReasoningSegment, "`ReasoningSegment`")
        self._segments = list(segments)

    def add_segment(self, segment: ReasoningSegment) -> None:
        """
        Add a segment to the reasoning.

        :param segment: reasoning segment
        """
        _validate_list_of([segment], "segment", ReasoningSegment, "`ReasoningSegment`")
        self._segments.append(segment)

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        try:
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            segments = []
            for segment in loaded_obj["segments"]:
                segments.append(ReasoningSegment(text=segment["text"]))
        except Exception:
            raise MemorValidationError(INVALID_REASONING_STRUCTURE_MESSAGE)
        self._segments = segments

    def to_dict(self) -> Dict[str, Any]:
        """Convert the reasoning to a dictionary."""
        return {
            "type": "Reasoning",
            "segments": [segment.to_dict() for segment in self._segments],
        }

    def to_json(self) -> Dict[str, Any]:
        """Convert the reasoning to a JSON object."""
        return self.to_dict()

    @property
    def segments(self) -> List[ReasoningSegment]:
        """Get the reasoning segments."""
        return self._segments

    @property
    def text(self) -> str:
        """Get the full reasoning text."""
        return "\n".join(segment.text for segment in self._segments)
