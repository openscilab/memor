from memor import Response, Role

TEST_CASE_NAME = "Response tests"


def test_response_message():
    response = Response(message="I am fine.", score=0.9, role=Role.ASSISTANT)
    assert response.message == "I am fine."


def test_response_score():
    response = Response(message="I am fine.", score=0.9, role=Role.ASSISTANT)
    assert response.score == 0.9
