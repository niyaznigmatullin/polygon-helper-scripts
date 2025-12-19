#!/usr/bin/env python3
"""
LLM Helper Module

This module handles interactions with Language Learning Models (LLMs).
"""

from typing import List

try:
    import openai
except ImportError:
    openai = None


class LLMHelper:
    """Helper class for interacting with Language Learning Models"""

    def __init__(self, api_key: str, base_url: Optional[str]):
        """
        Initialize the LLM helper with an API key.

        Args:
            api_key: OpenAI API key

        Raises:
            Exception: If OpenAI library is not installed
        """
        if not openai:
            raise Exception("OpenAI library not installed. Please install with: pip install openai")

        self.api_key = api_key
        if base_url:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = openai.OpenAI(api_key=api_key)

    def ask_llm(self, context: str, prompt: List[str], max_tokens: int = 3000, temperature: float = 0.4) -> str:
        """
        Send a prompt to the LLM and get a response.

        Args:
            context: System message providing context for the LLM
            prompt: List of user messages to send to the LLM
            max_tokens: Maximum number of tokens in the response
            temperature: Temperature parameter for response randomness

        Returns:
            The LLM's response as a string

        Raises:
            Exception: If API call fails
        """
        try:
            print(prompt)

            # Make API call to GPT
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": context},
                ] + [{"role": "user", "content": x} for x in prompt],
                max_tokens=max_tokens,
                temperature=temperature
            )

            print(response.choices)

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Failed to get LLM response: {e}")
