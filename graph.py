r"""Helper functions to draw graphs

Using 'graph' is not required, but it provides some nice utilities to
easily draw graphics
"""

#'

import pylab
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import stats as sts
import oset
import subprocess
import itertools
import re
import results
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

__all__ = ["dataset_bars", "line_graph", "dataset_line_graph", 
    "foo_line_graph", "foo_line_graph2", "save_figures", "show"]

x_axis_map = dict()
y_axis_map = dict()
algs_map   = dict()
x_axis_f = lambda k: x_axis_map[k] if k in x_axis_map else k
y_axis_f = lambda k: y_axis_map[k] if k in y_axis_map else k
algs_f   = lambda k: algs_map[k]   if k in algs_map   else k
line_styles = lambda : itertools.cycle([':','-.','--','-'])

def open_figures():
    for i in itertools.count(1):
        fig = pylab.figure(i)
        if fig.axes:
            yield fig
        else:
            plt.close()
            return

def show(**kwargs):
    for fig in open_figures():
        fig.gca().set_title('')

        if 'adjust' in kwargs:
            fig.subplots_adjust(**kwargs['adjust'])

        if 'xscale' in kwargs or 'yscale' in kwargs:
            DefaultSize = fig.get_size_inches()
            xscale = kwargs['xscale'] if 'xscale' in kwargs else 1
            yscale = kwargs['yscale'] if 'yscale' in kwargs else 1
            fig.set_size_inches(DefaultSize[0]*xscale, DefaultSize[1]*yscale)
    pylab.show()

def save_figures(**kwargs):
    names = []
    for fig in open_figures():
        name = fig.gca().get_title()
        name = name.strip("/").replace("/","_").replace(".","_")\
                .replace(" ","_").replace("(","_").replace(")","_")
        names.append(name)
        fig.gca().set_title('')
        matplotlib.pyplot.close()

        if 'legend' in name:
            lgd = fig.gca().get_legend()
            fig.savefig("/tmp/" + name + ".pdf", bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
            subprocess.call("pdfcrop /tmp/" + name + ".pdf /tmp/" + name + ".pdf", shell=True)
        else:
            #fig.subplots_adjust(top=0.9,bottom=0.15, right=0.97, left=0.12)
            #fig.set_size_inches(DefaultSize[0]*2./3, DefaultSize[1]*2./3*0.8)
            if 'adjust' in kwargs:
                fig.subplots_adjust(**kwargs['adjust'])

            if 'xscale' in kwargs or 'yscale' in kwargs:
                DefaultSize = fig.get_size_inches()
                xscale = kwargs['xscale'] if 'xscale' in kwargs else 1
                yscale = kwargs['yscale'] if 'yscale' in kwargs else 1
                fig.set_size_inches(DefaultSize[0]*xscale, DefaultSize[1]*yscale)

            fig.savefig("/tmp/" + name + ".pdf")
            #subprocess.call("pdfcrop /tmp/" + name + ".pdf /tmp/" + name + ".pdf", shell=True)
    pylab.close('all')
    return names

def lines(settings, anames, key, xkey, relative=False, base=None, **kwargs):
    slist, plist, values = sts.settings_stats(settings, key, relative, base, anames)
    xs = [s[xkey] for s in slist]

    fig = plt.figure()
    plot_stats = ['mean']
    for si, stat in enumerate(plot_stats):
        stat_values = [v[stat] for v in values]
        for vi, _ in enumerate(values):
            print anames(slist[vi]), stat_values[vi]
        best = np.argmin(stat_values)
        print "Best %s: %s (%f)" % (stat, anames(slist[best]), stat_values[best])
        ax = plt.subplot(len(plot_stats), 1, si+1)
        
        ticklabels = xs
        xs = range(len(xs))
        plt.plot(xs, stat_values)

        plt.xticks(xs, ticklabels)
        plt.grid(axis='y')

        if 'title' in kwargs:
            pylab.title(kwargs['title'])
        if 'ylabel' in kwargs:
            ylabel = stat + " " + kwargs['ylabel']
            if base:
                ylabel += " (\% over " + base + ")"
            elif relative:
                ylabel += " (\% over best per instance)"
            pylab.ylabel(ylabel)
        if 'xlabel' in kwargs:
            pylab.xlabel(kwargs['xlabel'])
        if 'ylim' in kwargs:
            pylab.ylim(kwargs['ylim'])

    # Size adjustment
    DefaultSize = fig.get_size_inches()
    fig.subplots_adjust(top=0.9,bottom=0.23, right=0.95, left=0.12)
    fig.set_size_inches(DefaultSize[0]*2./3, DefaultSize[1]*2./3)

def bxes(settings, anames, key, relative=False, base=None, **kwargs):
    slist, plist, values = sts.settings_stats(settings, key, relative, base, anames)
    vs = [y['values'] for y in values];
    print vs
    fig = plt.figure()
    plt.boxplot(vs, sym='', whis=1)
    locs, _ = plt.xticks()
    plt.xticks(locs, [anames(s) for s in slist], rotation=0)
    plt.grid(axis='y')
    if 'title' in kwargs:
        pylab.title(kwargs['title'])
    if 'ylabel' in kwargs:
        ylabel = kwargs['ylabel']
        if base:
            ylabel += " (\% over " + base + ")"
        elif relative:
            ylabel += " (\% over best per isntance)"
        pylab.ylabel(ylabel)
    if 'ylim' in kwargs:
        pylab.ylim(kwargs['ylim'])

    # Size adjustment
    DefaultSize = fig.get_size_inches()
    fig.subplots_adjust(top=0.9,bottom=0.23, right=0.95, left=0.12)
    fig.set_size_inches(DefaultSize[0]*2./3, DefaultSize[1]*2./3)

def dataset_lines(settings, dataset_key, anames, key, relative=False, base=None, **kwargs):
    xs = sorted(set([s[dataset_key] for s in settings]))
    ys = [[] for x in xs]

    stat = 'mean'
    for i, x in enumerate(xs):
        x_settings = dict([(s,settings[s]) for s in settings if s[dataset_key] == x])
        slist, plist, values = sts.settings_stats(x_settings, key, relative, base, anames)
        stat_values = [v[stat] for v in values]
        best = np.argmin(stat_values)
        print "Best %s [%s]: %s (%f)" % (stat, x, anames(slist[best]), stat_values[best])
        ys[i] = stat_values

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ys = np.array(ys)
    lsi = line_styles()

    ticklabels = xs
    xs = range(len(xs))
    for i in xrange(ys.shape[1]):
        ax = plt.plot(xs, ys[:,i], label=anames(slist[i]), linewidth=3, \
            ls=lsi.next(), marker='o', markersize=10)
    plt.xticks(xs, ticklabels)
    
    plt.grid(axis='y')
    #plt.legend(loc='upper center', ncol=len(slist), bbox_to_anchor=(0, .1,1,1))

    if 'title' in kwargs:
        pylab.title(kwargs['title'])
    if 'ylabel' in kwargs:
        ylabel = stat + " " + kwargs['ylabel']
        if base:
            ylabel += " (\% over " + base + ")"
        elif relative:
            ylabel += " (\% over best per instance)"
        pylab.ylabel(ylabel)
    if 'xlabel' in kwargs:
        pylab.xlabel(kwargs['xlabel'])
    if 'ylim' in kwargs:
        pylab.ylim(kwargs['ylim'])

def dataset_legend(settings, dataset_key, anames, key, relative=False, base=None, **kwargs):
    fig = pylab.figure()

    xs = sorted(set([s[dataset_key] for s in settings]))
    x_settings = dict([(s,settings[s]) for s in settings if s[dataset_key] == xs[0]])
    slist, plist, values = sts.settings_stats(x_settings, key, relative, base, anames)
    pylab.title("legend " + dataset_key)

    ax = fig.add_subplot(111)
    ax.set_axis_off()
    lsi = line_styles()
    for s in slist:
        ax.plot([0],[0], label=anames(s), linewidth=3, ls=lsi.next())

    pylab.legend(ncol=len(slist), loc=10)

