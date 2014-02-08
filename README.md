# refactoring101

## Overview

This repo contains code samples demonstrating how to transform a complex, linear script into a modular, 
easier-to-maintain package. The code is written as a reference for the *Python: Beyond the Basics* class 
at [NICAR 2014][], but can also work as a stand-alone tutorial.

The tutorial uses a small, [fake set of election results][] for demonstration purposes.

Project code evolves through four phases, each contained in a numbered *elex* directory. Below are descriptions of each phase, 
along with related questions and exercises that often anticipate the next phase or set of skills.

The goal is to demonstrate how to use Python functions, modules, packages and classes to organize code more effectively. 
We also introduce unit testing as a strategy for writing programs that you can update with confidence. The overarching theme:
 **_As an application or program grows in size, writing readable code with tests can help tame complexity and keep you sane._**

Wondering how to use this tutorial or why the hell we called it *refactoring101*? The [FAQ][] has answers to 
these and sundry other questions. Also, check out the [Resources][] page for wisdom from our tribal elders.

[NICAR 2014]: http://ire.org/conferences/nicar-2014/
[fake set of election results]: https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html
[FAQ]: https://github.com/PythonJournos/refactoring101/wiki/FAQ
[Resources]: https://github.com/PythonJournos/refactoring101/wiki/Resources

## Phase 1 - Spaghetti

We begin with a single, linear script in the _elex1/_ directory. Below are a few reasons why this [code smells][] (some might even say it reeks):

[code smells]: http://en.wikipedia.org/wiki/Code_smell

* It's hard to understand. You have to read the entire script before getting a full sense of what it does.
* It's hard to debug when something goes wrong.
* It's pretty much impossible to test, beyond eye-balling the output file.
* None of the code is reusable by other programs.

#### Questions

* What is a unit test? 
* Can you identify three sections of logic that could be unit tested?


####  Exercises

* Slice up this code into a bunch of functions, where related bits of logic are grouped together.
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
* Organize functions in election_results.py into two or more new modules. (Hint: There is no right answer here. 
[Naming things is hard][]; aim for directory and file names that are short but meaningful to a normal human).

[Naming things is hard]: http://martinfowler.com/bliki/TwoHardThings.html

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

> **Note**: You must add the _refactoring101_ directory to your _PYTHONPATH_ before any of the tests or script will work. 

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
* What is *self* and how does it relate to class instances?

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

The goal is to [hide complexity][] behind simple [interfaces][].

We perform these refactorings in a step-by-step fashion and attempt to [write tests before the actual code][].

> NOTE: We've assigned git tags to code commits so you can examine the state of affairs at each step of coding.
> You can [check out these tags][] in your local repo, or view them on github by clicking links in the README. 
> Tag links look like this: [elex4.1.0][]

[hide complexity]: http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)
[interfaces]: http://en.wikipedia.org/wiki/Interface_(computing)
[write tests before the actual code]: http://en.wikipedia.org/wiki/Test-driven_development
[check out these tags]: http://githowto.com/tagging_versions
[elex4.1.0]: https://github.com/PythonJournos/refactoring101/tree/elex4.1.0

So how do we start modeling our domain? We clearly have races and candidates, which seem like natural...wait for it...
"candidates" for model classes. We also have county-level results associated with each candidate.

Let's start by creating Candidate and Race classes with some simple behavior.
These classes will eventually be our workhorses, handling most of the grunt work needed 
to produce the summary report. But let's start with the basics.


### Candidate model

Candidates have a name, party and county election results. The candidate model also seems like a natural 
place for some of the data transforms and computations that now live in _lib/parser.py_ and _lib/analysis.py_:

* total candiate votes from all counties
* candidate vote percentage
* winner status
* margin of victory, if appropriate

Before we dive into migrating data transforms and computed values, let's start with the basics. 
We'll store our new election classes in a *lib/models.py* ([Django[] users, this should be familiar). 
We'll store tests in a new *test_models.py* module.

[Django]: https://docs.djangoproject.com/en/dev/topics/db/models

We'll run tests on the command line using the [nose][] library: 

```bash
nosetests -v tests/test_models.py
# or run all tests in the tests/ directory
nosetests -v tests/*.py
```

[nose]: https://nose.readthedocs.org/en/latest/index.html

Now let's start writing some test-driven code!

#### Add name bits

We'll start by creating a Candidate class that automatically parses a full name into first and last names (remember,
candidate names in our source data are in the form *Lastname, Firstname*).

* Create *elex4/tests/test_models.py* and add test for Candidate name parts ([elex4.1.0][])
* Run test; see it fail 
* Write a Candidate class with *first_name* and *last_name* attributes ([elex4.1.1][])

  > *Note*: You can cheat here. Recall that the name parsing code was
  > already written in *lib/parser.py*.

* Run test; see it pass

[elex4.1.0]: https://github.com/PythonJournos/refactoring101/blob/elex4.1.0/elex4/tests/test_models.py "test_models.py"
[elex4.1.1]: https://github.com/PythonJournos/refactoring101/blob/elex4.1.1/elex4/lib/models.py        "lib/models.py"

Let's apply a similar process for the party transformation.

#### Add party

The candidate party requires special handling for Democratics and Republicans. Otherwise we'll default to the raw party value.

* Migrate party-related tests from *tests/test_parser.py* to *TestCandidate* in *tests/test_models.py*. 

  > **Note**: Don't forget to add the party argument to the Candidate instance in *test_candidate_name*. 
  > Otherwise you'll get an error!
  
* Run test; see it fail ([elex4.2.0][])
* Convert the *clean_party* function to a method on *Candidate* and apply it during initialization. ([elex4.2.1][])
  
  ```python
    def __clean_party(self, party):
        # code that does stuff
  ```
  
    > **Note**: Make sure you add *self* as the first parameter to the *__clean_party* method. Otherwise you'll get
    > get a *TypeError* about not passing enough arguments. Bonus points if you know why.
 
* Run test; see it pass

[elex4.2.0]: https://github.com/PythonJournos/refactoring101/blob/elex4.2.0/elex4/tests/test_models.py "test_models.py"
[elex4.2.1]: https://github.com/PythonJournos/refactoring101/blob/elex4.2.1/elex4/lib/models.py        "lib/models.py"

##### Observations

In the party refactoring above, notice that we're not directly testing the *clean_party* method but simply 
checking for the correct value of the *party* attribute on candidate instances. The *clean_party* code has been nicely 
tucked out of sight. In fact, we emphasize that this method is an *implementation detail* --
part of the *Candidate* class's internal housekeeping -- by prefixing it with two underscores. 

This syntax denotes a [private method][] that is not intended for use by code outside the 
*Candidate* class. We're restricting (though not completely preventing) the outside world from using it,
since it's quite possible this code wil change or be removed in the future. 

> More frequently, you'll see a single underscore prefix used to denote private methods and variables.
> This is fine, though note that only the double underscores trigger the name-mangling
> intended to limit usage of the method.

[private method]: http://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references

We now have two sets of code (and related tests) for the same functionality. But we're not quite ready 
to delete the original *clean_party* function in _lib/parser.py_. Ideally, we'll delete that code and its tests
*after* we've written tests that exercise the summarization logic. That way, we'll have greater confidence that 
converting from a function-based to a class-based strategy hasn't corrupted the summary numbers.

##### Questions

* In order to migrate functions to methods on the Candidate class, we had to
  make the first parameter in each method *self*. Why?

### Add vote

Each candidate has a single name and party, and numerous county-level results. 
As part of our summary report, county-level results need to be rolled up into a racewide total for each candidate. 
At a high level, it seems natural for each candidate to track his or her own vote totals.

Below are a few other basic assumptions, or requirements, that will help us flesh out
vote-handling on the Candidate class:

* A candidate should start with zero votes
* Adding a vote should increment the vote count
* County-level results should be accessible

With this basic list of requirements in hand, we're ready to start coding. For each requirement, we'll start by
writing a (failing) test that captures this assumption; then we'll write code to make the test pass. The goal
is to capture our assumptions in the form of tests, and then write code to meet those assumnptions.

1. Add test for zero vote count as initial Candidate state ([elex4.3.0][])

  > Note: We created a new *TestCandidateVotes* class with a *setUp* method that lets us
  > re-use the same candidate instance across all test methods. This
  > makes our tests less brittle -- e.g., if we add a parameter to the
  > *Candidate* class, we only have to update the candidate instance in
  > the *setUp* method, rather than in every test method (as 
  > we will have to do in the *TestCandidate* class)

1. Run test; see it fail
1. Update Candidate to have initial vote count of zero ([elex4.3.1][])
1. Run test; see it pass
1. Add test for *Candidate.add_votes* method ([elex4.3.2][]) 
1. Run test; see it fail
1. Create the *Candidate.add_votes* method ([elex4.3.3][])
1. Run test; see it pass
1. Create test for county_results attribute ([elex4.3.4][])
1. Run test; see it fail
1. Update *Candidate.add_votes* method to store county-level results ([elex4.3.5][])
1. Run test; see it pass

[elex4.3.0]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.0/elex4/tests/test_models.py "test_models.py"
[elex4.3.1]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.1/elex4/lib/models.py        "lib/models.py"
[elex4.3.2]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.2/elex4/tests/test_models.py "test_models.py"
[elex4.3.3]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.3/elex4/lib/models.py        "lib/models.py"
[elex4.3.4]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.4/elex4/tests/test_models.py "test_models.py"
[elex4.3.5]: https://github.com/PythonJournos/refactoring101/blob/elex4.3.5/elex4/lib/models.py        "lib/models.py"

#### Questions

* What does the TestCase *setUp* method do?
* The test methods *test_vote_count_update* and *test_county_results_access* 
  each add 20 votes to the candidate instance created in *setUp*. Why
  are candidate votes equal to 20 in both tests, instead of
  adding up to 40 in one of them (which would cause a test failure)?
* In what order are test methods run?
* What other unittest.TestCase methods are available?

#### Exercises

* Read the [unittest docs][] page.
* The *Candidate.add_votes* method has a potential bug: It can't handle votes that are strings instead of proper integers.
  This bug might crop up if our parser fails to convert strings to integers. Write a test to capture the bug, then update 
  the method to handle such "dirty data" gracefully.

[unittest docs]: http://docs.python.org/2/library/unittest.html

## Race model

## TODO

* Race.office and district 
* Race.add_result (gets or creates candidate instance)
* Candidate.winner, margin, vote_pct (since these require all Candidates to be available via parent Race class)
* Write high-level tests for summarize output
* Update Parser to return Candidate and Race classes
* Update summary script to use Cand/Race objects returned by Parser class
* Add another tree view of directory; doesn't look so different from
  _elex3_ tree view (mainly added models.py and test_models.py), but the underlying implementation has
  changed dramatically (hopefully for the better)
* Add disclaimers about our pragmatic approach, vs more disciplined approaches
  involving test isolation, etc.
