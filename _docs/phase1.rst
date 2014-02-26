Phase 1 - Spaghetti
-------------------

We begin with a single, linear script in the *elex1/* directory. Below
are a few reasons why this `code
smells <http://en.wikipedia.org/wiki/Code_smell>`__ (some might say it
reeks):

-  It's hard to understand. You have to read the entire script before
   getting a full sense of what it does.
-  It's hard to debug when something goes wrong.
-  It's pretty much impossible to test, beyond eye-balling the output
   file.
-  None of the code is reusable by other programs.

Questions
^^^^^^^^^

-  What are `unit
   tests <http://docs.python.org/2/library/unittest.html>`__?
-  Can you identify three sections of logic that could be unit tested?
-  What are
   `modules <http://docs.python.org/2/tutorial/modules.html>`__?
-  What are
   `packages <http://docs.python.org/2/tutorial/modules.html#packages>`__?

Exercises
^^^^^^^^^

-  Slice up this code into a bunch of functions, where related bits of
   logic are grouped together.
-  Write a unit test for one or more functions extracted from this
   module.
