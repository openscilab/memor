# -*- coding: utf-8 -*-
"""Memor errors."""

class MemorError(Exception):
    """Base class for all errors in Memor."""

    pass

class MemorValidationError(MemorError, ValueError):
    """Base class for validation errors in Memor."""

    pass


class MemorRenderError(MemorError):
    """Base class for render error in Memor."""

    pass
