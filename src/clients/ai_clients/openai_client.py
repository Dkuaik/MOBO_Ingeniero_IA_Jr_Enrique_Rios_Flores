"""
OpenAI AI Client for connecting to OpenAI API.
"""

import openai
from src.config.settings import OPENAI_API_KEY
from .ia_client_interface import AIClient


class OpenAIClient(AIClient):
    """
    Client for interacting with OpenAI API.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client.

        Args:
            model (str): The model to use for completions.
        """
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the configured OpenAI model.

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
            raise Exception(f"Error generating text with OpenAI: {str(e)}")

    def chat_completion(self, messages: list, **kwargs) -> dict:
        """
        Perform a chat completion using the configured OpenAI model.

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
            raise Exception(f"Error in chat completion with OpenAI: {str(e)}")


# Example usage
if __name__ == "__main__":
    client = OpenAIClient()
    prompt = "Hello, how are you?"
    response = client.generate_text(prompt)
    print(response)