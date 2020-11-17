#!/usr/bin/env python3

from linearsystem import from_bmatrix, matrix
import sys


def from_bmatrix(s):
    s = s.replace("\n", "")
    lines = s.split("\\")
    arr = []
    for line in lines:
        if line != "":
            arr.append(list(map(int, line.split(" &"))))
    return matrix(arr)


s = sys.argv[1].replace("\\n", "\n")
s = s.replace("\t", "")
A = from_bmatrix(s)

A.reduce(True)
print(A.tex_str())
