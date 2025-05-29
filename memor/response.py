# -*- coding: utf-8 -*-
"""Response class."""
from typing import List, Dict, Union, Tuple, Any
import datetime
import json
import warnings
from .message import Message
from .params import MEMOR_VERSION
from .params import DATE_TIME_FORMAT
from .params import DATA_SAVE_SUCCESS_MESSAGE
from .params import INVALID_RESPONSE_STRUCTURE_MESSAGE
from .params import INVALID_ROLE_MESSAGE, INVALID_RENDER_FORMAT_MESSAGE, INVALID_MODEL_MESSAGE
from .params import AI_STUDIO_SYSTEM_WARNING
from .params import Role, RenderFormat, LLMModel
from .tokens_estimator import TokensEstimator
from .errors import MemorValidationError
from .functions import get_time_utc, generate_message_id
from .functions import _validate_string, _validate_pos_float, _validate_pos_int, _validate_message_id
from .functions import _validate_date_time, _validate_probability, _validate_path


class Response(Message):
    """
    Response class.

    >>> from memor import Response, Role
    >>> response = Response(message="Hello!", score=0.9, role=Role.ASSISTANT, temperature=0.5, model=LLMModel.GPT_4)
    >>> response.message
    'Hello!'
    """

    def __init__(
            self,
            message: str = "",
            score: float = None,
            role: Role = Role.ASSISTANT,
            temperature: float = None,
            tokens: int = None,
            inference_time: float = None,
            model: Union[LLMModel, str] = LLMModel.DEFAULT,
            date: datetime.datetime = get_time_utc(),
            file_path: str = None) -> None:
        """
        Response object initiator.

        :param message: response message
        :param score: response score
        :param role: response role
        :param temperature: temperature
        :param tokens: tokens
        :param inference_time: inference time
        :param model: agent model
        :param date: response date
        :param file_path: response file path
        """
        super().__init__()
        self._score = None
        self._role = Role.ASSISTANT
        self._temperature = None
        self._inference_time = None
        self._model = LLMModel.DEFAULT.value
        if file_path:
            self.load(file_path)
        else:
            if message:
                self.update_message(message)
            if score:
                self.update_score(score)
            if role:
                self.update_role(role)
            if model:
                self.update_model(model)
            if temperature:
                self.update_temperature(temperature)
            if tokens:
                self.update_tokens(tokens)
            if inference_time:
                self.update_inference_time(inference_time)
            if date:
                _validate_date_time(date, "date")
                self._date_created = date
            self._id = generate_message_id()
        _validate_message_id(self._id)

    def __eq__(self, other_response: "Response") -> bool:
        """
        Check responses equality.

        :param other_response: another response
        """
        if isinstance(other_response, Response):
            return self._message == other_response._message and self._score == other_response._score and self._role == other_response._role and self._temperature == other_response._temperature and \
                self._model == other_response._model and self._tokens == other_response._tokens and self._inference_time == other_response._inference_time
        return False

    def __repr__(self) -> str:
        """Return string representation of Response."""
        return "Response(message={message})".format(message=self._message)

    def update_score(self, score: float) -> None:
        """
        Update the response score.

        :param score: score
        """
        _validate_probability(score, "score")
        self._score = score
        self._mark_modified()

    def update_temperature(self, temperature: float) -> None:
        """
        Update the temperature.

        :param temperature: temperature
        """
        _validate_pos_float(temperature, "temperature")
        self._temperature = temperature
        self._mark_modified()

    def update_inference_time(self, inference_time: float) -> None:
        """
        Update inference time.

        :param inference_time: inference time
        """
        _validate_pos_float(inference_time, "inference_time")
        self._inference_time = inference_time
        self._mark_modified()

    def update_model(self, model: Union[LLMModel, str]) -> None:
        """
        Update the agent model.

        :param model: model
        """
        if isinstance(model, str):
            self._model = model
        elif isinstance(model, LLMModel):
            self._model = model.value
        else:
            raise MemorValidationError(INVALID_MODEL_MESSAGE)
        self._mark_modified()

    def save(self, file_path: str) -> Dict[str, Any]:
        """
        Save method.

        :param file_path: response file path
        """
        result = {"status": True, "message": DATA_SAVE_SUCCESS_MESSAGE}
        try:
            with open(file_path, "w") as file:
                json.dump(self.to_json(), file)
        except Exception as e:
            result["status"] = False
            result["message"] = str(e)
        return result

    @staticmethod
    def _validate_extract_json(json_object: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate and extract JSON object.

        :param json_object: JSON object
        """
        try:
            result = dict()
            if isinstance(json_object, str):
                loaded_obj = json.loads(json_object)
            else:
                loaded_obj = json_object.copy()
            result["message"] = loaded_obj["message"]
            result["score"] = loaded_obj["score"]
            result["temperature"] = loaded_obj["temperature"]
            result["tokens"] = loaded_obj.get("tokens", None)
            result["inference_time"] = loaded_obj.get("inference_time", None)
            result["model"] = loaded_obj["model"]
            result["role"] = Role(loaded_obj["role"])
            result["memor_version"] = loaded_obj["memor_version"]
            result["id"] = loaded_obj.get("id", generate_message_id())
            result["date_created"] = datetime.datetime.strptime(loaded_obj["date_created"], DATE_TIME_FORMAT)
            result["date_modified"] = datetime.datetime.strptime(loaded_obj["date_modified"], DATE_TIME_FORMAT)
        except Exception:
            raise MemorValidationError(INVALID_RESPONSE_STRUCTURE_MESSAGE)
        _validate_string(result["message"], "message")
        if result["score"] is not None:
            _validate_probability(result["score"], "score")
        if result["temperature"] is not None:
            _validate_pos_float(result["temperature"], "temperature")
        if result["tokens"] is not None:
            _validate_pos_int(result["tokens"], "tokens")
        if result["inference_time"] is not None:
            _validate_pos_float(result["inference_time"], "inference_time")
        _validate_string(result["model"], "model")
        _validate_message_id(result["id"])
        _validate_string(result["memor_version"], "memor_version")
        return result

    def from_json(self, json_object: Union[str, Dict[str, Any]]) -> None:
        """
        Load attributes from the JSON object.

        :param json_object: JSON object
        """
        data = self._validate_extract_json(json_object)
        self._message = data["message"]
        self._score = data["score"]
        self._temperature = data["temperature"]
        self._tokens = data["tokens"]
        self._inference_time = data["inference_time"]
        self._model = data["model"]
        self._role = data["role"]
        self._memor_version = data["memor_version"]
        self._id = data["id"]
        self._date_created = data["date_created"]
        self._date_modified = data["date_modified"]

    def to_json(self) -> Dict[str, Any]:
        """Convert the response to a JSON object."""
        data = self.to_dict().copy()
        data["date_created"] = datetime.datetime.strftime(data["date_created"], DATE_TIME_FORMAT)
        data["date_modified"] = datetime.datetime.strftime(data["date_modified"], DATE_TIME_FORMAT)
        data["role"] = data["role"].value
        return data

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        return {
            "type": "Response",
            "message": self._message,
            "score": self._score,
            "temperature": self._temperature,
            "tokens": self._tokens,
            "inference_time": self._inference_time,
            "role": self._role,
            "model": self._model,
            "id": self._id,
            "memor_version": MEMOR_VERSION,
            "date_created": self._date_created,
            "date_modified": self._date_modified,
        }

    def render(self,
               render_format: RenderFormat = RenderFormat.DEFAULT) -> Union[str,
                                                                            Dict[str, Any],
                                                                            List[Tuple[str, Any]]]:
        """
        Render the response.

        :param render_format: render format
        """
        if not isinstance(render_format, RenderFormat):
            raise MemorValidationError(INVALID_RENDER_FORMAT_MESSAGE)
        if render_format == RenderFormat.STRING:
            return self._message
        elif render_format == RenderFormat.OPENAI:
            return {"role": self._role.value,
                    "content": self._message}
        elif render_format == RenderFormat.AI_STUDIO:
            if self._role == Role.SYSTEM:
                warnings.warn(AI_STUDIO_SYSTEM_WARNING, UserWarning)
            return {"role": self._role.value,
                    "parts": [{"text": self._message}]}
        elif render_format == RenderFormat.DICTIONARY:
            return self.to_dict()
        elif render_format == RenderFormat.ITEMS:
            return self.to_dict().items()
        return self._message

    @property
    def score(self) -> float:
        """Get the response score."""
        return self._score

    @property
    def temperature(self) -> float:
        """Get the temperature."""
        return self._temperature

    @property
    def inference_time(self) -> float:
        """Get inference time."""
        return self._inference_time

    @property
    def model(self) -> str:
        """Get the agent model."""
        return self._model
