#! /usr/bin/env python
from mdp_solvers import relative_value_iteration 
from mdp_solvers import value_iteration 
from mdp_solvers import relative_value_lp

import sys
from numpy import isclose
import pprint

n=8
cutoff = 100

def generate_s(p):
    def s(k):
        return 1/((p/k)+ (1-p))
    return s


def equi_rate(n, i, s, mu):
    if n == 0 or i == 0:
        return 0
    if i >= n:
        return n*mu
    else:
        return i*s(float(n)/i)*mu

def generate_mdp(lambd_1, lambd_2, s1, s2, mu_1, mu_2):
    rewards = {}
    transitions = {}
    values = {}
    normalizer = 1.0/(lambd_1 + lambd_2 + n*max([mu_1,mu_2]))
    arr_1 = lambd_1*normalizer
    arr_2 = lambd_2*normalizer
    for i in range(cutoff+1):
        for j in range(cutoff+1):
            values[(i,j)] = 0
            actions = range(n+1)
            if i+j:
                actions.append(i*(float(n)/(i+j)))
            probabilities = {}
            rewards[(i,j)] = {}
            for a in actions:
                equi_1 = equi_rate(a, i, s1, mu_1)*normalizer
                equi_2 = equi_rate(n-a, j, s2, mu_2)*normalizer
                total = 0
                p_a = {}
                if i < cutoff:
                    p_a[(i+1, j)] = arr_1
                    total += arr_1
                if j < cutoff:
                    p_a[(i, j+1)] = arr_2
                    total += arr_2
                if i > 0 and equi_1 > 0:
                    p_a[(i-1, j)] = equi_1
                    total += equi_1
                if j > 0 and equi_2 > 0:
                    p_a[(i, j-1)] = equi_2
                    total += equi_2
                p_a[(i,j)] = 1 - total
                rewards[(i,j)][a] = float(i+j)
                probabilities[a] = p_a
            transitions[(i,j)] = probabilities
    return transitions, rewards, values

if __name__ == "__main__":
    p1 = float(sys.argv[1])
    p2 = float(sys.argv[2])
    lambd_1 = float(sys.argv[3])
    lambd_2 = float(sys.argv[4])
    mu_1 = float(sys.argv[5])
    mu_2 = float(sys.argv[6])
    s1 = generate_s(p1)
    s2 = generate_s(p2)
    print p1, p2

    transitions, rewards, values = generate_mdp(lambd_1, lambd_2, s1, s2, mu_1, mu_2)
    hist, pol, iterations, initial_values, g = value_iteration(rewards, values, transitions, 1, minimize=True, limit = None)
    print "VALUE FUNCTION"
    print hist[-1]
    print "POLICY"
    print pol
    print "AVG"
    print g





