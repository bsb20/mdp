#! /usr/bin/env python

import sys
import ast
import pprint

def matrix(source, dim,string=False):
    out = []
    for i in range(dim):
        row = []
        for j in range(dim):
            if string:
                pass
            else:
                row.append(source[(i,j)])
        out.append(row)
    return out


def parse(fname, keyword, display=8, output=False):
    f = open(fname)
    prev = ""
    for line in f:
        if prev == "VALUE FUNCTION" and keyword == prev:
            values = ast.literal_eval(line.strip())
            d = matrix(values, display)
            if output:
                pprint.pprint(d)
            return d
        if prev == "POLICY" and keyword == prev:
            policy = ast.literal_eval(line.strip())
            d = matrix(policy, display)
            if output:
                pprint.pprint(matrix(policy, display))
            return d
        if prev == "RATES" and keyword == prev:
            rates = ast.literal_eval(line.strip())
            d = matrix(rates, display)
            if output:
                pprint.pprint(matrix(rates, display))
            return d
        prev = line.strip()
    


if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2], 8, True)
