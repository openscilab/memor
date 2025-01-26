from memor import Prompt, Response, Role

TEST_CASE_NAME = "Prompt tests"

def test_prompt_message():
    prompt = Prompt(message="Hello, how are you?", responses=["I am fine."], role=Role.USER)
    assert prompt.message == "Hello, how are you?"

def test_prompt_add_response():
    prompt = Prompt(message="Hello, how are you?", responses=["I am fine."], role=Role.USER)
    response = Response(message="Great!", role=Role.ASSISTANT)
    prompt.add_response(response)
    assert response in prompt.responses
