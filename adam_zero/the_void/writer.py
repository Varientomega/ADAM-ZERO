"""TheVoid: persistent second-brain writer for ADAM-ZERO.

Directory layout:
  ~/TheVoid/
    index.md                  — master index of all entries
    threads/
      claude_ai/              — by source
        YYYY-MM-DD_<title>.md
      chatgpt/
      gemini/
    vibe_sessions/
      bolt/
      lovable/
      replit/
      v0/
    scrapes/                  — general web scrapes
    tasks/                    — task execution logs
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles

from adam_zero.platforms.base import ExtractedThread, VibeChatResult


class TheVoid:
    """Writes structured knowledge into the second-brain directory."""

    def __init__(self, root: str | None = None):
        raw_root = root or os.getenv("THE_VOID_PATH", "~/TheVoid")
        self.root = Path(raw_root).expanduser().resolve()
        self._ensure_dirs()

    # ── Directory bootstrap ──────────────────────────────────────────────────

    def _ensure_dirs(self) -> None:
        dirs = [
            self.root,
            self.root / "threads" / "claude_ai",
            self.root / "threads" / "chatgpt",
            self.root / "threads" / "gemini",
            self.root / "vibe_sessions" / "bolt",
            self.root / "vibe_sessions" / "lovable",
            self.root / "vibe_sessions" / "replit",
            self.root / "vibe_sessions" / "v0",
            self.root / "scrapes",
            self.root / "tasks",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

        index_path = self.root / "index.md"
        if not index_path.exists():
            index_path.write_text(
                "# TheVoid — Index\n\nADAM-ZERO knowledge base.\n\n"
                "| Date | Type | Title | Path |\n"
                "|------|------|-------|------|\n"
            )

    # ── Public write methods ────────────────────────────────────────────────

    async def save_thread(self, thread: ExtractedThread) -> str:
        """Save a full LLM thread. Returns the file path."""
        slug = _to_slug(thread.title)
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        source_dir = self.root / "threads" / thread.source.replace(".", "_")
        source_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date_str}_{slug}.md"
        path = source_dir / filename

        content = thread.to_markdown()
        await _write(path, content)
        await self._append_index(date_str, "thread", thread.title, str(path.relative_to(self.root)))
        return str(path)

    async def save_vibe_session(self, result: VibeChatResult, session_title: str | None = None) -> str:
        """Save a vibe coding session. Returns file path."""
        title = session_title or f"{result.platform.title()} Session"
        slug = _to_slug(title)
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        ts = datetime.utcnow().strftime("%H%M%S")
        platform_dir = self.root / "vibe_sessions" / result.platform
        platform_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date_str}_{ts}_{slug}.md"
        path = platform_dir / filename

        lines = [
            f"# {title}",
            f"\n**Platform:** {result.platform}",
            f"**Date:** {date_str}",
        ]
        if result.project_url:
            lines.append(f"**Project URL:** {result.project_url}")
        if result.preview_url:
            lines.append(f"**Preview URL:** {result.preview_url}")
        lines.append("\n---\n")
        lines.append("## Prompt\n")
        lines.append(result.prompt_sent)
        lines.append("\n## Response\n")
        lines.append(result.response)
        if result.code_blocks:
            lines.append("\n## Code Blocks\n")
            for i, block in enumerate(result.code_blocks, 1):
                lines.append(f"### Block {i}\n```\n{block}\n```\n")

        await _write(path, "\n".join(lines))
        await self._append_index(date_str, "vibe", title, str(path.relative_to(self.root)))
        return str(path)

    async def save_scrape(self, url: str, content: str, title: str | None = None) -> str:
        """Save a raw web scrape. Returns file path."""
        title = title or _url_to_title(url)
        slug = _to_slug(title)
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        ts = datetime.utcnow().strftime("%H%M%S")
        filename = f"{date_str}_{ts}_{slug}.md"
        path = self.root / "scrapes" / filename

        header = f"# {title}\n\n**URL:** {url}\n**Scraped:** {datetime.utcnow().isoformat()}\n\n---\n\n"
        await _write(path, header + content)
        await self._append_index(date_str, "scrape", title, str(path.relative_to(self.root)))
        return str(path)

    async def save_task_log(self, task_id: str, instruction: str, output: str, success: bool) -> str:
        """Save a task execution log. Returns file path."""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        ts = datetime.utcnow().strftime("%H%M%S")
        status = "SUCCESS" if success else "FAILED"
        filename = f"{date_str}_{ts}_{task_id}_{status}.md"
        path = self.root / "tasks" / filename

        content = (
            f"# Task {task_id} — {status}\n\n"
            f"**Date:** {datetime.utcnow().isoformat()}\n"
            f"**Status:** {status}\n\n"
            f"## Instruction\n\n{instruction}\n\n"
            f"## Output\n\n{output}\n"
        )
        await _write(path, content)
        await self._append_index(date_str, "task", f"Task {task_id}", str(path.relative_to(self.root)))
        return str(path)

    async def save_note(self, title: str, content: str, tags: list[str] | None = None, subdir: str = "scrapes") -> str:
        """Generic note saver. Returns file path."""
        slug = _to_slug(title)
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        ts = datetime.utcnow().strftime("%H%M%S")
        target_dir = self.root / subdir
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date_str}_{ts}_{slug}.md"
        path = target_dir / filename

        tag_line = ""
        if tags:
            tag_line = f"\n**Tags:** {', '.join(f'#{t}' for t in tags)}\n"

        header = f"# {title}\n\n**Date:** {date_str}{tag_line}\n\n---\n\n"
        await _write(path, header + content)
        await self._append_index(date_str, "note", title, str(path.relative_to(self.root)))
        return str(path)

    # ── Index management ────────────────────────────────────────────────────

    async def _append_index(self, date: str, kind: str, title: str, rel_path: str) -> None:
        index_path = self.root / "index.md"
        row = f"| {date} | {kind} | {title} | [{rel_path}]({rel_path}) |\n"
        async with aiofiles.open(index_path, "a") as f:
            await f.write(row)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _to_slug(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:60]


def _url_to_title(url: str) -> str:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".strip("/")


async def _write(path: Path, content: str) -> None:
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(content)
