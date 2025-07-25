# -*- coding: utf-8 -*-
"""Setup module."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requires() -> list:
    """Read requirements.txt."""
    requirements = open("requirements.txt", "r").read()
    return list(filter(lambda x: x != "", requirements.split()))


def read_description() -> str:
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        with open("CHANGELOG.md") as c:
            description += "\n"
            description += c.read()
        return description
    except Exception:
        return '''With Memor, LLM users can store their conversation history using an intuitive and structured data format.
It abstracts user prompts and model responses into a "Session", a sequence of message exchanges that forms the basic unit of interaction.
In addition to the content, each message can include generation details like decoding temperature and token count.
Therefore users could create comprehensive and reproducible logs of their interactions.
Because of the model-agnostic design, users can begin a conversation with one LLM and switch to another keeping the context.
For example, they might use a retrieval-augmented model (like a RAG system) to gather relevant context for a math problem, then switch to a model better suited for reasoning to solve it featuring the retried information that is presented in the chat-history by Memor.

Memor also lets users select and share specific parts of past conversations across different models. This means users are not only able to reproduce and review previous chats through structured logs, but can also flexibly transfer the content of their conversations between LLMs.
In nutshell, Memor makes it easy to manage and reuse conversations with large language models effectively.
'''


setup(
    name='memor',
    packages=[
        'memor', ],
    version='0.8',
    description='Memor: Reproducible Structured Memory for LLMs',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    author='Memor Development Team',
    author_email='memor@openscilab.com',
    url='https://github.com/openscilab/memor',
    download_url='https://github.com/openscilab/memor/tarball/v0.8',
    keywords="llm memory management conversational history ai agent",
    project_urls={
            'Source': 'https://github.com/openscilab/memor',
    },
    install_requires=get_requires(),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    license='MIT',
)
