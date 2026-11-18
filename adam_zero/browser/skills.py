"""High-level reusable browser skills built on Playwright."""

from __future__ import annotations

import asyncio
import re
from typing import Any

from markdownify import markdownify
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout


class BrowserSkills:
    """Composable browser actions available to the agent."""

    def __init__(self, page: Page):
        self.page = page

    # ── Navigation ──────────────────────────────────────────────────────────

    async def navigate(self, url: str) -> str:
        """Navigate to a URL and return the page title."""
        await self.page.goto(url, wait_until="domcontentloaded")
        await self._wait_for_stable()
        return await self.page.title()

    async def current_url(self) -> str:
        return self.page.url

    # ── Scrolling ────────────────────────────────────────────────────────────

    async def scroll_down(self, pixels: int = 800) -> None:
        await self.page.evaluate(f"window.scrollBy(0, {pixels})")
        await asyncio.sleep(0.4)

    async def scroll_to_bottom(self, max_scrolls: int = 60) -> int:
        """Scroll to the absolute bottom, loading lazy content. Returns scroll count."""
        last_height = await self.page.evaluate("document.body.scrollHeight")
        scrolls = 0
        for _ in range(max_scrolls):
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(0.8)
            new_height = await self.page.evaluate("document.body.scrollHeight")
            scrolls += 1
            if new_height == last_height:
                break
            last_height = new_height
        return scrolls

    async def scroll_to_top(self) -> None:
        await self.page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.3)

    # ── Interaction ──────────────────────────────────────────────────────────

    async def click(self, selector: str, timeout: int = 10000) -> None:
        await self.page.click(selector, timeout=timeout)
        await asyncio.sleep(0.3)

    async def click_text(self, text: str) -> None:
        """Click the first element containing specific visible text."""
        await self.page.get_by_text(text, exact=False).first.click()
        await asyncio.sleep(0.3)

    async def type_text(self, selector: str, text: str, clear_first: bool = True) -> None:
        elem = self.page.locator(selector).first
        if clear_first:
            await elem.clear()
        await elem.type(text, delay=30)

    async def press_key(self, key: str) -> None:
        await self.page.keyboard.press(key)
        await asyncio.sleep(0.2)

    async def fill_form(self, fields: dict[str, str]) -> None:
        """
        Fill multiple form fields.
        fields: {selector: value} — selector can be CSS, label text, or placeholder text.
        """
        for selector, value in fields.items():
            try:
                await self.type_text(selector, value)
            except Exception:
                # Fallback: try by label/placeholder
                try:
                    await self.page.get_by_label(selector).fill(value)
                except Exception:
                    await self.page.get_by_placeholder(selector).fill(value)

    # ── Waiting ──────────────────────────────────────────────────────────────

    async def wait_for_selector(self, selector: str, timeout: int = 15000) -> bool:
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except PlaywrightTimeout:
            return False

    async def wait_for_text(self, text: str, timeout: int = 20000) -> bool:
        try:
            await self.page.get_by_text(text, exact=False).first.wait_for(
                state="visible", timeout=timeout
            )
            return True
        except PlaywrightTimeout:
            return False

    async def wait_for_url_change(self, current: str, timeout: int = 15000) -> str:
        await self.page.wait_for_url(lambda u: u != current, timeout=timeout)
        return self.page.url

    async def _wait_for_stable(self, timeout: int = 5000) -> None:
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
        except PlaywrightTimeout:
            pass  # Page may never go fully idle — that's fine

    # ── Extraction ───────────────────────────────────────────────────────────

    async def get_text(self) -> str:
        """Return full visible text content of the page."""
        return await self.page.inner_text("body")

    async def get_markdown(self) -> str:
        """Return page content as clean markdown."""
        html = await self.page.inner_html("body")
        return markdownify(html, heading_style="ATX", strip=["script", "style", "nav", "footer"])

    async def get_element_text(self, selector: str) -> str:
        elem = self.page.locator(selector).first
        return await elem.inner_text()

    async def get_all_links(self) -> list[dict[str, str]]:
        """Return all links as [{text, href}]."""
        anchors = await self.page.query_selector_all("a[href]")
        links = []
        for a in anchors:
            href = await a.get_attribute("href")
            text = (await a.inner_text()).strip()
            if href and not href.startswith("javascript:"):
                links.append({"text": text, "href": href})
        return links

    async def extract_code_blocks(self) -> list[str]:
        """Extract all code blocks from the page."""
        blocks = await self.page.query_selector_all("pre, code")
        result = []
        for b in blocks:
            text = (await b.inner_text()).strip()
            if text:
                result.append(text)
        return result

    async def screenshot(self, path: str) -> str:
        """Take a screenshot and save it. Returns path."""
        await self.page.screenshot(path=path, full_page=True)
        return path

    # ── Utilities ────────────────────────────────────────────────────────────

    async def execute_js(self, script: str) -> Any:
        return await self.page.evaluate(script)

    async def is_element_visible(self, selector: str) -> bool:
        try:
            elem = self.page.locator(selector).first
            return await elem.is_visible()
        except Exception:
            return False

    async def get_input_value(self, selector: str) -> str:
        return await self.page.input_value(selector)

    async def select_option(self, selector: str, value: str) -> None:
        await self.page.select_option(selector, value=value)

    def _clean_text(self, text: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", text).strip()
