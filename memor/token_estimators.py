# -*- coding: utf-8 -*-
"""Token estimators functions."""

import re
from enum import Enum
from typing import Set, List


def _is_code_snippet(message: str) -> bool:
    """Check if the message is a code snippet based on common coding symbols."""
    return bool(re.search(r"[=<>+\-*/{}();]", message))


def _preprocess_message(message: str, is_code: bool) -> str:
    """Preprocess message by replacing contractions in non-code text."""
    if not is_code:
        return re.sub(r"(?<=\w)'(?=\w)", " ", message)
    return message


def _tokenize_message(message: str) -> List[str]:
    """Tokenize the message based on words, symbols, and numbers."""
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[+\-*/=<>(){}[\],.:;]|\"[^\"]*\"|'[^']*'|\d+|\S", message)


def _count_code_tokens(token: str, common_keywords: Set[str]) -> int:
    """Count tokens in code snippets considering different token types."""
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


def _count_text_tokens(token: str, common_prefixes: set, common_suffixes: Set[str]) -> int:
    """Count tokens in regular text considering prefixes, suffixes, and subwords."""
    if len(token) == 1 and not token.isalnum():
        return 1
    if token.isdigit():
        return max(1, len(token) // 4)
    prefix_count = sum(1 for prefix in common_prefixes if token.startswith(prefix) and len(token) > len(prefix) + 3)
    suffix_count = sum(1 for suffix in common_suffixes if token.endswith(suffix) and len(token) > len(suffix) + 3)
    subword_count = max(1, len(re.findall(r"[aeiou]+|[^aeiou]+", token)) // 2)
    return prefix_count + suffix_count + subword_count


def universal_token_estimator(message: str) -> int:
    """Estimate the number of tokens in a given text or code snippet."""
    is_code = _is_code_snippet(message)
    message = _preprocess_message(message, is_code)
    tokens = _tokenize_message(message)

    common_keywords = {"if", "else", "elif", "while", "for", "def", "return", "import", "from", "class",
                       "try", "except", "finally", "with", "as", "break", "continue", "pass", "lambda",
                       "True", "False", "None", "and", "or", "not", "in", "is", "global", "nonlocal"}
    common_prefixes = {"un", "re", "in", "dis", "pre", "mis", "non", "over", "under", "sub", "trans"}
    common_suffixes = {"ing", "ed", "ly", "es", "s", "ment", "able", "ness", "tion", "ive", "ous"}

    return sum(
        _count_code_tokens(
            token,
            common_keywords) if is_code else _count_text_tokens(
            token,
            common_prefixes,
            common_suffixes) for token in tokens)


def openai_token_estimator(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Estimate the number of tokens in a given text for a specified OpenAI model."""
    if not isinstance(text, str):
        return 0

    char_count = len(text)
    token_estimate = char_count / 4

    token_estimate += (text.count(" ") + sum(1 for char in text if char in ",.?!;:")) * 0.5
    if any(keyword in text for keyword in ["```", "def", "import"]):
        token_estimate *= 1.1
    token_estimate += text.count("\n") * 0.8
    token_estimate += sum(len(word) / 10 for word in text.split() if len(word) > 15)
    if "http" in text:
        token_estimate *= 1.1
    token_estimate += sum(1 for char in text if ord(char) > 10000) * 0.8
    if "gpt-4" in model.lower():
        token_estimate *= 1.05

    return int(max(1, token_estimate))


class TokenEstimator(Enum):
    """Token estimator enum."""

    UNIVERSAL = universal_token_estimator
    OPENAI = openai_token_estimator
    DEFAULT = UNIVERSAL
