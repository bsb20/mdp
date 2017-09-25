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
        for mu_1_pow in range(11):
            for mu_2_pow in range(11):
                mu_1 = 2**mu_1_pow
                mu_2 = 2**mu_2_pow
                if (not args.leq and mu_1 < mu_2) or (args.leq and mu_1 <= mu_2):
                    policy1_avg = parse("{0}{1}/{0}_mu_{2}_{3}.txt".format(args.policy1, suffix, mu_1, mu_2), "AVG")
                    policy2_avg = parse("{0}{1}/{0}_mu_{2}_{3}.txt".format(args.policy2, suffix, mu_1, mu_2), "AVG")

                    print mu_1, mu_2, ":"
                    print args.policy1, policy1_avg, args.policy2, policy2_avg, "Diff", float(policy1_avg) - float(policy2_avg), "Percentage Diff", 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
    if args.action == "heat":
        for mu_1_pow in range(11):
            for mu_2_pow in range(11):
                mu_1 = 2**mu_1_pow
                mu_2 = 2**mu_2_pow
                if (not args.leq and mu_1 < mu_2) or (args.leq and mu_1 <= mu_2):
                    policy1_avg = parse("{0}{1}/{0}_mu_{2}_{3}.txt".format(args.policy1, suffix, mu_1, mu_2), "AVG")
                    policy2_avg = parse("{0}{1}/{0}_mu_{2}_{3}.txt".format(args.policy2, suffix, mu_1, mu_2), "AVG")
                    diff[(mu_1, mu_2)] = 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
                    diff[(mu_2, mu_1)] = 100*(float(policy1_avg) - float(policy2_avg))/policy2_avg
                if mu_1 == mu_2 and not args.leq:
                    diff[(mu_1, mu_2)] = 0
        data = []
        max_pct = 0
        for mu_1_pow in range(11):
            row = []
            for mu_2_pow in range(11):
                mu_1 = 2**mu_1_pow
                mu_2 = 2**mu_2_pow
                if mu_1 == mu_2:
                    row.append(diff[(mu_1,mu_2)] if args.leq else 0)
                elif mu_1 < mu_2:
                    if diff[(mu_1,mu_2)] > max_pct:
                        max_pct = diff[(mu_1,mu_2)]
                    row.append(diff[(mu_1,mu_2)])
                else:
                    row.append(diff[(mu_2,mu_1)])
            data.append(row)
        fig, ax = plt.subplots()
        heatmap = plt.pcolor(data, cmap=plt.cm.Reds, vmin=0, vmax=100)
        labels = [2**x for x in range(11)]
        ax.set_yticks(np.arange(len(data)) + 0.5, minor=False)
        ax.set_xticks(np.arange(len(data[0])) + 0.5, minor=False)
        ax.set_xticklabels(labels, minor=False, fontsize=16)
        ax.set_yticklabels(labels, minor=False, fontsize=16)
        ax.set_xlabel("$mu_1$", fontsize=18)
        ax.set_ylabel("$mu_2$", fontsize=18)
        plt.colorbar().ax.tick_params(labelsize=16) 
        plt.savefig("figures/{0}_v_{1}_mu.png".format(args.policy1, args.policy2), bbox_inches='tight',dpi=100)
        plt.show()

