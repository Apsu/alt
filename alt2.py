#!/usr/bin/env python

import operator
import sys
from typing import Dict, List, Tuple
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

# PRMIT
LHAND = [
    [(-1,0),(-1,+1)],
    [(-1,0),(-1,+1),(+1,-1)],
    [(-1,0),(-1,+1),(+1,-1)],
    [(-1,0),(-1,+1),(+1,-1),(+1,0),(+1,+1),(0,+1)],
    [(0,-1),(0,+1)]
]

# TIMRP
RHAND = [
    [(0,-1),(0,+1)],
    [(-1,0),(-1,+1),(+1,0),(+1,-1),(+1,-2),(0,-1)],
    [(-1,0),(-1,+1),(+1,0)],
    [(-1,0),(-1,+1),(+1,0)],
    [(-1,0),(+1,0)],
]

HANDS = LHAND + RHAND
FINGERS = [f"L{f}" for f in "PRMIT"] + [f"R{f}" for f in "TIMRP"]
HOMEMAP = [(1,0),(1,1),(1,2),(1,3)] + [(2,3),(2,5)] + [(1,6),(1,7),(1,8),(1,9)]
ALTMAP = {
    LAYOUT[k]: [LAYOUT[tuple(map(operator.add, k, a))] for a in HANDS[i]]
    for i, k in enumerate(HOMEMAP)
}
"""
'a': ['q', 'w'], 
's': ['w', 'e', 'z'],
'd': ['e', 'r', 'x'],
'f': ['r', 't', 'c', 'v', 'b', 'g'],
'v': ['c', 'b'],
'n': ['b', 'm'],
'j': ['u', 'i', 'm', 'n', 'b', 'h'],
'k': ['i', 'o', ','],
'l': ['o', 'p', '.'],
';': ['p', '/']
"""
LAYOUT = {
    k:(r,c) for r, x in enumerate([
        "qwertyuiop",
        "asdfghjkl;",
        "zxcvbnm,./",
        " "
    ])
    for c, k in enumerate(x)
}

class FingerMap:
    def __init__(self, fmap: List[List[str]]):
        self.fmap = fmap
    def __getitem__(self, index: Tuple[int, int]) -> str:
        return self.fmap[index[0]][index[1]]

FINGERMAP = FingerMap([
    # q   w    e    r    t    y    u    i    o    p
    ["p","rp","rm","mi","im","IM","IM","MR","RP","RP"],
    # a   s    d    f    g   h   j    k    l    ;
    ["p","rm","mi","im","i","I","IM","MR","RP","P"],
    # z   x   c    v    b      n    m    ,   .   /
    ["r","m","ti","ti","tTiI","TI","TI","M","R","P"],
    # " "
    ["tT"]
])

def predict(word: str) -> List[str]:
    predictions = [
        FINGERMAP[LAYOUT[char]]
        for char in word
    ]

    return list(product(*predictions))
    # return predictions

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a word")
        sys.exit(-1)

    print(predict(sys.argv[1]))