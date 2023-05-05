#!/usr/bin/env python

import json
import random

from art import text2art

from typing import Dict, Any

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal
from textual.widgets import Header, Footer, Label
from textual.events import Key, Resize
from textual.color import Color

FINGERS = ["lp", "lr", "lm", "li", "lt", "rt", "ri", "rm", "rr", "rp"]
# COLORS = ["#ff0000ff", "#ff8700ff", "#ffd300ff", "#deff0aff", "#a1ff0aff", "#0aff99ff", "#0aefffff", "#147df5ff", "#580affff", "#be0affff"]
# COLORS = ["#7400b8ff", "#6930c3ff", "#5e60ceff", "#5390d9ff", "#4ea8deff", "#48bfe3ff", "#56cfe1ff", "#64dfdfff", "#72efddff", "#80ffdbff"]
# COLORS = ["#fbf8cc","#fde4cf","#ffcfd2","#f1c0e8","#cfbaf0","#a3c4f3","#90dbf4","#8eecf5","#98f5e1","#b9fbc0"]
PALETTE = ["#001219","#005f73","#0a9396","#94d2bd","#e9d8a6","#ee9b00","#ca6702","#bb3e03","#ae2012","#9b2226"]


class KbKey(Label):
    pass

class Legend(Label):
    pass

class Letter(Label):
    pass


class Alt(App):
    """Keyboard layout alt-fingering tool"""

    TITLE = "Alt"
    CSS_PATH = "layout.css"
    BINDINGS = [ ("escape", "quit", "Exit program") ]
    keyboard: Dict[str, Any] = {}
    wordlist: Dict[str, Any]

    def __init__(self):
        super().__init__()
        with open("wordlists/english.json") as f:
            self.wordlist = json.load(f)

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header(show_clock=True)

        with Vertical():
            with Horizontal():
                for letter in "testing":
                    finger = random.choice(FINGERS)
                    color = random.choice(PALETTE)
                    yield Letter(text2art(letter, font="c_consen")).set_styles(f"color: {color};")

            with Grid():
                with open("layouts/qwerty.json") as f:
                    layout = json.load(f)
                    self.sub_title = layout["name"]
                    for key, val in dict(sorted(layout["keys"].items(), key=lambda x:(x[1]['row'], x[1]['col']))).items():
                        self.keyboard[key] = val
                        self.keyboard[key]["widget"] = KbKey(key, classes=f"row{val['row']}")
                        yield self.keyboard[key]["widget"]

                for index, finger in enumerate(FINGERS):
                    yield Legend(finger.upper()).set_styles(f"background: {PALETTE[index]};")

        yield Footer()

    def on_key(self, event: Key) -> None:
        # self.ticker.walk()
        # self.query(KbKey).remove_class(*FINGERS)
        self.query(KbKey).set_styles(f"background: {Color.parse('$background')};")
        if event.character in self.keyboard:
            finger = self.keyboard[event.character]["finger"].lower()
            color = PALETTE[FINGERS.index(finger)]
            self.keyboard[event.character]["widget"].set_styles(f"background: {color};")

if __name__ == "__main__":
    app = Alt()
    app.run()