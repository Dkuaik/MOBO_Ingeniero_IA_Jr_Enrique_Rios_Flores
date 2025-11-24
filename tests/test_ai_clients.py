import pytest
from unittest.mock import Mock, patch
from src.clients.ai_clients.ia_client_interface import AIClient
from src.clients.ai_clients.openai_client import OpenAIClient
from src.clients.ai_clients.claude_client import ClaudeClient
from src.clients.ai_clients.openrouter_client import OpenRouterClient
from src.clients.ai_clients.client_factory import AIClientFactory


class TestAIClientInterface:
    """Test the AIClient interface."""

    def test_interface_is_abstract(self):
        """Test that AIClient cannot be instantiated directly."""
        with pytest.raises(TypeError):
            AIClient()


class TestOpenAIClient:
    """Test OpenAI client."""

    @patch('src.clients.ai_clients.openai_client.openai.OpenAI')
    def test_init(self, mock_openai):
        """Test OpenAI client initialization."""
        client = OpenAIClient()
        mock_openai.assert_called_once()
        assert client.model == "gpt-3.5-turbo"

    @patch('src.clients.ai_clients.openai_client.openai.OpenAI')
    def test_generate_text(self, mock_openai_class):
        """Test generate_text method."""
        mock_client = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        result = client.generate_text("Hello")

        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch('src.clients.ai_clients.openai_client.openai.OpenAI')
    def test_chat_completion(self, mock_openai_class):
        """Test chat_completion method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        messages = [{"role": "user", "content": "Hello"}]
        result = client.chat_completion(messages)

        assert result == mock_response
        mock_client.chat.completions.create.assert_called_once()


class TestClaudeClient:
    """Test Claude client."""

    @patch('src.clients.ai_clients.claude_client.anthropic.Anthropic')
    def test_init(self, mock_anthropic):
        """Test Claude client initialization."""
        client = ClaudeClient()
        mock_anthropic.assert_called_once()
        assert client.model == "claude-3-haiku-20240307"

    @patch('src.clients.ai_clients.claude_client.anthropic.Anthropic')
    def test_generate_text(self, mock_anthropic_class):
        """Test generate_text method."""
        mock_client = Mock()
        mock_content = Mock()
        mock_content.text = "Test response"
        mock_response = Mock()
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        client = ClaudeClient()
        result = client.generate_text("Hello")

        assert result == "Test response"
        mock_client.messages.create.assert_called_once()

    @patch('src.clients.ai_clients.claude_client.anthropic.Anthropic')
    def test_chat_completion(self, mock_anthropic_class):
        """Test chat_completion method."""
        mock_client = Mock()
        mock_content = Mock()
        mock_content.text = "Test response"
        mock_usage = Mock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 5
        mock_response = Mock()
        mock_response.content = [mock_content]
        mock_response.usage = mock_usage
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client

        client = ClaudeClient()
        messages = [{"role": "user", "content": "Hello"}]
        result = client.chat_completion(messages)

        expected = {
            "choices": [{"message": {"content": "Test response"}}],
            "usage": {"input_tokens": 10, "output_tokens": 5}
        }
        assert result == expected


class TestOpenRouterClient:
    """Test OpenRouter client."""

    @patch('src.clients.ai_clients.openrouter_client.openai.OpenAI')
    def test_init(self, mock_openai):
        """Test OpenRouter client initialization."""
        client = OpenRouterClient()
        mock_openai.assert_called_once()
        assert client.model == "google/gemini-2.5-flash"

    @patch('src.clients.ai_clients.openrouter_client.openai.OpenAI')
    def test_generate_text(self, mock_openai_class):
        """Test generate_text method."""
        mock_client = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenRouterClient()
        result = client.generate_text("Hello")

        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()

    @patch('src.clients.ai_clients.openrouter_client.openai.OpenAI')
    def test_chat_completion(self, mock_openai_class):
        """Test chat_completion method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = OpenRouterClient()
        messages = [{"role": "user", "content": "Hello"}]
        result = client.chat_completion(messages)

        assert result == mock_response


class TestAIClientFactory:
    """Test AI client factory."""

    def test_create_openai_client(self):
        """Test creating OpenAI client."""
        client = AIClientFactory.create_client("openai")
        assert isinstance(client, OpenAIClient)

    def test_create_claude_client(self):
        """Test creating Claude client."""
        client = AIClientFactory.create_client("claude")
        assert isinstance(client, ClaudeClient)

    def test_create_openrouter_client(self):
        """Test creating OpenRouter client."""
        client = AIClientFactory.create_client("openrouter")
        assert isinstance(client, OpenRouterClient)

    def test_create_invalid_provider(self):
        """Test creating client with invalid provider."""
        with pytest.raises(ValueError, match="Unsupported AI provider"):
            AIClientFactory.create_client("invalid")

    def test_create_with_model(self):
        """Test creating client with custom model."""
        client = AIClientFactory.create_client("openai", model="gpt-4")
        assert isinstance(client, OpenAIClient)
        assert client.model == "gpt-4"