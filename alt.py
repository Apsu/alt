#!/usr/bin/env python

import click
import json
import yaml
from statistics import mean, median, mode

from typing import Dict, Tuple


class Layout():
    def __init__(self, file: str, thumbs: bool) -> None:
        with open(file) as f:
            self.layout = yaml.safe_load(f)

        # If thumbrow disabled
        if not thumbs:
            for key in self.layout["keys"]:
                # Skip space
                if key == ' ':
                    continue
                # Filter thumbs from fingers list
                self.layout["keys"][key]["fingers"] = [
                    f for f in self.layout["keys"][key]["fingers"]
                    if "T" not in f
                ]

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
@click.option("--max_age", "-m", default=3, help="Largest SFS to avoid")
@click.option("--file", "-f", help="Monkeytype wordlist to parse")
@click.option("--verbose", "-v", default=False, is_flag=True, help="Show keypresses")
@click.option("--thumbs", "-t", default=False, is_flag=True, help="Use thumbrow or not")
@click.option("--bigrams", "-b", default=False, is_flag=True, help="Show SFBs or not")
@click.argument("query", required=False)
def alt(file: str, max_age: int, verbose: bool, thumbs: bool, bigrams: bool, query: str) -> None:
    """Analyze string of characters"""

    layout = Layout("layouts/qwerty.yaml", thumbs)
    keyboard = Keyboard(layout, max_age)

    if file:
        with open(f"wordlists/{file}.txt") as f:
            query = ' '.join(f.readlines())
    elif query:
        print(query)
    else:
        print("One of --file or query required")
        return

    prev_char = ""
    prev_finger = ""
    sfbs = []
    rpts= []
    alts = []
    ages = []
    unknowns = []
    results = []
    usage = {finger:0 for finger in [f"L{f}" for f in "PRMIT"] + [f"R{f}" for f in "TIMRP"] }

    with click.progressbar(query, label="Processing") as query_bar:
        for char in query_bar:
            finger, age = keyboard.press(char)
            if finger == "None":
                unknowns.append(char)
                continue
            def_finger = layout.fingers(char)[0]
            ages.append(float(age))
            if finger != def_finger:
                alts.append((char, finger))
            if finger == prev_finger:
                if char != prev_char:
                    sfbs.append((prev_char, char, finger))
                else:
                    rpts.append((char, finger))
            prev_char = char
            prev_finger = finger
            results.append((char, finger))
            usage[finger] += 1

    if verbose:
        for res in results:
            print(f"{res[0]} -> {res[1]}")

    len_query = len(query)
    print("-"*12)
    print(f"SFBS: {len(sfbs) / len_query:.2%}")
    if bigrams:
        for sfb in sorted(set(sfbs)):
            print(f"{sfb[0]}{sfb[1]}: {sfb[2]}")
    print(f"RPTS: {len(rpts) / len_query:.2%}")
    print(f"ALTS: {len(alts) / len_query:.2%}")
    print(f"UNKNOWNS: {len(unknowns) / len_query:.2%}")
    print(f"AGES: avg = {mean(ages)}, median = {median(ages)}, mode = {mode(ages)}")
    print(f"USAGE: {' '.join([f'{f}:{u/len_query:.2%}' for f, u in usage.items()])}")

if __name__ == "__main__":
    alt() # type:ignore
