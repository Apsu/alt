#!/usr/bin/env python

import click
import operator
import sys

from collections import Counter
from typing import Dict, List, Tuple
from itertools import product, pairwise, combinations

LAYOUT = {
    k:(r,c) for r, x in enumerate([
        "qwertyuiop",
        "asdfghjkl;'",
        "zxcvbnm,./",
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
    ["p","rp","mr","im","i","IM","IM","MI","RM","RP"],
    # a   s    d    f    g   h   j    k    l   ;   '
    ["p","rm","mi","im","i","I","IM","MR","R","P","P"],
    # z   x   c   v   b    n   m    ,   .   /
    ["r","m","i","i","Ii","I","I","M","R","P"],
])

def parse(word: str) -> List[str]:
    options = [FINGERMAP[LAYOUT[char]] for char in word if char in LAYOUT]
    columns = [LAYOUT[char][1] for char in word if char in LAYOUT]
    cpairs = list(pairwise(columns))
    wpairs = list(pairwise(word))

    f = lambda x: "prmitTIMRPP".index(x)
    eq = lambda x: operator.eq(*x[0]) if not operator.eq(*x[1]) else False
    dist = lambda x, y: abs(f(x) - y)

    def score(option: List[str]) -> Tuple[int, int, int]:
        opairs = list(pairwise(option))
        sfb_score = sum(map(eq, zip(opairs, wpairs)))
        sfs_score = len(set(zip(option, word)))
        dfh_score = sum([dist(*cxy) for cxy in zip(option, columns)])
        return sfb_score, sfs_score, dfh_score

    predictions = sorted([(option, score(option))
        for option in product(*options)
        ], key=lambda k: (k[1][0], k[1][1], k[1][2])
    )

    return predictions[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a word")
        sys.exit(-1)

    sfbs = 0
    length = 0
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            for word in line.split():
                parsed = parse(word.lower())
                sfbs += parsed[1][0]
                length += len(word)
                # print(word)
                # print(parsed)

    print(f"SFBs: {sfbs / length:.2%}")
