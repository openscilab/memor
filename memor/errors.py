# -*- coding: utf-8 -*-
"""Memor errors."""


class MemorValidationError(ValueError):
    """Base class for validation errors in Memor."""

    pass


class MemorRenderError(Exception):
    """Base class for render error in Memor."""

    pass
