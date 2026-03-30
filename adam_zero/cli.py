"""ADAM-ZERO CLI — menace-mode web agent."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

import anthropic

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import argparse

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint

from adam_zero.core.agent import AdamZero
from adam_zero.the_void.writer import TheVoid

console = Console()

BANNER = """
[bold red]  █████╗ ██████╗  █████╗ ███╗   ███╗      ███████╗███████╗██████╗  ██████╗ [/]
[bold red] ██╔══██╗██╔══██╗██╔══██╗████╗ ████║      ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗[/]
[bold red] ███████║██║  ██║███████║██╔████╔██║        ███╔╝ █████╗  ██████╔╝██║   ██║[/]
[bold red] ██╔══██║██║  ██║██╔══██║██║╚██╔╝██║       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║[/]
[bold red] ██║  ██║██████╔╝██║  ██║██║ ╚═╝ ██║      ███████╗███████╗██║  ██║╚██████╔╝[/]
[bold red] ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ [/]
[dim]Web automation. Vibe coding. Second-brain harvesting.[/]
"""


def _check_api_key():
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print(
            Panel(
                "[bold red]ANTHROPIC_API_KEY not set.[/]\n"
                "Set it in your environment or copy [cyan].env.example[/] → [cyan].env[/]",
                title="[red]Missing API Key[/]",
            )
        )
        sys.exit(1)


def _build_agent(args) -> AdamZero:
    headless = not getattr(args, "visible", False)
    void_path = getattr(args, "void", None)
    return AdamZero(headless=headless, void_path=void_path)


def _print_result(result) -> None:
    status = "[bold green]SUCCESS[/]" if result.success else "[bold red]FAILED[/]"
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("Status", status)
    table.add_row("Task ID", result.task_id)
    table.add_row("Duration", f"{result.duration_s}s")
    if result.artifacts:
        table.add_row("Saved to TheVoid", "\n".join(result.artifacts))
    console.print(Panel(table, title="[bold]Task Result[/]"))

    if result.output:
        console.print(Panel(Markdown(result.output), title="[bold]Output[/]"))
    if result.error:
        console.print(Panel(f"[red]{result.error}[/]", title="[bold red]Error[/]"))


# ── Commands ─────────────────────────────────────────────────────────────────

async def cmd_run(args) -> None:
    """adam run "do something on the web" """
    _check_api_key()
    agent = _build_agent(args)
    instruction = " ".join(args.instruction)

    console.print(BANNER)
    console.print(Panel(f"[bold cyan]{instruction}[/]", title="[bold]Task[/]"))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("ADAM-ZERO running...", total=None)
        result = await agent.run(instruction)

    _print_result(result)


async def cmd_extract(args) -> None:
    """adam extract <url> --source claude"""
    _check_api_key()
    agent = _build_agent(args)
    url = args.url
    source = args.source

    instruction = f"Extract the full thread from {url} (source: {source}) and save it to TheVoid."
    console.print(Panel(f"[bold cyan]Extracting:[/] {url}", title="[bold]Thread Extraction[/]"))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        progress.add_task("Extracting thread...", total=None)
        result = await agent.run(instruction)

    _print_result(result)


async def cmd_vibe(args) -> None:
    """adam vibe bolt "build me a todo app" """
    _check_api_key()
    agent = _build_agent(args)
    platform = args.platform
    prompt = " ".join(args.prompt)
    project_url = getattr(args, "project_url", None)

    instruction = f'Send this prompt to the {platform} vibe coder and save the session to TheVoid: "{prompt}"'
    if project_url:
        instruction += f" Continue from project URL: {project_url}"

    console.print(Panel(f"[bold cyan]{platform.upper()}:[/] {prompt}", title="[bold]Vibe Coder[/]"))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        progress.add_task(f"Talking to {platform}...", total=None)
        result = await agent.run(instruction)

    _print_result(result)


async def cmd_scrape(args) -> None:
    """adam scrape <url> --title "My Note" """
    _check_api_key()
    agent = _build_agent(args)
    url = args.url
    title = getattr(args, "title", None) or url

    instruction = (
        f"Navigate to {url}, scroll to the bottom to load all content, "
        f"extract the full page as markdown, and save it to TheVoid with title: {title!r}"
    )

    console.print(Panel(f"[bold cyan]Scraping:[/] {url}", title="[bold]Web Scrape[/]"))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        progress.add_task("Scraping...", total=None)
        result = await agent.run(instruction)

    _print_result(result)


def cmd_void(args) -> None:
    """adam void -- show TheVoid index"""
    void_path = getattr(args, "void", None)
    void = TheVoid(root=void_path)
    index = void.root / "index.md"
    if index.exists():
        console.print(Markdown(index.read_text()))
    else:
        console.print(f"[dim]TheVoid is empty. Run a task to populate it.[/]")
    console.print(f"\n[dim]Root:[/] {void.root}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="adam",
        description="ADAM-ZERO — web automation agent",
    )
    parser.add_argument("--visible", action="store_true", help="Show browser window (non-headless)")
    parser.add_argument("--void", metavar="PATH", help="Override TheVoid directory path")

    sub = parser.add_subparsers(dest="command", required=True)

    # adam run
    run_p = sub.add_parser("run", help="Run any task in plain English")
    run_p.add_argument("instruction", nargs="+", help="Task instruction")

    # adam extract
    ext_p = sub.add_parser("extract", help="Extract an LLM thread and save to TheVoid")
    ext_p.add_argument("url", help="Thread URL")
    ext_p.add_argument("--source", choices=["claude", "chatgpt", "gemini"], default="claude", help="LLM source platform")

    # adam vibe
    vibe_p = sub.add_parser("vibe", help="Talk to a vibe coding agent")
    vibe_p.add_argument("platform", choices=["bolt", "lovable", "replit", "v0"])
    vibe_p.add_argument("prompt", nargs="+", help="Prompt to send")
    vibe_p.add_argument("--project-url", help="Continue from an existing project URL")

    # adam scrape
    scrape_p = sub.add_parser("scrape", help="Scrape a URL and save to TheVoid")
    scrape_p.add_argument("url", help="URL to scrape")
    scrape_p.add_argument("--title", help="Title for the saved note")

    # adam void
    sub.add_parser("void", help="Show TheVoid index")

    args = parser.parse_args()

    if args.command == "run":
        asyncio.run(cmd_run(args))
    elif args.command == "extract":
        asyncio.run(cmd_extract(args))
    elif args.command == "vibe":
        asyncio.run(cmd_vibe(args))
    elif args.command == "scrape":
        asyncio.run(cmd_scrape(args))
    elif args.command == "void":
        cmd_void(args)


if __name__ == "__main__":
    main()
