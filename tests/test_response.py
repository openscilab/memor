import datetime
import json
import copy
import pytest
from memor import Response, Role, MemorValidationError
from memor import RenderFormat

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


def test_tokens4():
    response = Response(message="I am fine.", tokens=4)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `tokens` must be a positive integer."):
        response.update_tokens(-2)


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
    response = Response(message="I am fine.", model="GPT-4")
    assert response.model == "GPT-4"


def test_model2():
    response = Response(message="I am fine.", model="GPT-4")
    response.update_model("GPT-4o")
    assert response.model == "GPT-4o"


def test_model3():
    response = Response(message="I am fine.", model="GPT-4")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `model` must be a string."):
        response.update_model(4)


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
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response1_json = response1.to_json()
    response2 = Response()
    response2.from_json(response1_json)
    assert response1 == response2


def test_json2():
    response = Response()
    with pytest.raises(MemorValidationError, match=r"Invalid response structure. It should be a JSON object with proper fields."):
        response.from_json("{}")


def test_save1():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    result = response.save("response_test1.json")
    with open("response_test1.json", "r") as file:
        saved_response = json.loads(file.read())
    assert result["status"] and response.to_json() == saved_response


def test_save2():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    result = response.save("f:/")
    assert result["status"] == False


def test_load1():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    result = response1.save("response_test2.json")
    response2 = Response(file_path="response_test2.json")
    assert result["status"] and response1 == response2


def test_load2():
    with pytest.raises(MemorValidationError, match=r"Invalid path. Path must be a string."):
        response = Response(file_path=2)


def test_load3():
    with pytest.raises(FileNotFoundError, match=r"Path response_test10.json does not exist."):
        response = Response(file_path="response_test10.json")


def test_copy1():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = copy.copy(response1)
    assert id(response1) != id(response2)


def test_copy2():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = response1.copy()
    assert id(response1) != id(response2)


def test_str():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    assert str(response) == response.message


def test_repr():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
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


def test_equality1():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = response1.copy()
    assert response1 == response2


def test_equality2():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.6)
    assert response1 != response2


def test_equality3():
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    assert response1 == response2


def test_equality4():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    assert response != 2


def test_date_modified():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    assert isinstance(response.date_modified, datetime.datetime)


def test_date_created():
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    assert isinstance(response.date_created, datetime.datetime)
