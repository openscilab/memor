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
With Memor, LLM users can store their conversation history using an intuitive and structured data format.
It abstracts user prompts and model responses into a "Session", a sequence of message exchanges that forms the basic unit of interaction.
In addition to the content, each message can include generation details like decoding temperature and token count.
Therefore users could create comprehensive and reproducible logs of their interactions.
Because of the model-agnostic design, users can begin a conversation with one LLM and switch to another keeping the context.
For example, they might use a retrieval-augmented model (like a RAG system) to gather relevant context for a math problem, then switch to a model better suited for reasoning to solve it featuring the retrieved information that is presented in the chat-history by Memor.
</p>

<p align="justify">
Memor also lets users select and share specific parts of past conversations across different models. This means users are not only able to reproduce and review previous chats through structured logs, but can also flexibly transfer the content of their conversations between LLMs.
In a nutshell, Memor makes it easy to manage and reuse conversations with large language models effectively.
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
Let's say you want to have conversation session with [MistralAI](https://mistral.ai/)'s LLM through API call. You have `mistral_client` all set-up with the following code:
```py
from mistralai import Mistral

mistral_client = Mistral(api_key="YOUR_MISTRAL_API")
```

Then you may use this client in a loop for a unending interaction with it in CLI. Using the following code snippet you can have a running example for chatting with LLM easily:
```py
while True:
    user_input = input("You: ")
    response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    print("MistralAI:", response.choices[0].message.content)
```

Let's try it with an example:
```
You: Imagine you have 3 apples. You eat one of them. How many apples remain?
MistralAI: If you start with 3 apples and you eat one of them, you would have 2 apples remaining.
You: How about starting from 2 apples?
MistralAI: If you start with 2 apples and add 2 more, you'll have 4 apples.
```
Wait what? Why it adds 2 more apples?
Ops! We're not using the history of conversation and we're starting over after each call. That's why it can't remember the actual problem and it hallucinated.

### ❌ Messy solution
Well you can have a `history` list and fill it up as you go through like bellow, but that's not the best approach. You should take care of this history and can't save more details rather than messages there. It also gets messy when you want to save different things in different codes using the same approach.
```py
history = []
while True:
    user_input = input("You: ")
    response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=[
            *history,
            {"role": "user", "content": user_input}
        ]
    )
    print("MistralAI:", response.choices[0].message.content)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response.choices[0].message.content})
```

### ✅ Memor solution
Memor provides `Prompt`, `Response`, and `Session` as abstraction by which you can save your conversation history much structured.
You can set a `Session` object before starting the conversation, make a `Prompt` object from your prompt and a `Response` object from LLM's response. Then adding them to the created `Session` can keep the conversation history.

```py
from memor import Session, Prompt, Response
from memor import RenderFormat

session = Session()
while True:
    user_input = input("You: ")
    prompt = Prompt(message=user_input)
    session.add_message(prompt) # Add user input to session
    response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=session.render(RenderFormat.OPENAI)  # Render the whole session history
    )
    print("MistralAI:", response.choices[0].message.content)
    response = Response(message=response.choices[0].message.content)
    session.add_message(response) # Add model response to session
```
Then your conversations would always carry past interaction logs and have more meaningful conversations; Let's try the example we started with again:
```
You: Imagine you have 3 apples. You eat one of them. How many apples remain?
MistralAI: If you start with 3 apples and you eat one of them, you will have 2 apples remaining.
You: How about starting from 2 apples?
MistralAI: If you start with 2 apples and you eat one of them, you will have 1 apple remaining. Here's the simple math:
2 apples - 1 apple = 1 apple
```
Hurray! It's working now.

Memor is doing much more than what you've just saw. In the following, we describe different abstracted classes to show more features of Memor.

### Prompt

The `Prompt` class is a core abstraction in Memor, representing a user input (or query) that can be associated with one or more responses from an LLM. It encapsulates not just the prompt text but also metadata, a template for rendering, role designation, and serialization capabilities.

```pycon
>>> from memor import Prompt, Response, PresetPromptTemplate
>>> responses = [
    Response(message="I'm fine."),
    Response(message="I'm not fine."),
]
>>> prompt = Prompt(
    message="Hello, how are you?",
    responses=responses,
    template=PresetPromptTemplate.BASIC.PROMPT_RESPONSE_STANDARD
)
>>> print(prompt.render())
Prompt: Hello, how are you?
Response: I'm fine.
```

#### Parameters

| Name         | Type                                     | Description                                                |
| ------------ | ---------------------------------------- | ---------------------------------------------------------- |
| `message`    | `str`                                    | The core prompt message content                            |
| `responses`  | `List[Response]`                         | Optional list of associated responses                      |
| `role`       | `Role`                                   | Role of the message sender (`USER`, `SYSTEM`, etc.)        |
| `tokens`     | `int`                                    | Optional token count override                              |
| `template`   | `PromptTemplate \| PresetPromptTemplate` | Template used to format the prompt                         |
| `file_path`  | `str`                                    | Optional path to load a prompt from a JSON file            |
| `init_check` | `bool`                                   | Whether to verify template rendering during initialization |

#### Methods

| Method                               | Description                                 |
| ------------------------------------ | ------------------------------------------- |
| `add_response(response, index=None)` | Add a new response (append or insert)       |
| `remove_response(index)`             | Remove response at specified index          |
| `select_response(index)`             | Mark a specific response as selected        |
| `update_template(template)`          | Update the rendering template               |
| `render(render_format)`              | Render the prompt in a specified format     |
| `to_json()` / `from_json(json)`      | Serialize or deserialize prompt data        |
| `save(path)` / `load(path)`          | Save or load prompt from file               |
| `update_message(message)`            | Update the prompt text                      |
| `update_role(role)`                  | Change the prompt role                      |
| `update_tokens(tokens)`              | Set a custom token count                    |
| `copy()` / `regenerate_id()`         | Clone prompt or reset ID                    |
| `check_render()`                     | Validate if current prompt setup can render |
| `estimate_tokens(method)`            | Estimate token usage for the prompt         |


### Response
[TBD]

### Prompt Templates
[TBC]
#### Preset Templates

Memor provides a variety of pre-defined prompt templates to control how prompts and responses are rendered. Each template is prefixed by an optional instruction string and includes variations for different formatting styles. Following are different variants of parameters:

| **Instruction Name** | **Description** |
|---------------|----------|
| `INSTRUCTION1` | "I'm providing you with a history of a previous conversation. Please consider this context when responding to my new question." |
| `INSTRUCTION2` | "Here is the context from a prior conversation. Please learn from this information and use it to provide a thoughtful and context-aware response to my next questions." |
| `INSTRUCTION3` | "I am sharing a record of a previous discussion. Use this information to provide a consistent and relevant answer to my next query." |

| **Template Title** | **Description** |
|--------------|----------|
| `PROMPT` | Only includes the prompt message. |
| `RESPONSE` | Only includes the response message. |
| `RESPONSE0` to `RESPONSE3` | Include specific responses from a list of multiple responses. |
| `PROMPT_WITH_LABEL` | Prompt with a "Prompt: " prefix. |
| `RESPONSE_WITH_LABEL` | Response with a "Response: " prefix. |
| `RESPONSE0_WITH_LABEL` to `RESPONSE3_WITH_LABEL` | Labeled response for the i-th response. |
| `PROMPT_RESPONSE_STANDARD` | Includes both labeled prompt and response on a single line. |
| `PROMPT_RESPONSE_FULL` | A detailed multi-line representation including role, date, model, etc. |

You can access them like this:

```py
from memor import PresetPromptTemplate

template = PresetPromptTemplate.INSTRUCTION1.PROMPT_RESPONSE_STANDARD
```

#### Custom Templates

You can define custom templates for your prompts using the `PromptTemplate` class. This class provides two key parameters that control its functionality:

+ `content`: A string that defines the template structure, following Python string formatting conventions. You can include dynamic fields using placeholders like `{field_name}`, which will be automatically populated using attributes from the prompt object. Some common examples of auto-filled fields are shown below:

| **Prompt Object Attribute**           | **Placeholder Syntax**             | **Description**                              |
|--------------------------------------|------------------------------------|----------------------------------------------|
| `prompt.message`                     | `{prompt[message]}`                | The main prompt message                       |
| `prompt.selected_response`           | `{prompt[response]}`               | The selected response for the prompt          |
| `prompt.date_modified`               | `{prompt[date_modified]}`          | Timestamp of the last modification            |
| `prompt.responses[2].message`        | `{responses[2][message]}`          | Message from the response at index 2          |
| `prompt.responses[0].inference_time` | `{responses[0][inference_time]}`   | Inference time for the response at index 0    |


+ `custom_map`: In addition to the attributes listed above, you can define and insert custom placeholders (e.g., `{field_name}`) and provide their values through a dictionary. When rendering the template, each placeholder will be replaced with its corresponding value from `custom_map`.


Suppose you want to prepend an instruction to every prompt message. You can define and use a template as follows:

```py
template = PromptTemplate(content="{instruction}, {prompt[message]}", custom_map={"instruction": "Hi"})
prompt = Prompt(message="How are you?", template=template)
prompt.render()
Hi, How are you?
```

By using this dynamic structure, you can create flexible and sophisticated prompt templates with Memor. You can design specific schemas for your conversational or instructional formats when interacting with LLM.

### Session
[TBD]

## Examples
You can explore real-world usage of Memor in the [`examples`](https://github.com/openscilab/memor/tree/main/examples) directory.
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