Races have Candidates!
======================

With the basics of our `Candidate` class out of the way, let's 
move on to building out the `Race` class. This higher-level
class will manage updates to our candidate instances, along with metadata 
about the race itself such as election date and office/district.

Recall that in *elex3*, the *lib/parser.py* ensured that county-level results were assigned to the appropriate candidate.
We'll now migrate that logic over to the `Race` class, along with a few other repsonsibilities:

-  Tracking overall vote count for the race
-  Updating candidates with new county-level votes
-  Determining which candidate, if any, won the race

Metadata and Total votes
------------------------

The *Race* class keeps a running tally of all votes. This figure is 
the sum of all county-level votes received by individual candidates.

Let's build out the *Race* class with basic metadata fields and an *add\_result* method
that updates the total vote count.

This should be pretty straight-forward, and you'll notice that the tests mirror those used to 
perform vote tallies on *Candidate* instances.

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

Candidate Bookkeeping
---------------------

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
\_\_get\_or\_create\_candidate. This method attempts to fetch a
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

Assigning Winners
-----------------

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
