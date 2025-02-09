import datetime
import json
import copy
import pytest
from memor import CustomPromptTemplate, MemorValidationError

TEST_CASE_NAME = "CustomPromptTemplate tests"


def test_title1():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.title == None


def test_title2():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_title("template1")
    assert template.title == "template1"


def test_title3():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title=None)
    assert template.title == None


def test_content1():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.content == "Act as a {language} developer and respond to this question:\n{prompt_message}"


def test_content2():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_content(content="Act as a {language} developer and respond to this query:\n{prompt_message}")
    assert template.content == "Act as a {language} developer and respond to this query:\n{prompt_message}"


def test_custom_map1():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert template.custom_map == {"language": "Python"}


def test_custom_map2():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_map({"language": "C++"})
    assert template.custom_map == {"language": "C++"}


def test_date_modified():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert isinstance(template.date_modified, datetime.datetime)


def test_date_created():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert isinstance(template.date_created, datetime.datetime)


def test_json1():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template1_json = template1.to_json()
    template2 = CustomPromptTemplate()
    template2.from_json(template1_json)
    assert template1 == template2


def test_json2():
    template = CustomPromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid template structure. It should be a JSON object with proper fields."):
        template.from_json("{}")


def test_save1():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template.save("template_test1.json")
    with open("template_test1.json", "r") as file:
        saved_template = json.loads(file.read())
    assert result["status"] and json.loads(template.to_json()) == saved_template


def test_save2():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template.save("f:/")
    assert result["status"] == False


def test_load():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template1.save("template_test2.json")
    template2 = CustomPromptTemplate(file_path="template_test2.json")
    assert result["status"] and template1 == template2


def test_copy1():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = copy.copy(template1)
    assert id(template1) != id(template2)


def test_copy2():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = template1.copy()
    assert id(template1) != id(template2)


def test_str():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert str(template) == template.content


def test_repr():
    template = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    assert repr(template) == "CustomPromptTemplate(content={content})".format(content=template.content)


def test_equality1():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template2 = template1.copy()
    assert template1 == template2


def test_equality2():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    template2 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template2")
    assert template1 != template2


def test_equality3():
    template1 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    template2 = CustomPromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="template1")
    assert template1 == template2
