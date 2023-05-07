#!/usr/bin/env python

import click
import yaml

from typing import Dict


class Layout():
    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.layout = yaml.safe_load(f)

    def fingers(self, key: str) -> list[str]:
        if key in self.layout["keys"]:
            fingers = self.layout["keys"][key]["fingers"]
            return fingers
        return []


class Hands():
    hands: Dict[str, Dict] = {
        finger: {
            "age": 0,
            "key": ""
        }
        for finger in
            [f"L{f}" for f in "PRMIT"] +
            [f"R{f}" for f in "TIMRP"]
    }

    def __init__(self, max_age: int = 2) -> None:
        self.max_age = max_age

    def age(self, finger: str) -> int:
        return self.hands[finger]["age"]

    def reset(self) -> None:
        for k in self.hands:
            self.hands[k] = {"age": 0, "key": ""}

    def pressed(self, finger: str, char: str) -> bool:
        # Was this character pressed by this finger?
        return self.hands[finger]["key"] == char

    def press(self, finger: str, char: str) -> None:
        for k in self.hands:
            age = self.hands[k]["age"]
            # Target finger
            if k == finger:
                self.hands[k] = {"age": 1, "key": char}
            # Other fingers
            else:
                # Used recently
                if age > 0:
                    # But not too recently
                    if age < self.max_age:
                        # Increment
                        self.hands[k]["age"] += 1
                    # Stale, reset
                    else:
                        self.hands[k] = {"age": 0, "key": ""}


class Keyboard():
    layout: Layout
    hands: Hands

    def __init__(self, layout: Layout, max_age: int) -> None:
        self.layout = layout
        self.hands = Hands(max_age)

    def press(self, char: str) -> str:
        # Get options
        options = self.layout.fingers(char)
        # LRU tracker
        lru = {}
        # Walk options
        for finger in options:
            idx = self.hands.age(finger)

            # If not used recently or same key was pressed last by this finger
            if idx == 0 or self.hands.pressed(finger, char) == True:
                # Mark used
                self.hands.press(finger, char)
                return finger
            # Track ages
            else:
                lru[finger] = self.hands.age(finger)

        # Return least recently used
        oldest = max(lru.items(), key=lambda k: k[1])
        self.hands.press(oldest[0], char)
        return oldest[0]


@click.command()
@click.option("--max_age", "-m", default=3, help="Largest SFS to avoid")
@click.argument("query", nargs=-1)
def alt(query: str, max_age: int) -> None:
    """Analyze string of characters"""

    layout = Layout("layouts/qwerty.yaml")

    keyboard = Keyboard(layout, max_age)

    for char in ''.join(query):
        print(f"{char} -> {keyboard.press(char)}")


if __name__ == "__main__":
    alt() # type:ignore
