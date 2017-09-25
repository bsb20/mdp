#! /usr/bin/env python
from mdp_solvers import evaluate_policy
import parallel_mdp

import sys
from numpy import isclose
import pprint

n=8
cutoff = 100

def generate_s(p):
    def s(k):
        return 1/((p/k)+ (1-p)) if k else 0
    return s

def equi_rate(n, i, s, mu):
    if n == 0:
        return 0
    if n < 1:
        return n
    if i >= n:
        return n*mu
    else:
        return i*s(float(n)/max([i,1]))*mu

def get_rate(a, i, j, p1, p2, l1, l2, mu_1, mu_2):
    normalizer = 1.0/(l1 + l2 + n*max([mu_1,mu_2]))
    return normalizer*(equi_rate(a, i, generate_s(p1), mu_1) + equi_rate(n-a, j, generate_s(p2), mu_2))

def get_max(p1, p2):
    max_rate = 0
    max_action = 0
    s1=generate_s(p1)
    s2=generate_s(p2)
    for i in range(n):
        new_rate = s1(i) + s2(n-i)
        if new_rate > max_rate:
            max_rate = new_rate
            max_action = i
    return max_rate, max_action

def find_ex(p1, p2):
    max_rate, max_action = get_max(p1, p2)
    opt_n = -1
    opt_action = 0
    s1=generate_s(p1)
    s2=generate_s(p2)
    for i in range(n+1):
        new_n =  2.0/(s1(i) + s2(n-i)) + s1(i)/((s1(i) + s2(n-i))*s2(n)) + s2(n-i)/((s1(i) + s2(n-i))*s1(n))
        print "n:", new_n, "rate:", s1(i) + s2(n-i)
        if new_n < opt_n or opt_n < 0:
            opt_n = new_n
            opt_action = i
    print opt_action, max_action
    return opt_action != max_action



def generate_equi(lambd_1, lambd_2, s1, s2, mu_1, mu_2):
    policy = {}
    rates = {}
    normalizer = 1.0/(lambd_1 + lambd_2 + n*max([mu_1,mu_2]))
    for i in range(cutoff+1):
        for j in range(cutoff+1):
            a = i*(float(n)/(i+j) if i+j else n)
            rate = normalizer*(equi_rate(a, i, s1, mu_1) + equi_rate(n-a, j, s2, mu_2))
            policy[(i,j)] = a
            rates[(i,j)] = rate
    transitions, rewards, values = parallel_mdp.generate_mdp(lambd_1, lambd_2, s1, s2, mu_1, mu_2)
    print "evaluating"
    greedy_values, g = evaluate_policy(policy, values, rewards, transitions, 1)
    
    return policy, greedy_values, rates, g

if __name__ == "__main__":
    p1 = float(sys.argv[1])
    p2 = float(sys.argv[2])
    lambd_1 = int(sys.argv[3])
    lambd_2 = int(sys.argv[4])
    mu_1 = int(sys.argv[5])
    mu_2 = int(sys.argv[6])

    s1 = generate_s(p1)
    s2 = generate_s(p2)
    print p1, p2

    parallel_mdp.p1 = float(sys.argv[1])
    parallel_mdp.p2 = float(sys.argv[2])
    parallel_mdp.s1 = generate_s(p1)
    parallel_mdp.s2 = generate_s(p2)
 
    policy, greedy_values, rates, g = generate_equi(lambd_1, lambd_2, s1, s2, mu_1, mu_2)
    print "VALUE FUNCTION"
    print greedy_values
    print "POLICY"
    print policy
    print "RATES"
    print rates
    print "AVG"
    print g






