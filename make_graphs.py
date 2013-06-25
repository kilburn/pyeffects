#/usr/bin/env python

import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read("config.ini")
path = config.get('results', 'path')

from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Palatino']})
import results
import graph
import stats as sts
import numpy as np
import nearest
import matplotlib.pyplot as plt

key = 'hits'
algorithm_settings = ['algorithm']

def name(x):
    name = ''
    if 'algorithm' in x:
        name += x['algorithm']
    # if 'a' in x:
    #     name += 'a=' + str(x['a'])
    # if 'b' in x:
    #     name += 'b=' + str(x['b'])
    # if 'c' in x:
    #     name += 'c=' + str(x['c'])
    # if not name:
    #     raise ValueError("Unable to find name for " + str(x))
    return name

def lines(path, xkey, base=None, **kwargs):
    settings = results.list_settings(path, group=[xkey])
    graph.lines(settings, name, key, xkey, **kwargs)

def bar(path, base=None, **kwargs):
    settings = results.list_settings(path, group=algorithm_settings)
    graph.bxes(settings, name, key, **kwargs)

def dataset_lines(path, dataset_key, base=None, **kwargs):
    # This would filter those problems where a == 'mid-high'
    # filfn = lambda x : x['a'] != 'mid-high'
    filfn = lambda x : True

    settings = results.list_settings(path, filfn, group=algorithm_settings+[dataset_key])
    graph.dataset_lines(settings, dataset_key, name, key, **kwargs)
    #graph.dataset_legend(settings, dataset_key, name, key, **kwargs)

def generate():
    #lines(path, 'a', xlabel='A setting', ylabel='hits', title="First cool graph")
    #bar(path, title='Second cool graph', ylabel='hits')

    options = {}
    dataset_lines(path, 'a', xlabel='a setting', ylabel='hits', title='a_evolution', **options)
    dataset_lines(path, 'b', xlabel='b setting', ylabel='hits', title='b_evolution', **options)
    dataset_lines(path, 'c', xlabel='c setting', ylabel='hits', title='c_evolution', **options)

    #adjust = {'top': 0.95, 'bottom': 0.15, 'right': 0.96, 'left': 0.1}
    #graph.save_figures(adjust=adjust, xscale=.7, yscale=.5)
    #graph.show(adjust=adjust, xscale=.7, yscale=.5)
    graph.show()

if __name__ == "__main__":
    generate()
