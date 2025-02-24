import datetime
import copy
import pytest
from memor import Session, Prompt, Response, Role
from memor import PresetPromptTemplate, PromptTemplate
from memor import RenderFormat, MemorValidationError, MemorRenderError

TEST_CASE_NAME = "Session tests"


def test_title1():
    session = Session(title="session1")
    assert session.title == "session1"


def test_title2():
    session = Session(title="session1")
    session.update_title("session2")
    assert session.title == "session2"


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


def test_json1():
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


def test_render1():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render() == "Hello, how are you?\nI am fine.\n"


def test_render2():
    prompt = Prompt(message="Hello, how are you?", role=Role.USER)
    response = Response(message="I am fine.")
    session = Session(messages=[prompt, response], title="session1")
    assert session.render(RenderFormat.OPENAI) == [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I am fine."}]


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
