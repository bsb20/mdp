#! /usr/bin/env python
from mdp_solvers import evaluate_policy
import parallel_mdp

import sys
from numpy import isclose
import pprint

n=8
lambd_1 = 7
lambd_2 = 7
mu_1 = 2
mu_2 = 2
cutoff = 100
def generate_s(p):
    def s(k):
        return 1/((p/k)+ (1-p))
    return s

def equi_rate(n, i, s, mu):
    if n == 0:
        return 0
    if i >= n:
        return n*mu
    else:
        return i*s(float(n)/max([i,1]))*mu

def get_rate(a, i, j, p1, p2, l1=lambd_1, l2=lambd_2):
    normalizer = 1.0/(l1 + l2 + n*max([mu_1,mu_2]))
    return normalizer*(equi_rate(a, i, generate_s(p1), mu_1) + equi_rate(n-a, j, generate_s(p2), mu_2))


def generate_greedy():
    policy = {}
    rates = {}
    normalizer = 1.0/(lambd_1 + lambd_2 + n*max([mu_1,mu_2]))
    for i in range(cutoff+1):
        for j in range(cutoff+1):
            max_rate = 0
            max_action = 0
            for a in range(n+1):
                new_rate = normalizer*(equi_rate(a, i, s1, mu_1) + equi_rate(n-a, j, s2, mu_2))
                if new_rate > max_rate:
                    max_rate = new_rate
                    max_action = a
            policy[(i,j)] = max_action
            rates[(i,j)] = max_rate


    transitions, rewards, values = parallel_mdp.generate_mdp()
    print "evaluating"
    greedy_values = {}#evaluate_policy(policy, values, rewards, transitions, 1)
    return policy, greedy_values, rates

if __name__ == "__main__":
    p1 = float(sys.argv[1])
    p2 = float(sys.argv[2])
    s1 = generate_s(p1)
    s2 = generate_s(p2)
    print p1, p2

    parallel_mdp.p1 = float(sys.argv[1])
    parallel_mdp.p2 = float(sys.argv[2])
    parallel_mdp.s1 = generate_s(p1)
    parallel_mdp.s2 = generate_s(p2)
 
    policy, greedy_values, rates = generate_greedy()
    print "VALUE FUNCTION"
    print greedy_values
    print "POLICY"
    print policy
    print "RATES"
    print rates






