import datetime
import json
import copy
import pytest
from memor import PromptTemplate, MemorValidationError

TEST_CASE_NAME = "PromptTemplate tests"


def test_title1():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.title is None


def test_title2():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_title("template1")
    assert template.title == "template1"


def test_title3():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title=None)
    assert template.title is None


def test_title4():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title=None)
    with pytest.raises(MemorValidationError, match=r"Invalid value. `title` must be a string."):
        template.update_title(25)


def test_content1():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.content == "Act as a {language} developer and respond to this question:\n{prompt_message}"


def test_content2():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_content(content="Act as a {language} developer and respond to this query:\n{prompt_message}")
    assert template.content == "Act as a {language} developer and respond to this query:\n{prompt_message}"


def test_content3():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    with pytest.raises(MemorValidationError, match=r"Invalid value. `content` must be a string."):
        template.update_content(content=22)


def test_custom_map1():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.custom_map == {"language": "Python"}


def test_custom_map2():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_map({"language": "C++"})
    assert template.custom_map == {"language": "C++"}


def test_custom_map3():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    with pytest.raises(MemorValidationError, match=r"Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."):
        template.update_map(["C++"])


def test_date_modified():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert isinstance(template.date_modified, datetime.datetime)


def test_date_created():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert isinstance(template.date_created, datetime.datetime)


def test_json1():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template1_json = template1.to_json()
    template2 = PromptTemplate()
    template2.from_json(template1_json)
    assert template1 == template2


def test_json2():
    template = PromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid template structure. It should be a JSON object with proper fields."):
        template.from_json("{}")


def test_save1():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template.save("template_test1.json")
    with open("template_test1.json", "r") as file:
        saved_template = json.loads(file.read())
    assert result["status"] and template.to_json() == saved_template


def test_save2():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template.save("f:/")
    assert result["status"] == False


def test_load1():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template1.save("template_test2.json")
    template2 = PromptTemplate(file_path="template_test2.json")
    assert result["status"] and template1 == template2


def test_load2():
    with pytest.raises(MemorValidationError, match=r"Invalid path. Path must be a string."):
        _ = PromptTemplate(file_path=22)


def test_load3():
    with pytest.raises(FileNotFoundError, match=r"Path template_test10.json does not exist."):
        _ = PromptTemplate(file_path="template_test10.json")


def test_copy1():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = copy.copy(template1)
    assert id(template1) != id(template2)


def test_copy2():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = template1.copy()
    assert id(template1) != id(template2)


def test_str():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert str(template) == template.content


def test_repr():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert repr(template) == "PromptTemplate(content={content})".format(content=template.content)


def test_equality1():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = template1.copy()
    assert template1 == template2


def test_equality2():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    template2 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template2")
    assert template1 != template2


def test_equality3():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    template2 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    assert template1 == template2


def test_equality4():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    assert template != 2
