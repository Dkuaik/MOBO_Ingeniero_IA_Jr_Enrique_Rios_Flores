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

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, tools=None) -> str:
        """
        Generate text using the configured OpenRouter model.

        Args:
            prompt (str): The input prompt for text generation.
            max_tokens (int): Maximum number of tokens to generate.
            temperature (float): Sampling temperature for generation.
            tools: Optional tools for function calling.

        Returns:
            str: The generated text response.
        """
        try:
            # For Gemini models, use completions API with prompt
            response = self.client.completions.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].text
        except Exception as e:
            raise Exception(f"Error generating text with OpenRouter: {str(e)}")

    def _handle_tool_calls(self, tool_calls, messages):
        """Handle tool calls by executing them and continuing the conversation."""
        from src.clients.mcp.mcp_client import MCPClient
        import asyncio
        import json

        results = []
        for tool_call in tool_calls:
            if tool_call.function.name == "get_usd_price":
                # Execute the tool
                mcp_client = MCPClient()
                try:
                    usd_data = asyncio.run(mcp_client.get_usd_price())
                    results.append(f"USD rates: {usd_data}")
                except Exception as e:
                    results.append(f"Error getting USD rates: {str(e)}")
            else:
                results.append(f"Unknown tool: {tool_call.function.name}")

        return "\n".join(results)

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