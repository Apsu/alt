#!/usr/bin/env python

import click
import yaml

from typing import Dict, List, Any, Iterator, Tuple


class Layout():
    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.layout = yaml.safe_load(f)

    # def fingers(self, text: str) -> list[tuple[str, Any]]:
    #     return [(key, self.layout["keys"][key]["fingers"] if key in self.layout["keys"] else []) for key in text]

    def fingers(self, key: str) -> list[str]:
        if key in self.layout["keys"]:
            fingers = self.layout["keys"][key]["fingers"]
            return fingers
        return []
    

class Hands():
    max_use: int = 2
    hands: Dict[str, Dict] = {
        finger: {
            "use": 0,
            "key": ""
        }
        for finger in
            [f"L{f}" for f in "PRMIT"] +
            [f"R{f}" for f in "TIMRP"]
    }

    def __getitem__(self, k: str) -> Tuple[int, str]:
        return self.hands[k]["use"], self.hands[k]["key"]

    def reset(self) -> None:
        for k in self.hands:
            self.hands[k] = {"use": 0, "key": ""}
    
    def pressed(self, finger: str, char: str) -> bool:
        return self.hands[finger]["key"] == char
    
    def press(self, finger: str, char: str) -> None:
        for k in self.hands:
            use = self.hands[k]["use"]
            if k != finger:
                if use > 0:
                    if use < self.max_use:
                        self.hands[k]["use"] += 1
                    else:
                        self.hands[k] = {"use": 0, "key": ""}
            else:
                self.hands[k] = {"use": 1, "key": char}
    
class Keyboard():
    layout: Layout
    hands: Hands

    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.hands = Hands()

    def press(self, char: str) -> str:
        # Get options
        fingers = self.layout.fingers(char) 
        # Walk options
        lru = {}
        use = ""
        for finger in fingers:
            idx, key = self.hands[finger]

            # If not used recently or same key was pressed last by finger
            if idx == 0 or self.hands.pressed(finger, char):
                # Mark used
                self.hands.press(finger, char)
                return finger
            # Track usages
            else:
                lru[finger] = self.hands[finger]

        # Get least recently used
        oldest = max(lru, key=lambda k:k[0])
        print(f"LRU: {lru}, Oldest: {oldest}")
        # No option found so return first choice
        self.hands.press(fingers[0], char)
        return fingers[0]

@click.command()
@click.argument("query")
def alt(query: str) -> None:
    layout = Layout("layouts/qwerty.yaml")

    keyboard = Keyboard(layout)

    for char in query:
        print(f"{char} -> {keyboard.press(char)}")

if __name__ == "__main__":
    alt() # type:ignore
