#!/usr/bin/env python

import sys
from typing import Dict, List
from itertools import product

LAYOUT = {
    (r, c): k for r, x in enumerate([
        "qwertyuiop",
        "asdfghjkl;",
        "zxcvbnm,./",
        " "
    ])
    for c, k in enumerate(x)
}

FINGERS = [f"L{f}" for f in "PRMI"] + [f"R{f}" for f in "IMRP"]

# PRMI
LHAND = [
    [(+1,0),(+1,+1)],
    [(+1,0),(+1,+1),(-1,-1)],
    [(+1,0),(+1,+1),(-1,-1)],
    [(+1,0),(+1,+1),(-1,-1),(-1,0),(-1,+1),(0,+1)],
]
# IMRP
RHAND = [
    [(+1,0),(+1,+1),(-1,0),(-1,-1),(-1,-2),(0,-1)],
    [(+1,0),(+1,+1),(-1,0)],
    [(+1,0),(+1,+1),(-1,0)],
    [(+1,0),(-1,0)],
]

def predict(word: str) -> List[str]:
    predictions = []
    len_word = len(word)
    for index, char in enumerate(word):
        next_char = word[index+1] if index < len_word-1 else ""
        print(f"{char}:{next_char}")

    return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a word")
        sys.exit(-1)

    print(predict(sys.argv[1]))