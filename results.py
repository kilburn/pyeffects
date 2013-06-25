r"""Test for theHelper functions to locate and load datasets and problems

Using 'resuts' is not required, but it provides some nice utilities to load
problems and/or sets of problems into the standard library used across
the application.
"""

#'

import os
import sys
import fnmatch
import traceback
import scipy
import numpy
import pickle
import re

#__all__ = ["list_datasets", "list_algorithms", "list_problems", "load_problems", "load_problem"]

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple((k, self[k]) for k in sorted(self)))

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def list_settings(path, fnfilter=None, group=None):
    settings = dict()

    files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]
    #print "Loading problems    0.0",
    for filenum,f in enumerate(files):
        psettings, pvalues = load_problem(path + '/' + f)

        if fnfilter is not None and not fnfilter(psettings):
            continue

        if group is not None:
            psettings = dict([(k,v) for k,v in psettings.iteritems() \
                    if k in group])

        psettings = hashabledict(psettings)
        if psettings in settings:
            settings[psettings].append(pvalues)
        else:
            settings[psettings] = [pvalues]

        #sys.stdout.write("\b\b\b\b\b\b%5.2f%%" % ((filenum+1)*100./len(files)))
        #sys.stdout.flush()

    #print "\nComputing changes",
    #sys.stdout.flush()
    changes = set()
    sts = list(settings.keys())
    for s1idx, s1 in enumerate(sts):
        #sys.stdout.write(".")
        #sys.stdout.flush()
        for s2 in sts[s1idx+1:]:
            dif = DictDiffer(s1, s2)
            changes.update(dif.changed())

    #print "\nFilter equal keys"
    result = dict()
    for key in settings:
        newkey = hashabledict([(k,key[k]) for k in key if k in changes])
        result[newkey] = settings[key]

    return result

def load_problem(path):
    """load_problem(path)

    Loads the problem file specified in path, returning a tuple of two dictionaries,
    one with the problem's settings and another one with its results.
    """
    values = dict()
    settings = dict()

    fh = open(path, "r")
    for line in fh:
        t = re.split(r'[#\s=]+', line.strip())
        if t[0] and len(t) == 2:
            # This is a setting
            values[t[0]] = t[1]
        elif not t[0] and len(t) == 3:
            # This is a value, so we try to make it int/float, or fallback to string
            try:
                t[2] = int(t[2])
            except ValueError:
                try:
                    t[2] = float(t[2])
                except ValueError:
                    pass
            settings[t[1]] = t[2]

    # Exctracts the last part of the problem path, and sets it as a value instead
    # of a setting.
    if 'problem' in settings:
        values['problem'] = settings['problem'].split('/')[-1]
        del(settings['problem'])

    fh.close()
    return (settings, values)

def select(settings, config):
    def equals(v1, v2):
        if type(v1) is float or type(v2) is float:
            return numpy.allclose(v1, v2)
        return v1 == v2

    for k in sorted(settings):
        if all([key in k and equals(k[key], config[key]) for key in config]):
            return settings[k]

    raise Exception, "Settings " + str(config) + " not found"

def find(problem, problems):
    """Find a problem (by name) in a list of problems"""
    for p in problems:
        if p['problem'] == problem:
            return p
    #raise ValueError("Not found")
    return None

if __name__ == '__main__':
    path = '../results'
    list_settings(path)
