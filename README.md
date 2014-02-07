# refactoring101

## Overview

This repo contains code samples demonstrating how to transform a complex, linear script into a modular, easier-to-maintain package. The code is written as a reference for the *Python: Beyond the Basics* class at [NICAR 2014](http://ire.org/conferences/nicar-2014/), but can also work as a stand-alone tutorial.

The tutorial uses a small, [fake set of election results](https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv) created for demonstration purposes.

Project code evolves through four phases, each contained in a numbered *elex* directory. Below are descriptions of each phase, along with related questions and exercises that often anticipate the next phase or set of skills.

The goal is to demonstrate how to use Python functions, modules, packages and classes to organize code more effectively. We also introduce unit testing as a strategy for writing programs that you can update with confidence. The overarching theme: **_As an application or program grows in size, writing readable code with tests can help tame complexity and keep you sane._**

Wondering how to use this tutorial or why the hell we called it *refactoring101*? The [FAQ](https://github.com/PythonJournos/refactoring101/wiki/FAQ) has answers to these and sundry other questions. Also, check out the [Resources](https://github.com/PythonJournos/refactoring101/wiki/Resources) page for wisdom from our tribal elders.

## Phase 1 - Spaghetti

We begin with a single, linear script in the _elex1/_ directory. Below are a few reasons why this [code smells](http://en.wikipedia.org/wiki/Code_smell) (some might even say it reeks):

* It's hard to understand. You have to read the entire script before getting a full sense of what it does.
* It's hard to debug when something goes wrong.
* It's pretty much impossible to test, beyond eye-balling the output file.
* None of the code is reusable by other programs.

#### Questions

* What is a unit test? 
* Can you identify three sections of logic that could be unit tested?


####  Exercises

* Try slicing up this code into a bunch of functions, where related bits of logic are grouped together.
* Write a unit test for one or more functions extracted from this module.


## Phase 2 - Function Breakdown

In the _elex2/_ directory, we've chopped up the original election_results.py code into a bunch of
functions, and added a few tests. We've also turned this code directory
into a package by adding an *\__init__.py* file.  This code is an improvement over _elex1/_, but it still
could be a lot better.

#### Questions

* What is a module?
* What is a package?
* What is *\__init__.py* and why do we use it?

#### Exercises

* List three ways this code is better than the previous version; and three ways it could be improved.
* Organize functions in election_results.py into two or more new modules. (Hint: There is no right answer here. [Naming things is hard](http://martinfowler.com/bliki/TwoHardThings.html); aim for directory and file names that are short but meaningful to a normal human).

## Phase 3 - Modularize

In this third phase, we chop up our original election_results.py module into a legitimate 
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

* **_lib/_** contains re-usable bits of code.
* **_scripts/_** contains...well..scripts that leverage our re-usable code.
* **_tests/_** contains tests for re-usable bits of code.

Note that we did not change any of our functions. Mostly we just re-organized them into new modules, 
with the goal of grouping related bits of logic in common-sense locations. We also migrated 
imports and "namespaced" imports of our own re-usable code under _elex3.lib_.

**Important**: You must add the _refactoring101_ directory to your _PYTHONPATH_ before any of the tests or script will work. 

```bash
$ cd /path/to/refactoring101
$ export PYTHONPATH=`pwd`:$PYTHONPATH
```

#### Questions

* Do you _like_ the package structure and module names? How would you organize or name things differently?
* Why is it necessary to add the _refactoring101/_ directory to your PYTHONPATH?
* What are three ways to update the PYTHONPATH?
* What is a class? What is a method? 
* What is an object in Python? What is an instance?
* What is the __init__ method on a class used for?
* What is _self_ and how does it relate to class instances?

#### Exercises

* Look at the original results data, and model out some
  classes and methods to reflect "real-world" entities in the realm of elections.
* Examine functions in _lib/_ and try assigning three functions to one of your new classes.
* Try extracting logic from the _summarize_ function and re-implement it as a method on one of your classes.
* Break the code. Find the code that determines the winner. Comment out the


## Phase 4 - Model Your Domain

In this section, we create classes that model the real world of 
elections. These classes are intended to serve as a more intuitive container 
for data transformations and complex bits of logic currently scattered across our application.

The goal is to [hide complexity][] behind simple interfaces.

We perform these refactorings in a step-by-step fashion and attempt to [write tests before the actual code][]. 
*NOTE:We've assigned git tags to various stages of the code so you can examine the state of affairs at different points. 
You can check out these tags in your local repo, or view them on github by clicking links in the README. 
Tag links look like this: [elex4.1.0][]*

[hide complexity]: http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)
[write tests before the actual code]: http://en.wikipedia.org/wiki/Test-driven_development
[elex4.1.0]: https://github.com/PythonJournos/refactoring101/tree/elex4.1.0

So how do we start modeling our domain? We clearly have races and candidates, and the results associated with each 
candidate.

Let's start by creating the Candidate and Race classes with some simple behavior 
Gradually, we'll flesh out these classes to handle most of the grunt work needed 
to produce the summary report.


### Candidate model

Candidates have a name, party and county election results. The candidate model also seems like a natural 
place for some of the computations that now live in _lib/parser.py_ and _lib/analysis.py_:

* total candiate votes from all counties
* candidate vote percentage
* winner status
* margin of victory, if appropriate

Before we dive into migrating computed values, let's start with the basics. 
We've decided to store our new election classes in a models.py (Django users, this should be familiar). 
Therefore, we'll store tests in a new *test_models.py* module.

We can run those tests by doing the following:
```bash
nosetests -v tests/test_models.py
```

Now let's start writing some test-driven code.

#### Add name bits

* Create test_models.py
* Add test for Candidate name handling ([elex4.1.0][])
* Run test to see it fail 
* Write a Candidate class that exposes first and last name attributes ([elex4.1.1][])
* Run test to see it pass

[elex4.1.0]: https://github.com/PythonJournos/refactoring101/blob/elex4.1.0/elex4/tests/test_models.py "test_models.py"
[elex4.1.1]: https://github.com/PythonJournos/refactoring101/blob/elex4.1.1/elex4/lib/models.py        "lib/models.py"


Let's apply a similar process for the party transformation.

#### Add party

* Migrate party tests from *test_parser.py* to TestCandidate. **Note**: We
  had to update Candidate creation in *test_candidate_name* as well to prevent it from breaking!
* Run test to see it fail ([elex4.2.0][])
* Convert clean_party function to a method on Candidate. Make sure you add *self* as first parameter!
  Apply the method during initialization. ([elex4.2.1][])
* Run test and see it pass

[elex4.2.0]: https://github.com/PythonJournos/refactoring101/blob/elex4.2.0/elex4/tests/test_models.py "test_models.py"
[elex4.2.1]: https://github.com/PythonJournos/refactoring101/blob/elex4.2.1/elex4/lib/models.py        "lib/models.py"

##### Notes

Notice we're not directly testing the *clean_party* method, but simply checking
the *Candidate.party* attribute for correct values. *clean_party* has been nicely 
tucked out of sight. In fact, we emphasize that this method is an *implementation detail* --
part of the candidate class's internal housekeeping -- by prefixing it with two underscores. 

This syntax denotes a [private method][] that is not intended for use by code outside the 
*Candidate* class. We're restricting (though not completely preventing) the outside world from using it,
since it's quite possible this code wil change or be removed entirely in the future. 

> More frequently, you'll see a single underscore prefix used to denote private methods.
> This is fine, though note that only the double underscores trigger the name-mangling
> intended to limit usage of the method.

[private method]: http://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references

So we now have two sets of code for the same functionality, and two sets of related
tests. But we're not yet ready to delete the original *clean_party* function in _lib/parser.py_
and its tests. Ideally, we'll delete that code *after* we have tests that exercise the output of the 
summary logic. That way, we'll have greater confidence that converting from a function-based approach
a class-based strategy hasn't corrupted the summary numbers.

##### Questions

* In order to migrate functions to methods on the Candidate class, we had to
  make the first parameter in each method *self*. Why?

##### Exercises


## TODO

* Candidate.votes
* Race.office and district 
* Race.add_result (gets or creates candidate instance)
* Candidate.winner, margin, vote_pct (since these require all Candidates to be available via parent Race class)
* Write high-level tests for summarize output
* Update Parser to return Candidate and Race classes
* Update summary script to use Cand/Race objects returned by Parser class



