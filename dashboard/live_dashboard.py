from __future__ import annotations

import asyncio
from typing import Any

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from dashboard.keyboard_handler import KeyboardHandler
from dashboard.log_ring_buffer import LogRingBuffer
from dashboard.pages import (
    render_catalog,
    render_compliance,
    render_executive,
    render_finance,
    render_fulfillment,
    render_marketing,
    render_orders,
    render_system,
)
from dashboard.terminal_page_registry import TerminalPage, TerminalPageRegistry


class LiveDashboard:
    """Gestionnaire terminal à hauteur fixe et propriétaire unique de la sortie."""

    LINE_COUNT = 30
    PAGE_LINE_COUNT = 20

    def __init__(self, container: Any, refresh_seconds: float = 5) -> None:
        self.container = container
        self.refresh_seconds = refresh_seconds
        self.console = Console()
        self.stop_event = asyncio.Event()
        self.events = LogRingBuffer(6)
        self.keyboard = KeyboardHandler()
        self.pages = TerminalPageRegistry()
        self._register_pages()
        self.page = "executive"

    def _register_pages(self) -> None:
        for key, title, renderer in (
            ("executive", "Executive", render_executive),
            ("catalog", "Catalog", render_catalog),
            ("orders", "Orders", render_orders),
            ("fulfillment", "Fulfillment", render_fulfillment),
            ("finance", "Finance", render_finance),
            ("marketing", "Marketing", render_marketing),
            ("compliance", "Compliance", render_compliance),
            ("system", "System", render_system),
        ):
            self.pages.register(TerminalPage(key, title, renderer))

    def _fit(self, text: str, width: int) -> str:
        text = text.replace("\r", " ").replace("\n", " ")
        if len(text) > width:
            text = text[: max(0, width - 1)] + "…"
        return text.ljust(width)

    def render_lines(self, width: int | None = None) -> list[str]:
        state = self.container.dashboard_state()
        width = max(78, (width or self.console.width) - 6)
        page = self.pages.page(self.page)
        page_lines = list(page.render(state, width))[: self.PAGE_LINE_COUNT]
        page_lines.extend([""] * (self.PAGE_LINE_COUNT - len(page_lines)))
        events = list(self.events.lines())[-6:]
        events.extend([""] * (6 - len(events)))
        rows = page_lines + [
            "EVENTS (anneau fixe; les entrées anciennes sont remplacées)",
            *events,
            "PAGES [1] Executive [2] Catalog [3] Orders [4] Fulfillment [5] Finance [6] Marketing [7] Compliance [8] System",
            "CONTROL [R] Refresh [Q] Quit | sortie workers redirigée vers l'anneau d'événements",
            f"INPUT page={page.title} | mise à jour en place | aucune ligne ajoutée",
        ]
        rows = rows[: self.LINE_COUNT]
        rows.extend([""] * (self.LINE_COUNT - len(rows)))
        return [self._fit(row, width) for row in rows]

    def render(self) -> Group:
        lines = self.render_lines()
        body = Text("\n".join(lines), no_wrap=True, overflow="crop")
        return Group(Panel(body, border_style="cyan", padding=(0, 1), expand=True))

    def handle_key(self, key: str) -> bool:
        action = self.keyboard.action(key)
        if action == "quit":
            self.stop()
            return True
        if action in self.pages.keys():
            self.page = action
            self.events.append(f"Page changée: {self.pages.page(action).title}")
            return True
        return action == "refresh"

    async def run(self) -> None:
        self.events.append("Gestionnaire terminal initialisé")
        with Live(
            self.render(), console=self.console, refresh_per_second=4,
            screen=True, auto_refresh=False, transient=False,
        ) as live:
            elapsed = self.refresh_seconds
            while not self.stop_event.is_set():
                key = self.keyboard.read_key()
                forced = self.handle_key(key) if key else False
                if forced or elapsed >= self.refresh_seconds:
                    live.update(self.render(), refresh=True)
                    elapsed = 0.0
                interval = min(0.1, self.refresh_seconds)
                try:
                    await asyncio.wait_for(self.stop_event.wait(), timeout=interval)
                except asyncio.TimeoutError:
                    elapsed += interval

    def stop(self) -> None:
        self.stop_event.set()
