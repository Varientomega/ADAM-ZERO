"""v0.dev (Vercel) platform handler."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseVibePlatform, VibeChatResult

V0_BASE = "https://v0.dev"

_INPUT_SELECTORS = [
    "textarea[placeholder*='message']",
    "textarea[placeholder*='Message']",
    "textarea[placeholder*='Describe']",
    "textarea[placeholder*='Build']",
    "[data-testid='prompt-input']",
    "textarea",
]


class V0Handler(BaseVibePlatform):
    name = "v0"

    async def send_prompt(
        self, prompt: str, project_url: str | None = None
    ) -> VibeChatResult:
        target = project_url or V0_BASE
        await self.s.navigate(target)
        await asyncio.sleep(2)

        input_sel = await self._find_input()
        await self.s.type_text(input_sel, prompt)
        await asyncio.sleep(0.3)
        await self.s.press_key("Enter")

        response = await self.wait_for_generation()
        code_blocks = await self.s.extract_code_blocks()
        preview_url = await self._get_preview_url()

        return VibeChatResult(
            platform="v0",
            prompt_sent=prompt,
            response=response,
            code_blocks=code_blocks,
            preview_url=preview_url,
            project_url=self.s.page.url,
        )

    async def wait_for_generation(self) -> str:
        await asyncio.sleep(3)
        for _ in range(180):
            # v0 shows a stop/cancel button while generating
            busy = await self.s.is_element_visible(
                "[aria-label='Stop'], [aria-label='Cancel'], .generating-indicator"
            )
            if not busy:
                await asyncio.sleep(1.5)
                busy = await self.s.is_element_visible(
                    "[aria-label='Stop'], [aria-label='Cancel'], .generating-indicator"
                )
                if not busy:
                    break
            await asyncio.sleep(1)

        return await self._get_last_response()

    async def _find_input(self) -> str:
        for sel in _INPUT_SELECTORS:
            if await self.s.is_element_visible(sel):
                return sel
        raise RuntimeError("v0: could not find prompt input")

    async def _get_last_response(self) -> str:
        try:
            msgs = await self.s.page.query_selector_all(
                "[data-role='assistant'], .chat-message-assistant, .prose"
            )
            if msgs:
                return await msgs[-1].inner_text()
        except Exception:
            pass
        return await self.s.get_text()

    async def _get_preview_url(self) -> str | None:
        try:
            preview = self.s.page.locator("iframe[sandbox], iframe[src*='preview']").first
            src = await preview.get_attribute("src")
            return src
        except Exception:
            return None
