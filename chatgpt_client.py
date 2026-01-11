"""ChatGPT API client for additional capabilities."""
import os
from typing import Optional, List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatGPTClient:
    """ChatGPT client for additional AI capabilities."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize ChatGPT client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages: List[Dict[str, str]], model: str = "gpt-4") -> str:
        """
        Send a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: The model to use

        Returns:
            The response content
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    def review_code(self, code: str, language: str = "python") -> str:
        """
        Use ChatGPT to review code.

        Args:
            code: The code to review
            language: Programming language

        Returns:
            Review comments
        """
        messages = [
            {"role": "system", "content": "You are a code reviewer. Provide constructive feedback."},
            {"role": "user", "content": f"Please review this {language} code:\n\n```{language}\n{code}\n```"}
        ]
        return self.chat(messages)

    def suggest_improvements(self, description: str) -> str:
        """
        Get suggestions for improving a feature or system.

        Args:
            description: Description of what to improve

        Returns:
            Suggestions
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant that suggests improvements."},
            {"role": "user", "content": f"Please suggest improvements for: {description}"}
        ]
        return self.chat(messages)


if __name__ == "__main__":
    # Example usage
    client = ChatGPTClient()
    review = client.review_code("def add(a, b):\n    return a + b", "python")
    print("=== CODE REVIEW ===")
    print(review)
