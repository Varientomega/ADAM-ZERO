"""Gemini thread extractor."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseLLMExtractor, ExtractedThread, ThreadMessage


class GeminiExtractor(BaseLLMExtractor):
    source = "gemini"

    async def extract(self, thread_url: str) -> ExtractedThread:
        await self.s.navigate(thread_url)
        await asyncio.sleep(3)

        await self.s.scroll_to_top()
        await asyncio.sleep(1)
        await self.s.scroll_to_bottom(max_scrolls=60)
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
        for sel in ["title", "h1", ".conversation-title", "[aria-label='Conversation title']"]:
            try:
                text = await self.s.get_element_text(sel)
                if text.strip() and "gemini" not in text.lower():
                    return text.strip()
            except Exception:
                pass
        return "Gemini Thread"

    async def _extract_messages(self) -> list[ThreadMessage]:
        messages: list[ThreadMessage] = []
        idx = 0

        try:
            # Gemini uses user-query and model-response
            user_elems = await self.s.page.query_selector_all(
                "user-query, .user-query, [data-turn-type='user']"
            )
            model_elems = await self.s.page.query_selector_all(
                "model-response, .model-response, [data-turn-type='model']"
            )

            all_elems = []
            for e in user_elems:
                box = await e.bounding_box()
                if box:
                    all_elems.append(("user", e, box["y"]))
            for e in model_elems:
                box = await e.bounding_box()
                if box:
                    all_elems.append(("assistant", e, box["y"]))

            all_elems.sort(key=lambda x: x[2])

            for role, elem, _ in all_elems:
                text = (await elem.inner_text()).strip()
                if text:
                    messages.append(ThreadMessage(role=role, content=text, index=idx))
                    idx += 1

        except Exception:
            md = await self.s.get_markdown()
            messages.append(ThreadMessage(role="raw", content=md, index=0))

        return messages
