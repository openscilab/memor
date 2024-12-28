# -*- coding: utf-8 -*-
"""Memor functions."""


def _load_prompt_from_response_obj(response_obj):
    """Fetch some Prompt fields from an OpenAI response API object."""
    responses = []
    role = None
    for choice in response_obj["choices"]:
        responses.append(choice["message"]["content"])
        role = choice["message"]["role"]
    model = response_obj["model"]
    return dict(
        responses=responses,
        role=role,
        model=model
    )
