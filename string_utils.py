"""String utilities for normalizing user input.

Pure functions, no side effects, fully tested.
"""

from __future__ import annotations


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace and trim ends.

    Args:
        text: Arbitrary input string. Empty string returns empty string.

    Returns:
        The input with runs of whitespace collapsed to a single space and
        leading/trailing whitespace stripped.
    """
    if not text:
        return ""
    return " ".join(text.split())


def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    """Truncate ``text`` to ``max_len`` characters, appending ``suffix``.

    Args:
        text: Input string.
        max_len: Maximum length of the returned string. Must be >= len(suffix).
        suffix: Marker appended when truncation occurs. Defaults to ``"..."``.

    Returns:
        The original string when shorter than ``max_len``; otherwise the
        truncated form ending in ``suffix``.

    Raises:
        ValueError: If ``max_len`` is smaller than ``len(suffix)``.
    """
    if max_len < len(suffix):
        raise ValueError("max_len must be at least len(suffix)")
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix
