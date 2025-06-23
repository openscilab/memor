<div align="center">
    <h1>Memor: A Python Library for Managing and Transferring Conversational Memory Across LLMs</h1>
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
Memor is a library designed to help users manage the memory of their interactions with Large Language Models (LLMs).
It enables users to seamlessly access and utilize the history of their conversations when prompting LLMs.
That would create a more personalized and context-aware experience.
Memor stands out by allowing users to transfer conversational history across different LLMs, eliminating cold starts where models don't have information about user and their preferences.
Users can select specific parts of past interactions with one LLM and share them with another.
By bridging the gap between isolated LLM instances, Memor revolutionizes the way users interact with AI by making transitions between models smoother.

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
- Run `pip install memor==0.7`
### Source code
- Download [Version 0.7](https://github.com/openscilab/memor/archive/v0.7.zip) or [Latest Source](https://github.com/openscilab/memor/archive/dev.zip)
- Run `pip install .`

## Usage
Define your prompt and the response(s) to that; Memor will wrap it into a object with a templated representation.
You can create a session by combining multiple prompts and responses, gradually building it up:

```pycon
>>> from memor import Session, Prompt, Response, Role
>>> from memor import PresetPromptTemplate, RenderFormat, LLMModel
>>> response = Response(message="I am fine.", model=LLMModel.GPT_4, role=Role.ASSISTANT, temperature=0.9, score=0.9)
>>> prompt = Prompt(message="Hello, how are you?",
                    responses=[response],
                    role=Role.USER,
                    template=PresetPromptTemplate.INSTRUCTION1.PROMPT_RESPONSE_STANDARD)
>>> system_prompt = Prompt(message="You are a friendly and informative AI assistant designed to answer questions on a wide range of topics.",
                    role=Role.SYSTEM)
>>> session = Session(messages=[system_prompt, prompt])
>>> session.render(RenderFormat.OPENAI)
```

The rendered output will be a list of messages formatted for compatibility with the OpenAI API.

```json
[{"content": "You are a friendly and informative AI assistant designed to answer questions on a wide range of topics.", "role": "system"},
 {"content": "I'm providing you with a history of a previous conversation. Please consider this context when responding to my new question.\n"
             "Prompt: Hello, how are you?\n"
             "Response: I am fine.",
  "role": "user"}]
```

### Prompt Templates

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

```pycon
>>> from memor import PresetPromptTemplate
>>> template = PresetPromptTemplate.INSTRUCTION1.PROMPT_RESPONSE_STANDARD
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

```pycon
>>> template = PromptTemplate(content="{instruction}, {prompt[message]}", custom_map={"instruction": "Hi"})
>>> prompt = Prompt(message="How are you?", template=template)
>>> prompt.render()
Hi, How are you?
```

By using this dynamic structure, you can create flexible and sophisticated prompt templates with Memor. You can design specific schemas for your conversational or instructional formats when interacting with LLM.

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