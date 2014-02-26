Phase 2 - Function Breakdown
----------------------------

In the *elex2/* directory, we've chopped up the original
election\_results.py code into a bunch of functions and turned this code
directory into a package by adding an \*\_\_init\_\_.py\* file.

We've also added a suite of tests. This way we can methodically change
the underlying code in later phases, while having greater confidence
that we haven't corrupted our summary numbers.

We can't stress this step enough: Testing existing code is *the*
critical first step in refactoring. If the code doesn't have tests,
write some, at least for the most important bits of logic. Otherwise
you're just `changing
shit <http://hamletdarcy.blogspot.com/2009/06/forgotten-refactorings.html>`__
(see Ray Ozzie).

Fortunately, our code has a suite of `unit
tests <http://docs.python.org/2/library/unittest.html>`__ for name
parsing and, most importantly, the summary logic.

Python has built-in facilities for running tests, but they're a little
raw for our taste. We'll use the
`nose <https://nose.readthedocs.org/en/latest/index.html>`__ library to
more easily run our tests:

.. code:: bash

    nosetests -v tests/test_parser.py
    # or run all tests in the tests/ directory
    nosetests -v tests/*.py

Observations
^^^^^^^^^^^^

At a high level, this code is an improvement over *elex1/*, but it could
still be much improved. We'll get to that in Phase 3, when we introduce
`modules <http://docs.python.org/2/tutorial/modules.html>`__ and
`packages <http://docs.python.org/2/tutorial/modules.html#packages>`__.

Questions
^^^^^^^^^

-  What is \*\_\_init\_\_.py\* and why do we use it?
-  In what order are test methods run?
-  What does the TestCase *setUp* method do?
-  What other TestCase methods are available?

Exercises
^^^^^^^^^

-  Install `nose <https://nose.readthedocs.org/en/latest/index.html>`__
   and run the tests. Try breaking a few tests and run them to see the
   results.
-  List three ways this code is better than the previous version; and
   three ways it could be improved.
-  Organize functions in *election\_results.py* into two or more new
   modules. (Hint: There is no right answer here. `Naming things is
   hard <http://martinfowler.com/bliki/TwoHardThings.html>`__; aim for
   directory and file names that are short but meaningful to a normal
   human).
