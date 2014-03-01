Candidates, of course
=====================

An election has a set of races, each of which have candidates.
So a `Candidate` class is a natural starting point for data modeling.

What basic characteristics does a candidate have in the context of the
`source data <https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html>`__?

Name, party and county election results jump out.

A candidate also has seems like a natural place for data transforms and
computations that now live in *lib/parser.py* and *lib/summary.py*:

-  candidate name parsing
-  total candiate votes from all counties
-  winner status

Before we migrate the hard stuff, let's start with the basics.

We'll store new election classes in a *lib/models.py*
(`Django <https://docs.djangoproject.com/en/dev/topics/db/models>`__
users, this should be familiar). We'll store tests for our new classes
in *test\_models.py* module.

Now let's start writing some test-driven code!

Name Parsing
------------

The Candidate class should be responsible for parsing a
full name into first and last names (remember, candidate names in our
source data are in the form *(Lastname, Firstname*).

-  Create *elex4/tests/test\_models.py* and add test for Candidate name
   parts
-  Run test; see it fail
-  Write a Candidate class with a private method to parse the full name

    *Note*: You can cheat here. Recall that the name parsing code was
    already written in *lib/parser.py*.

-  Run test; see it pass

Observations
~~~~~~~~~~~~

In the refactoring above, notice that we're not directly testing the
*name\_parse* method but simply checking for the correct value of the
first and last names on candidate instances. The *name\_parse* code has
been nicely tucked out of sight. In fact, we emphasize that this method
is an *implementation detail* -- part of the *Candidate* class's
internal housekeeping -- by prefixing it with two underscores.

This syntax denotes a `private
method <http://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references>`__
that is not intended for use by code outside the *Candidate* class.
We're restricting (though not completely preventing) the outside world
from using it, since it's quite possible this code wil change or be
removed in the future.

    More frequently, you'll see a single underscore prefix used to
    denote private methods and variables. This is fine, though note that
    only the double underscores trigger the name-mangling intended to
    limit usage of the method.

Questions
~~~~~~~~~

-  In order to migrate functions to methods on the Candidate class, we
   had to make the first parameter in each method *self*. Why?


County results
--------------

In addition to a name and party, each *Candidate* has county-level
results. As part of our summary report, county-level results need to be
rolled up into a racewide total for each candidate. At a high level, it
seems natural for each candidate to track his or her own vote totals.

Below are a few basic assumptions, or requirements, that will help us
flesh out vote-handling on the *Candidate* class:

-  A candidate should start with zero votes
-  Adding a vote should increment the vote count
-  County-level results should be accessible

With this basic list of requirements in hand, we're ready to start
coding. For each requirement, we'll start by writing a (failing) test
that captures this assumption; then we'll write code to make the test
pass (i.e. meet our assumption).

1. Add test to ensure *Candidate*'s initial vote count is zero

    Note: We created a new *TestCandidateVotes* class with a *setUp*
    method that lets us re-use the same candidate instance across all
    test methods. This makes our tests less brittle -- e.g., if we add a
    parameter to the *Candidate* class, we only have to update the
    candidate instance in the *setUp* method, rather than in every test
    method (as we will have to do in the *TestCandidate* class)

1. Run test; see it fail
2. Update *Candidate* class to have initial vote count of zero
3. Run test; see it pass

Now let's add a method to update the candidate's total vote totals for
each county result.

1. Add test for *Candidate.add\_votes* method
2. Run test; see it fail
3. Create the *Candidate.add\_votes* method
4. Run test; see it pass

Finally, let's stash the county-level results for each candidate.
Although we're not using these lower-level numbers in our summary
report, it's easy enough to add in case we need them for down the road.

1. Create test for county\_results attribute
2. Run test; see it fail
3. Update *Candidate.add\_votes* method to store county-level results
4. Run test; see it pass

Questions
~~~~~~~~~

Exercises
~~~~~~~~~

-  The *Candidate.add\_votes* method has a potential bug: It can't
   handle votes that are strings instead of proper integers. This bug
   might crop up if our parser fails to convert strings to integers.
   Write a unit test to capture the bug, then update the method to
   handle such "dirty data" gracefully.
