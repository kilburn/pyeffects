r"""Helper functions to extract statistics from the problem results.

Using 'stats' is not required, but it provides some nice utilities to
compute statistics of the problems' results.
"""

__all__ = ["problems_stats"]

import scipy as sp
import ast
import results
import numpy as np
import scipy.stats as sts

def key_value(problem, key):
    return ast.literal_eval(problem[key])

def key_fun(key):
    return lambda(problem) : key_value(problem, key)

def key_stats(values):
    return dict({
            'mean'   : sp.mean(values),
            'std'    : sp.std(values)/sp.sqrt(len(values)),
            'max'    : sp.array(values).max(),
            'min'    : sp.array(values).min(),
            'median' : sp.median(values),
            'p25'    : sp.percentile(values, 25),
            'p75'    : sp.percentile(values, 75),
            'values' : sp.array(values)
            })

def problems_stats(problems, fun):
    """
    Returns the statistics (mean, median, etc.) of a numeric value 
    derived from each problem's results.

    problems is expected to contain a list of dictionaries, where 
    each key of each of this dictionaries represents a result value.

    fun can be either a string that is the key of which result we 
    want to compute the statistics of, or a function that takes the
    whole dictionary and computes a number as a result.
    """
    if not hasattr(fun, '__call__'):
        fun = key_fun(fun)

    return key_stats([fun(item) for item in problems])

def settings_stats(settings, key, relative=False, base=None, anames=None):
    """
    Returns the statistics (mean, median, etc.) of a numeric value 
    derived from each problem's results.

    settings is expected to contain a list of dictionaries, where 
    each key of each of this dictionaries represents a result value.

    key is the key of the problems' result for which to compute statistics
    """

    def solved_problem(p):
        """ Check if a problem has been solved using all settings """
        if p is None:
            print "Problem", p, "not found."
            return False
        if key not in p:
            print "Missing key", key, "in problem", p
        return key in p

    slist = sorted([s for s in settings])
    for s in slist:
        print s
    plist = set((p['problem'] for p in settings[s] for s in slist))

    if not relative:
        base = None

    if base:
        ibase = next(i for i,s in enumerate(slist) if anames(s) == base)

    # Filter those problems that are not solved with any of the settings
    plist = [p for p in plist if all( \
                [solved_problem(results.find(p, settings[s])) for s in slist] \
            )]

    values = np.zeros((len(plist), len(slist)))
    for pi, p in enumerate(plist):
        ps = np.zeros(len(slist))
        for i,s in enumerate(slist):
            ps[i] = results.find(p, settings[s])[key]
            if base and i == ibase:
                imin = ps[i]
        if base:
            values[pi,:] = ((ps / imin) - 1)*100
        elif relative:
            values[pi,:] = ps / ps.min()
        else:
            values[pi,:] = ps

    # TODO: Test for pairwise significance
    # for i in xrange(len(slist)):
    #     for j in xrange(i, len(slist)):
    #         z, p = sts.ranksums(values[:,i], values[:,j])
    #         if p < .95:
    #             print "WARNING: (z,p=%f) statistically meaningless %s - %s" % (p, anames(slist[i]), anames(slist[j]))

    if base:
        values = np.delete(values, ibase, 1)
        del(slist[ibase])

    # Compute stats
    stats = [key_stats(values[:,si]) for si, s in enumerate(slist)]

    return (slist, plist, stats)


