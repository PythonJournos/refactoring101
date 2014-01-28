# refactoring101

## Overview

This repo contains code samples demonstrating how to transform a complex, linear script into a modular, easier-to-maintain package. Code was written for the *Python: Beyond the Basics* class at [NICAR 2014](http://ire.org/conferences/nicar-2014/). The code uses a small, [fake set of election results](https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv) created for demonstration purposes.

The project code evolves through four phases, each contained in a numbered *elex* directory. Below are notes,
questions and exercises related to each phase. The overarching theme: *As an application or program grows in size, writing readable, testable code can help tame complexity and keep you sane.* We explore how to use Python modules, packages and classes to organize
code more effectively. We also introduce unit testing as one strategy for writing programs that you can update with confidence.

## Phase 1 - Spaghetti

We begin with a single, linear script in the _elex1/_ directory. Below are a few reasons why this [code smells](http://en.wikipedia.org/wiki/Code_smell) (well, some might say reeks!):

* It's hard to understand. You have to read the entire script before getting a full sense of what it does.
* It's hard to debug when something goes wrong.
* It's pretty much impossible to test, beyond eye-balling the output file.
* None of the code is reusable by other programs.

#### Questions

* What is a unit test? 
* Can you identify three sections of logic that could be unit tested?


####  Exercises

* Try slicing up this code into a bunch of functions, where related bits of functionality are grouped together (hint: See
*elex2/election_results.py* for one way of slicing up this file)
* Write a unit test for one or more functions extracted from this module (hint: see test file in _elex2/_)


## Phase 2 - Function Breakdown

In the _elex2/_ directory, we've chopped up the original election_results.py code into a bunch of
functions, and added a few tests. We've also turned this code directory
into a package by adding an *\__init__.py* file.  This code is an improvement over _elex1/_, but it still
could be a lot better.

#### Questions

* What is a module?
* What is a package?
* What is *\__init__.py* and why do we use it?

####Exercises

* List three ways this code is better than the previous version; and three ways it could be improved.
* There is a bug in the percentage function, related to when a
candidate receives zero votes. Try capturing the bug in a new test case,
then update the percentage function so that it properly handles this edge case.

## Phase 3 - Modularize

In this third phase, we chop up our origin election_results.py module into a legitimate 
Python package. The new (hopefully self-explanatory) directory structure looks like below:

```
elex3/
├── __init__.py
├── lib
│   ├── __init__.py
│   ├── analysis.py
│   ├── parser.py
│   └── scraper.py
├── scripts
│   └── save_summary_to_csv.py
└── tests
    ├── __init__.py
    ├── test_analysis.py
    └── test_parser.py

```

* *_lib/_* contains re-usable bits of code are placed in modules in the _lib/_ directory.
* *_scripts/_* contains...well..scripts that leverage our re-usable code.
* *_tests/_* contains tests for re-usable bits of code.

Note that we did not change any of our functions. Mostly we just re-organized them into new modules, 
with the goal of grouping related bits of logic in common-sense locations.

One significant change: You must add the _refactoring101_ directory to your _PYTHONPATH_
before any of the tests or script will work. 

```bash
$ cd /path/to/refactoring101
$ export PYTHONPATH=`pwd`:$PYTHONPATH
```

#### Questions

* Why is it necessary to add the _refactoring101/_ directory to your PYTHONPATH?
* What are three ways to update the PYTHONPATH?
* What is a class? What is a method? 
* What is an object in Python? What is an instance?

#### Exercises

* Look at the original results data, and model out some
  classes and methods to reflect "real-world" entities in the realm of elections.
* Examine functions in _lib/_ and try assigning three functions to 
  one of your new classes. Try extracting logic from functions to create
  new methods on your classes (e.g., Election.margin_of_victory)

## Phase 4 - Model Your Domain

TODO: Create models.py with Election, Race, Candidate classes.
