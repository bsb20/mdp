#! /usr/bin/env python
import pprint
from copy import deepcopy
from ggplot import *
from pandas import DataFrame
import sys
from cvxopt import matrix, solvers
solvers.options['show_progress']=False
import numpy as np
epsilon = .000001
#alpha = float(sys.argv[1])
alpha = .99
threshold = .000018

rewards = {1:{"advertise": 4, "nothing": 6}, 2:{"research": -5, "nothing":-3}}
transitions ={1:{"advertise": {1:.8, 2:.2}, "nothing": {1:.5,2:.5}}, 2:{"research": {1:.7, 2:.3}, "nothing":{1:.4,2:.6}}}
values = {1:0, 2:0}


def value_iteration(rewards, initial_values, transitions, alpha, minimize=False, limit=None, keep_history = False):
    if keep_history:
        history = [deepcopy(initial_values)]
    prev = deepcopy(initial_values)
    delta = 1
    iterations = 0
    print threshold
    while delta > threshold and (limit is None or iterations <= limit):
        print iterations, ":", delta
        iterations += 1
        policy = {}
        values = {}
        delta = 0
        max_delta = None
        min_delta = float('inf')
        for state in rewards:
            moves = {}
            for action in rewards[state]:
                r = rewards[state][action]
                discounted_future_value = 0
                for s, p in transitions[state][action].items():
                    discounted_future_value += alpha * p * prev[s]
                moves[action] = r + discounted_future_value
            current_move = ""
            current_value = None
            for action in moves:
                if minimize:
                    if not current_value or moves[action]  < current_value - epsilon:
                        current_move = action 
                        current_value = moves[action]
                else:
                    if moves[action] + epsilon > current_value:
                        current_move = action 
                        current_value = moves[action]
            if current_value - prev[state] > max_delta:
                max_delta = current_value - prev[state]
            if current_value - prev[state] < min_delta:
                min_delta = current_value - prev[state]
            policy[state] = current_move
            values[state] = current_value
        prev = values
        if keep_history:
            history.append(values)
        delta = max_delta - min_delta
    if not keep_history:
        history = [prev]
    return history, policy, iterations, initial_values, max_delta

def plot_value_iteration(history):
    iterations = []
    values = []
    states = []
    for iteration, v in enumerate(history):
        for state in v:
            iterations.append(iteration)
            states.append(str(state))
            values.append(v[state])
    df = DataFrame({"iterations": iterations, "value": values, "state":states})
    plt = ggplot(df, aes(x="iterations", y="value", color="state")) + geom_line() + ggtitle("State Values During Value Iteration") + xlab("iteration") + ylab("value")
    return plt

        
def policy_iteration(rewards, initial_values, transitions, alpha):
    history = [deepcopy(rewards)]
    delta = 1
    prev_policy = None
    policy = {1:"nothing", 2:"nothing"}
    policies = [policy]
    values_list = []
    while policy != prev_policy:
        values = evaluate_policy(policy, initial_values, rewards, transitions, alpha)
        values_list.append(values)
        prev_policy = policy
        policy={}
        for state in rewards:
            #max over actions for this state
            moves = {}
            for action in rewards[state]:
                r = rewards[state][action]
                discounted_future_value = 0
                for s, p in transitions[state][action].items():
                    discounted_future_value += alpha * p * values[s]
                moves[action] = r + discounted_future_value
            current_move = ""
            current_value = None
            for action in moves:
                if moves[action] + epsilon > current_value:
                    current_move = action 
                    current_value = moves[action]
            policy[state] = current_move
        policies.append(policy)
    return policies, policies[-1], values, values_list
        

def evaluate_policy(policy, initial_values, rewards, transitions, alpha):
    values = initial_values
    delta = 1
    iterations = 0
    while delta > threshold:
        prev = values
        values = {}
        print iterations, ":", delta
        iterations += 1
        delta = 0
        max_delta = None
        min_delta = float('inf')
        for state in rewards:
            moves = {}
            for action in rewards[state]:
                r = rewards[state][action]
                discounted_future_value = 0
                for s, p in transitions[state][action].items():
                    discounted_future_value += alpha * p * prev[s]
                moves[action] = r + discounted_future_value
            current_move = policy[state]
            current_value = moves[current_move]
            if current_value - prev[state] > max_delta:
                max_delta = current_value - prev[state]
            if current_value - prev[state] < min_delta:
                min_delta = current_value - prev[state]
            values[state] = current_value
        delta = max_delta - min_delta
    return values, max_delta

def lp(rewards, transitions, alpha):
    c = []
    G = []
    h = []
    for state in rewards:
        c.append(1.0)
        for action in rewards[state]:
            h.append(float(-rewards[state][action]))
            constraint = [0.0] * len(rewards)
            constraint[state -1] = -1.0
            for s in rewards:
                constraint[s-1] += alpha*float(transitions[state][action][s])
            G.append(constraint)
    print c
    print G
    print h
    solution = solvers.lp(matrix(np.array(c)), matrix(np.array(G)), matrix(np.array(h)))
    if solution['status'] == 'optimal':
        print "Policy From LP:"
        for s, state in enumerate(rewards):
            for i, action in enumerate(rewards[state]):
                if solution["s"][len(rewards)*(s-1) + i] < epsilon:
                    print "state ", state, ": "
                    print "value: ", solution['x'][state-1]
                    print "action: ", action
    else:
        print "LP Infeasible"

def relative_value_lp(rewards, transitions, minimize=False):
    A=[]
    b=[]
    G=[]
    h=[]
    c=[]
    var_count = 0
    var_map = {}
    for state in sorted(rewards):
        for action in rewards[state]:
            if minimize:
                c.append(float(rewards[state][action]))
            else:
                c.append(float(-rewards[state][action]))
            var_map[(state,action)] = var_count
            var_count += 1
    A.append([1.0]*var_count)
    b.append(1.0)
    for var in range(var_count):
        row = [0.0]*var_count
        row[var] = -1.0
        G.append(row)
        h.append(0.0)
    for s_i, state in enumerate(sorted(rewards)):
        row = [0.0] * var_count
        for i, action in enumerate(rewards[state]):
            row[var_map[(state,action)]] = 1.0
        for j_i, j in enumerate(sorted(rewards)):
            for i, action in enumerate(rewards[j]):
                if state in transitions[j][action]:
                    row[var_map[(state,action)]] -= transitions[j][action][state]
        G.append(row)
        h.append(0.0)
        G.append([-x for x in row])
        h.append(0.0)
    print A
    print b
    print c
    print G
    print h
    solution = solvers.lp(matrix(np.array(c)), matrix(np.array(G)), matrix(np.array(h)), matrix(np.array(A)), matrix(np.array(b)))
    print solution['status']
    if solution['status'] == 'optimal':
        print "Policy from LP (average reward per period):"
        for s, state in enumerate(rewards):
            for i, action in enumerate(rewards[state]):
                if solution["x"][len(rewards)*(s-1) + i] > epsilon:
                    print state, ": ", action
        print "g:", -solution["primal objective"]



    

def relative_value_iteration(rewards, initial_values, s_bar, master_transitions, minimize=False):
    beta = 1
    transitions = deepcopy(master_transitions)
    for state in transitions:
        for action in transitions[state]:
            if s_bar in transitions[state][action] and transitions[state][action][s_bar] < beta:
                if transitions[state][action][s_bar] > 0:
                    beta = transitions[state][action][s_bar]
                else:
                    raise ValueError("No valid beta for this state")
    print "Using beta=",beta
    for state in transitions:
        for action in transitions[state]:
            for j in transitions[state][action]:
                if j == s_bar:
                    transitions[state][action][j] = (transitions[state][action][j] - beta)/(1-beta)
                else:
                    transitions[state][action][j] = transitions[state][action][j]/(1-beta)
    hist, pol, iterations, init = value_iteration(rewards, initial_values, transitions, 1-beta, minimize)
    values = hist[-1]
    print "Converged Value Function:"
    print values
    print "Using Selected Policy:"
    print pprint.pprint(pol)
    print "after", iterations, "iterations"
    print "g=", beta * values[s_bar]
    for state in rewards:
        print "h(",state, ")=", values[state] - values[s_bar]

        

       

    
if __name__ == "__main__":
    initial_values = {1:0, 2:0}
    policies, pol, values, values_list = policy_iteration(rewards, initial_values, transitions, .9)
    print "Policy iteration:"
    print "Tried:"
    print policies
    print values_list
    print "Selected:"
    print pol
    print "Value function:"
    print values
    print
    print
    hist, pol, iterations, initial_values = value_iteration(rewards, initial_values, transitions, .99)
    print "Value iteration:"
    print iterations, "iterations"
    print "Converged value function: ", hist[-1]
    print "Under selected policy: ", pol
    print
    print
    lp(rewards, transitions, .95)
    print
    print
    #average reward per period analogs
    s_bar = 2
    print "Average rewards per period using relative state s_bar =",s_bar
    print "Using Value Iteration on a modified MDP:"
    relative_value_iteration(rewards,  initial_values, s_bar, transitions)
    print 
    print
    relative_value_lp(rewards, transitions)
    print
    print
    #Value iteration chart, done at the end for convenience
    plot_value_iteration(hist).show()


