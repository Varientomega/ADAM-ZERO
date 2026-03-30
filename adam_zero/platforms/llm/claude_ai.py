"""Claude.ai thread extractor."""

from __future__ import annotations

import asyncio
import re

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseLLMExtractor, ExtractedThread, ThreadMessage

# claude.ai conversation URL pattern: https://claude.ai/chat/<uuid>
_MSG_SELECTORS = [
    "[data-testid='human-turn'], [data-testid='ai-turn']",
    ".human-turn, .ai-turn",
    "[class*='HumanMessage'], [class*='AssistantMessage']",
]

_HUMAN_SELECTORS = [
    "[data-testid='human-turn']",
    ".human-turn",
    "[class*='HumanMessage']",
]

_AI_SELECTORS = [
    "[data-testid='ai-turn']",
    ".ai-turn",
    "[class*='AssistantMessage']",
]


class ClaudeAIExtractor(BaseLLMExtractor):
    source = "claude.ai"

    async def extract(self, thread_url: str) -> ExtractedThread:
        await self.s.navigate(thread_url)
        await asyncio.sleep(3)

        # Scroll to top then bottom to load all messages
        await self.s.scroll_to_top()
        await asyncio.sleep(1)
        await self.s.scroll_to_bottom(max_scrolls=40)
        await asyncio.sleep(1)

        title = await self._get_title()
        messages = await self._extract_messages()

        return ExtractedThread(
            source=self.source,
            url=thread_url,
            title=title,
            messages=messages,
            total_messages=len(messages),
        )

    async def _get_title(self) -> str:
        for sel in ["title", "[data-testid='conversation-title']", ".conversation-title", "h1"]:
            try:
                text = await self.s.get_element_text(sel)
                if text.strip():
                    return text.strip()
            except Exception:
                pass
        return f"Claude.ai Thread"

    async def _extract_messages(self) -> list[ThreadMessage]:
        messages: list[ThreadMessage] = []
        idx = 0

        # Try to get human turns
        try:
            human_elems = await self.s.page.query_selector_all(
                "[data-testid='human-turn'], .human-turn"
            )
            ai_elems = await self.s.page.query_selector_all(
                "[data-testid='ai-turn'], .ai-turn"
            )

            # Interleave them by DOM order
            all_elems = []
            for e in human_elems:
                box = await e.bounding_box()
                if box:
                    all_elems.append(("user", e, box["y"]))
            for e in ai_elems:
                box = await e.bounding_box()
                if box:
                    all_elems.append(("assistant", e, box["y"]))

            all_elems.sort(key=lambda x: x[2])  # sort by vertical position

            for role, elem, _ in all_elems:
                text = (await elem.inner_text()).strip()
                if text:
                    messages.append(ThreadMessage(role=role, content=text, index=idx))
                    idx += 1

        except Exception:
            # Fallback: scrape raw text
            text = await self.s.get_markdown()
            messages.append(ThreadMessage(role="raw", content=text, index=0))

        return messages
