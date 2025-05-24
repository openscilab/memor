import os
import datetime
import uuid
import json
import copy
import pytest
from memor import Response, Role, LLMModel, MemorValidationError
from memor import RenderFormat
from memor import TokensEstimator

TEST_CASE_NAME = "Response tests"


def test_message1():
    response = Response(message="I am fine.")
    assert response.message == "I am fine."


def test_message2():
    response = Response(message="I am fine.")
    response.update_message("OK!")
    assert response.message == "OK!"


def test_message3():
    response = Response(message="I am fine.")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `message` must be a string."):
        response.update_message(22)


def test_tokens1():
    response = Response(message="I am fine.")
    assert response.tokens is None


def test_tokens2():
    response = Response(message="I am fine.", tokens=4)
    assert response.tokens == 4


def test_tokens3():
    response = Response(message="I am fine.", tokens=4)
    response.update_tokens(6)
    assert response.tokens == 6


def test_estimated_tokens1():
    response = Response(message="I am fine.")
    assert response.estimate_tokens(TokensEstimator.UNIVERSAL) == 5


def test_estimated_tokens2():
    response = Response(message="I am fine.")
    assert response.estimate_tokens(TokensEstimator.OPENAI_GPT_3_5) == 4


def test_estimated_tokens3():
    response = Response(message="I am fine.")
    assert response.estimate_tokens(TokensEstimator.OPENAI_GPT_4) == 4


def test_tokens4():
    response = Response(message="I am fine.", tokens=4)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `tokens` must be a positive integer."):
        response.update_tokens(-2)


def test_inference_time1():
    response = Response(message="I am fine.")
    assert response.inference_time is None


def test_inference_time2():
    response = Response(message="I am fine.", inference_time=8.2)
    assert response.inference_time == 8.2


def test_inference_time3():
    response = Response(message="I am fine.", inference_time=8.2)
    response.update_inference_time(9.5)
    assert response.inference_time == 9.5


def test_inference_time4():
    response = Response(message="I am fine.", inference_time=8.2)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `inference_time` must be a positive float."):
        response.update_inference_time(-5)


def test_score1():
    response = Response(message="I am fine.", score=0.9)
    assert response.score == 0.9


def test_score2():
    response = Response(message="I am fine.", score=0.9)
    response.update_score(0.5)
    assert response.score == 0.5


def test_score3():
    response = Response(message="I am fine.", score=0.9)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `score` must be a value between 0 and 1."):
        response.update_score(-2)


def test_role1():
    response = Response(message="I am fine.", role=Role.ASSISTANT)
    assert response.role == Role.ASSISTANT


def test_role2():
    response = Response(message="I am fine.", role=Role.ASSISTANT)
    response.update_role(Role.USER)
    assert response.role == Role.USER


def test_role3():
    response = Response(message="I am fine.", role=None)
    assert response.role == Role.ASSISTANT


def test_role4():
    response = Response(message="I am fine.", role=Role.ASSISTANT)
    with pytest.raises(MemorValidationError, match=r"Invalid role. It must be an instance of Role enum."):
        response.update_role(2)


def test_temperature1():
    response = Response(message="I am fine.", temperature=0.2)
    assert response.temperature == 0.2


def test_temperature2():
    response = Response(message="I am fine.", temperature=0.2)
    response.update_temperature(0.7)
    assert response.temperature == 0.7


def test_temperature3():
    response = Response(message="I am fine.", temperature=0.2)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `temperature` must be a positive float."):
        response.update_temperature(-22)


def test_model1():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    assert response.model == LLMModel.GPT_4.value


def test_model2():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    response.update_model(LLMModel.GPT_4O)
    assert response.model == LLMModel.GPT_4O.value


def test_model3():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    response.update_model("my-trained-llm-instruct")
    assert response.model == "my-trained-llm-instruct"


def test_model4():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    with pytest.raises(MemorValidationError, match=r"Invalid model. It must be an instance of LLMModel enum."):
        response.update_model(4)


def test_id1():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    assert uuid.UUID(response.id, version=4) == uuid.UUID(response._id, version=4)


def test_id2():
    response = Response(message="I am fine.", model=LLMModel.GPT_4)
    response._id = "123"
    _ = response.save("response_test3.json")
    with pytest.raises(MemorValidationError, match=r"Invalid message ID. It must be a valid UUIDv4."):
        _ = Response(file_path="response_test3.json")


def test_date1():
    date_time_utc = datetime.datetime.now(datetime.timezone.utc)
    response = Response(message="I am fine.", date=date_time_utc)
    assert response.date_created == date_time_utc


def test_date2():
    response = Response(message="I am fine.", date=None)
    assert isinstance(response.date_created, datetime.datetime)


def test_date3():
    with pytest.raises(MemorValidationError, match=r"Invalid value. `date` must be a datetime object that includes timezone information."):
        _ = Response(message="I am fine.", date="2/25/2025")


def test_date4():
    with pytest.raises(MemorValidationError, match=r"Invalid value. `date` must be a datetime object that includes timezone information."):
        _ = Response(message="I am fine.", date=datetime.datetime.now())


def test_json1():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response1_json = response1.to_json()
    response2 = Response()
    response2.from_json(response1_json)
    assert response1 == response2


def test_json2():
    response = Response()
    with pytest.raises(MemorValidationError, match=r"Invalid response structure. It should be a JSON object with proper fields."):
        # an corrupted JSON string without `message` field
        response.from_json(r"""{
                           "type": "Response",
                           "score": 0.8,
                           "temperature": 0.5,
                           "tokens": null,
                           "inference_time": null,
                           "role": "user",
                           "model": "gpt-4",
                           "id": "7dfce0e0-53bc-4500-bf79-7c9cd705087c",
                           "memor_version": "0.6",
                           "date_created": "2025-05-07 21:54:48 +0000",
                           "date_modified": "2025-05-07 21:54:48 +0000"}""")
    assert response.message == ''
    assert response.model == 'unknown'
    assert response.temperature is None
    assert response.role == Role.ASSISTANT
    assert response.score is None
    assert response.inference_time is None
    assert response.tokens is None


def test_json3():
    response = Response()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `score` must be a value between 0 and 1."):
        # an corrupted JSON string with invalid `score` field
        response.from_json(r"""{
                           "message": "I am fine.",
                           "type": "Response",
                           "score": "invalid",
                           "temperature": 0.5,
                           "tokens": null,
                           "inference_time": null,
                           "role": "user",
                           "model": "gpt-4",
                           "id": "7dfce0e0-53bc-4500-bf79-7c9cd705087c",
                           "memor_version": "0.6",
                           "date_created": "2025-05-07 21:54:48 +0000",
                           "date_modified": "2025-05-07 21:54:48 +0000"}""")
    assert response.message == ''
    assert response.model == 'unknown'
    assert response.temperature is None
    assert response.role == Role.ASSISTANT
    assert response.score is None
    assert response.inference_time is None
    assert response.tokens is None


def test_json4():
    response = Response()
    with pytest.raises(MemorValidationError, match="Invalid value. `temperature` must be a positive float."):
        response.from_json(r"""{
                           "message": "I am fine.",
                           "type": "Response",
                           "score": 0.8,
                           "temperature": -0.5,
                           "tokens": null,
                           "inference_time": null,
                           "role": "user",
                           "model": "gpt-4",
                           "id": "7dfce0e0-53bc-4500-bf79-7c9cd705087c",
                           "memor_version": "0.6",
                           "date_created": "2025-05-07 21:54:48 +0000",
                           "date_modified": "2025-05-07 21:54:48 +0000"}""")
    assert response.message == ''
    assert response.model == 'unknown'
    assert response.temperature is None


def test_json5():
    response = Response()
    with pytest.raises(MemorValidationError, match="Invalid value. `tokens` must be a positive int."):
        response.from_json(r"""{
                           "message": "I am fine.",
                           "type": "Response",
                           "score": 0.8,
                           "temperature": 0.5,
                           "tokens": -1,
                           "inference_time": null,
                           "role": "user",
                           "model": "gpt-4",
                           "id": "7dfce0e0-53bc-4500-bf79-7c9cd705087c",
                           "memor_version": "0.6",
                           "date_created": "2025-05-07 21:54:48 +0000",
                           "date_modified": "2025-05-07 21:54:48 +0000"}""")
    assert response.message == ''
    assert response.model == 'unknown'
    assert response.temperature is None
    assert response.tokens is None


def test_json6():
    response = Response()
    with pytest.raises(MemorValidationError, match="Invalid value. `inference_time` must be a positive float."):
        response.from_json(r"""{
                           "message": "I am fine.",
                           "type": "Response",
                           "score": 0.8,
                           "temperature": 0.5,
                           "tokens": null,
                           "inference_time": -1,
                           "role": "user",
                           "model": "gpt-4",
                           "id": "7dfce0e0-53bc-4500-bf79-7c9cd705087c",
                           "memor_version": "0.6",
                           "date_created": "2025-05-07 21:54:48 +0000",
                           "date_modified": "2025-05-07 21:54:48 +0000"}""")
    assert response.message == ''
    assert response.model == 'unknown'
    assert response.temperature is None
    assert response.tokens is None
    assert response.inference_time is None


def test_save1():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    result = response.save("response_test1.json")
    with open("response_test1.json", "r") as file:
        saved_response = json.loads(file.read())
    assert result["status"] and response.to_json() == saved_response


def test_save2():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    result = response.save("f:/")
    assert result["status"] == False


def test_load1():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    result = response1.save("response_test2.json")
    response2 = Response(file_path="response_test2.json")
    assert result["status"] and response1 == response2


def test_load2():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: 2"):
        response = Response(file_path=2)


def test_load3():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: response_test10.json"):
        response = Response(file_path="response_test10.json")


def test_copy1():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response2 = copy.copy(response1)
    assert id(response1) != id(response2) and response1.id != response2.id


def test_copy2():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response2 = response1.copy()
    assert id(response1) != id(response2) and response1.id != response2.id


def test_str():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert str(response) == response.message


def test_repr():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert repr(response) == "Response(message={message})".format(message=response.message)


def test_render1():
    response = Response(message="I am fine.")
    assert response.render() == "I am fine."


def test_render2():
    response = Response(message="I am fine.")
    assert response.render(RenderFormat.OPENAI) == {"role": "assistant", "content": "I am fine."}


def test_render3():
    response = Response(message="I am fine.")
    assert response.render(RenderFormat.DICTIONARY) == response.to_dict()


def test_render4():
    response = Response(message="I am fine.")
    assert response.render(RenderFormat.ITEMS) == response.to_dict().items()


def test_render5():
    response = Response(message="I am fine.")
    with pytest.raises(MemorValidationError, match=r"Invalid render format. It must be an instance of RenderFormat enum."):
        response.render("OPENAI")


def test_render6():
    response = Response(message="I am fine.")
    assert response.render(RenderFormat.AI_STUDIO) == {'role': 'assistant', 'parts': [{'text': 'I am fine.'}]}


def test_render7():
    response = Response(message="I am fine.", role=Role.SYSTEM)
    with pytest.warns(UserWarning, match="Google AI Studio models may not support content with a system role."):
        _ = response.render(RenderFormat.AI_STUDIO)


def test_equality1():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response2 = response1.copy()
    assert response1 == response2


def test_equality2():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.6)
    assert response1 != response2


def test_equality3():
    response1 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert response1 == response2


def test_equality4():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert response != 2


def test_length1():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert len(response) == 10


def test_length2():
    response = Response()
    assert len(response) == 0


def test_date_modified():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert isinstance(response.date_modified, datetime.datetime)


def test_date_created():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    assert isinstance(response.date_created, datetime.datetime)


def test_size():
    response = Response(message="I am fine.", model=LLMModel.GPT_4, temperature=0.5, role=Role.USER, score=0.8)
    response.save("response_test3.json")

    assert os.path.getsize("response_test3.json") == response.size
    assert response.size == response.get_size()
