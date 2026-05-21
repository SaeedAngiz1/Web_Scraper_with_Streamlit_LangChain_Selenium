import pytest
from unittest.mock import MagicMock, patch
from parse import get_model

@pytest.fixture
def mock_langchain_modules():
    """Mock the langchain modules so we don't need to actually instantiate them."""
    ollama_mock = MagicMock()
    openai_mock = MagicMock()
    anthropic_mock = MagicMock()
    google_mock = MagicMock()

    modules = {
        'langchain_ollama': ollama_mock,
        'langchain_openai': openai_mock,
        'langchain_anthropic': anthropic_mock,
        'langchain_google_genai': google_mock,
    }

    with patch.dict('sys.modules', modules):
        yield {
            'Ollama': ollama_mock.OllamaLLM,
            'OpenAI': openai_mock.ChatOpenAI,
            'Anthropic': anthropic_mock.ChatAnthropic,
            'Google GenAI': google_mock.ChatGoogleGenerativeAI,
        }

@pytest.mark.parametrize("provider, base_url, api_key, model_name, expected_kwargs", [
    ("Ollama", None, "ignored_key", "llama3", {"model": "llama3"}),
    ("Ollama", "http://localhost:11434", "ignored_key", "llama3", {"model": "llama3", "base_url": "http://localhost:11434"}),
    ("OpenAI", None, "sk-123", "gpt-4", {"model": "gpt-4", "api_key": "sk-123"}),
    ("OpenAI", "https://api.openai.com/v1", "sk-123", "gpt-4", {"model": "gpt-4", "api_key": "sk-123", "base_url": "https://api.openai.com/v1"}),
    ("Anthropic", None, "ant-123", "claude-3", {"model_name": "claude-3", "api_key": "ant-123"}),
    ("Anthropic", "https://api.anthropic.com", "ant-123", "claude-3", {"model_name": "claude-3", "api_key": "ant-123", "base_url": "https://api.anthropic.com"}),
    ("Google GenAI", None, "gem-123", "gemini-pro", {"model": "gemini-pro", "google_api_key": "gem-123"}),
    ("Google GenAI", "https://api.google.com", "gem-123", "gemini-pro", {"model": "gemini-pro", "google_api_key": "gem-123"}), # Base URL is currently ignored in the code
])
def test_get_model_providers(mock_langchain_modules, provider, base_url, api_key, model_name, expected_kwargs):
    """Test get_model successfully retrieves and initializes the correct LLM model."""

    # Run the function
    model_instance = get_model(provider, base_url, api_key, model_name)

    # Assert correct module was called
    mock_class = mock_langchain_modules[provider]

    # Check that it was instantiated with the correct kwargs
    mock_class.assert_called_once_with(**expected_kwargs)

    # Check that it returned the instance created by our mock
    assert model_instance == mock_class.return_value

def test_get_model_unsupported_provider():
    """Test get_model raises an error when an unsupported provider is given."""
    with pytest.raises(ValueError, match="Unsupported provider: UnsupportedProvider"):
        get_model("UnsupportedProvider", None, "key", "model")
