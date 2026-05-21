import pytest
from unittest.mock import patch, MagicMock
from parse import parse_content

class MockMessage:
    def __init__(self, content):
        self.content = content

@patch('parse.get_model')
@patch('parse.ChatPromptTemplate.from_template')
def test_parse_content_string_response(mock_from_template, mock_get_model):
    mock_prompt = MagicMock()
    mock_chain = MagicMock()
    mock_from_template.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    mock_chain.invoke.side_effect = ["Result 1", "Result 2"]

    dom_chunks = ["chunk1", "chunk2"]
    parse_description = "description"

    res = parse_content(dom_chunks, parse_description, "Ollama", None, None, "model")

    assert res == "Result 1\nResult 2"
    assert mock_chain.invoke.call_count == 2
    mock_chain.invoke.assert_any_call({"dom_content": "chunk1", "parse_description": "description"})
    mock_chain.invoke.assert_any_call({"dom_content": "chunk2", "parse_description": "description"})


@patch('parse.get_model')
@patch('parse.ChatPromptTemplate.from_template')
def test_parse_content_object_response(mock_from_template, mock_get_model):
    mock_prompt = MagicMock()
    mock_chain = MagicMock()
    mock_from_template.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain
    mock_chain.invoke.side_effect = [MockMessage("Result 1"), MockMessage("Result 2")]

    dom_chunks = ["chunk1", "chunk2"]
    parse_description = "description"

    res = parse_content(dom_chunks, parse_description, "Ollama", None, None, "model")

    assert res == "Result 1\nResult 2"
    assert mock_chain.invoke.call_count == 2


@patch('parse.get_model')
@patch('parse.ChatPromptTemplate.from_template')
def test_parse_content_empty_chunks(mock_from_template, mock_get_model):
    mock_prompt = MagicMock()
    mock_chain = MagicMock()
    mock_from_template.return_value = mock_prompt
    mock_prompt.__or__.return_value = mock_chain

    res = parse_content([], "description", "Ollama", None, None, "model")

    assert res == ""
    assert mock_chain.invoke.call_count == 0
