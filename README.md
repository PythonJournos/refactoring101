refactoring101
==============

NICAR tutorial on transforming a complex, linear script into a modular, easier-to-maintain package.


The project goes through four stages, each contained in a "code" directory. Below are notes,
questions and exercises related to each stage.


code1
-----

In this stage, we have a single linear script with no functions.

A few reasons why this code stinks:

* It's hard to understand. You have to read the entire file before getting a full sense of what it does.
* It's hard to debug when something goes wrong.
* It's pretty much impossible to test, beyond eye-balling the output file.
* None of the code is reusable by other programs.


Exercise
~~~~~~~~

Try slicing up this code into a bunch of functions (hint: See
*code2/election_results.py* for one way of slicing up this file)


code2
-----

We've chopped up the original election_results.py code into a bunch of
functions, and added a few tests. We've also turned this code directory
into a module by adding an __init__.py file. 

Questions
~~~~~~~~~

* What is a module?
* What is a package?
* What is __init__.py and why do we use it?


Exercise
~~~~~~~~~

There is a bug in the percentage function, related to when a
candidate receives zero votes. Try capturing the bug in a new test case,
then update the percentage function so that it properly handles this edge case.
