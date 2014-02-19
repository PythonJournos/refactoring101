from unittest import TestCase

from elex4.lib.models import Candidate, Race


class TestCandidate(TestCase):

    def test_candidate_name(self):
        "Candidates should have first_name and last_name attributes"
        cand = Candidate("Smith, Joe", "GOP")
        self.assertEquals(cand.first_name, "Joe")
        self.assertEquals(cand.last_name, "Smith")


class TestCandidateVotes(TestCase):

    def setUp(self):
        self.cand = Candidate("Smith, Joe", "GOP")

    def test_default_zero_votes(self):
        "Candidate vote count should default to zero"
        self.assertEquals(self.cand.votes, 0)

    def test_vote_count_update(self):
        "Candidate.add_votes method should update vote count"
        self.cand.add_votes("Some County", 20)
        self.assertEquals(self.cand.votes, 20)

    def test_county_results_access(self):
        "Candidate.add_votes method should store county results"
        self.cand.add_votes("Some County", 20)
        expected = { "Some County": 20 }
        self.assertEquals(self.cand.county_results, expected)


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
        self.doe_result = {
            'date': '2012-11-06',
            'candidate': 'Doe, Jane',
            'party': 'GOP',
            'office': 'President',
            'county': 'Fairfax',
            'votes': 1000,
        }
        self.race = Race("2012-11-06", "President", "")

    def test_total_votes_default(self):
        "Race total votes should default to zero"
        self.assertEquals(self.race.total_votes, 0)

    def test_total_votes_update(self):
        "Race.add_result should update racewide vote count"
        self.race.add_result(self.smith_result)
        self.assertEquals(self.race.total_votes, 2000)

    def test_add_result_to_candidate(self):
        "Race.add_result should update a unique candidate instance"
        # Add a vote twice. If it's the same candidate, vote total should be sum of results
        self.race.add_result(self.smith_result)
        self.race.add_result(self.smith_result)
        cand_key = (self.smith_result['party'], self.smith_result['candidate'])
        candidate = self.race.candidates[cand_key]
        self.assertEquals(candidate.votes, 4000)

    def test_winner_has_flag(self):
        "Winner flag should be assigned to candidates with most votes"
        self.race.add_result(self.doe_result)
        self.race.add_result(self.smith_result)
        self.race.assign_winner()
        smith = [cand for cand in self.race.candidates.values() if cand.last_name == 'Smith'][0]
        self.assertEqual(smith.winner, 'X')

    def test_loser_has_no_winner_flag(self):
        "Winner flag should not be assigned to candidate who does not have highest vote total"
        self.race.add_result(self.doe_result)
        self.race.add_result(self.smith_result)
        self.race.assign_winner()
        doe = [cand for cand in self.race.candidates.values() if cand.last_name == 'Doe'][0]
        self.assertEqual(doe.winner, '')

    def test_tie_race(self):
        "Winner flag should not be assigned to any candidate in a tie race"
        # Modify Doe vote count to make it a tie
        self.doe_result['votes'] = 2000
        self.race.add_result(self.doe_result)
        self.race.add_result(self.smith_result)
        self.race.assign_winner()
        for cand in self.race.candidates.values():
            self.assertEqual(cand.winner, '')
