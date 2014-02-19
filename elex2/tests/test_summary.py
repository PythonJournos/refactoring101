from os.path import dirname, join
from unittest import TestCase
import json

from elex2.election_results import summarize


class TestSummaryResults(TestCase):

    # Read the results of the parse_and_clean function stored in a test fixture
    json_file = open(join(dirname(__file__), 'sample_results_parsed.json'), 'rb')
    SAMPLE_RESULTS = json.load(json_file)
    # Q: Why aren't we just using the parse_and_clean method instead of
    # using a snapshot of that function's output?
    # A: To achieve better test isolation!
    
    # Q: Why aren't reading in the JSON in a setUp method?
    # A: setUp is called before each test method. This ensures we only
    # incur the overhead of reading in the JSON once. In python2.7 or newer,
    # you should use the setUpClass method instead of a class attribute.
    # http://docs.python.org/2/library/unittest.html#unittest.TestCase.setUpClass

    # We will, however, use the setUp method to call the summarize
    # funciton afresh before each of our test methods.
    def setUp(self):
        results = summarize(self.SAMPLE_RESULTS)
        self.race = results['President']

    def test_racewide_vote_total(self):
        "Summary results should be annotated with total votes cast in race"
        self.assertEqual(self.race['all_votes'], 31)

    def test_candiate_vote_totals(self):
        "Summary candidates should reflect total votes from all counties"
        # Loop through candidates and find Smith rather than relying on
        # default sorting of candidates, which would make this test brittle
        # the implementation changed.
        smith = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Smith'][0]
        self.assertEqual(smith['votes'], 15)

    def test_winner_has_flag(self):
        "Winner flag should be assigned to candidates with most votes"
        doe = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Doe'][0]
        self.assertEqual(doe['winner'], 'X')

    def test_loser_has_no_winner_flag(self):
        "Winner flag should be not be assigned to candidate with that does not have highest vote total"
        smith = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Smith'][0]
        self.assertEqual(smith['winner'], '')


class TestTieRace(TestCase):

    # Q: Why do we need a new class and fixture for this race?
    # A: So that we can change the vote counts so that we have a tie, of course!
    # We don't *need* a new test class, but hey, why not?
    json_file = open(join(dirname(__file__), 'sample_results_parsed_tie_race.json'), 'rb')
    SAMPLE_RESULTS = json.load(json_file)

    def test_tie_race_winner_flags(self):
        "Winner flag should not be assigned to any candidate in a tie race"
        results = summarize(self.SAMPLE_RESULTS)
        race = results['President']
        for cand in race['candidates']:
            self.assertEqual(cand['winner'], '')
