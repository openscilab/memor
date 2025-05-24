import os
import re
import datetime
import copy
import pytest
from memor import Session, Prompt, Response, Role
from memor import PromptTemplate
from memor import RenderFormat
from memor import MemorRenderError, MemorValidationError
from memor import TokensEstimator

TEST_CASE_NAME = "Session tests"


def test_title1():
    session = Session(title="session1")
    assert session.title == "session1"


def test_title2():
    session = Session(title="session1")
    session.update_title("session2")
    assert session.title == "session2"


def test_title3():
    session = Session(title="session1")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `title` must be a string."):
        session.update_title(2)


def test_messages1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    assert session.messages == [prompt, response]


def test_messages2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages([prompt, response, prompt, response])
    assert session.messages == [prompt, response, prompt, response]


def test_messages3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    session = Session(messages=[prompt])
    with pytest.raises(MemorValidationError, match=r"Invalid value. `messages` must be a list of `Prompt` or `Response`."):
        session.update_messages([prompt, "I am fine."])


def test_messages4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    session = Session(messages=[prompt])
    with pytest.raises(MemorValidationError, match=r"Invalid value. `messages` must be a list of `Prompt` or `Response`."):
        session.update_messages("I am fine.")


def test_messages_status1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    assert session.messages_status == [True, True]


def test_messages_status2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages_status([False, True])
    assert session.messages_status == [False, True]


def test_messages_status3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    with pytest.raises(MemorValidationError, match=r"Invalid value. `status` must be a list of booleans."):
        session.update_messages_status(["False", True])


def test_messages_status4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    with pytest.raises(MemorValidationError, match=r"Invalid message status length. It must be equal to the number of messages."):
        session.update_messages_status([False, True, True])


def test_messages_status5():
    s = Session()
    p1 = Prompt("Prompt1")
    p2 = Prompt("Prompt2")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `status` must be a list of booleans."):
        s.update_messages(messages=[p1, p2], status="status")
    assert s.messages == []
    assert s.messages_status == []


def test_enable_message():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages_status([False, False])
    session.enable_message(0)
    assert session.messages_status == [True, False]


def test_disable_message():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages_status([True, True])
    session.disable_message(0)
    assert session.messages_status == [False, True]


def test_mask_message():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.mask_message(0)
    assert session.messages_status == [False, True]


def test_unmask_message():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages_status([False, False])
    session.unmask_message(0)
    assert session.messages_status == [True, False]


def test_masks():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.update_messages_status([False, True])
    assert session.masks == [True, False]


def test_add_message1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.add_message(Response("Good!"))
    assert session.messages[2] == Response("Good!")


def test_add_message2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.add_message(message=Response("Good!"), status=False, index=0)
    assert session.messages[0] == Response("Good!") and session.messages_status[0] == False


def test_add_message3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    with pytest.raises(MemorValidationError, match=r"Invalid message. It must be an instance of `Prompt` or `Response`."):
        session.add_message(message="Good!", status=False, index=0)


def test_add_message4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    with pytest.raises(MemorValidationError, match=r"Invalid value. `status` must be a boolean."):
        session.add_message(message=prompt, status="False", index=0)


def test_remove_message1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.remove_message(1)
    assert session.messages == [prompt] and session.messages_status == [True]


def test_remove_message2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.remove_message_by_index(1)
    assert session.messages == [prompt] and session.messages_status == [True]


def test_remove_message3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.remove_message_by_id(response.id)
    assert session.messages == [prompt] and session.messages_status == [True]


def test_remove_message4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.remove_message(response.id)
    assert session.messages == [prompt] and session.messages_status == [True]


def test_remove_message5():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    with pytest.raises(MemorValidationError, match=r"Invalid value. `identifier` must be an integer or a string."):
        session.remove_message(3.5)


def test_clear_messages():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    assert len(session) == 2
    session.clear_messages()
    assert len(session) == 0


def test_copy1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session")
    session2 = copy.copy(session1)
    assert id(session1) != id(session2)


def test_copy2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session")
    session2 = session1.copy()
    assert id(session1) != id(session2)


def test_str():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert str(session) == session.render(render_format=RenderFormat.STRING)


def test_repr():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert repr(session) == "Session(title={title})".format(title=session.title)


def test_json():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session1")
    session1_json = session1.to_json()
    session2 = Session()
    session2.from_json(session1_json)
    assert session1 == session2


def test_save1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    result = session.save("f:/")
    assert result["status"] == False


def test_save2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session1")
    _ = session1.render()
    result = session1.save("session_test1.json")
    session2 = Session(file_path="session_test1.json")
    assert result["status"] and session1 == session2 and session2.render_counter == 1


def test_load1():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: 22"):
        _ = Session(file_path=22)


def test_load2():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: session_test10.json"):
        _ = Session(file_path="session_test10.json")


def test_load3():
    session = Session()
    with pytest.raises(MemorValidationError, match=r"Invalid session structure. It should be a JSON object with proper fields."):
        # a corrupted JSON string without `messages_status` field
        session.from_json(r"""{
                          "type": "Session",
                          "title": "session1",
                          "render_counter": 1,
                          "messages": [
                          {
                            "type": "Prompt",
                            "message": "Hello, how are you?",
                            "responses": [],
                            "selected_response_index": 0,
                            "tokens": null,
                            "role": "user",
                            "id":"465a5bc3-2ede-46b5-af47-294637e44407",
                            "template": {
                                "title": "Basic/Prompt",
                                "content": "{instruction}{prompt[message]}",
                                "memor_version": "0.6",
                                "custom_map": {"instruction": ""},
                                "date_created": "2025-05-07 21:57:05 +0000",
                                "date_modified": "2025-05-07 21:57:05 +0000"},
                            "memor_version": "0.6",
                            "date_created": "2025-05-07 21:57:05 +0000",
                            "date_modified": "2025-05-07 21:57:05 +0000"},
                          {
                            "type": "Response",
                            "message": "I am fine.",
                            "score": null,
                            "temperature": null,
                            "tokens": null,
                            "inference_time": null,
                            "role": "assistant",
                            "model": "unknown",
                            "id": "8a2a32b8-d828-4309-9583-2185fba9e3bb",
                            "memor_version": "0.6",
                            "date_created": "2025-05-07 21:57:05 +0000",
                            "date_modified": "2025-05-07 21:57:05 +0000"
                          }],
                          "memor_version": "0.6",
                          "date_created": "2025-05-07 21:57:05 +0000",
                          "date_modified": "2025-05-07 21:57:05 +0000"}""")
    assert session.messages == [] and session.title is None
    assert session.render_counter == 0
    assert session.messages_status == []


def test_load4():
    session = Session()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `title` must be a string."):
        # a corrupted JSON string with invalid `title` field
        session.from_json(r"""{
                          "type": "Session",
                          "title": 0,
                          "render_counter": 1,
                          "messages_status": [true, false],
                          "messages": [
                          {
                            "type": "Prompt",
                            "message": "Hello, how are you?",
                            "responses": [],
                            "selected_response_index": 0,
                            "tokens": null,
                            "role": "user",
                            "id":"465a5bc3-2ede-46b5-af47-294637e44407",
                            "template": {
                                "title": "Basic/Prompt",
                                "content": "{instruction}{prompt[message]}",
                                "memor_version": "0.6",
                                "custom_map": {"instruction": ""},
                                "date_created": "2025-05-07 21:57:05 +0000",
                                "date_modified": "2025-05-07 21:57:05 +0000"},
                            "memor_version": "0.6",
                            "date_created": "2025-05-07 21:57:05 +0000",
                            "date_modified": "2025-05-07 21:57:05 +0000"},
                          {
                            "type": "Response",
                            "message": "I am fine.",
                            "score": null,
                            "temperature": null,
                            "tokens": null,
                            "inference_time": null,
                            "role": "assistant",
                            "model": "unknown",
                            "id": "8a2a32b8-d828-4309-9583-2185fba9e3bb",
                            "memor_version": "0.6",
                            "date_created": "2025-05-07 21:57:05 +0000",
                            "date_modified": "2025-05-07 21:57:05 +0000"
                          }],
                          "memor_version": "0.6",
                          "date_created": "2025-05-07 21:57:05 +0000",
                          "date_modified": "2025-05-07 21:57:05 +0000"}""")
    assert session.messages == [] and session.title is None
    assert session.render_counter == 0
    assert session.messages_status == []


def test_render1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render() == "Hello, how are you?\nI am fine.\n"


def test_render2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render(RenderFormat.OPENAI) == [{"role": "user", "content": "Hello, how are you?"}, {
        "role": "assistant", "content": "I am fine."}]


def test_render3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render(RenderFormat.DICTIONARY)["content"] == "Hello, how are you?\nI am fine.\n"


def test_render4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert ("content", "Hello, how are you?\nI am fine.\n") in session.render(RenderFormat.ITEMS)


def test_render5():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    with pytest.raises(MemorValidationError, match=r"Invalid render format. It must be an instance of RenderFormat enum."):
        session.render("OPENAI")


def test_render6():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render(RenderFormat.AI_STUDIO) == [{'role': 'user', 'parts': [{'text': 'Hello, how are you?'}]}, {
        'role': 'assistant', 'parts': [{'text': 'I am fine.'}]}]


def test_render7():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    session.disable_message(0)
    assert session.render() == 'I am fine.\n'
    assert session.render(RenderFormat.OPENAI) == [{'content': 'I am fine.', 'role': 'assistant'}]
    assert session.render(RenderFormat.AI_STUDIO) == [{'role': 'assistant', 'parts': [{'text': 'I am fine.'}]}]
    session.enable_message(0)
    session.disable_message(1)
    assert session.render() == 'Hello, how are you?\n'
    assert session.render(RenderFormat.OPENAI) == [{'content': 'Hello, how are you?', 'role': 'user'}]
    assert session.render(RenderFormat.AI_STUDIO) == [{'role': 'user', 'parts': [{'text': 'Hello, how are you?'}]}]


def test_check_render1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.check_render()


def test_check_render2():
    template = PromptTemplate(content="{response[2][message]}")
    prompt = Prompt(message="Hello, how are you?", role=Role.USER, template=template, init_check=False)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1", init_check=False)
    assert not session.check_render()


def test_render_counter1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render_counter == 0
    for _ in range(10):
        __ = session.render()
    assert session.render_counter == 10


def test_render_counter2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render_counter == 0
    for _ in range(10):
        __ = session.render()
    for _ in range(2):
        __ = session.render(enable_counter=False)
    assert session.render_counter == 10


def test_render_counter3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1", init_check=True)
    _ = str(session)
    _ = session.check_render()
    _ = session.estimate_tokens()
    assert session.render_counter == 0


def test_init_check():
    template = PromptTemplate(content="{response[2][message]}")
    prompt = Prompt(message="Hello, how are you?", role=Role.USER, template=template, init_check=False)
    response = Response(message="I am fine.")
    with pytest.raises(MemorRenderError, match=r"Prompt template and properties are incompatible."):
        _ = Session(messages=[prompt, response], title="session1")


def test_equality1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session1")
    session2 = session1.copy()
    assert session1 == session2


def test_equality2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session1")
    session2 = Session(messages=[prompt, response], title="session2")
    assert session1 != session2


def test_equality3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response], title="session1")
    session2 = Session(messages=[prompt, response], title="session1")
    assert session1 == session2


def test_equality4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session != 2


def test_date_modified():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert isinstance(session.date_modified, datetime.datetime)


def test_date_created():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert isinstance(session.date_created, datetime.datetime)


def test_length():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert len(session) == len(session.messages) and len(session) == 2


def test_iter():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response, prompt, response], title="session1")
    messages = []
    for message in session:
        messages.append(message)
    assert session.messages == messages


def test_addition1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = Session(messages=[prompt, prompt, response, response], title="session2")
    session3 = session1 + session2
    assert session3.title is None and session3.messages == session1.messages + session2.messages


def test_addition2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = Session(messages=[prompt, prompt, response, response], title="session2")
    session3 = session2 + session1
    assert session3.title is None and session3.messages == session2.messages + session1.messages


def test_addition3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = session1 + response
    assert session2.title == "session1" and session2.messages == session1.messages + [response]


def test_addition4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = session1 + prompt
    assert session2.title == "session1" and session2.messages == session1.messages + [prompt]


def test_addition5():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = response + session1
    assert session2.title == "session1" and session2.messages == [response] + session1.messages


def test_addition6():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    session2 = prompt + session1
    assert session2.title == "session1" and session2.messages == [prompt] + session1.messages


def test_addition7():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    with pytest.raises(TypeError, match=re.escape(r"Unsupported operand type(s) for +: `Session` and `int`")):
        _ = session1 + 2


def test_addition8():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session1 = Session(messages=[prompt, response, prompt, response], title="session1")
    with pytest.raises(TypeError, match=re.escape(r"Unsupported operand type(s) for +: `Session` and `int`")):
        _ = 2 + session1


def test_contains1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert prompt in session and response in session


def test_contains2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response1 = Response(message="I am fine.")
    response2 = Response(message="Good!")
    session = Session(messages=[prompt, response1], title="session")
    assert response2 not in session


def test_contains3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert "I am fine." not in session


def test_getitem1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session[0] == session.messages[0] and session[1] == session.messages[1]


def test_getitem2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response, response, response], title="session")
    assert session[:] == session.messages


def test_getitem3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session[0] == session.get_message_by_index(0) and session[1] == session.get_message_by_index(1)


def test_getitem4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session[0] == session.get_message(0) and session[1] == session.get_message(1)


def test_getitem5():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session[0] == session.get_message_by_id(prompt.id) and session[1] == session.get_message_by_id(response.id)


def test_getitem6():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session[0] == session.get_message(prompt.id) and session[1] == session.get_message(response.id)


def test_getitem7():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `identifier` must be an integer, string or a slice."):
        _ = session[3.5]


def test_getitem8():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    with pytest.raises(MemorValidationError, match=r"Invalid value. `identifier` must be an integer, string or a slice."):
        _ = session.get_message(3.5)


def test_estimated_tokens1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.estimate_tokens(TokensEstimator.UNIVERSAL) == 12


def test_estimated_tokens2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.estimate_tokens(TokensEstimator.OPENAI_GPT_3_5) == 14


def test_estimated_tokens3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.estimate_tokens(TokensEstimator.OPENAI_GPT_4) == 15


def test_search1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.search(query="hello") == [0]


def test_search2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.search(query="hello", case_sensitive=True) == []


def test_search3():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.search(query="^hello", use_regex=True) == [0]


def test_search4():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    assert session.search(query="a") == [0, 1]


def test_search5():
    template = PromptTemplate(content="{response[2][message]}")
    prompt = Prompt(message="Hello, how are you?", role=Role.USER, template=template, init_check=False)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session", init_check=False)
    assert session.search(query="a") == [1]


def test_size():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session")
    session.save("session_test2.json")
    assert os.path.getsize("session_test2.json") == session.size
    assert session.size == session.get_size()
