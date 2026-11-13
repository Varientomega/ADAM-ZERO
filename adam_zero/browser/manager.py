"""Playwright browser manager."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


class BrowserManager:
    """Manages a persistent Playwright browser instance."""

    def __init__(self, headless: bool | None = None, timeout: int | None = None):
        self.headless = headless if headless is not None else os.getenv("HEADLESS", "true").lower() == "true"
        self.timeout = timeout or int(os.getenv("BROWSER_TIMEOUT", "30000"))
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def start(self) -> Page:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-dev-shm-usage",
            ],
        )
        self._context = await self._browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            java_script_enabled=True,
        )
        self._context.set_default_timeout(self.timeout)
        self._page = await self._context.new_page()

        # Anti-detection: mask webdriver property
        await self._page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return self._page

    async def stop(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

    async def new_page(self) -> Page:
        if not self._context:
            raise RuntimeError("Browser not started. Call start() first.")
        page = await self._context.new_page()
        await page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        return page

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Browser not started.")
        return self._page

    async def load_cookies(self, cookies: list[dict]) -> None:
        """Inject saved cookies into the browser context."""
        if self._context:
            await self._context.add_cookies(cookies)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[Page, None]:
        """Async context manager for a full browser session."""
        try:
            page = await self.start()
            yield page
        finally:
            await self.stop()
