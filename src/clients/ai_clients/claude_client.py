"""
Claude AI Client for connecting to Anthropic API.
"""

import anthropic
from src.config.settings import ANTHROPIC_API_KEY
from .ia_client_interface import AIClient


class ClaudeClient(AIClient):
    """
    Client for interacting with Anthropic Claude API.
    """

    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the Claude client.

        Args:
            model (str): The model to use for completions.
        """
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = model

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using the configured Claude model.

        Args:
            prompt (str): The input prompt for text generation.
            max_tokens (int): Maximum number of tokens to generate.
            temperature (float): Sampling temperature for generation.

        Returns:
            str: The generated text response.
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error generating text with Claude: {str(e)}")

    def chat_completion(self, messages: list, **kwargs) -> dict:
        """
        Perform a chat completion using the configured Claude model.

        Args:
            messages (list): List of message dictionaries with 'role' and 'content'.
            **kwargs: Additional parameters for the completion.

        Returns:
            dict: The completion response.
        """
        try:
            # Convert messages to Anthropic format if needed
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    # Anthropic handles system messages differently
                    anthropic_messages.append({"role": "user", "content": f"System: {msg['content']}"})
                else:
                    anthropic_messages.append(msg)

            response = self.client.messages.create(
                model=self.model,
                messages=anthropic_messages,
                **kwargs
            )
            # Convert back to dict format similar to OpenAI
            return {
                "choices": [{"message": {"content": response.content[0].text}}],
                "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}
            }
        except Exception as e:
            raise Exception(f"Error in chat completion with Claude: {str(e)}")


# Example usage
if __name__ == "__main__":
    client = ClaudeClient()
    prompt = "Hello, how are you?"
    response = client.generate_text(prompt)
    print(response)