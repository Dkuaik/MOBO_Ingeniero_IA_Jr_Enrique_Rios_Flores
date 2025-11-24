"""
Factory for creating AI clients based on configuration.
This demonstrates dependency injection by allowing selection of the AI provider at runtime.
"""

from typing import Optional
from .ia_client_interface import AIClient
from .openai_client import OpenAIClient
from .claude_client import ClaudeClient
from .openrouter_client import OpenRouterClient


class AIClientFactory:
    """
    Factory class for creating AI client instances.
    Allows injecting different AI clients based on the provider type.
    """

    @staticmethod
    def create_client(provider: str, **kwargs) -> AIClient:
        """
        Create an AI client instance based on the provider.

        Args:
            provider (str): The AI provider ('openai', 'claude', 'openrouter').
            **kwargs: Additional arguments for client initialization.

        Returns:
            AIClient: An instance of the requested AI client.

        Raises:
            ValueError: If the provider is not supported.
        """
        provider = provider.lower()

        if provider == "openai":
            model = kwargs.get("model", "gpt-3.5-turbo")
            return OpenAIClient(model=model)
        elif provider == "claude":
            model = kwargs.get("model", "claude-3-haiku-20240307")
            return ClaudeClient(model=model)
        elif provider == "openrouter":
            return OpenRouterClient()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}. Supported: openai, claude, openrouter")


if __name__ == "__main__":
   pass