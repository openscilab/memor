from memor import CustomPromptTemplate

TEST_CASE_NAME = "CustomPromptTemplate tests"


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


def test_content():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert template.content == "Act as a {language} developer and respond to this question:\n{prompt_message}"


def test_custom_map():
    template = CustomPromptTemplate(content="Act as a {language} developer and respond to this question:\n{prompt_message}", custom_map={"language": "Python"})
    assert template.custom_map == {"language": "Python"}
