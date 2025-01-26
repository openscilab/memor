from memor import Prompt, Response, Role

TEST_CASE_NAME = "Prompt tests"

def test_prompt_message():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response], role=Role.USER)
    assert prompt.message == "Hello, how are you?"

def test_prompt_add_response():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0], role=Role.USER)
    response1 = Response(message="Great!", role=Role.ASSISTANT)
    prompt.add_response(response1)
    assert response1 in prompt.responses
