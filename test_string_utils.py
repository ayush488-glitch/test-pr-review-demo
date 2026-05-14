"""Tests for string_utils."""

import pytest

from string_utils import normalize_whitespace, truncate


def test_normalize_whitespace_collapses_runs() -> None:
    assert normalize_whitespace("hello   world") == "hello world"


def test_normalize_whitespace_strips_edges() -> None:
    assert normalize_whitespace("  hi  ") == "hi"


def test_normalize_whitespace_empty() -> None:
    assert normalize_whitespace("") == ""


def test_truncate_short_string_unchanged() -> None:
    assert truncate("hi", 10) == "hi"


def test_truncate_appends_suffix() -> None:
    assert truncate("hello world", 8) == "hello..."


def test_truncate_rejects_invalid_max_len() -> None:
    with pytest.raises(ValueError):
        truncate("anything", 2)
