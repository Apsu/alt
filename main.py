#!/usr/bin/env python

import json
import random

from pathlib import Path
from typing import Dict, Any, Iterable

from textual import events, log
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.reactive import reactive
from textual.widgets import Header, Footer, Label
from textual.events import Resize

FINGERS = ["lp", "lr", "lm", "li", "lt", "rt", "ri", "rm", "rr", "rp"]

class KbKey(Label):
    pass

class Legend(Label):
    pass

class Ticker(Label):
    def __init__(self, words:list[str] = []):
        super().__init__()
        self.words = " ".join(random.choices(words, k=100))
        self.index = 0

    def on_resize(self, message: Resize):
        self.width = message.size.width // 2
        self.ping()

    def walk(self):
        self.index += 1 if self.index < len(self.words) else 0
        self.ping()

    def ping(self):
        current = self.words[self.index:self.index + self.width]
        self.update(f"[r]{current[:1]}[/r]{current[1:]}")


# class FilteredDirectoryTree(DirectoryTree):
#     def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        # return [path for path in paths if not path.name.startswith(".")]

class AltApp(App):
    """Keyboard layout alt-fingering tool"""

    TITLE = "Alt"
    CSS_PATH = "layout.css"
    BINDINGS = [ ("escape", "quit", "Exit program") ]
    keyboard: Dict[str, Any] = {}
    wordlist: Dict[str, Any]
    ticker: Ticker

    def __init__(self):
        super().__init__()
        with open("wordlists/english.json") as f:
            self.wordlist = json.load(f)

        self.ticker = Ticker(self.wordlist["words"])

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header(show_clock=True)

        yield self.ticker

        with Grid():
            with open("layouts/qwerty.json") as f:
                layout = json.load(f)
                self.sub_title = layout["name"]
                for key, val in dict(sorted(layout["keys"].items(), key=lambda x:(x[1]['row'], x[1]['col']))).items():
                    self.keyboard[key] = val
                    self.keyboard[key]["widget"] = KbKey(key, classes=f"row{val['row']}")
                    yield self.keyboard[key]["widget"]

            for finger in FINGERS:
                yield Legend(finger.upper(), classes=f"legend {finger}")

        yield Footer()

    def on_key(self, event: events.Key) -> None:
        self.ticker.walk()
        self.query(KbKey).remove_class(*FINGERS)
        if event.character in self.keyboard:
            finger = self.keyboard[event.character]["finger"].lower()
            self.keyboard[event.character]["widget"].toggle_class(finger)

if __name__ == "__main__":
    app = AltApp()
    app.run()