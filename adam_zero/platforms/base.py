"""Base classes for all platform handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from adam_zero.browser.skills import BrowserSkills


@dataclass
class VibeChatResult:
    platform: str
    prompt_sent: str
    response: str
    code_blocks: list[str] = field(default_factory=list)
    preview_url: str | None = None
    project_url: str | None = None
    raw_html: str | None = None


@dataclass
class ThreadMessage:
    role: str          # "user" | "assistant" | "system"
    content: str
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedThread:
    source: str        # "claude.ai" | "chatgpt" | etc.
    url: str
    title: str
    messages: list[ThreadMessage]
    total_messages: int

    def to_markdown(self) -> str:
        lines = [f"# {self.title}", f"\n**Source:** {self.source}  ", f"**URL:** {self.url}\n", "---\n"]
        for msg in self.messages:
            role_label = "**You**" if msg.role == "user" else f"**{self.source.title()} ({msg.role})**"
            lines.append(f"{role_label}\n\n{msg.content}\n\n---\n")
        return "\n".join(lines)


class BaseVibePlatform(ABC):
    """Abstract base for vibe coding platform handlers."""

    name: str = "base"

    def __init__(self, skills: BrowserSkills):
        self.s = skills

    @abstractmethod
    async def send_prompt(self, prompt: str, project_url: str | None = None) -> VibeChatResult:
        """Send a prompt to the platform and wait for a complete response."""
        ...

    @abstractmethod
    async def wait_for_generation(self) -> str:
        """Poll until code generation is complete. Returns the generated output."""
        ...


class BaseLLMExtractor(ABC):
    """Abstract base for LLM thread extractors."""

    source: str = "base"

    def __init__(self, skills: BrowserSkills):
        self.s = skills

    @abstractmethod
    async def extract(self, thread_url: str) -> ExtractedThread:
        """Extract all messages from a thread URL."""
        ...
