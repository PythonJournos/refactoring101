from os.path import dirname, join
from unittest import TestCase
import json

from elex4.lib.models import Race
from elex4.lib.summary import summarize


class TestSummaryBase(TestCase):

    def setUp(self):
        # Recall that sample data only has a single Presidential race
        race = Race('2012-11-06', 'President', '')
        for result in self.SAMPLE_RESULTS:
            race.add_result(result)
        # summarize function expects a dict, keyed by race
        summary = summarize({'President': race})
        self.race = summary['President']

class TestSummaryResults(TestSummaryBase):

    json_file = open(join(dirname(__file__), 'sample_results_parsed.json'), 'rb')
    SAMPLE_RESULTS = json.load(json_file)

    def test_racewide_vote_total(self):
        "Summary results should be annotated with total votes cast in race"
        self.assertEqual(self.race['all_votes'], 31)

    def test_candiate_vote_totals(self):
        "Summary candidates should reflect total votes from all counties"
        smith = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Smith'][0]
        self.assertEqual(smith['votes'], 15)

    def test_winner_has_flag(self):
        "Winner flag should be assigned to candidates with most votes"
        doe = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Doe'][0]
        self.assertEqual(doe['winner'], 'X')

    def test_loser_has_no_winner_flag(self):
        "Winner flag should not be assigned to candidate that does not have highest vote total"
        smith = [cand for cand in self.race['candidates'] if cand['last_name'] == 'Smith'][0]
        self.assertEqual(smith['winner'], '')


class TestTieRace(TestSummaryBase):

    json_file = open(join(dirname(__file__), 'sample_results_parsed_tie_race.json'), 'rb')
    SAMPLE_RESULTS = json.load(json_file)

    def test_tie_race_winner_flags(self):
        "Winner flag should not be assigned to any candidate in a tie race"
        for cand in self.race['candidates']:
            self.assertEqual(cand['winner'], '')
