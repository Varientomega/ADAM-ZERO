"""Lovable.dev platform handler."""

from __future__ import annotations

import asyncio

from adam_zero.browser.skills import BrowserSkills
from adam_zero.platforms.base import BaseVibePlatform, VibeChatResult

LOVABLE_BASE = "https://lovable.dev"

_INPUT_SELECTORS = [
    "textarea[placeholder*='message']",
    "textarea[placeholder*='Build']",
    "textarea[placeholder*='Describe']",
    "[contenteditable='true']",
    "textarea",
]


class LovableHandler(BaseVibePlatform):
    name = "lovable"

    async def send_prompt(
        self, prompt: str, project_url: str | None = None
    ) -> VibeChatResult:
        target = project_url or LOVABLE_BASE
        await self.s.navigate(target)
        await asyncio.sleep(2)

        input_sel = await self._find_input()
        await self.s.type_text(input_sel, prompt)
        await asyncio.sleep(0.3)
        await self.s.press_key("Enter")

        response = await self.wait_for_generation()
        code_blocks = await self.s.extract_code_blocks()

        # Lovable shows preview in an iframe
        preview_url = await self._get_preview_url()

        return VibeChatResult(
            platform="lovable",
            prompt_sent=prompt,
            response=response,
            code_blocks=code_blocks,
            preview_url=preview_url,
            project_url=self.s.page.url,
        )

    async def wait_for_generation(self) -> str:
        await asyncio.sleep(3)
        for _ in range(180):
            # Lovable shows a spinner or "Editing..." while busy
            editing = await self.s.is_element_visible("[data-state='editing'], .loading-indicator, [aria-label='Stop']")
            if not editing:
                # Double-check: wait another second and verify
                await asyncio.sleep(1)
                editing = await self.s.is_element_visible("[data-state='editing'], .loading-indicator, [aria-label='Stop']")
                if not editing:
                    break
            await asyncio.sleep(1)

        return await self._get_last_response()

    async def _find_input(self) -> str:
        for sel in _INPUT_SELECTORS:
            if await self.s.is_element_visible(sel):
                return sel
        raise RuntimeError("Lovable: could not find chat input")

    async def _get_last_response(self) -> str:
        try:
            msgs = await self.s.page.query_selector_all(".message, [data-role='assistant'], .assistant-message")
            if msgs:
                return await msgs[-1].inner_text()
        except Exception:
            pass
        return await self.s.get_text()

    async def _get_preview_url(self) -> str | None:
        try:
            iframe = self.s.page.locator("iframe[src*='preview'], iframe[src*='lovable']").first
            src = await iframe.get_attribute("src")
            return src
        except Exception:
            return None
