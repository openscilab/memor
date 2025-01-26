from memor import CustomPromptTemplate

TEST_CASE_NAME = "CustomPromptTemplate tests"


def test_custom_prompt_template_content():
    template = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"})
    assert template.content == "What is your name?"


def test_custom_prompt_template_custom_map():
    template = CustomPromptTemplate(content="What is your name?", custom_map={"name": "John"})
    assert template.custom_map == {"name": "John"}
