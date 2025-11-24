"""
OpenRouter AI Client for connecting to OpenRouter API.
"""

import openai
from src.config.settings import OPENROUTER_API_KEY, OPENROUTER_MODEL
from .ia_client_interface import AIClient


class OpenRouterClient(AIClient):
    """
    Client for interacting with OpenRouter API.
    """

    def __init__(self):
        """
        Initialize the OpenRouter client.
        """
        self.client = openai.OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = OPENROUTER_MODEL

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the configured OpenRouter model.

        Args:
            prompt (str): The input prompt for text generation.
            max_tokens (int): Maximum number of tokens to generate.
            temperature (float): Sampling temperature for generation.

        Returns:
            str: The generated text response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text with OpenRouter: {str(e)}")

    def chat_completion(self, messages: list, **kwargs) -> dict:
        """
        Perform a chat completion using the configured OpenRouter model.

        Args:
            messages (list): List of message dictionaries with 'role' and 'content'.
            **kwargs: Additional parameters for the completion.

        Returns:
            dict: The completion response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response
        except Exception as e:
            raise Exception(f"Error in chat completion with OpenRouter: {str(e)}")


# Example usage
if __name__ == "__main__":
    client = OpenRouterClient()
    prompt = "Hello, how are you?"
    response = client.generate_text(prompt)
    print(response)