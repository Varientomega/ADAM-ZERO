"""LLM thread extraction handlers."""

from adam_zero.platforms.llm.claude_ai import ClaudeAIExtractor
from adam_zero.platforms.llm.chatgpt import ChatGPTExtractor
from adam_zero.platforms.llm.gemini import GeminiExtractor

REGISTRY: dict[str, type] = {
    "claude.ai": ClaudeAIExtractor,
    "claude": ClaudeAIExtractor,
    "chatgpt": ChatGPTExtractor,
    "openai": ChatGPTExtractor,
    "gemini": GeminiExtractor,
    "google": GeminiExtractor,
}

__all__ = ["ClaudeAIExtractor", "ChatGPTExtractor", "GeminiExtractor", "REGISTRY"]
