#! /usr/bin/env python

import ast

def parse_config(fname):
    config = {"n":8,
            "lambd_1": 2,
            "lambd_2": 2,
            "mu_1": 2,
            "mu_2": 2,
            "cutoff": 100
            }
    f = open(fname)
    config_file_str = ""
    for line in f:
        config_file_str += line.strip()
    config_file_obj = ast.literal_eval(config_file_str)
    config.update(config_file_obj)
        
