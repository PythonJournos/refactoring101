Phase 4 - Model Your Domain
---------------------------

In this section, we create classes that model the real world of
elections. These classes are intended to serve as a more intuitive
container for data transformations and complex bits of logic currently
scattered across our application.

The goal is to `hide
complexity <http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)>`__
behind simple
`interfaces <http://en.wikipedia.org/wiki/Interface_(computing)>`__.

We perform these refactorings in a step-by-step fashion and attempt to
`write tests before the actual
code <http://en.wikipedia.org/wiki/Test-driven_development>`__.

So how do we start modeling our domain? We clearly have races and
candidates, which seem like natural...wait for it... "candidates" for
model classes. We also have county-level results associated with each
candidate.

Let's start by creating Candidate and Race classes with some simple
behavior. These classes will eventually be our workhorses, handling most
of the grunt work needed to produce the summary report. But let's start
with the basics.

Candidate model
~~~~~~~~~~~~~~~

Candidates have a name, party and county election results. The candidate
model also seems like a natural place for data transforms and
computations that now live in *lib/parser.py* and *lib/summary.py*:

-  candidate name parsing
-  total candiate votes from all counties
-  winner status

Before we migrate the hard stuff, let's start with the basics.

We'll store our new election classes in a *lib/models.py*
(`Django <https://docs.djangoproject.com/en/dev/topics/db/models>`__
users, this should be familiar). We'll store tests for our new classes
in *test\_models.py* module.

Now let's start writing some test-driven code!

Parse name
^^^^^^^^^^

We'll start by creating a Candidate class that automatically parses a
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
''''''''''''

TODO: Change below to a private name\_parse method

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
'''''''''

-  In order to migrate functions to methods on the Candidate class, we
   had to make the first parameter in each method *self*. Why?

Add vote
~~~~~~~~

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
^^^^^^^^^

Exercises
^^^^^^^^^

-  The *Candidate.add\_votes* method has a potential bug: It can't
   handle votes that are strings instead of proper integers. This bug
   might crop up if our parser fails to convert strings to integers.
   Write a unit test to capture the bug, then update the method to
   handle such "dirty data" gracefully.

Race model
----------

Races have a date, office, and possibly a district if it's a
congressional office. They also, of course, have candidates. In *elex3*,
the *lib/parsery.py* code managed candiates, ensuring that county-level
results were assigned to the appropriate candidate.

We'll now migrate that logic over to the Race class, along with a few
other repsonsibilities:

-  Keep track of individual candidates and update their vote counts
-  Determine which, candidate, any, won the race
-  Track overall vote count in the race

Update racewide votes
~~~~~~~~~~~~~~~~~~~~~

The Race class has to keep a running tally of all votes. This represnts
the sum of all votes received by individual candidates.

Let's build out our initial *Race* class with an *add\_result* method
that handles these updates. This should be pretty straightforward, and
you'll notice that the tests mirror those used to perform the vote
tallies on *Candidate* instances.

.. code:: python


    # Don't forget to import Race from elex4.lib.models at the top of your test module!

    class TestRace(TestCase):

        def setUp(self):
            self.smith_result = {
                'date': '2012-11-06',
                'candidate': 'Smith, Joe',
                'party': 'Dem',
                'office': 'President',
                'county': 'Fairfax',
                'votes': 2000,
            }
            self.race = Race("2012-11-06", "President", "")

        def test_total_votes_default(self):
            "Race total votes should default to zero"
            self.assertEquals(self.race.total_votes, 0)

        def test_total_votes_update(self):
            "Race.add_result should update racewide vote count"
            self.race.add_result(self.smith_result)
            self.assertEquals(self.race.total_votes, 2000)

Go ahead and run those tests and watch them fail.

Now let's build out our initial *Race* class with an *add\_result*
method to make the tests pass.

::

    class Race(object):

        def __init__(self, date, office, district):
            self.date = date
            self.office = office
            self.district = district
            self.total_votes = 0

        def add_result(self, result):
            self.total_votes += result['votes']

Update candidates
~~~~~~~~~~~~~~~~~

In earlier phases of the project, the parser code ensured that
county-level results were grouped with the appropriate, unique candidate
in each race. If you recall, those county results were stored in a list
for each candidate:

.. code:: python

    # elex3.lib.parser.py

    def parse_and_clean

      # ... snipped...

          # Store county-level results by slugified office and district (if there is one), 
            # then by candidate party and raw name
            race_key = row['office'] 
            if row['district']:
                race_key += "-%s" % row['district']

            # Create unique candidate key from party and name, in case multiple candidates have same
            cand_key = "-".join((row['party'], row['candidate']))

            # Get or create dictionary for the race
            race = results[race_key]

            # Get or create candidate dictionary with a default value of a list; Add result to the list
            race.setdefault(cand_key, []).append(row)

We now have Candidate classes that manage their own county results. But
we need to migrate the bookkeeping of Candidate instances from the
parser code to the *Race* class. Specifically, we need create a new
Candidate instance or fetch a pre-existing instance, as appropriate, for
each county result.

Let's start by adding a test to our *TestRace* class that ensures we're
updating a single candiate instance, rather than accidentally creating
duplicate instances.

.. code:: python


    class TestRace(TestCase):

        # ... snipped ...

        def test_add_result_to_candidate(self):
            "Race.add_result should update a unique candidate instance"
            # Add a vote twice. If it's the same candidate, vote total should be sum of results
            self.race.add_result(self.smith_result)
            self.race.add_result(self.smith_result)
            cand_key = (self.smith_result['party'], self.smith_result['candidate'])
            candidate = self.race.candidates[cand_key]
            self.assertEquals(candidate.votes, 4000)

Run that test and watch it fail. You'll notice we have a new
*candidates* attribute that is a dictionary. This is pretty much the
same approach we used in earlier phases, where we stored candidate data
by a unique key. However, instead of using a slug, we're now using
tuples as keys.

    Accessing *candidate* data directly in this way is a code smell, and
    it could be argued that we should also write a candidate lookup
    method. We'll leave that as an exercise.

Now let's update the *Race* class and its *add\_result* method to make
the test pass.

.. code:: python


    class Race(object):

        def __init__(self, date, office, district):
            # .... snipped .... 
            # We add the candiddates dictionary
            self.candidates = {}

        def add_result(self, result):
            self.total_votes += result['votes']
            # Below lines
            candidate = self.__get_or_create_candidate(result)
            candidate.add_votes(result['county'], result['votes'])

        # Private methods
        def __get_or_create_candidate(self, result):
            key = (result['party'], result['candidate'])
            try:
                candidate = self.candidates[key]
            except KeyError:
                candidate = Candidate(result['candidate'], result['party'])
                self.candidates[key] = candidate
            return candidate

Above, the bulk of our work is handled by a new private method called
\*\_\_get\_or\_create\_candidate\ *. This method attempts to fetch a
pre-existing *\ Candidate\* instance or creates a new one and adds it to
the dictionary, before returning the instance.

Once we have the correct instance, we call its *add\_votes* method to
update the vote count and add the result to that candidate's county
results list.

Our test verifies this by calling the *add\_result* method twice and
then checking the candidate instance's vote count to ensure the vote
count is correct.

    Testing purists may point out that we've violated the principle of
    `test isolation <http://c2.com/cgi/wiki?UnitTestIsolation>`__, since
    this unit test directly accesses the candidate instance and relies
    on its underlying vote tallying logic. There are testing strategies
    and tools, such as mocks, to help avoid or minimize such *tight
    coupling* between unit tests. For the sake of simplicity, we'll wave
    our hand at that issue in this tutorial and leave it as a study
    exercise for the reader.

Assign winner
~~~~~~~~~~~~~

We're now ready for the last major piece of the puzzle, namely,
migrating the code that determines race winners. This logic was
previously handled in the *summary* function and its related tests.

.. code:: python

    # elex3/lib/summary.py

    # ... snipped ....

        # sort cands from highest to lowest vote count
        sorted_cands = sorted(cands, key=itemgetter('votes'), reverse=True)

        # Determine winner, if any
        first = sorted_cands[0]
        second = sorted_cands[1]

        if first['votes'] != second['votes']:
            first['winner'] = 'X'

    # ... snipped ....

We'll migrate our tests and apply some minor updates to reflect the fact
that we're now storing data in Candidate and Race classes, rather than
nested dictionaries and lists.

    It's important to note that while we're modifying the test syntax to
    accommodate our new objects, we're not changing the *substance* of
    the tests.

First, let's add an extra sample result to the *setUp* method to support
each test.

.. code:: python


    # elex4/tests/test_models.py

    class TestRace(TestCase):

        def setUp(self):
        

          # ... snipped ....

            self.doe_result = {
                'date': '2012-11-06',
                'candidate': 'Doe, Jane',
                'party': 'GOP',
                'office': 'President',
                'county': 'Fairfax',
                'votes': 1000,
            } 

Next, let's migrate the winner, non-winner and tie race tests from
*elex3/tests/test\_summary* to the *TestRace* class in
*elex4/tests/test\_models.py*.

.. code:: python


    class TestRace(TestCase):

          # ... snipped ....

        def test_winner_has_flag(self):
            "Winner flag should be assigned to candidates with most votes"
            self.race.add_result(self.doe_result)
            self.race.add_result(self.smith_result)
            # Our new method triggers the assignment of the winner flag
            self.race.assign_winner()
            smith = [cand for cand in self.race.candidates.values() if cand.last_name == 'Smith'][0]
            self.assertEqual(smith.winner, 'X')

        def test_loser_has_no_winner_flag(self):
            "Winner flag should not be assigned to candidate that does not have highest vote total"
            self.race.add_result(self.doe_result)
            self.race.add_result(self.smith_result)
            self.race.assign_winner()
            doe = [cand for cand in self.race.candidates.values() if cand.last_name == 'Doe'][0]

        def test_tie_race(self):
            "Winner flag should not be assigned to any candidate in a tie race"
            # Modify Doe vote count to make it a tie for this test method
            self.doe_result['votes'] = 2000
            self.race.add_result(self.doe_result)
            self.race.add_result(self.smith_result)
            self.race.assign_winner()
            for cand in self.race.candidates.values():
                self.assertEqual(cand.winner, '')

These tests mirror the test methods in *elex3/tests/test\_summary.py*.
We've simply tweaked them to reflect our class-based apprach and to
exercise the new *Race* method that assigns the winner flag.

We'll eventually delete the duplicative tests in *test\_summary.py*, but
we're not quite ready to do so yet.

First, let's make these tests pass by tweaking the *Candidate* class and
implementing the *Race.assign\_winner* method:

.. code:: python

    # elex4/lib/models.py

    class Candidate(object):

        def __init__(self, raw_name, party):

            # ... snipped...

            # Add a new winner attribute to candidate class with empty string as default value
            self.winner = ''


    class Race(object):

        # ... snipped...

        def assign_winner(self):
            # Sort cands from highest to lowest vote count
            sorted_cands = sorted(self.candidates.values(), key=attrgetter('votes'), reverse=True)

            # Determine winner, if any
            first = sorted_cands[0]
            second = sorted_cands[1]

            if first.votes != second.votes:
                first.winner = 'X'

Above, notice that we added a default *Candidate.winner* attribute, and
a *Race.assign\_winner* method. The latter is nearly a straight copy of
our original winner-assignment logic in the *summarize* function. The
key differences are:

-  We're calling *self.candidate.values()* to get a list of *Candidate*
   instances, since these are now stored in a dictionary.
-  We're using *attrgetter* instead of *itemgetter* to access the
   candidate's vote count for purposes of sorting. This is necessary, of
   course, because we're now sorting by the value of an instance
   attribute rather than the value of a dictionary key.
-  We're accessing the *votes* attribute on candidate instances rather
   than performing dictionary lookups.

Swapping Implementations
------------------------

With most of our core logic encapsulated in the *Candidate* and *Race*
classes, we're finally ready to update the parser and summary code. This
is the step we've been waiting for -- where we radically simplify these
functions by outsourcing most of the work to our (hopefully)
easier-to-understand domain models.

Updates such as this on a large, active application often feels like
changing the engine on a moving car. It's scary, and you're never quite
sure if you're about to cause a wreck. Fortunately, we have a suite of
tests that let us apply our changes and quickly get feedback on whether
we broke anything.

Let's start at the "entry point" of our application, namely, the parser.
We'll update this code to use our Race class instead of nested
dictionaries and lists.

Parser update
~~~~~~~~~~~~~

.. code:: python


    def parse_and_clean():
        
        # ... snipped ...

        results = {}

        # Initial data clean-up
        for row in reader:
            # Convert votes to integer
            row['votes'] = int(row['votes'])

            # Store races by slugified office and district (if there is one)
            race_key = row['office'] 
            if row['district']:
                race_key += "-%s" % row['district']

            try:
                race = results[race_key]
            except KeyError:
                race = Race(row['date'], row['office'], row['district'])
                results[race_key] = Race

            race.add_result(row)

        # ... snipped ...

Here are the list of changes:

-  Delete the candidate name parsing code
-  Simplify results storage and use try/except to get/create Race
   instances
-  Update Race and, by extension, candidate vote totals, by calling
   *add\_result* on *Race* instance.

Before porting the *summarize* function to use this new input, let's
update the parser tests and ensure evertyhing runs correctly. We'll
tweak our test to use dotted-attribute notation instead of dictionary
lookups, to reflect the new class-based approach.

.. code:: python

    # elex4/tests/test_parser.py

    class TestParser(TestCase):

        def test_name_parsing(self):
            "Parser should split full candidate name into first and last names"
            race = results['President']
            smith = [cand for cand in race.candidates.values() if cand.last_name == 'Smith'][0]
            # Below lines changed from dictionary access
            self.assertEqual(smith.first_name, 'Joe')   # formerly, smith['first_name']
            self.assertEqual(smith.last_name, 'Smith')  # formerly, smith['last_name']

Now run the tests:

::

    nosetests -v elex4/tests/test_parser.py

The updated *parse\_and\_clean* function is easier to read and maintain
than its original version, but it could still be much improved. For
instance, we could easily hide the race-key logic and type conversion of
votes inside the *Race* class.

We could also transform the function into a class, and encapsulate the
get/create logic for *Race* instances in a private method, similar to
the \*Race.\_\_get\_or\_create\_candidate\* method.

We'll leave such refactorings as exercises for the reader.

Exercises
^^^^^^^^^

-  The *parse\_and\_clean* function, though simplified, still has too
   much cruft. Perform the following refactorings:
-  Move code that converts votes to an integer inside the *Race* class
-  Create a *Race.key*
   `property <http://docs.python.org/2/library/functions.html#property>`__
   that encapsulates this logic, and remove it from the parser function
-  Simplify the return value of *parse\_and\_clean* to only return a
   list of *Race* instances, rather than a dictionary. This will require
   also refactoring the *summarize* function
-  Refactor the *parse\_and\_clean* function into a *Parser* class with
   a private \*\_\_get\_or\_create\_race\* method.

Summarize refactor
~~~~~~~~~~~~~~~~~~

Refactoring the *summarize* function is a bit trickier than the parser
code, since we plan to change the input data for this function. Recall
that the parser code now returns a dict of *Race* instances, rather than
nested dicts. The *summarize* function needs to be updated to handle
this type of input.

This also means that we can no longer feed the test fixture JSON, as is,
to the *summarize* function in our *setUp* method. Instead, we need to
build input data that mirrors what would be returned by the updated
*parse\_and\_clean* function: Namely, a dictionary containing *Race*
instances as values.

First, we'll simplify the test fixtures by removing the nested object
structure. Instead, we'll make them a simple array of result objects.

    Note: We could re-use the same JSON fixtures from *elex3* without
    modification, but this would result in a more convoluted *setUp*
    method. Wherever possible, use the simplest test data possible.

Then we'll update the *setUp* method to handle our simpflified JSON
fixtures, and we'll move into a new *TestSummaryBase* class.
*TestSummaryResults* and *TestTieRace* will *sub-class* this new base
class instead of *TestCase*, allowing them both to make use of the same
*setUp* code.

This is an example of class
`inheritance <http://docs.python.org/2/tutorial/classes.html#inheritance>`__.
Python classes can inherit methods and attributes from other classes by
*subclassing* one or more parent classes. This is a powerful, core
concept of object-oriented programming that helps keep code clean and
re-usable.

And it's one that we've been using for a while, when we subclassed
*unittest.TestCase* in our test classes. We're essentially substituting
our own parent class, one that blends the rich functionality of
*TestCase* with a custom *setUp* method. This allows the same *setUp*
code to be used by methods in multiple subclasses.

.. code:: python


    class TestSummaryBase(TestCase):

        def setUp(self):
            # Recall that sample data only has a single Presidential race
            race = Race('2012-11-06', 'President', '')
            for result in self.SAMPLE_RESULTS:
                race.add_result(result)
            # summarize function expects a dict, keyed by race
            summary = summarize({'President': race})
            self.race = summary['President']


    # Update the main test classes to inherit this base class, instead of
    # directly from TestCase

    class TestSummaryResults(TestSummaryBase):

    # ... snipped ...


    class TestTieRace(TestSummaryBase):

    # ... snipped ...

If you ran the *test\_summary.py* suite now, you'd see all tests
failing.

Now we're ready to swap in our new class-based implementation. This time
we'll be deleting quite a bit of code, and tweaking what remains. Below
is the new code, followed by a list of major changes:

.. code:: python


        # We removed the defaultdict and use a plain-old dict
        summary = {}

        for race_key, race in results.items():
            cands = []
            # Call our new assign_winner method
            race.assign_winner()
            # Loop through Candidate instances and extract a dictionary 
            # of target values. Basically, we're throwing away county-level
            # results since we don't need those for the summary report
            for cand in race.candidates.values():
                # Remove lower-level county results
                # This is a dirty little trick to botainfor easily obtaining
                # a dictionary of candidate attributes.
                info = cand.__dict__.copy()
                # Remove county results
                info.pop('county_results')
                cands.append(info)

            summary[race_key] = {
                'all_votes': race.total_votes,
                'date': race.date,
                'office': race.office,
                'district': race.district,
                'candidates': cands,
            }

        return summary

Changes to the *summariz* function include:

-  Convert *summary* output to plain dictionary (instead of defaultdict)
-  Delete all code for sorting and determining winner. This is replaced
   by a call to the *assign\_winner* method on Race classes.
-  Create a list of candidate data as dictionaries without county-level
   results
-  Update code that adds data to the *summary* dictionary to use the
   race instance and newly created *cands* list.

Of course, we should run our test to make sure the implementation works.

::

    nosetests -v elex4/tests/test_summary.py

At this point, our refactoring work is complete. We should verify that
all tests run without failures:

::

    nosetests -v elex4/tests/test_*.py

Overall, the *summarize* function has grown much simpler by outsourcing
the bulk of work to the *Race* and *Candidate* classes. In fact, it
could be argued that the *summarize* function doesn't do enough at this
point to justify its existence. Its main role is massaging data into a
form that plays nice with the *save\_summary\_to\_csv.py* script.

It might make sense to push the remaining bits of logic into the
Race/Candidate model classes and the *save\_summary\_to\_csv.py* script.

You'll also notice that the *summary* tests closely mirror those for the
*Race* class in *elex4/tests/test\_models.py*. Redundant tests can cause
confusion and add maintenance overhead.

It would make sense at this point to delete the *summarize* tests for
underlying functionality -- tallying votes, assigning winners -- and
create new tests specific to the summary output. For example, you could
write a test that ensures the output structure meets expections.

Questions
^^^^^^^^^

-  What is a class attribute?
-  How does Python construct classes?
-  What is the
   `\_\_dict\_\_ <http://docs.python.org/2/library/stdtypes.html#object.__dict__>`__
   special attribute on a class?
-  How can the built-in
   `type <http://docs.python.org/2/library/functions.html#type>`__
   function be used to construct classes dynamically?

Exercises
^^^^^^^^^

-  Implement a *Race.summary*
   `property <http://docs.python.org/2/library/functions.html#property>`__
   that returns all data for the instance, minus the *Candidate* county
   results. Swap this implementation into the *summarize* function.
-  Delete tests in *elex4/tests/test\_summary.py* and add a new test
   that verifies the structure of the output.
