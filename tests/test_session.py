import re
import datetime
import copy
import pytest
from memor import Session, Prompt, Response, Role
from memor import RenderFormat, MemorValidationError

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


def test_remove_message():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response])
    session.remove_message(1)
    assert session.messages == [prompt] and session.messages_status == [True]


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
    result = session1.save("session_test1.json")
    session2 = Session(file_path="session_test1.json")
    assert result["status"] and session1 == session2


def test_load1():
    with pytest.raises(MemorValidationError, match=r"Invalid path. Path must be a string."):
        _ = Session(file_path=22)


def test_load2():
    with pytest.raises(FileNotFoundError, match=r"Path session_test10.json does not exist."):
        _ = Session(file_path="session_test10.json")


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
