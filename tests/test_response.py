import datetime
from memor import Response, Role

TEST_CASE_NAME = "Response tests"


def test_response_message():
    response = Response(message="I am fine.", score=0.9, role=Role.ASSISTANT)
    assert response.message == "I am fine."


def test_response_score():
    response = Response(message="I am fine.", score=0.9, role=Role.ASSISTANT)
    assert response.score == 0.9


def test_response_role():
    response = Response(message="I am fine.", score=0.9, role=Role.ASSISTANT)
    assert response.role == Role.ASSISTANT


def test_response_temperature():
    response = Response(message="I am fine.", temperature=0.2)
    assert response.temperature == 0.2


def test_response_model():
    response = Response(message="I am fine.", model="GPT-4")
    assert response.model == "GPT-4"


def test_response_date():
    date_time_utc = datetime.datetime.now(datetime.timezone.utc)
    response = Response(message="I am fine.", date=date_time_utc)
    assert response.date_created == date_time_utc


