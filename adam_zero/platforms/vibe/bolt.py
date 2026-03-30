"""Bolt.new platform handler."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseVibePlatform, VibeChatResult

BOLT_BASE = "https://bolt.new"

_CHAT_SELECTORS = [
    "textarea[placeholder*='message']",
    "textarea[placeholder*='Message']",
    "textarea[placeholder*='prompt']",
    "[data-testid='chat-input']",
    ".chat-input textarea",
    "textarea",
]

_STOP_INDICATORS = ["Stop generating", "Regenerate", "Copy code"]
_DONE_INDICATORS = ["preview", "open in", "deploy"]


class BoltHandler(BaseVibePlatform):
    name = "bolt"

    async def send_prompt(
        self, prompt: str, project_url: str | None = None
    ) -> VibeChatResult:
        target = project_url or BOLT_BASE
        await self.s.navigate(target)
        await asyncio.sleep(2)

        # Find the chat input
        input_selector = await self._find_input()
        await self.s.type_text(input_selector, prompt)
        await asyncio.sleep(0.3)
        await self.s.press_key("Enter")

        response = await self.wait_for_generation()
        code_blocks = await self.s.extract_code_blocks()
        preview_url = await self._get_preview_url()

        return VibeChatResult(
            platform="bolt",
            prompt_sent=prompt,
            response=response,
            code_blocks=code_blocks,
            preview_url=preview_url,
            project_url=self.s.page.url,
        )

    async def wait_for_generation(self) -> str:
        """Wait for Bolt to finish generating. Returns the last assistant message."""
        await asyncio.sleep(3)  # Let it start
        for _ in range(120):  # up to 2 min
            text = await self.s.get_text()
            # Bolt shows a stop button while generating
            stop_visible = await self.s.is_element_visible("[aria-label='Stop']")
            if not stop_visible:
                break
            await asyncio.sleep(1)

        return await self._get_last_response()

    async def _find_input(self) -> str:
        for sel in _CHAT_SELECTORS:
            if await self.s.is_element_visible(sel):
                return sel
        raise RuntimeError("Bolt: could not find chat input")

    async def _get_last_response(self) -> str:
        try:
            msgs = await self.s.page.query_selector_all(".message-content, [data-role='assistant']")
            if msgs:
                return await msgs[-1].inner_text()
        except Exception:
            pass
        return await self.s.get_text()

    async def _get_preview_url(self) -> str | None:
        try:
            frames = self.s.page.frames
            for frame in frames:
                if "webcontainer" in frame.url or "stackblitz" in frame.url:
                    return frame.url
        except Exception:
            pass
        return None
