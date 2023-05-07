#!/usr/bin/env python

import click
import json
import yaml
from statistics import mean, median, mode

from typing import Dict, Tuple


class Layout():
    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.layout = yaml.safe_load(f)

    def fingers(self, key: str) -> list[str]:
        if key in self.layout["keys"]:
            fingers = self.layout["keys"][key]["fingers"]
            return fingers
        return ["None"]


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
        self.max_age = max_age
        self.hands = Hands(max_age)

    def press(self, char: str) -> Tuple[str, int]:
        # Get options
        options = self.layout.fingers(char)
        if options == ["None"]:
            return "None", 0
        # LRU tracker
        lru = {}
        # Walk options
        def_finger = options[0]

        for finger in options:
            age = self.hands.age(finger)

            # If not used recently or same key was pressed last by this finger
            if age == 0 or self.hands.pressed(finger, char):
                # Mark used
                self.hands.press(finger, char)
                return finger, age
            # Track ages
            else:
                lru[finger] = self.hands.age(finger)

        # Return least recently used
        oldest = max(lru.items(), key=lambda k: k[1])
        # print(f"LRU: {char} {lru}, oldest: {oldest}")
        self.hands.press(oldest[0], char)
        return oldest


@click.command()
@click.option("--max_age", "-m", default=2, help="Largest SFS to avoid")
@click.option("--file", "-f", default="english", help="Monkeytype wordlist to parse")
@click.argument("query", required=False)
def alt(file: str, max_age: int, query: str) -> None:
    """Analyze string of characters"""

    layout = Layout("layouts/qwerty.yaml")
    keyboard = Keyboard(layout, max_age)

    prev_char = ""
    prev_finger = ""
    sfbs = []
    rpts= []
    alts = []
    ages = []
    unknowns = []

    if not query:
        with open(f"wordlists/{file}.json") as f:
            query = json.load(f)["words"]
    else:
        print(query)

    query = ' '.join(query).lower()
    len_query = len(query)

    for char in query:
        finger, age = keyboard.press(char)
        if finger == "None":
            unknowns.append(char)
            continue
        def_finger = layout.fingers(char)[0]
        ages.append(float(age))
        if finger != def_finger:
            alts.append((char, finger, age))
        if finger == prev_finger:
            if char != prev_char:
                sfbs.append((prev_char, char, finger))
            else:
                rpts.append((char, finger))
        prev_char = char
        prev_finger = finger

    print("-"*12)
    print(f"SFB: {len(sfbs) / len_query:.2%}")
    for sfb in sorted(set(sfbs)):
        print(f"{sfb[0]}{sfb[1]}: {sfb[2]}")
    print(f"RPT: {len(rpts) / len_query:.2%}")
    print(f"ALTS: {len(alts) / len_query:.2%}")
    print(f"UNKNOWN: {len(unknowns) / len_query:.2%}")
    print(f"AGES: avg = {mean(ages)}, median = {median(ages)}, mode = {mode(ages)}")


if __name__ == "__main__":
    alt() # type:ignore
