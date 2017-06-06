#! /usr/bin/env python

from parser import parse
from parser import matrix
from parallel_greedy import get_rate
from matplotlib import pyplot as plt

import numpy as np
import pprint
import matplotlib
import sys

def get_mdp_rates(mdp_policy, p1, p2, lambd):
    mdp_rates = []
    for i, row in enumerate(mdp_policy):
        rates_row = [get_rate(a, i, j, p1, p2, lambd, lambd) for j, a in enumerate(row)]
        mdp_rates.append(rates_row)
    return mdp_rates

if __name__ == "__main__":
    print "HERE"
    diff = {}
    if len(sys.argv) >= 2:
        lambd = int(sys.argv[1])
        suffix = "_{0}_{0}".format(lambd)
    else:
        lambd = 5
        suffix = ""
    for p1 in np.arange(.1,1,.1):
        for p2 in np.arange(.1,1,.1):
            if p1 < p2:
                greedy_rates = parse("greedy{0}/greedy_{1}_{2}.txt".format(suffix, int(10*p1),int(10*p2)), "RATES")
                mdp_policy = parse("opt{0}/{1}_{2}.txt".format(suffix, int(10*p1),int(10*p2)), "POLICY")
                mdp_rates = []
                for i, row in enumerate(mdp_policy):
                    rates_row = [get_rate(a, i, j, p1, p2, lambd, lambd) for j, a in enumerate(row)]
                    mdp_rates.append(rates_row)
                print "p={0}, p={1}".format(p1,p2)
                print "GREEDY"
                pprint.pprint([["{0:0.3f}".format(y) for y in x] for x in greedy_rates])
                print "MDP"
                pprint.pprint([["{0:0.3f}".format(y) for y in x] for x in mdp_rates])
                if mdp_rates == greedy_rates:
                    score = 0
                else:
                    score = 0
                    for i, v1 in enumerate(mdp_rates):
                        for j, v2 in enumerate(v1):
                            score += abs(v2 - greedy_rates[i][j])
                diff[(p1, p2)] = score
                diff[(p2, p1)] = score
            if p1 == p2:
                diff[(p1, p2)] = 0
    data = []
    for p1 in np.arange(.1,1,.1):
        row = []
        for p2 in np.arange(.1,1,.1):
            print p1, p2
            if p1 == p2:
                row.append(0)
            elif p1 < p2:
                row.append(diff[(p1,p2)])
            else:
                row.append(diff[(p2,p1)])
        data.append(row)
    heatmap = plt.pcolor(data, cmap=matplotlib.cm.Blues)
    plt.show()

