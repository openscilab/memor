import os
import datetime
import json
import copy
import pytest
from memor import PromptTemplate, TemplateEngine
from memor import MemorValidationError, MemorRenderError

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


def test_title5():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="")
    assert template.title == ""


def test_title6():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"},
        title="Title1")
    template.update_title(None)
    assert template.title is None


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


def test_content4():
    template = PromptTemplate(
        content="",
        custom_map={
            "language": "Python"})
    assert template.content == ""


def test_content5():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_content(content=None)
    assert template.content is None


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


def test_custom_map4():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={})
    assert template.custom_map == {}


def test_custom_map5():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.update_map(None)
    assert template.custom_map is None


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
        # a corrupted JSON string with an invalid `content` field
        template.from_json(r"""{
                            "content": invalid,
                            "title": "template1",
                            "memor_version": "0.6",
                            "custom_map": {"language": "Python"},
                            "date_created": "2025-05-07 21:52:33 +0000",
                            "date_modified": "2025-05-07 21:52:33 +0000"}""")
    assert template.content is None
    assert template.custom_map is None
    assert template.title is None


def test_json3():
    template = PromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `content` must be a string."):
        # a corrupted JSON string with wrong `content` field
        template.from_json(r"""{
                            "content": 0,
                            "title": "template1",
                            "memor_version": "0.6",
                            "custom_map": {"language": "Python"},
                            "date_created": "2025-05-07 21:52:33 +0000",
                            "date_modified": "2025-05-07 21:52:33 +0000"}""")
    assert template.content is None
    assert template.custom_map is None
    assert template.title is None


def test_json4():
    template = PromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `title` must be a string."):
        # a corrupted JSON string with wrong `title` field
        template.from_json(r"""{
                            "title": 0,
                            "content": "Act as a {language} developer and respond to this question:\n{prompt_message}",
                            "memor_version": "0.6",
                            "custom_map": {"language": "Python"},
                            "date_created": "2025-05-07 21:52:33 +0000",
                            "date_modified": "2025-05-07 21:52:33 +0000"}""")
    assert template.content is None
    assert template.custom_map is None
    assert template.title is None


def test_json5():
    template = PromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid custom map: it must be a dictionary with keys and values that can be converted to strings."):
        # a corrupted JSON string with wrong `custom_map` field
        template.from_json(r"""{
                            "title": "template1",
                            "content": "Act as a {language} developer and respond to this question:\n{prompt_message}",
                            "memor_version": "0.6",
                            "custom_map": 0,
                            "date_created": "2025-05-07 21:52:33 +0000",
                            "date_modified": "2025-05-07 21:52:33 +0000"}""")
    assert template.content is None
    assert template.custom_map is None
    assert template.title is None


def test_json6():
    template = PromptTemplate()
    with pytest.raises(MemorValidationError, match=r"Invalid value. `memor_version` must be a string."):
        # a corrupted JSON string with wrong `memor_version` field
        template.from_json(r"""{
                            "title": "template1",
                            "content": "Act as a {language} developer and respond to this question:\n{prompt_message}",
                            "memor_version": 0.6,
                            "custom_map": {"language": "Python"},
                            "date_created": "2025-05-07 21:52:33 +0000",
                            "date_modified": "2025-05-07 21:52:33 +0000"}""")
    assert template.content is None
    assert template.custom_map is None
    assert template.title is None


def test_json7():
    template1 = PromptTemplate(content="Act as a Python developer and respond to this question:\n{prompt_message}")
    assert template1.custom_map is None
    template1_json = template1.to_json()
    template2 = PromptTemplate()
    template2.from_json(template1_json)
    assert template1 == template2
    assert template2.custom_map is None


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
    assert not result["status"]


def test_load1():
    template1 = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    result = template1.save("template_test2.json")
    template2 = PromptTemplate(file_path="template_test2.json")
    assert result["status"] and template1 == template2


def test_load2():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: 22"):
        _ = PromptTemplate(file_path=22)


def test_load3():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: template_test10.json"):
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


def test_size():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={
            "language": "Python"})
    template.save("template_test3.json")
    assert os.path.getsize("template_test3.json") == template.size
    assert template.size == template.get_size()


def test_render1():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={"language": "Python"})
    assert template.render({"prompt_message": "Mock Question"}
                           ) == "Act as a Python developer and respond to this question:\nMock Question"


def test_render2():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={"language": "Python"})
    assert template.render({"language": "Rust", "prompt_message": "Mock Question"}
                           ) == "Act as a Rust developer and respond to this question:\nMock Question"


def test_render3():
    template = PromptTemplate(
        content="Act as a {language} developer and respond to this question:\n{prompt_message}",
        custom_map={"language": "Python"})
    with pytest.raises(MemorRenderError, match="Template and context are incompatible."):
        template.render()


def test_render4():
    template = PromptTemplate()
    with pytest.raises(MemorRenderError, match="Template and context are incompatible."):
        template.render()


def test_from_content_file1(tmp_path):
    file_path = tmp_path / "template.txt"
    file_path.write_text("Hello World", encoding="utf-8")
    template = PromptTemplate.from_content_file(str(file_path))
    assert template.content == "Hello World"


def test_from_content_file2(tmp_path):
    file_path = tmp_path / "review.txt"
    file_path.write_text("{{ name }}", encoding="utf-8")
    template = PromptTemplate.from_content_file(str(file_path), engine=TemplateEngine.JINJA)
    assert template.title == "review"


def test_from_content_file3(tmp_path):
    file_path = tmp_path / "review.txt"
    file_path.write_text("{{ name }}", encoding="utf-8")
    template = PromptTemplate.from_content_file(
        str(file_path),
        title="My Template",
        engine=TemplateEngine.JINJA
    )
    assert template.title == "My Template"
    assert template.engine == TemplateEngine.JINJA


def test_from_content_file4(tmp_path):
    file_path = tmp_path / "template.txt"
    file_path.write_text("Hello", encoding="utf-8")
    custom_map = {"instruction": "test"}
    template = PromptTemplate.from_content_file(
        str(file_path),
        custom_map=custom_map,
    )
    assert template.custom_map == custom_map
    assert template.engine == TemplateEngine.FORMAT


def test_from_content_file5():
    with pytest.raises(FileNotFoundError, match=r"Invalid path: must be a string and refer to an existing location. Given path: this-file-does-not-exist.txt"):
        PromptTemplate.from_content_file("this-file-does-not-exist.txt")


def test_render_jinja1():
    template = PromptTemplate(
        content="Act as a {{ language }} developer and respond to this question:\n{{ prompt_message }}",
        custom_map={"language": "Python"},
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"prompt_message": "Mock Question"}
    ) == "Act as a Python developer and respond to this question:\nMock Question"


def test_render_jinja2():
    template = PromptTemplate(
        content="Act as a {{ language }} developer and respond to this question:\n{{ prompt_message }}",
        custom_map={"language": "Python"},
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"language": "Rust", "prompt_message": "Mock Question"}
    ) == "Act as a Rust developer and respond to this question:\nMock Question"


def test_render_jinja3():
    template = PromptTemplate(
        content="Act as a {{ language }} developer and respond to this question:\n{{ prompt_message }}",
        custom_map={"language": "Python"},
        engine=TemplateEngine.JINJA,
    )
    with pytest.raises(MemorRenderError, match="Template and context are incompatible."):
        template.render()


def test_render_jinja4():
    template = PromptTemplate(
        content="Hello {{ name }}!",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"name": "Alice"}
    ) == "Hello Alice!"


def test_render_jinja5():
    template = PromptTemplate(
        content="{% if is_admin %}Admin{% else %}User{% endif %}",
        engine=TemplateEngine.JINJA,
    )
    assert template.render({"is_admin": True}) == "Admin"
    assert template.render({"is_admin": False}) == "User"


def test_render_jinja6():
    template = PromptTemplate(
        content="{% for item in items %}{{ item }} {% endfor %}",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"items": ["A", "B", "C"]}
    ) == "A B C "


def test_render_jinja7():
    template = PromptTemplate(
        content="{{ user.name }} is {{ user.age }} years old",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"user": {"name": "Alice", "age": 30}}
    ) == "Alice is 30 years old"


def test_render_jinja8():
    template = PromptTemplate(
        content="{{ missing_variable }}",
        engine=TemplateEngine.JINJA,
    )
    with pytest.raises(MemorRenderError, match="Template and context are incompatible."):
        template.render({})


def test_render_jinja9():
    template = PromptTemplate(
        content="",
        engine=TemplateEngine.JINJA,
    )
    assert template.render({}) == ""


def test_render_jinja10():
    template = PromptTemplate(
        content="{{ value|upper }}",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"value": "python"}
    ) == "PYTHON"


def test_render_jinja11():
    template = PromptTemplate(
        content="{{ numbers|length }}",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {"numbers": [1, 2, 3, 4]}
    ) == "4"


def test_render_jinja12():
    template = PromptTemplate(
        content="{% for user in users %}{{ user.name }};{% endfor %}",
        engine=TemplateEngine.JINJA,
    )
    assert template.render(
        {
            "users": [
                {"name": "Alice"},
                {"name": "Bob"},
                {"name": "Charlie"},
            ]
        }
    ) == "Alice;Bob;Charlie;"


def test_variables1():
    template = PromptTemplate(
        content="{% for user in users %}{{ user.name }};{% endfor %}",
        engine=TemplateEngine.JINJA,
    )
    assert template.variables == ["users"]


def test_variables2():
    template = PromptTemplate("{user1}, {user2}, {prompt}")
    assert template.variables == ['prompt', 'user1', 'user2']


def test_variables3():
    template = PromptTemplate()
    assert template.variables == []


def test_get_missing_variables1():
    template = PromptTemplate(
        content="{% for user in users %}{{ user.name }};{% endfor %}",
        engine=TemplateEngine.JINJA,
    )
    assert template.get_missing_variables({"users": []}) == []
    assert template.get_missing_variables({"test": []}) == ["users"]


def test_get_missing_variables2():
    template = PromptTemplate("{user1}, {user2}, {prompt}", custom_map={"prompt": "hi"})
    assert template.get_missing_variables({"user1": "test"}) == ["user2"]
