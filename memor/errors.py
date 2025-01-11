# -*- coding: utf-8 -*-
"""Memor errors."""


class MemorValidationError(ValueError):
    """Base class for memor errors."""

    pass


class MemorRenderError(Exception):
    """Memor render error class."""

    pass
