# refactoring101

## Overview

This repo contains code samples demonstrating how to transform a complex, linear script into a modular, 
easier-to-maintain package. The code is written as a reference for the *Python: Beyond the Basics* class 
at [NICAR 2014][], but can also work as a stand-alone tutorial.

The tutorial uses a small, [fake set of election results][] for demonstration purposes.

Project code evolves through four phases, each contained in a numbered *elex* directory. Below are descriptions of each phase, 
along with related questions and exercises that anticipate the next phase or set of skills.

The goal is to demonstrate how to use Python functions, modules, packages and classes to organize code more effectively. 
We also introduce unit testing as a strategy for writing programs that you can update with confidence. The overarching theme:
 **_As an application or program grows in size, writing readable code with tests can help tame complexity and keep you sane._**

Wondering how to use this tutorial or why the hell we called it *refactoring101*? The [FAQ][] has answers to 
these and sundry other questions. Also, check out the [Resources][] page for wisdom from our tribal elders.

[NICAR 2014]: http://ire.org/conferences/nicar-2014/
[fake set of election results]: https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html
[FAQ]: https://github.com/PythonJournos/refactoring101/wiki/FAQ
[Resources]: https://github.com/PythonJournos/refactoring101/wiki/Resources

## Inspiration

> "[Complexity kills][]." ~ *Ray Ozzie*

> "The art of simplicity is a puzzle of complexity." ~ *Douglas Horton*

> "...you're not refactoring; you're just [changing shit][]." ~ *Hamlet D'Arcy*

[Complexity kills]: http://ozzie.net/docs/dawn-of-a-new-day/
[changing shit]: http://hamletdarcy.blogspot.com/2009/06/forgotten-refactorings.html

## Phase 1 - Spaghetti

We begin with a single, linear script in the _elex1/_ directory. Below are a few reasons why this [code smells][] (some might say it reeks):

[code smells]: http://en.wikipedia.org/wiki/Code_smell

* It's hard to understand. You have to read the entire script before getting a full sense of what it does.
* It's hard to debug when something goes wrong.
* It's pretty much impossible to test, beyond eye-balling the output file.
* None of the code is reusable by other programs.

#### Questions

* What are [unit tests][]? 
* Can you identify three sections of logic that could be unit tested?
* What are [modules][]?
* What are [packages][]?

[unit tests]: http://docs.python.org/2/library/unittest.html
[modules]: http://docs.python.org/2/tutorial/modules.html
[packages]: http://docs.python.org/2/tutorial/modules.html#packages


####  Exercises

* Slice up this code into a bunch of functions, where related bits of logic are grouped together.
* Write a unit test for one or more functions extracted from this module.


## Phase 2 - Function Breakdown

In the _elex2/_ directory, we've chopped up the original election_results.py code into a bunch of
functions and turned this code directory into a package by adding an *\__init__.py* file.

We've also added a suite of tests. This way we can methodically change the underlying code in later phases,
while having greater confidence that we haven't corrupted our summary numbers. 

We can't stress this step enough: Testing existing code is *the* critical first step in refactoring.
If the code doesn't have tests, write some, at least for the most important bits of logic. Otherwise you're just [changing shit][] (see Ray Ozzie).

Fortunately, our code has a suite of [unit tests][] for name parsing and, most importantly, the summary logic.


Python has built-in facilities for running tests, but they're a little raw for our taste. We'll use the [nose][] library
to more easily run our tests:

```bash
nosetests -v tests/test_parser.py
# or run all tests in the tests/ directory
nosetests -v tests/*.py
```

[nose]: https://nose.readthedocs.org/en/latest/index.html

#### Observations

At a high level, this code is an improvement over _elex1/_, but it could still be much improved. We'll get to that
in Phase 3, when we introduce [modules][] and [packages][].

#### Questions

* What is *\__init__.py* and why do we use it?
* In what order are test methods run?
* What does the TestCase *setUp* method do?
* What other TestCase methods are available?

#### Exercises

* Install [nose][] and run the tests. Try breaking a few tests and run them to see the results.
* List three ways this code is better than the previous version; and three ways it could be improved.
* Organize functions in *election_results.py* into two or more new modules. (Hint: There is no right answer here. 
[Naming things is hard][]; aim for directory and file names that are short but meaningful to a normal human).

[Naming things is hard]: http://martinfowler.com/bliki/TwoHardThings.html

## Phase 3 - Modularize

In this third phase, we chop up our original *election_results.py* module into a legitimate 
Python package. The new directory structure is (hopefully) self-explanatory:


```
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

```

* **_lib/_** contains re-usable bits of code.
* **_scripts/_** contains...well..scripts that leverage our re-usable code.
* **_tests/_** contains tests for re-usable bits of code and related fixtures.

Note that we did not change any of our functions. Mostly we just re-organized them into new modules, 
with the goal of grouping related bits of logic in common-sense locations. We also updated 
imports and "namespaced" them of our own re-usable code under _elex3.lib_.

Here's where we start seeing the benefits of the tests we wrote in the *elex2* phase. While we've heavily
re-organized our underlying code structure, we can run the same tests (with a few minor updates to *import* statements) to ensure that we haven't broken anything.


> **Note**: You must add the _refactoring101_ directory to your _PYTHONPATH_ before any of the tests or script will work. 

```bash
$ cd /path/to/refactoring101
$ export PYTHONPATH=`pwd`:$PYTHONPATH

$ nosetests -v elex3/tests/*.py
$ python elex3/scripts/save_summary_to_csv.py
```

Check out the results of the *save_summary_to_csv.py* command. The new *summary_results.csv* should be stored *inside* 
the *elex3* directory, and should match the results file produced by *elex2/election_results.py*.


#### Questions

* Do you _like_ the package structure and module names? How would you organize or name things differently?
* Why is it necessary to add the _refactoring101/_ directory to your PYTHONPATH?
* What are three ways to add a library to the PYTHONPATH?
* What is a class? What is a method? 
* What is an object in Python? What is an instance?
* What is the __init__ method on a class used for?
* What is *self* and how does it relate to class instances?

#### Exercises

* Look at the original results data, and model out some
  classes and methods to reflect "real world" entities in the realm of elections.
* Examine functions in _lib/_ and try assigning three functions to one of your new classes.
* Try extracting logic from the _summarize_ function and re-implement it as a method on one of your classes.

## Phase 4 - Model Your Domain

In this section, we create classes that model the real world of 
elections. These classes are intended to serve as a more intuitive container 
for data transformations and complex bits of logic currently scattered across our application.

The goal is to [hide complexity][] behind simple [interfaces][].

We perform these refactorings in a step-by-step fashion and attempt to [write tests before the actual code][].

[hide complexity]: http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)
[interfaces]: http://en.wikipedia.org/wiki/Interface_(computing)
[write tests before the actual code]: http://en.wikipedia.org/wiki/Test-driven_development

So how do we start modeling our domain? We clearly have races and candidates, which seem like natural...wait for it...
"candidates" for model classes. We also have county-level results associated with each candidate.

Let's start by creating Candidate and Race classes with some simple behavior.
These classes will eventually be our workhorses, handling most of the grunt work needed 
to produce the summary report. But let's start with the basics.


### Candidate model

Candidates have a name, party and county election results. The candidate model also seems like a natural 
place for data transforms and computations that now live in _lib/parser.py_ and _lib/summary.py_:

* candidate name parsing
* total candiate votes from all counties
* winner status

Before we migrate the hard stuff, let's start with the basics. 

We'll store our new election classes in a *lib/models.py* ([Django][] users, this should be familiar). 
We'll store tests for our new classes in *test_models.py* module.

[Django]: https://docs.djangoproject.com/en/dev/topics/db/models

Now let's start writing some test-driven code!

#### Parse name

We'll start by creating a Candidate class that automatically parses a full name into first and last names (remember,
candidate names in our source data are in the form *(Lastname, Firstname*).

* Create *elex4/tests/test_models.py* and add test for Candidate name parts
* Run test; see it fail 
* Write a Candidate class with a private method to parse the full name

  > *Note*: You can cheat here. Recall that the name parsing code was
  > already written in *lib/parser.py*.

* Run test; see it pass



##### Observations

TODO: Change below to a private name_parse method

In the refactoring above, notice that we're not directly testing the *name_parse* method but simply 
checking for the correct value of the first and last names on candidate instances. The *name_parse* 
code has been nicely tucked out of sight. In fact, we emphasize that this method is an *implementation detail* --
part of the *Candidate* class's internal housekeeping -- by prefixing it with two underscores. 

This syntax denotes a [private method][] that is not intended for use by code outside the 
*Candidate* class. We're restricting (though not completely preventing) the outside world from using it,
since it's quite possible this code wil change or be removed in the future. 

> More frequently, you'll see a single underscore prefix used to denote private methods and variables.
> This is fine, though note that only the double underscores trigger the name-mangling
> intended to limit usage of the method.

[private method]: http://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references


##### Questions

* In order to migrate functions to methods on the Candidate class, we had to
  make the first parameter in each method *self*. Why?

### Add vote

In addition to a name and party, each *Candidate* has county-level results. 
As part of our summary report, county-level results need to be rolled up into a racewide total for each candidate. 
At a high level, it seems natural for each candidate to track his or her own vote totals.

Below are a few basic assumptions, or requirements, that will help us flesh out
vote-handling on the *Candidate* class:

* A candidate should start with zero votes
* Adding a vote should increment the vote count
* County-level results should be accessible

With this basic list of requirements in hand, we're ready to start coding. For each requirement, we'll start by
writing a (failing) test that captures this assumption; then we'll write code to make the test pass (i.e. meet
our assumption).

1. Add test to ensure *Candidate*'s initial vote count is zero 

  > Note: We created a new *TestCandidateVotes* class with a *setUp* method that lets us
  > re-use the same candidate instance across all test methods. This
  > makes our tests less brittle -- e.g., if we add a parameter to the
  > *Candidate* class, we only have to update the candidate instance in
  > the *setUp* method, rather than in every test method (as 
  > we will have to do in the *TestCandidate* class)

1. Run test; see it fail
1. Update *Candidate* class to have initial vote count of zero
1. Run test; see it pass

Now let's add a method to update the candidate's total vote totals for each county result.

1. Add test for *Candidate.add_votes* method
1. Run test; see it fail
1. Create the *Candidate.add_votes* method
1. Run test; see it pass

Finally, let's stash the county-level results for each candidate.
Although we're not using these lower-level numbers in our summary report, it's easy enough to
add in case we need it for some other use case down the road.

1. Create test for county_results attribute 
1. Run test; see it fail
1. Update *Candidate.add_votes* method to store county-level results
1. Run test; see it pass

#### Questions


#### Exercises

* The *Candidate.add_votes* method has a potential bug: It can't handle votes that are strings instead of proper integers.
  This bug might crop up if our parser fails to convert strings to integers. Write a unit test to capture the bug, then 
  update the method to handle such "dirty data" gracefully.


## Race model

## TODO

* Add Race code and tests (and docs)
* Update Parser to return Candidate and Race classes
* Update summary script to use Cand/Race objects returned by Parser class
* Add tree view of *elex4* directory; doesn't look so different from
  _elex3_ tree view (mainly added models.py and test_models.py), but the underlying implementation has
  changed dramatically (hopefully for the better)
