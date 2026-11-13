"""ChatGPT thread extractor."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseLLMExtractor, ExtractedThread, ThreadMessage


class ChatGPTExtractor(BaseLLMExtractor):
    source = "chatgpt"

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
        for sel in ["title", "h1", "[data-testid='conversation-title']", "nav .truncate"]:
            try:
                text = await self.s.get_element_text(sel)
                if text.strip() and "chatgpt" not in text.lower():
                    return text.strip()
            except Exception:
                pass
        return "ChatGPT Thread"

    async def _extract_messages(self) -> list[ThreadMessage]:
        messages: list[ThreadMessage] = []
        idx = 0

        try:
            # ChatGPT uses data-message-author-role attribute
            msg_elems = await self.s.page.query_selector_all(
                "[data-message-author-role]"
            )
            for elem in msg_elems:
                role = await elem.get_attribute("data-message-author-role")
                # Get the content div inside
                content_elem = await elem.query_selector(".markdown, .text-base, p")
                if content_elem:
                    text = (await content_elem.inner_text()).strip()
                else:
                    text = (await elem.inner_text()).strip()
                if text:
                    messages.append(ThreadMessage(role=role or "unknown", content=text, index=idx))
                    idx += 1
        except Exception:
            # Fallback
            try:
                all_msgs = await self.s.page.query_selector_all(
                    "[class*='Message'], [class*='message'], article"
                )
                for i, elem in enumerate(all_msgs):
                    text = (await elem.inner_text()).strip()
                    if text:
                        role = "user" if i % 2 == 0 else "assistant"
                        messages.append(ThreadMessage(role=role, content=text, index=idx))
                        idx += 1
            except Exception:
                md = await self.s.get_markdown()
                messages.append(ThreadMessage(role="raw", content=md, index=0))

        return messages
