"""ADAM-ZERO core agent — Claude-powered web automation brain."""

from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any

import anthropic

from adam_zero.browser.manager import BrowserManager
from adam_zero.browser.skills import BrowserSkills
from adam_zero.core.task import Task, TaskResult, TaskStatus
from adam_zero.platforms.base import ExtractedThread, VibeChatResult
from adam_zero.the_void.writer import TheVoid

# ── Tool definitions sent to Claude ─────────────────────────────────────────

TOOLS: list[dict] = [
    {
        "name": "navigate",
        "description": "Navigate the browser to a URL.",
        "input_schema": {
            "type": "object",
            "properties": {"url": {"type": "string", "description": "Full URL to navigate to"}},
            "required": ["url"],
        },
    },
    {
        "name": "click",
        "description": "Click an element on the page using a CSS selector.",
        "input_schema": {
            "type": "object",
            "properties": {"selector": {"type": "string"}},
            "required": ["selector"],
        },
    },
    {
        "name": "click_text",
        "description": "Click the first element that contains specific visible text.",
        "input_schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "type_text",
        "description": "Type text into an input element. Uses CSS selector.",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "text": {"type": "string"},
                "clear_first": {"type": "boolean", "default": True},
            },
            "required": ["selector", "text"],
        },
    },
    {
        "name": "fill_form",
        "description": "Fill multiple form fields at once. fields is a dict of {selector: value}.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fields": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "CSS selector → value mapping",
                }
            },
            "required": ["fields"],
        },
    },
    {
        "name": "scroll_down",
        "description": "Scroll the page down by a number of pixels (default 800).",
        "input_schema": {
            "type": "object",
            "properties": {"pixels": {"type": "integer", "default": 800}},
        },
    },
    {
        "name": "scroll_to_bottom",
        "description": "Scroll to the very bottom of the page, loading all lazy content.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "scrape_page",
        "description": "Return the current page content as clean markdown text.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_links",
        "description": "Return all links on the current page as a list of {text, href}.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "screenshot",
        "description": "Take a screenshot of the current page and save it to TheVoid.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Filename without extension"}},
        },
    },
    {
        "name": "wait_for",
        "description": "Wait for a CSS selector to appear on the page.",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "timeout": {"type": "integer", "default": 15000},
            },
            "required": ["selector"],
        },
    },
    {
        "name": "press_key",
        "description": "Press a keyboard key (e.g. Enter, Tab, Escape, Control+a).",
        "input_schema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    },
    {
        "name": "current_url",
        "description": "Return the current URL of the browser.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "extract_thread",
        "description": (
            "Extract the full conversation from an LLM thread URL "
            "(claude.ai, chatgpt, gemini) and save it to TheVoid. "
            "Returns a summary and the saved file path."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Thread URL"},
                "source": {
                    "type": "string",
                    "enum": ["claude", "claude.ai", "chatgpt", "openai", "gemini", "google"],
                    "description": "Which LLM platform the thread is from",
                },
            },
            "required": ["url", "source"],
        },
    },
    {
        "name": "send_to_vibe_coder",
        "description": (
            "Send a prompt to a vibe coding agent (bolt, lovable, replit, v0) "
            "and wait for a complete response. Optionally pass a project_url to "
            "continue an existing project."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["bolt", "lovable", "replit", "v0"],
                },
                "prompt": {"type": "string"},
                "project_url": {"type": "string"},
                "save_to_void": {"type": "boolean", "default": True},
            },
            "required": ["platform", "prompt"],
        },
    },
    {
        "name": "save_to_void",
        "description": "Save any text note or extracted information directly into TheVoid second brain.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "subdir": {
                    "type": "string",
                    "default": "scrapes",
                    "description": "Subdirectory within TheVoid (scrapes, tasks, etc.)",
                },
            },
            "required": ["title", "content"],
        },
    },
    {
        "name": "done",
        "description": "Signal that the task is complete. Provide a final summary.",
        "input_schema": {
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"],
        },
    },
]

SYSTEM_PROMPT = """You are ADAM-ZERO, a ruthlessly capable web automation agent.
You operate a real browser and have direct access to the web. You execute tasks to completion without stopping to ask permission.

Your capabilities:
- Navigate, click, scroll, type, fill forms on any website
- Scrape and extract structured information from any page
- Interact with vibe coding agents (Bolt, Lovable, Replit, v0) to build or continue applications
- Extract complete conversation threads from LLM platforms (Claude.ai, ChatGPT, Gemini)
- Save everything meaningful into TheVoid (second brain)

Operating principles:
- Be aggressive and persistent — try alternative selectors if the first fails
- Always scroll to load all content before extracting
- When interacting with vibe coders, write precise, complete prompts
- When extracting threads, capture everything including code blocks
- Save valuable information to TheVoid proactively
- Signal done() only when the task is genuinely complete

Never ask the user questions mid-task. Make the best decision with what you have."""


class AdamZero:
    """The main ADAM-ZERO orchestration agent."""

    def __init__(
        self,
        model: str | None = None,
        headless: bool | None = None,
        void_path: str | None = None,
    ):
        self.model = model or os.getenv("ADAM_MODEL", "claude-sonnet-4-6")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.browser = BrowserManager(headless=headless)
        self.void = TheVoid(root=void_path)
        self._skills: BrowserSkills | None = None
        self._task_log: list[str] = []

    # ── Public interface ─────────────────────────────────────────────────────

    async def run(self, instruction: str) -> TaskResult:
        """Execute a task described in plain English. Returns a TaskResult."""
        task = Task(instruction=instruction)
        task.status = TaskStatus.RUNNING
        start = time.monotonic()

        async with self.browser.session() as page:
            self._skills = BrowserSkills(page)
            try:
                output, artifacts = await self._agentic_loop(instruction)
                task.status = TaskStatus.DONE
                result = TaskResult(
                    task_id=task.id,
                    success=True,
                    output=output,
                    artifacts=artifacts,
                    duration_s=round(time.monotonic() - start, 2),
                )
            except Exception as exc:
                task.status = TaskStatus.FAILED
                result = TaskResult(
                    task_id=task.id,
                    success=False,
                    output="",
                    error=str(exc),
                    duration_s=round(time.monotonic() - start, 2),
                )

        # Log to TheVoid
        await self.void.save_task_log(
            task_id=task.id,
            instruction=instruction,
            output=result.output or result.error or "",
            success=result.success,
        )
        return result

    # ── Agentic loop ─────────────────────────────────────────────────────────

    async def _agentic_loop(self, instruction: str) -> tuple[str, list[str]]:
        """Run the Claude tool-use loop until done() is called."""
        messages: list[dict] = [{"role": "user", "content": instruction}]
        artifacts: list[str] = []
        final_summary = ""
        max_turns = 40

        for _ in range(max_turns):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            # Collect assistant content
            assistant_blocks = []
            tool_calls = []
            for block in response.content:
                assistant_blocks.append(block)
                if block.type == "tool_use":
                    tool_calls.append(block)

            messages.append({"role": "assistant", "content": response.content})

            if not tool_calls:
                # No tool calls — extract text and finish
                texts = [b.text for b in response.content if hasattr(b, "text")]
                final_summary = " ".join(texts)
                break

            # Execute all tool calls
            tool_results = []
            for call in tool_calls:
                if call.name == "done":
                    final_summary = call.input.get("summary", "Task complete.")
                    return final_summary, artifacts

                result_content, artifact = await self._execute_tool(call.name, call.input)
                if artifact:
                    artifacts.append(artifact)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": result_content,
                })

            messages.append({"role": "user", "content": tool_results})

        return final_summary or "Task completed (max turns reached).", artifacts

    # ── Tool dispatcher ──────────────────────────────────────────────────────

    async def _execute_tool(self, name: str, inp: dict) -> tuple[str, str | None]:
        """Execute a tool call. Returns (result_text, optional_artifact_path)."""
        s = self._skills
        artifact = None

        try:
            if name == "navigate":
                title = await s.navigate(inp["url"])
                return f"Navigated to: {title} ({await s.current_url()})", None

            elif name == "click":
                await s.click(inp["selector"])
                return f"Clicked: {inp['selector']}", None

            elif name == "click_text":
                await s.click_text(inp["text"])
                return f"Clicked text: {inp['text']}", None

            elif name == "type_text":
                await s.type_text(inp["selector"], inp["text"], inp.get("clear_first", True))
                return f"Typed into {inp['selector']}", None

            elif name == "fill_form":
                await s.fill_form(inp["fields"])
                return f"Filled {len(inp['fields'])} form fields", None

            elif name == "scroll_down":
                await s.scroll_down(inp.get("pixels", 800))
                return "Scrolled down", None

            elif name == "scroll_to_bottom":
                n = await s.scroll_to_bottom()
                return f"Scrolled to bottom ({n} scroll steps)", None

            elif name == "scrape_page":
                md = await s.get_markdown()
                # Truncate for context window
                return md[:8000] if len(md) > 8000 else md, None

            elif name == "get_links":
                links = await s.get_all_links()
                return json.dumps(links[:50]), None

            elif name == "screenshot":
                fname = inp.get("name", "screenshot")
                path = str(self.void.root / "scrapes" / f"{fname}.png")
                await s.screenshot(path)
                artifact = path
                return f"Screenshot saved: {path}", artifact

            elif name == "wait_for":
                found = await s.wait_for_selector(inp["selector"], inp.get("timeout", 15000))
                return f"Element {'found' if found else 'not found'}: {inp['selector']}", None

            elif name == "press_key":
                await s.press_key(inp["key"])
                return f"Pressed: {inp['key']}", None

            elif name == "current_url":
                return await s.current_url(), None

            elif name == "extract_thread":
                from adam_zero.platforms.llm import REGISTRY as LLM_REGISTRY
                source_key = inp["source"].lower()
                extractor_cls = LLM_REGISTRY.get(source_key)
                if not extractor_cls:
                    return f"Unknown LLM source: {source_key}", None
                extractor = extractor_cls(s)
                thread = await extractor.extract(inp["url"])
                path = await self.void.save_thread(thread)
                artifact = path
                summary = (
                    f"Extracted {thread.total_messages} messages from '{thread.title}' "
                    f"({thread.source}). Saved to: {path}"
                )
                return summary, artifact

            elif name == "send_to_vibe_coder":
                from adam_zero.platforms.vibe import REGISTRY as VIBE_REGISTRY
                platform_key = inp["platform"].lower()
                handler_cls = VIBE_REGISTRY.get(platform_key)
                if not handler_cls:
                    return f"Unknown vibe platform: {platform_key}", None
                handler = handler_cls(s)
                result: VibeChatResult = await handler.send_prompt(
                    prompt=inp["prompt"],
                    project_url=inp.get("project_url"),
                )
                if inp.get("save_to_void", True):
                    path = await self.void.save_vibe_session(result)
                    artifact = path
                    return (
                        f"Sent to {platform_key}. Response ({len(result.response)} chars). "
                        f"Code blocks: {len(result.code_blocks)}. Saved: {path}"
                    ), artifact
                return f"Sent to {platform_key}. Response: {result.response[:500]}", None

            elif name == "save_to_void":
                path = await self.void.save_note(
                    title=inp["title"],
                    content=inp["content"],
                    tags=inp.get("tags"),
                    subdir=inp.get("subdir", "scrapes"),
                )
                artifact = path
                return f"Saved to TheVoid: {path}", artifact

            else:
                return f"Unknown tool: {name}", None

        except Exception as exc:
            return f"Tool error ({name}): {exc}", None
