#!/usr/bin/env python

import operator
import sys

from typing import Dict, List, Tuple
from itertools import product, pairwise

LAYOUT = {
    k:(r,c) for r, x in enumerate([
        "qwertyuiop",
        "asdfghjkl;'",
        "~zxcvbnm,./",
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
    ["p","rp","mr","im","im","IM","IM","MI","RM","RP"],
    # a   s    d    f    g   h   j    k    l   ;   '
    ["p","rm","mi","im","i","I","IM","MR","R","P","P"],
    #    z   x   c   v   b    n   m   ,   .   /
    ["","r","m","i","i","Ii","I","I","M","R","P"],
])

def parse(word: str) -> List[str]:
    options = [FINGERMAP[LAYOUT[char]] for char in word]
    columns = [LAYOUT[char][1] for char in word]
    cpairs = list(pairwise(columns))

    f = lambda x: "prmitTIMRPP".index(x)
    eq = lambda x: operator.eq(*x)
    # Distance from home column
    dist = lambda x, y: abs(f(x) - y)

    def score(option):
        opairs = list(pairwise(option))
        sfb_score = sum(map(eq, opairs))
        d_score = sum([
            dist(*cxy)
            for cxy in zip(option, columns)
        ])
        u_score = len(option) - len(set(option))
        return sfb_score, u_score, d_score

    predictions = sorted([(option, score(option))
        for option in
        product(*options)
        ], key=lambda k: (k[1][0], k[1][1], k[1][2])
    )

    return predictions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a word")
        sys.exit(-1)

    for word in sys.argv[1].split():
        print(parse(word)[0])
