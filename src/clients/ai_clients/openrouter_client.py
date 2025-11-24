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
            if tools:
                # Use chat completions for tool support
                messages = [{"role": "user", "content": prompt}]
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    tools=tools,
                    tool_choice="auto"
                )
                message = response.choices[0].message
                if message.tool_calls:
                    tool_results = self._handle_tool_calls(message.tool_calls)
                    # Add assistant message with tool calls
                    messages.append(message)
                    # Add tool results for each call
                    for i, tool_call in enumerate(message.tool_calls):
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_results[i] if i < len(tool_results) else "Error: No result"
                        })
                    # Get final response
                    final_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    return final_response.choices[0].message.content
                else:
                    return message.content
            else:
                # Use completions API for simple text generation
                response = self.client.completions.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].text
        except Exception as e:
            raise Exception(f"Error generating text with OpenRouter: {str(e)}")

    def _handle_tool_calls(self, tool_calls):
        """Handle tool calls by executing them and returning results per call."""
        import requests

        results = []
        for tool_call in tool_calls:
            if tool_call.function.name == "get_usd_price":
                # Execute the tool directly
                try:
                    response = requests.get("https://open.er-api.com/v6/latest/USD")
                    response.raise_for_status()
                    data = response.json()
                    results.append(f"USD rates: {data}")
                except Exception as e:
                    results.append(f"Error getting USD rates: {str(e)}")
            else:
                results.append(f"Unknown tool: {tool_call.function.name}")

        return results

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