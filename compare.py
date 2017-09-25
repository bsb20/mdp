#! /usr/bin/env python

from parser import parse
from parser import matrix
from parallel_greedy import get_rate
from matplotlib import pyplot as plt

import numpy as np
import pprint
import matplotlib
import sys

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compare policies")
    parser.add_argument("--l1", type = str, default=5)
    parser.add_argument("--l2", type = str, default=5)
    parser.add_argument("--leq", action="store_true")
    parser.add_argument("action", type=str, default="heat")
    parser.add_argument("policy1", type=str, default="greedy")
    parser.add_argument("policy2", type=str, default="opt")
    args = parser.parse_args()
    diff = {}
    suffix = "_{0}_{1}".format(args.l1, args.l2)
    args.l1 = float(args.l1)
    args.l2 = float(args.l2)
    if args.action == "avg":
        for p1 in np.arange(.1,1,.1):
            for p2 in np.arange(.1,1,.1):
                p1 = round(p1, 2)
                p2 = round(p2, 2)
                if (not args.leq and p1 < p2) or (args.leq and p1 <= p2):
                    policy1_avg = parse("{0}{1}/{0}_{2}_{3}.txt".format(args.policy1, suffix, int(10*p1),int(10*p2)), "AVG")
                    policy2_avg = parse("{0}{1}/{0}_{2}_{3}.txt".format(args.policy2, suffix, int(10*p1),int(10*p2)), "AVG")

                    print p1, p2, ":"
                    print args.policy1, policy1_avg, args.policy2, policy2_avg, "Diff", float(policy1_avg) - float(policy2_avg), "Percentage Diff", 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
    if args.action == "heat":
        for p1 in np.arange(.1,1,.1):
            for p2 in np.arange(.1,1,.1):
                p1 = round(p1, 2)
                p2 = round(p2, 2)
                if (not args.leq and p1 < p2) or (args.leq and p1 <= p2):
                    policy1_avg = parse("{0}{1}/{0}_{2}_{3}.txt".format(args.policy1, suffix, int(10*p1),int(10*p2)), "AVG")
                    policy2_avg = parse("{0}{1}/{0}_{2}_{3}.txt".format(args.policy2, suffix, int(10*p1),int(10*p2)), "AVG")
                    diff[(p1, p2)] = 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
                    diff[(p2, p1)] = 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
                if p1 == p2 and not args.leq:
                    diff[(p1, p2)] = 0
        data = []
        max_pct = 0
        for p1 in np.arange(.1,1,.1):
            row = []
            for p2 in np.arange(.1,1,.1):
                p1 = round(p1, 2)
                p2 = round(p2, 2)
                if p1 == p2:
                    print p1, p2
                    print diff[(p1,p2)]
                    row.append(diff[(p1,p2)] if args.leq else 0)
                elif p1 < p2:
                    if diff[(p1,p2)] > max_pct:
                        max_pct = diff[(p1,p2)]
                    row.append(diff[(p1,p2)])
                else:
                    row.append(diff[(p2,p1)])
            data.append(row)
        fig, ax = plt.subplots()
        heatmap = plt.pcolor(data, cmap=plt.cm.Reds, vmin=0, vmax=65)
        labels = [float(x)/10 for x in range(1,10)]
        ax.set_yticks(np.arange(len(data)) + 0.5, minor=False)
        ax.set_xticks(np.arange(len(data[0])) + 0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, fontsize=16)
        ax.set_yticklabels(labels, minor=False, fontsize=16)
        ax.set_xlabel("$p_1$", fontsize=18)
        ax.set_ylabel("$p_2$", fontsize=18)
        plt.colorbar().ax.tick_params(labelsize=16) 
        plt.savefig("figures/{0}_v_{1}.png".format(args.policy1, args.policy2), bbox_inches='tight',dpi=100)
        plt.show()

