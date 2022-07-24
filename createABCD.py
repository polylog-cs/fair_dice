import itertools
import math
import numpy as np
import textwrap

permutations = []
for perm in itertools.permutations(["A", "B", "C", "D"]):
    permutations.append(
        {"A" : perm[0], "B" : perm[1], "C" : perm[2], "D" : perm[3]}
    )

str1 = "ABCD"

def extend(str):
    out = ""
    for perm in permutations:
        for i in range(len(str)):
            out += perm[str[i]]
    return out

str4 = extend(extend(extend(str1)))
for str in textwrap.wrap(str4, 4*24):
    print(str)
