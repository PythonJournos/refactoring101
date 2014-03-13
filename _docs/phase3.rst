Modules, packages, oh my!!
==========================

In this third phase, we chop up our original *election\_results.py*
module into a legitimate Python package. The new directory structure is
(hopefully) self-explanatory:

::

    ├── elex3
    │   ├── __init__.py
    │   ├── lib
    │   │   ├── __init__.py
    │   │   ├── parser.py
    │   │   ├── scraper.py
    │   │   └── summary.py
    │   ├── scripts
    │   │   └── save_summary_to_csv.py
    │   └── tests
    │       ├── __init__.py
    │       ├── sample_results.csv
    │       ├── sample_results_parsed.json
    │       ├── sample_results_parsed_tie_race.json
    │       ├── test_parser.py
    │       └── test_summary.py

-  ``lib/`` contains re-usable bits of code.
-  ``scripts/`` contains...well..scripts that leverage our re-usable
   code.
-  ``tests/`` contains tests for re-usable bits of code and related
   fixtures.

Note that we did not change any of our functions. Mostly we just
re-organized them into new modules, with the goal of grouping related
bits of logic in common-sense locations. We also updated imports and
"namespaced" them of our own re-usable code under *elex3.lib*.

Here's where we start seeing the benefits of the tests we wrote in the
*elex2* phase. While we've heavily re-organized our underlying code
structure, we can run the same tests (with a few minor updates to
*import* statements) to ensure that we haven't broken anything.

    **Note**: You must add the *refactoring101* directory to your
    *PYTHONPATH* before any of the tests or script will work.

.. code:: bash

    $ cd /path/to/refactoring101
    $ export PYTHONPATH=`pwd`:$PYTHONPATH

    $ nosetests -v elex3/tests/*.py
    $ python elex3/scripts/save_summary_to_csv.py

Check out the results of the *save\_summary\_to\_csv.py* command. The
new *summary\_results.csv* should be stored *inside* the *elex3*
directory, and should match the results file produced by
*elex2/election\_results.py*.

Questions
---------

-  Do you *like* the package structure and module names? How would you
   organize or name things differently?
-  Why is it necessary to add the *refactoring101/* directory to your
   PYTHONPATH?
-  What are three ways to add a library to the PYTHONPATH?
-  What is a class? What is a method?
-  What is an object in Python? What is an instance?
-  What is the **init** method on a class used for?
-  What is *self* and how does it relate to class instances?

Exercises
---------

-  Look at the original results data, and model out some classes and
   methods to reflect "real world" entities in the realm of elections.
-  Examine functions in *lib/* and try assigning three functions to one
   of your new classes.
-  Try extracting logic from the *summarize* function and re-implement
   it as a method on one of your classes.
