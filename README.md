<div align="center">
    <img src="https://github.com/openscilab/memor/raw/main/otherfiles/logo.png" alt="Memor Logo" width="424">
    <h1>Memor: Reproducible Structured Memory for LLMs</h1>
    <br/>
    <a href="https://codecov.io/gh/openscilab/memor"><img src="https://codecov.io/gh/openscilab/memor/branch/dev/graph/badge.svg?token=TS5IAEXX7O"></a>
    <a href="https://badge.fury.io/py/memor"><img src="https://badge.fury.io/py/memor.svg" alt="PyPI version"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/built%20with-Python3-green.svg" alt="built with Python3"></a>
    <a href="https://github.com/openscilab/memor"><img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/openscilab/memor"></a>
    <a href="https://discord.gg/cZxGwZ6utB"><img src="https://img.shields.io/discord/1064533716615049236.svg" alt="Discord Channel"></a>
</div>

----------


## Overview
<p align="justify">
With Memor, users can store their LLM conversation history using an intuitive and structured data format.
It abstracts user prompts and model responses into a "Session", a sequence of message exchanges.
In addition to the content, it includes details like decoding temperature and token count of each message.
Therefore users could create comprehensive and reproducible logs of their interactions.
Because of the model-agnostic design, users can begin a conversation with one LLM and switch to another keeping the context the same.
For example, they might use a retrieval-augmented model (like RAG) to gather relevant context for a math problem, and then switch to a model better suited for reasoning to solve the problem based on the retrieved information presented by Memor.
</p>

<p align="justify">
Memor also lets users select, filter, and then share the specific parts of the past conversations across different models. This means users are not only able to reproduce and review previous chats through structured logs, but can also flexibly transfer the content of their conversations between LLMs.
In a nutshell, Memor makes it easy and effective to manage and reuse conversations with large language models.
</p>
<table>
    <tr>
        <td align="center">PyPI Counter</td>
        <td align="center">
            <a href="https://pepy.tech/projects/memor">
                <img src="https://static.pepy.tech/badge/memor">
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">Github Stars</td>
        <td align="center">
            <a href="https://github.com/openscilab/memor">
                <img src="https://img.shields.io/github/stars/openscilab/memor.svg?style=social&label=Stars">
            </a>
        </td>
    </tr>
</table>
<table>
    <tr> 
        <td align="center">Branch</td>
        <td align="center">main</td>
        <td align="center">dev</td>
    </tr>
    <tr>
        <td align="center">CI</td>
        <td align="center">
            <img src="https://github.com/openscilab/memor/actions/workflows/test.yml/badge.svg?branch=main">
        </td>
        <td align="center">
            <img src="https://github.com/openscilab/memor/actions/workflows/test.yml/badge.svg?branch=dev">
            </td>
    </tr>
</table>
<table>
    <tr> 
        <td align="center">Code Quality</td>
        <td align="center"><a href="https://www.codefactor.io/repository/github/openscilab/memor"><img src="https://www.codefactor.io/repository/github/openscilab/memor/badge" alt="CodeFactor"></a></td>
        <td align="center"><a href="https://app.codacy.com/gh/openscilab/memor/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade"><img src="https://app.codacy.com/project/badge/Grade/3758f5116c4347ce957997bb7f679cfa"/></a></td>
    </tr>
</table>


## Installation

### PyPI
- Check [Python Packaging User Guide](https://packaging.python.org/installing/)
- Run `pip install memor==0.8`
### Source code
- Download [Version 0.8](https://github.com/openscilab/memor/archive/v0.8.zip) or [Latest Source](https://github.com/openscilab/memor/archive/dev.zip)
- Run `pip install .`

## Usage
Memor provides `Prompt`, `Response`, and `Session` as abstractions by which you can save your conversation history much structured. You can set a `Session` object before starting a conversation, make a `Prompt` object from your prompt and a `Response` object from LLM's response. Then adding them to the created `Session` can keep the conversation history.

```py
from memor import Session, Prompt, Response
from memor import RenderFormat
from mistralai import Mistral

client = Mistral(api_key="YOUR_MISTRAL_API")
session = Session()
while True:
    user_input = input(">> You: ")
    prompt = Prompt(message=user_input)
    session.add_message(prompt) # Add user input to session
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=session.render(RenderFormat.OPENAI)  # Render the whole session history
    )
    print("<< MistralAI:", response.choices[0].message.content)
    response = Response(message=response.choices[0].message.content)
    session.add_message(response) # Add model response to session
```
Your conversations would carry the past interactions and LLM remembers your session's information:
```
>> You: Imagine you have 3 apples. You eat one of them. How many apples remain?
<< MistralAI: If you start with 3 apples and you eat one of them, you will have 2 apples remaining.
>> You: How about starting from 2 apples?
<< MistralAI: If you start with 2 apples and you eat one of them, you will have 1 apple remaining. Here's the simple math:
2 apples - 1 apple = 1 apple
```

In the following, we detail different abstraction levels Memor provides for the conversation artifacts.

### Prompt

The `Prompt` class is a core abstraction in Memor, representing a user prompt. The prompt can be associated with one or more responses from an LLM, with the first one being the most confident usually. It encapsulates not just the prompt text but also metadata, a template for rendering into the API endpoint, and serialization capabilities that enable saving and reusing prompts.

```py
from memor import Prompt, Response, PresetPromptTemplate
prompt = Prompt(
    message="Hello, how are you?",
    responses=[
        Response(message="I'm fine."),
        Response(message="I'm not fine."),
    ],
    template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD
)
prompt.render()
# Prompt: Hello, how are you?
# Response: I'm fine.
```

#### Parameters

| Name         | Type                                     | Description                                                |
| ------------ | ---------------------------------------- | ---------------------------------------------------------- |
| `message`    | `str`                                    | The core prompt message content                            |
| `responses`  | `List[Response]`                         | List of associated responses                               |
| `role`       | `Role`                                   | Role of the message sender (`USER`, `SYSTEM`, etc.)        |
| `tokens`     | `int`                                    | Token count                                                |
| `template`   | `PromptTemplate \| PresetPromptTemplate` | Template used to format the prompt                         |
| `file_path`  | `str`                                    | Path to load a prompt from a JSON file                     |
| `init_check` | `bool`                                   | Whether to verify template rendering during initialization |

#### Methods

| Method                               | Description                                                   |
| ------------------------------------ | ------------------------------------------------------------- |
| `add_response(response, index=None)` | Add a new response (append or insert)                         |
| `remove_response(index)`             | Remove the response at specified index                        |
| `select_response(index)`             | Mark a specific response as selected to be included in memory |
| `update_template(template)`          | Update the rendering template                                 |
| `render(render_format)`              | Render the prompt in a specified format                       |
| `to_json()` / `from_json(json)`      | Serialize or deserialize the prompt data                      |
| `save(path)` / `load(path)`          | Save or load prompt from file                                 |
| `update_message(message)`            | Update the prompt text                                        |
| `update_role(role)`                  | Change the prompt role                                        |
| `update_tokens(tokens)`              | Set a custom token count                                      |
| `check_render()`                     | Validate if the current prompt setup can render               |
| `estimate_tokens(method)`            | Estimate the token usage for the prompt                       |
| `copy()`                             | Clone the prompt                                              |
| `regenerate_id()`                    | Reset the unique identifier of the prompt                     |


### Response
The `Response` class represents an answer or a completion generated by a model given a prompt. It encapsulates metadata such as score, temperature, model, tokens, inference time, and more. It also provides utilities for JSON serialization, rendering in multiple formats, and import/export functionality.

```py
from memor import Response, Role, LLMModel
response = Response(
    message="Sure! Here's a summary.",
    score=0.94,
    temperature=0.7,
    model=LLMModel.GPT_4,
    inference_time=0.3
)
response.render()
# Sure! Here's a summary.
```

#### Parameters

| Name             | Type                | Description                                          |
| ---------------- | ------------------- | -----------------------------------------------------|
| `message`        | `str`               | The content of the response                          |
| `score`          | `float`             | Evaluation score representing the response quality   |
| `role`           | `Role`              | Role of the message sender (`USER`, `SYSTEM`, etc.)  |
| `temperature`    | `float`             | Sampling temperature                                 |
| `top_k`          | `int`               | `k` in top-k sampling method                         |
| `top_p`          | `float`             | `p` in top-p (nucleus) sampling                      |
| `tokens`         | `int`               | Number of tokens in the response                     |
| `inference_time` | `float`             | Time spent generating the response (seconds)         |
| `model`          | `LLMModel` \| `str` | Model used                                           |
| `gpu`            | `str`               | GPU model used                                       |
| `date`           | `datetime.datetime` | Timestamp of the creation                            |
| `file_path`      | `str`               | Path to load a saved response                        |

#### Methods

| Method                      | Description                                 |
| --------------------------- | ------------------------------------------- |
| `update_score(score)`       | Update the response score                   |
| `update_temperature(temp)`  | Set the generation temperature              |
| `update_top_k(k)`           | Set the top-k value                         |
| `update_top_p(p)`           | Set the top-p value                         |
| `update_model(model)`       | Set the model name or enum                  |
| `update_gpu(gpu_name)`      | Set the GPU model identifier                |
| `update_inference_time(t)`  | Set the inference time in seconds           |
| `update_message(msg)`       | Update the response message                 |
| `update_role(role)`         | Update the sender role                      |
| `update_tokens(tokens)`     | Set the number of tokens                    |
| `render(format)`            | Render the response in a specific format    |
| `to_json()` / `from_json()` | Serialize or deserialize to/from JSON       |
| `save(path)` / `load(path)` | Save or load the response to/from a file    |
| `to_dict()`                 | Convert the object to a Python dictionary   |
| `copy()`                    | Clone the response                          |
| `regenerate_id()`           | Reset the unique identifier of the response |



### Prompt Templates
The `PromptTemplate` class provides a structured interface for managing, storing, and customizing text prompt templates used in prompt engineering tasks. This class supports template versioning, metadata tracking, file-based persistence, and integration with preset template formats. It is a core component of the memor library, designed to facilitate reproducible and organized prompt workflows for LLMs.

```py
from memor import Prompt, PromptTemplate
template = PromptTemplate(content="{instruction}, {prompt[message]}", custom_map={"instruction": "Hi"})
prompt = Prompt(message="How are you?", template=template)
prompt.render()
'Hi, How are you?'
```

#### Parameters

| Name         | Type             | Default | Description                                            |
| ------------ | ---------------- | ------- | ------------------------------------------------------ |
| `title`      | `str`            | `None`  | The template name                                      |
| `content`    | `str`            | `None`  | The template content string with placeholders          |
| `custom_map` | `Dict[str, str]` | `None`  | A dictionary of custom variables used in the template  |
| `file_path`  | `str`            | `None`  | Path to a JSON file to load the template from          |

#### Methods

| Method                                               | Description                                            |
| ---------------------------------------------------- | ------------------------------------------------------ |
| `update_title(title)`                                | Update the template title                              |
| `update_content(content)`                            | Update the template content                            |
| `update_map(custom_map)`                             | Update the custom variable map                         |
| `get_size()`                                         | Return the size (in bytes) of the JSON representation  |
| `save(path)` / `load(path)`                          | Save or load the template to/from a file               |
| `to_json()` / `from_json()`                          | Serialize or deserialize to/from JSON                  |
| `to_dict()`                                          | Convert the template to a plain Python dictionary      |
| `copy()`                                             | Return a shallow copy of the template instance         |

#### Preset Templates

Memor provides a variety of pre-defined `PromptTemplate`s to control how prompts and responses are rendered. Each template is prefixed by an optional instruction string and includes variations for different formatting styles. Following are different variants of parameters:

+ `INSTRUCTION1`: "*I'm providing you with a history of a previous conversation. Please consider this context when responding to my new question.*"
+ `INSTRUCTION2`: "*Here is the context from a prior conversation. Please learn from this information and use it to provide a thoughtful and context-aware response to my next questions.*"
+  `INSTRUCTION3`: "*I am sharing a record of a previous discussion. Use this information to provide a consistent and relevant answer to my next query.*"

| **Template Title** | **Description** |
|--------------|----------|
| `PROMPT` | Only includes the prompt message |
| `RESPONSE` | Only includes the response message |
| `RESPONSE0` to `RESPONSE3` | Include specific responses from a list of multiple responses |
| `PROMPT_WITH_LABEL` | Prompt with a "Prompt: " prefix |
| `RESPONSE_WITH_LABEL` | Response with a "Response: " prefix |
| `RESPONSE0_WITH_LABEL` to `RESPONSE3_WITH_LABEL` | Labeled response for the i-th response. |
| `PROMPT_RESPONSE_STANDARD` | Includes both labeled prompt and response on a single line |
| `PROMPT_RESPONSE_FULL` | A detailed multi-line representation including role, date, model, etc. |

You can access them using:

```py
from memor import PresetPromptTemplate
template = PresetPromptTemplate.INSTRUCTION1.PROMPT_RESPONSE_STANDARD
```

### Session
The `Session` class represents a conversation session composed of `Prompt` and `Response` messages. It supports creation, modification, saving, loading, searching, rendering, and token estimation — offering a structured way to manage LLM interaction histories. Each session tracks metadata such as title, creation/modification time, render count, and message activation (masking) status.

```py
from memor import Session, Prompt, Response
session = Session(title="Q&A Session", messages=[
            Prompt(message="What is the capital of France?"),
            Response(message="The capital of France is Paris.")
            ])
session.add_message(Prompt(message="What is the population of Paris?"))
print(session.render())
# What is the capital of France?
# The capital of France is Paris.
# What is the population of Paris?

results = session.search("Paris")
print("Found at indices:", results)
# Found at indices: [1, 2]

tokens = session.estimate_tokens()
print("Estimated tokens:", tokens)
# Estimated tokens: 35
```

#### Parameters

| Parameter    | Type                                 | Description                                   |
| ------------ | ------------------------------------ | --------------------------------------------- |
| `title`      | `str`                                | The title of the session                      |
| `messages`   | `List[Prompt or Response]`           | The list of initial messages                  |
| `init_check` | `bool`                               | Whether to check rendering at initialization  |
| `file_path`  | `str`                                | The Path to a saved session file              |

#### Methods

| Method                                                            | Description                                                   |
| ----------------------------------------------------------------- | ------------------------------------------------------------- |
| `add_message(message, status=True, index=None)`                   | Add a `Prompt` or `Response` to the session                   |
| `remove_message(identifier)`                                      | Remove a message by index or ID                               |
| `remove_message_by_index(index)`                                  | Remove a message by numeric index                             |
| `remove_message_by_id(message_id)`                                | Remove a message by its unique ID                             |
| `update_title(title)`                                             | Update the title of the session                               |
| `update_messages(messages, status=None)`                          | Replace all messages and optionally update their status list  |
| `update_messages_status(status)`                                  | Update the message status without changing the content        |
| `clear_messages()`                                                | Remove all messages from the session                          |
| `get_message(identifier)`                                         | Retrieve a message by index, slice, or ID                     |
| `get_message_by_index(index)`                                     | Get a message by integer index or slice                       |
| `get_message_by_id(message_id)`                                   | Get a message by its unique ID                                |
| `enable_message(index)`                                           | Mark the message at the given index as active                 |
| `disable_message(index)`                                          | Mark the message as inactive (masked)                         |
| `mask_message(index)`                                             | Alias for `disable_message()`                                 |
| `unmask_message(index)`                                           | Alias for `enable_message()`                                  |
| `search(query, use_regex=False, case_sensitive=False)`            | Search for a string or regex pattern in the messages          |
| `render(render_format=RenderFormat.DEFAULT, enable_counter=True)` | Render the session in the specified format                    |
| `check_render()`                                                  | Return `True` if the session renders without error            |
| `save(path)` / `load(path)`                                       | Save or load the session to/from a file                       |
| `to_json()` / `from_json()`                                       | Serialize or deserialize the session to/from JSON             |
| `to_dict()`                                                       | Return a Python dict representation of the session            |
| `get_size()`                                                      | Return session size in bytes (JSON-encoded)                   |
| `copy()`                                                          | Return a shallow copy of the session                          |
| `estimate_tokens(method=TokensEstimator.DEFAULT)`                 | Estimate the token count of the session content               |


## Examples
You can find more real-world usage of Memor in the [`examples`](https://github.com/openscilab/memor/tree/main/examples) directory.
This directory includes concise and practical Python scripts that demonstrate key features of Memor library.

## Issues & bug reports

Just fill an issue and describe it. We'll check it ASAP! or send an email to [memor@openscilab.com](mailto:memor@openscilab.com "memor@openscilab.com"). 

- Please complete the issue template
 
You can also join our discord server

<a href="https://discord.gg/cZxGwZ6utB">
  <img src="https://img.shields.io/discord/1064533716615049236.svg?style=for-the-badge" alt="Discord Channel">
</a>

## Show your support


### Star this repo

Give a ⭐️ if this project helped you!

### Donate to our project
If you do like our project and we hope that you do, can you please support us? Our project is not and is never going to be working for profit. We need the money just so we can continue doing what we do ;-) .			

<a href="https://openscilab.com/#donation" target="_blank"><img src="https://github.com/openscilab/memor/raw/main/otherfiles/donation.png" height="90px" width="270px" alt="Memor Donation"></a>