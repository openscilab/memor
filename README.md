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
        <td align="center"><a href="https://codebeat.co/projects/github-com-openscilab-memor-main"><img alt="codebeat badge" src="https://codebeat.co/badges/cd9a4239-280d-415d-95dd-faeea9270668"></a></td>
    </tr>
</table>


## Installation

### PyPI
- Check [Python Packaging User Guide](https://packaging.python.org/installing/)
- Run `pip install memor==0.3`
### Source code
- Download [Version 0.3](https://github.com/openscilab/memor/archive/v0.3.zip) or [Latest Source](https://github.com/openscilab/memor/archive/dev.zip)
- Run `pip install .`

## Usage
Define your prompt and the response(s) to that; Memor will wrap it into a object with a templated representation.
You can create a session by combining multiple prompts and responses, gradually building it up:

```pycon
>>> from memor import Session, Prompt, Response, Role
>>> from memor import PresetPromptTemplate, RenderFormat
>>> response = Response(message="I am fine.", role=Role.ASSISTANT, temperature=0.9, score=0.9)
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

## Issues & bug reports

Just fill an issue and describe it. We'll check it ASAP! or send an email to [memor@openscilab.com](mailto:memor@openscilab.com "memor@openscilab.com"). 

- Please complete the issue template
 
You can also join our discord server

<a href="https://discord.gg/cZxGwZ6utB">
  <img src="https://img.shields.io/discord/1064533716615049236.svg?style=for-the-badge" alt="Discord Channel">
</a>

## References

## Show your support


### Star this repo

Give a ⭐️ if this project helped you!

### Donate to our project
If you do like our project and we hope that you do, can you please support us? Our project is not and is never going to be working for profit. We need the money just so we can continue doing what we do ;-) .			

<a href="https://openscilab.com/#donation" target="_blank"><img src="https://github.com/openscilab/memor/raw/main/otherfiles/donation.png" height="90px" width="270px" alt="Memor Donation"></a>