import datetime
import copy
import pytest
from memor import Prompt, Response, Role
from memor import PresetPromptTemplate, PromptTemplate
from memor import RenderFormat, MemorValidationError, MemorRenderError

TEST_CASE_NAME = "Prompt tests"


def test_message1():
    prompt = Prompt(message="Hello, how are you?")
    assert prompt.message == "Hello, how are you?"


def test_message2():
    prompt = Prompt(message="Hello, how are you?")
    prompt.update_message("What's Up?")
    assert prompt.message == "What's Up?"


def test_message3():
    prompt = Prompt(message="Hello, how are you?")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `message` must be a string."):
        prompt.update_message(22)


def test_tokens1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    assert prompt.tokens is None


def test_tokens2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER, tokens=4)
    assert prompt.tokens == 4


def test_tokens3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER, tokens=4)
    prompt.update_tokens(7)
    assert prompt.tokens == 7


def test_tokens4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `tokens` must be a positive integer."):
        prompt.update_tokens("4")


def test_role1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    assert prompt.role == Role.USER


def test_role2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    prompt.update_role(Role.SYSTEM)
    assert prompt.role == Role.SYSTEM


def test_role3():
    prompt = Prompt(message="Hello, how are you?", role=None)
    assert prompt.role == Role.USER


def test_role4():
    prompt = Prompt(message="Hello, how are you?", role=None)
    with pytest.raises(MemorValidationError, match=r"Invalid role. It must be an instance of Role enum."):
        prompt.update_role(2)


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


def test_responses4():
    message = "Hello, how are you?"
    prompt = Prompt(message=message)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `responses` must be a list of `Response`."):
        prompt.update_responses({"I am fine.", "Good!"})


def test_responses5():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `responses` must be a list of `Response`."):
        prompt.update_responses([response0, "Good!"])


def test_add_response1():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0])
    response1 = Response(message="Great!")
    prompt.add_response(response1)
    assert prompt.responses[0] == response0 and prompt.responses[1] == response1


def test_add_response2():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0])
    response1 = Response(message="Great!")
    prompt.add_response(response1, index=0)
    assert prompt.responses[0] == response1 and prompt.responses[1] == response0


def test_add_response3():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0])
    with pytest.raises(MemorValidationError, match=r"Invalid response. It must be an instance of `Response`."):
        prompt.add_response(1)


def test_remove_response():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    response1 = Response(message="Great!")
    prompt = Prompt(message=message, responses=[response0, response1])
    prompt.remove_response(0)
    assert response0 not in prompt.responses


def test_select_response():
    message = "Hello, how are you?"
    response0 = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response0])
    response1 = Response(message="Great!")
    prompt.add_response(response1)
    prompt.select_response(index=1)
    assert prompt.selected_response == response1


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
    template = PromptTemplate(content="{message}-{response}")
    prompt = Prompt(message=message, template=template)
    assert prompt.template.content == "{message}-{response}"


def test_template4():
    message = "Hello, how are you?"
    prompt = Prompt(message=message, template=None)
    assert prompt.template == PresetPromptTemplate.DEFAULT.value


def test_template5():
    message = "Hello, how are you?"
    prompt = Prompt(message=message, template=PresetPromptTemplate.BASIC.RESPONSE)
    with pytest.raises(MemorValidationError, match=r"Invalid template. It must be an instance of `PromptTemplate` or `PresetPromptTemplate`."):
        prompt.update_template("{prompt_message}")


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
    assert str(prompt) == prompt.render(render_format=RenderFormat.STRING)


def test_repr():
    message = "Hello, how are you?"
    response = Response(message="I am fine.")
    prompt = Prompt(message=message, responses=[response], role=Role.USER,
                    template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert repr(prompt) == "Prompt(message={message})".format(message=prompt.message)


def test_json1():
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
    prompt1_json = prompt1.to_json()
    prompt2 = Prompt()
    prompt2.from_json(prompt1_json)
    assert prompt1 == prompt2


def test_json2():
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
    prompt1_json = prompt1.to_json(save_template=False)
    prompt2 = Prompt()
    prompt2.from_json(prompt1_json)
    assert prompt1 != prompt2 and prompt1.template == PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD.value and prompt2.template == PresetPromptTemplate.DEFAULT.value


def test_json3():
    prompt = Prompt()
    with pytest.raises(MemorValidationError, match=r"Invalid prompt structure. It should be a JSON object with proper fields."):
        prompt.from_json("{}")


def test_save1():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    result = prompt.save("f:/")
    assert result["status"] == False


def test_save2():
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
    result = prompt1.save("prompt_test1.json")
    prompt2 = Prompt(file_path="prompt_test1.json")
    assert result["status"] and prompt1 == prompt2


def test_load1():
    with pytest.raises(MemorValidationError, match=r"Invalid path. Path must be a string."):
        _ = Prompt(file_path=22)


def test_load2():
    with pytest.raises(FileNotFoundError, match=r"Path prompt_test10.json does not exist."):
        _ = Prompt(file_path="prompt_test10.json")


def test_save3():
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
    result = prompt1.save("prompt_test2.json", save_template=False)
    prompt2 = Prompt(file_path="prompt_test2.json")
    assert result["status"] and prompt1 != prompt2 and prompt1.template == PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD.value and prompt2.template == PresetPromptTemplate.DEFAULT.value


def test_render1():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT)
    assert prompt.render() == "Hello, how are you?"


def test_render2():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT)
    assert prompt.render(RenderFormat.OPENAI) == {"role": "user", "content": "Hello, how are you?"}


def test_render3():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT)
    assert prompt.render(RenderFormat.DICTIONARY)["content"] == "Hello, how are you?"


def test_render4():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT)
    assert ("content", "Hello, how are you?") in prompt.render(RenderFormat.ITEMS)


def test_render5():
    message = "How are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    template = PromptTemplate(content="{instruction}, {prompt[message]}", custom_map={"instruction": "Hi"})
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=template)
    assert prompt.render(RenderFormat.OPENAI) == {"role": "user", "content": "Hi, How are you?"}


def test_render6():
    message = "Hello, how are you?"
    response = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    template = PromptTemplate(content="{response[2][message]}")
    prompt = Prompt(
        message=message,
        responses=[response],
        role=Role.USER,
        template=template)
    with pytest.raises(MemorRenderError, match=r"Prompt template and properties are incompatible."):
        prompt.render()


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


def test_equality4():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert prompt != 2


def test_date_modified():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert isinstance(prompt.date_modified, datetime.datetime)


def test_date_created():
    message = "Hello, how are you?"
    response1 = Response(message="I am fine.", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    response2 = Response(message="Thanks!", model="GPT-4", temperature=0.5, role=Role.USER, score=0.8)
    prompt = Prompt(
        message=message,
        responses=[
            response1,
            response2],
        role=Role.USER,
        template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD)
    assert isinstance(prompt.date_created, datetime.datetime)
