Main effects plotter
====================

This is a small python utility to plot the main effects of a full factorial experiment.

Requirements
------------

To run this script, you will need:

 * *Python* >= 2.6
 * *Matplotlib*


Setup
-----

First of all, you need to copy the example configuration and adapt it to suit your needs:

	cp config.ini.dist config.ini
	nano/vim/gedit config.ini

For now the only configuration option specifies where to look for the results files, and defaults to the folder `results`. Obviously, you need some results there in order to graph something.

There's a script that generates some example results file for you to test. You can run it from the main directory and it will populate your `results` folder with some fake result data:

	python buildResults.py

Now inspect the results files generated and their format. Basically, you should have a result file for each of your experiments. The name does not matter at all.


Format
------

A results file describes the parameters or settings of an experiment, along with the actual results obtained from it. Each line on the results file specifies either one *parameter* or one *value*.

 * Lines specifying a *parameter* start with the character `#`, followed by the parameter name, an `=` sign and the parameter's value. 
   Spaces are ignored. For instance:

   		# experiment = conversion
		# elements = mg,ti
		# throws = 40

 * Lines specifying a *value* (or result) are of the form `value = x`, where `x` can be anything. For instance:

 		hits = 20
 		quality = poor


Running
-------

Once you have a couple of results ready, it's time to graph them. Open the `make_graphs.py` file and adapt the *key* (which value to graph) and *algorithm_settings* (which settings define an algorithm) variables, as well as the *name* function.

Now you can run this script and see some graphs. Good luck with that!

**Warning**: this is very rough code. Contact me if you want to use it and don't know where to start.
