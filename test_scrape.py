import pytest
from scrape import split_dom_content

def test_split_dom_content_empty():
    assert split_dom_content("") == []

def test_split_dom_content_shorter_than_max():
    # default max is 6000
    content = "a" * 100
    result = split_dom_content(content)
    assert len(result) == 1
    assert result[0] == content

def test_split_dom_content_exact_max():
    content = "a" * 6000
    result = split_dom_content(content)
    assert len(result) == 1
    assert result[0] == content

def test_split_dom_content_longer_not_multiple():
    content = "a" * 13000
    result = split_dom_content(content)
    assert len(result) == 3
    assert result[0] == "a" * 6000
    assert result[1] == "a" * 6000
    assert result[2] == "a" * 1000

def test_split_dom_content_exact_multiple():
    content = "a" * 18000
    result = split_dom_content(content)
    assert len(result) == 3
    assert result[0] == "a" * 6000
    assert result[1] == "a" * 6000
    assert result[2] == "a" * 6000

def test_split_dom_content_custom_max_length():
    content = "abcdefghij"
    result = split_dom_content(content, max_length=3)
    assert len(result) == 4
    assert result == ["abc", "def", "ghi", "j"]
