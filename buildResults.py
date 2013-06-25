#!/usr/bin/env python

import itertools as it
import subprocess
import random

settings  = ['a', 'b', 'c']
variables = ['a', 'b', 'c']
path = 'results'

def write_problem(combination, output):
    name = ".".join([kv[0] + variables[i] for i,kv in enumerate(combination)])
    for algorithm in ['algoritmo1', 'algoritmo2']:
        for i in xrange(3):
            pname = "%s/%s-%s-%d.txt" % (path, algorithm, name, i+1)
            with open(pname, 'w') as fh:
                for k,v in output.items():
                    fh.write("# %s = %s\n" % (k,v))
                fh.write("# problem = problem_%d\n" % (i+1))
                fh.write("# algorithm = %s\n" % algorithm)
                fh.write("hits = %s\n" % random.randint(1,100))

def main():
    values = [
        ('low', 'mid', 'mid-high'),
        (1000, 3000, 6000),
        (1., 1.5, 2.),
    ]
    values = [zip('LMH', v) for v in values]
    for combination in it.product(*values):
        output = {}
        for idx, key_value in enumerate(combination):
            output[settings[idx]] = key_value[1]
        write_problem(combination, output)

if __name__ == '__main__':
    main()