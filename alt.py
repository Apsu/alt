#!/usr/bin/env python

import click
import yaml

from typing import Dict, List, Any

Fingers: Dict[str, int] = {
    n: i for i, n in
    enumerate(
        [f"L{f}" for f in "PRMIT"] +
        [f"R{f}" for f in "TIMRP"]
    )
}

class Layout():
    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.layout = yaml.safe_load(f)

    def fingers(self, text: str) -> List[str]:
        return [self.layout["keys"][key]["finger"] if key in self.layout["keys"] else None for key in text]

    def finger(self, key: str) -> str:
        if key in self.layout["keys"]:
            return self.layout["keys"][key]["finger"]

class Hand():
    state: Dict[str, bool] = {f: False for f in "PRMIT"}

    def __init__(self) -> None:
        pass

    def press(key: str, layout: Layout) -> str:
        pass

@click.command()
@click.argument("word")
def alt(word: str) -> None:
    layout = Layout("layouts/qwerty.yaml")

    print(layout.fingers(word))

if __name__ == "__main__":
    alt()