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


# Example usage demonstrating dependency injection
def use_ai_client(client: AIClient, prompt: str) -> str:
    """
    Function that uses any AI client through the interface.
    This demonstrates how the interface allows decoupling from specific implementations.

    Args:
        client (AIClient): The injected AI client.
        prompt (str): The prompt to send.

    Returns:
        str: The generated response.
    """
    return client.generate_text(prompt)


# Example of injecting different clients
if __name__ == "__main__":
    # Inject OpenRouter client
    openrouter_client = AIClientFactory.create_client("openrouter")
    response1 = use_ai_client(openrouter_client, "Hello from OpenRouter!")
    print("OpenRouter:", response1)

    # Inject OpenAI client
    openai_client = AIClientFactory.create_client("openai", model="gpt-4")
    response2 = use_ai_client(openai_client, "Hello from OpenAI!")
    print("OpenAI:", response2)

    # Inject Claude client
    claude_client = AIClientFactory.create_client("claude")
    response3 = use_ai_client(claude_client, "Hello from Claude!")
    print("Claude:", response3)