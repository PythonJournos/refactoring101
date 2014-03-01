Enter stage left - Races and Candidates
=======================================

The *Candidate* and *Race* classes now encapsulate our core 
logic. It's time to put these classes to work.

This is the step we've been waiting for -- where we simplify the 
parser ond summary code by outsourcing complex logic to simple
domain models (i.e. *Candidate* and *Race* classes).

Major code updates such as this feel like changing the engine on a moving car:
It's scary, and you're never quite sure if an accident is waiting around the corner.
Fortunately, we have a suite of tests that let us apply our changes and quickly get 
feedback on whether we broke anything.

Let's start by swapping in the *Race* class in the parser code, the
entry point of our application. The *Race* class replaces nested dictionaries 
and lists.


Update Parser
-------------

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

Update Summary
--------------

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
