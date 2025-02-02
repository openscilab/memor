from memor import CustomPromptTemplate

TEST_CASE_NAME = "CustomPromptTemplate tests"


def test_equality1():
    template1 = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"})
    template2 = template1.copy()
    assert template1 == template2


def test_equality2():
    template1 = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"}, title="template1")
    template2 = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"}, title="template2")
    assert template1 != template2


def test_equality3():
    template1 = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"}, title="template1")
    template2 = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"}, title="template1")
    assert template1 == template2

def test_custom_prompt_template_content():
    template = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"})
    assert template.content == "What is your name?"


def test_custom_prompt_template_custom_map():
    template = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"})
    assert template.custom_map == {"name": "John"}
