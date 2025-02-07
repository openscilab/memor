from memor import CustomPromptTemplate

TEST_CASE_NAME = "CustomPromptTemplate tests"


def test_title1():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert template.title == "unknown"


def test_title2():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template.update_title("template1")
    assert template.title == "template1"


def test_content1():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert template.content == "Act as a {language} developer and respond to this question:\n{prompt_message}"


def test_content2():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template.update_content(content="Act as a {language} developer and respond to this query:\n{prompt_message}")
    assert template.content == "Act as a {language} developer and respond to this query:\n{prompt_message}"


def test_custom_map1():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert template.custom_map == {"language": "Python"}


def test_custom_map2():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template.update_map({"language": "C++"})
    assert template.custom_map == {"language": "C++"}


def test_copy1():
    template1 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template2 = copy.copy(template1)
    assert id(template1) != id(template2)


def test_copy2():
    template1 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template2 = template1.copy()
    assert id(template1) != id(template2)


def test_str():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert str(template) == template.content


def test_repr():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert repr(template) == "CustomPromptTemplate(content={content})".format(content=template.content)


def test_equality1():
    template1 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    template2 = template1.copy()
    assert template1 == template2


def test_equality2():
    template1 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"}, title="template1")
    template2 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"}, title="template2")
    assert template1 != template2


def test_equality3():
    template1 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"}, title="template1")
    template2 = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"}, title="template1")
    assert template1 == template2
