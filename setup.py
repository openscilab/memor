# -*- coding: utf-8 -*-
"""Setup module."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requires():
    """Read requirements.txt."""
    requirements = open("requirements.txt", "r").read()
    return list(filter(lambda x: x != "", requirements.split()))


def read_description():
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
        return '''Memor is a library designed to help users manage the memory of their interactions with Large Language Models (LLMs).
It enables users to seamlessly access and utilize the history of their conversations when prompting LLMs.
That would create a more personalized and context-aware experience.
Memor stands out by allowing users to transfer conversational history across different LLMs, eliminating cold starts where models don\'t have information about user and their preferences.
Users can select specific parts of past interactions with one LLM and share them with another.By bridging the gap between isolated LLM instances, Memor revolutionizes the way users interact with AI by making transitions between models smoother.'''


setup(
    name='memor',
    packages=[
        'memor', ],
    version='0.3',
    description='Memor: A Python Library for Managing and Transferring Conversational Memory Across LLMs',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    author='Memor Development Team',
    author_email='memor@openscilab.com',
    url='https://github.com/openscilab/memor',
    download_url='https://github.com/openscilab/memor/tarball/v0.3',
    keywords="llm memory management conversational history ai agent",
    project_urls={
            'Source': 'https://github.com/openscilab/memor',
    },
    install_requires=get_requires(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
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
