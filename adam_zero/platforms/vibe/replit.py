"""Replit Agent platform handler."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseVibePlatform, VibeChatResult

REPLIT_BASE = "https://replit.com/ai"

_INPUT_SELECTORS = [
    "textarea[placeholder*='message']",
    "textarea[placeholder*='Message']",
    "textarea[placeholder*='Ask']",
    "[data-cy='chat-input']",
    ".agent-input textarea",
    "textarea",
]


class ReplitHandler(BaseVibePlatform):
    name = "replit"

    async def send_prompt(
        self, prompt: str, project_url: str | None = None
    ) -> VibeChatResult:
        target = project_url or REPLIT_BASE
        await self.s.navigate(target)
        await asyncio.sleep(2)

        input_sel = await self._find_input()
        await self.s.type_text(input_sel, prompt)
        await asyncio.sleep(0.3)
        await self.s.press_key("Enter")

        response = await self.wait_for_generation()
        code_blocks = await self.s.extract_code_blocks()

        return VibeChatResult(
            platform="replit",
            prompt_sent=prompt,
            response=response,
            code_blocks=code_blocks,
            project_url=self.s.page.url,
        )

    async def wait_for_generation(self) -> str:
        await asyncio.sleep(3)
        for _ in range(180):
            # Replit shows a "Stop" button or loading spinner while generating
            busy = await self.s.is_element_visible(
                "[aria-label='Stop'], .agent-loading, [data-testid='loading']"
            )
            if not busy:
                await asyncio.sleep(1.5)
                busy = await self.s.is_element_visible(
                    "[aria-label='Stop'], .agent-loading, [data-testid='loading']"
                )
                if not busy:
                    break
            await asyncio.sleep(1)

        return await self._get_last_response()

    async def _find_input(self) -> str:
        for sel in _INPUT_SELECTORS:
            if await self.s.is_element_visible(sel):
                return sel
        raise RuntimeError("Replit: could not find chat input")

    async def _get_last_response(self) -> str:
        try:
            msgs = await self.s.page.query_selector_all(
                ".agent-message, [data-role='assistant'], .message-content"
            )
            if msgs:
                return await msgs[-1].inner_text()
        except Exception:
            pass
        return await self.s.get_text()
