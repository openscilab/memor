# -*- coding: utf-8 -*-
"""Tokens estimator functions."""

import re
from enum import Enum
from typing import Set, List
from .keywords import PROGRAMMING_LANGUAGES_KEYWORDS
from .keywords import COMMON_PREFIXES, COMMON_SUFFIXES


def _is_code_snippet(message: str) -> bool:
    """
    Check if the message is a code snippet based on common coding symbols.

    :param message: The input message to check.
    :return: Boolean indicating if the message is a code snippet.
    """
    return bool(re.search(r"[=<>+\-*/{}();]", message))


def _preprocess_message(message: str, is_code: bool) -> str:
    """
    Preprocess message by replacing contractions in non-code text.

    :param message: The input message to preprocess.
    :param is_code: Boolean indicating if the message is a code.
    :return: Preprocessed message.
    """
    if not is_code:
        return re.sub(r"(?<=\w)'(?=\w)", " ", message)
    return message


def _tokenize_message(message: str) -> List[str]:
    """
    Tokenize the message based on words, symbols, and numbers.

    :param message: The input message to tokenize.
    :return: List of tokens.
    """
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[+\-*/=<>(){}[\],.:;]|\"[^\"]*\"|'[^']*'|\d+|\S", message)


def _count_code_tokens(token: str, common_keywords: Set[str]) -> int:
    """
    Count tokens in code snippets considering different token types.

    :param token: The token to count.
    :param common_keywords: Set of common keywords in programming languages.
    :return: Count of tokens.
    """
    if token in common_keywords or re.match(r"[+\-*/=<>(){}[\],.:;]", token):
        return 1
    if token.isdigit():
        return max(1, len(token) // 4)
    if token.startswith(("'", '"')) and token.endswith(("'", '"')):
        return max(1, len(token) // 6)
    if "_" in token:
        return len(token.split("_"))
    if re.search(r"[A-Z]", token):
        return len(re.findall(r"[A-Z][a-z]*", token))
    return 1


def _count_text_tokens(token: str, prefixes: Set[str], suffixes: Set[str]) -> int:
    """
    Count tokens in text based on prefixes, suffixes, and subwords.

    :param token: The token to count.
    :param prefixes: Set of common prefixes.
    :param suffixes: Set of common suffixes.
    :return: Token count.
    """
    if len(token) == 1 and not token.isalnum():
        return 1
    if token.isdigit():
        return max(1, len(token) // 4)
    prefix_count = sum(token.startswith(p) for p in prefixes if len(token) > len(p) + 3)
    suffix_count = sum(token.endswith(s) for s in suffixes if len(token) > len(s) + 3)
    parts = re.findall(r"[aeiou]+|[^aeiou]+", token)
    subword_count = max(1, len(parts) // 2)

    return prefix_count + suffix_count + subword_count


def universal_tokens_estimator(message: str) -> int:
    """
    Estimate the number of tokens in a given text or code snippet.

    :param message: The input text or code snippet to estimate tokens for.
    :return: Estimated number of tokens.
    """
    is_code = _is_code_snippet(message)
    message = _preprocess_message(message, is_code)
    tokens = _tokenize_message(message)

    return sum(
        _count_code_tokens(
            token,
            PROGRAMMING_LANGUAGES_KEYWORDS) if is_code else _count_text_tokens(
            token,
            COMMON_PREFIXES,
            COMMON_SUFFIXES) for token in tokens)


def _openai_tokens_estimator(text: str) -> int:
    """
    Estimate the number of tokens in a given text for OpenAI's models.

    :param text: The input text to estimate tokens for.
    :return: Estimated number of tokens.
    """
    char_count = len(text)
    token_estimate = char_count / 4

    space_count = text.count(" ")
    punctuation_count = sum(1 for char in text if char in ",.?!;:")
    token_estimate += (space_count + punctuation_count) * 0.5

    if any(keyword in text for keyword in PROGRAMMING_LANGUAGES_KEYWORDS):
        token_estimate *= 1.1

    newline_count = text.count("\n")
    token_estimate += newline_count * 0.8

    long_word_penalty = sum(len(word) / 10 for word in text.split() if len(word) > 15)
    token_estimate += long_word_penalty

    if "http" in text:
        token_estimate *= 1.1

    rare_char_count = sum(1 for char in text if ord(char) > 10000)
    token_estimate += rare_char_count * 0.8

    return token_estimate


def openai_tokens_estimator_gpt_3_5(text: str) -> int:
    """
    Estimate the number of tokens in a given text for OpenAI's GPT-3.5 Turbo model.

    :param text: The input text to estimate tokens for.
    :return: Estimated number of tokens.
    """
    token_estimate = _openai_tokens_estimator(text)
    return int(max(1, token_estimate))


def openai_tokens_estimator_gpt_4(text: str) -> int:
    """
    Estimate the number of tokens in a given text for OpenAI's GPT-4 model.

    :param text: The input text to estimate tokens for.
    :return: Estimated number of tokens.
    """
    token_estimate = _openai_tokens_estimator(text)
    token_estimate *= 1.05  # Adjusting for GPT-4's tokenization
    return int(max(1, token_estimate))


class TokensEstimator(Enum):
    """Token estimator enum."""

    UNIVERSAL = universal_tokens_estimator
    OPENAI_GPT_3_5 = openai_tokens_estimator_gpt_3_5
    OPENAI_GPT_4 = openai_tokens_estimator_gpt_4
    DEFAULT = UNIVERSAL
