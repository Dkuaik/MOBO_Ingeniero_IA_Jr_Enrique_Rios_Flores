"""
Abstract interface for AI clients to enable dependency injection and abstraction.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class AIClient(ABC):
    """
    Abstract base class for AI clients. This interface allows injecting different
    AI service providers (OpenRouter, OpenAI, Claude, etc.) while maintaining
    a consistent API for text generation and chat completions.
    """

    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the AI model.

        Args:
            prompt (str): The input prompt for text generation.
            max_tokens (int): Maximum number of tokens to generate.
            temperature (float): Sampling temperature for generation.

        Returns:
            str: The generated text response.
        """
        pass

    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Perform a chat completion using the AI model.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'.
            **kwargs: Additional parameters for the completion.

        Returns:
            Dict[str, Any]: The completion response.
        """
        pass