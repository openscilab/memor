import json
import copy
from memor import Prompt, Response, Role
from memor import PresetPromptTemplate, CustomPromptTemplate

TEST_CASE_NAME = "Prompt tests"


def test_message1():
    prompt = Prompt(message="Hello, how are you?")
    assert prompt.message == "Hello, how are you?"


def test_message2():
    prompt = Prompt(message="Hello, how are you?")
    prompt.update_message("What's Up?")
    assert prompt.message == "What's Up?"


def test_role1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    assert prompt.role == Role.USER


def test_role2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    prompt.update_role(Role.SYSTEM)
    assert prompt.role == Role.SYSTEM


def test_responses1():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response])
    assert prompt.responses[0].message == "I am fine."


def test_responses2():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    response1 = Response(message="Good!")
    prompt = Prompt(message=message, responses=[response0, response1])
    assert prompt.responses[0].message == "I am fine." and prompt.responses[1].message == "Good!"


def test_responses3():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    response1 = Response(message="Good!")
    prompt = Prompt(message=message)
    prompt.update_responses([response0, response1])
    assert prompt.responses[0].message == "I am fine." and prompt.responses[1].message == "Good!"


def test_add_response():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0])
    response1 = Response(message="Great!")
    prompt.add_response(response1)
    assert response1 in prompt.responses


def test_remove_response():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    response1 = Response(message="Great!")
    prompt = Prompt(message=message, responses=[response0, response1])
    prompt.remove_response(0)
    assert response0 not in prompt.responses


def test_template1():
    message = "Hello, how are you?"
    prompt = Prompt(message=message, template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert prompt.template == PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD.value


def test_template2():
    message = "Hello, how are you?"
    prompt = Prompt(message=message, template=PresetPromptTemplate.BASIC.RESPONSE)
    prompt.update_template(PresetPromptTemplate.INSTRUCTION1.PROMPT)
    assert prompt.template.content == PresetPromptTemplate.INSTRUCTION1.PROMPT.value.content


def test_template3():
    message = "Hello, how are you?"
    template = CustomPromptTemplate(content="{message}-{response}")
    prompt = Prompt(message=message, template=template)
    assert prompt.template.content == "{message}-{response}"


def test_copy1():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt1 = Prompt(message=message, responses=[response], role=Role.USER,
                     template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    prompt2 = copy.copy(prompt1)
    assert id(prompt1) != id(prompt2)


def test_copy2():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt1 = Prompt(message=message, responses=[response], role=Role.USER,
                     template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    prompt2 = prompt1.copy()
    assert id(prompt1) != id(prompt2)


def test_str():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response], role=Role.USER,
                    template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert str(prompt) == prompt.message


def test_repr():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response], role=Role.USER,
                    template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert repr(prompt) == "Prompt(message={message})".format(message=prompt.message)


def test_equality1():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt1 = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    prompt2 = prompt1.copy()
    assert prompt1 == prompt2


def test_equality2():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt1 = Prompt(message=message, responses=[response1], role=Role.USER,
                     template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    prompt2 = Prompt(message=message, responses=[response2], role=Role.USER,
                     template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert prompt1 != prompt2


def test_equality3():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt1 = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    prompt2 = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert prompt1 == prompt2
