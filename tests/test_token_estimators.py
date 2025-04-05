from memor.tokens_estimator import openai_tokens_estimator_gpt_3_5, openai_tokens_estimator_gpt_4, universal_tokens_estimator

TEST_CASE_NAME = "Token Estimators tests"


def test_universal_tokens_estimator_with_contractions():
    message = "I'm going to the park."
    assert universal_tokens_estimator(message) == 7
    message = "They'll be here soon."
    assert universal_tokens_estimator(message) == 7


def test_universal_tokens_estimator_with_code_snippets():
    message = "def foo(): return 42"
    assert universal_tokens_estimator(message) == 7
    message = "if x == 10:"
    assert universal_tokens_estimator(message) == 6


def test_universal_tokens_estimator_with_loops():
    message = "for i in range(10):"
    assert universal_tokens_estimator(message) == 8
    message = "while True:"
    assert universal_tokens_estimator(message) == 4


def test_universal_tokens_estimator_with_long_sentences():
    message = "Understanding natural language processing is fun!"
    assert universal_tokens_estimator(message) == 17
    message = "Tokenization involves splitting text into meaningful units."
    assert universal_tokens_estimator(message) == 24


def test_universal_tokens_estimator_with_variable_names():
    message = "some_variable_name = 100"
    assert universal_tokens_estimator(message) == 5
    message = "another_long_var_name = 'test'"
    assert universal_tokens_estimator(message) == 6


def test_universal_tokens_estimator_with_function_definitions():
    message = "The function `def add(x, y): return x + y` adds two numbers."
    assert universal_tokens_estimator(message) == 20
    message = "Use `for i in range(5):` to loop."
    assert universal_tokens_estimator(message) == 14


def test_universal_tokens_estimator_with_numbers():
    message = "The year 2023 was great!"
    assert universal_tokens_estimator(message) == 6
    message = "42 is the answer to everything."
    assert universal_tokens_estimator(message) == 11


def test_universal_tokens_estimator_with_print_statements():
    message = "print('Hello, world!')"
    assert universal_tokens_estimator(message) == 5
    message = "name = \"Alice\""
    assert universal_tokens_estimator(message) == 3


def test_openai_tokens_estimator_with_function_definition():
    message = "def add(a, b): return a + b"
    assert openai_tokens_estimator_gpt_3_5(message) == 11


def test_openai_tokens_estimator_with_url():
    message = "Visit https://openai.com for more info."
    assert openai_tokens_estimator_gpt_3_5(message) == 18


def test_openai_tokens_estimator_with_long_words():
    message = "This is a verylongwordwithoutspaces and should be counted properly."
    assert openai_tokens_estimator_gpt_3_5(message) == 25


def test_openai_tokens_estimator_with_newlines():
    message = "Line1\nLine2\nLine3\n"
    assert openai_tokens_estimator_gpt_3_5(message) == 7


def test_openai_tokens_estimator_with_gpt4_model():
    message = "This is a test sentence that should be counted properly even with GPT-4. I am making it longer to test the model."
    assert openai_tokens_estimator_gpt_4(message) == 45
