# -*- coding: utf-8 -*-
"""Token estimators functions."""

import re

def universal_token_estimator(message: str) -> int:
    """
    Estimate the number of tokens in a given text or code snippet.

    :param message: The input message (text or code).
    :return: The estimated number of tokens.
    """
    is_code = bool(re.search(r"[=<>+\-*/{}();]", message))
    if not is_code:
        message = re.sub(r"(?<=\w)'(?=\w)", " ", message)
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[+\-*/=<>(){}[\],.:;]|\"[^\"]*\"|'[^']*'|\d+|\S", message)
    
    common_keywords = {
        "if", "else", "elif", "while", "for", "def", "return", "import", "from", "class",
        "try", "except", "finally", "with", "as", "break", "continue", "pass", "lambda",
        "True", "False", "None", "and", "or", "not", "in", "is", "global", "nonlocal"
    }
    common_prefixes = {"un", "re", "in", "dis", "pre", "mis", "non", "over", "under", "sub", "trans"}
    common_suffixes = {"ing", "ed", "ly", "es", "s", "ment", "able", "ness", "tion", "ive", "ous"}

    token_count = 0
    for token in tokens:
        if is_code:
            if token in common_keywords:
                token_count += 1
                continue
            if len(token) == 1 and re.match(r"[+\-*/=<>(){}[\],.:;]", token):
                token_count += 1
                continue
            if token.isdigit():
                token_count += max(1, len(token) // 4)
                continue
            if token.startswith(("'", '"')) and token.endswith(("'", '"')):
                token_count += max(1, len(token) // 6)
                continue

            if "_" in token:  # snake_case → split by "_"
                token_count += len(token.split("_"))
            elif re.search(r"[A-Z]", token):  # CamelCase → split at uppercase letters
                token_count += len(re.findall(r"[A-Z][a-z]*", token))
            else:
                token_count += 1  # Single-word identifiers
        else:
            if len(token) == 1 and not token.isalnum():
                token_count += 1
                continue
            if token.isdigit():
                token_count += max(1, len(token) // 4)
                continue

            prefix_count = sum(1 for prefix in common_prefixes if token.startswith(prefix) and len(token) > len(prefix) + 3)
            suffix_count = sum(1 for suffix in common_suffixes if token.endswith(suffix) and len(token) > len(suffix) + 3)
            subword_count = max(1, len(re.findall(r"[aeiou]+|[^aeiou]+", token)) // 2)

            token_count += prefix_count + suffix_count + subword_count

    return token_count


def openai_token_estimator(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Estimates the number of tokens in a given text for a specified OpenAI model.

    This function provides a rough estimate without relying on external libraries.
    It's based on observed tokenization patterns and should be used as an approximation.

    :param text: The text to estimate tokens for.
    :param model: The OpenAI model (e.g., "gpt-3.5-turbo", "gpt-4"). Defaults to "gpt-3.5-turbo".
    :return: An estimated number of tokens.
    """
    if not isinstance(text, str):
        return 0

    char_count = len(text)
    token_estimate = char_count / 4

    # 1. Spaces and punctuation often become separate tokens.
    space_count = text.count(" ")
    punctuation_count = sum(1 for char in text if char in ",.?!;:")
    token_estimate += (space_count + punctuation_count) * 0.5 # account for some of these being their own tokens

    # 2. Code and special characters may be tokenized differently.
    if "```" in text or "def" in text or "import" in text:
        token_estimate *= 1.1 # add a 10% penalty for possible code.

    # 3. Handle newlines
    newline_count = text.count("\n")
    token_estimate += newline_count * 0.8 # newlines are often tokens

    # 4. Handle very long words or sequences of characters without spaces
    words = text.split()
    for word in words:
        if len(word) > 15:
            token_estimate += len(word) / 10 # very long words could be split.

    # 5. very very basic url handling.
    if "http" in text:
        token_estimate *= 1.1

    # 6. Basic emoji handling.
    emoji_count = sum(1 for char in text if ord(char) > 10000)
    token_estimate+= emoji_count *0.8

    # 7. Model-specific adjustment (very rudimentary)
    if "gpt-4" in model.lower():
        token_estimate *= 1.05 # GPT-4 sometimes uses more tokens.

    return int(max(1, token_estimate)) # Ensure at least 1 token
