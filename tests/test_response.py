import datetime
from memor import Response, Role

TEST_CASE_NAME = "Response tests"


def test_response_message1():
    response = Response(message="I am fine.")
    assert response.message == "I am fine."


def test_response_message2():
    response = Response(message="I am fine.")
    response.update_message("OK!")
    assert response.message == "OK!"


def test_response_score1():
    response = Response(message="I am fine.", score=0.9)
    assert response.score == 0.9


def test_response_score2():
    response = Response(message="I am fine.", score=0.9)
    response.update_score(0.5)
    assert response.score == 0.5


def test_response_role1():
    response = Response(message="I am fine.", role=Role.ASSISTANT)
    assert response.role == Role.ASSISTANT


def test_response_role2():
    response = Response(message="I am fine.", role=Role.ASSISTANT)
    response.update_role(Role.USER)
    assert response.role == Role.USER


def test_response_temperature1():
    response = Response(message="I am fine.", temperature=0.2)
    assert response.temperature == 0.2


def test_response_temperature2():
    response = Response(message="I am fine.", temperature=0.2)
    response.update_temperature(0.7)
    assert response.temperature == 0.7


def test_response_model1():
    response = Response(message="I am fine.", model="GPT-4")
    assert response.model == "GPT-4"


def test_response_model2():
    response = Response(message="I am fine.", model="GPT-4")
    response.update_model("GPT-4o")
    assert response.model == "GPT-4o"


def test_response_date():
    date_time_utc = datetime.datetime.now(datetime.timezone.utc)
    response = Response(message="I am fine.", date=date_time_utc)
    assert response.date_created == date_time_utc


