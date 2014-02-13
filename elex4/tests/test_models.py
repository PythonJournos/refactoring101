from unittest import TestCase

from elex4.lib.models import Candidate, Race


class TestCandidate(TestCase):

    def test_candidate_name(self):
        "Candidates should have first_name and last_name attributes"
        cand = Candidate("Smith, Joe", "GOP")
        self.assertEquals(cand.first_name, "Joe")
        self.assertEquals(cand.last_name, "Smith")

    def test_party_gop(self):
        cand = Candidate("Smith, Joe", "GOP")
        self.assertEquals(cand.party, 'REP')

    def test_clean_party_dem(self):
        cand = Candidate("Smith, Joe", "Democratic")
        self.assertEquals(cand.party, 'DEM')

    def test_clean_party_others(self):
        cand = Candidate("Smith, Joe", "Green")
        self.assertEquals(cand.party, 'GREEN')


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

    def test_clean_office_rep(self):
        race = Race("2012-11-06", "U.S. Rep - 1")
        self.assertEquals(race.office, "U.S. House of Representatives")
        self.assertEquals(race.district, 1)

    def test_clean_office_other(self):
        race = Race("2012-11-06", "President")
        self.assertEquals(race.office, "President")
        self.assertEquals(race.district, "")

    def test_total_votes_default(self):
        "Race total votes should default to zero"
        race = Race("2012-11-06", "President")
        self.assertEquals(race.total_votes, 0)

    def test_total_votes_update(self):
        "Race.add_result should update total votes for each result"
        race = Race("2012-11-06", "President")
        race.add_result(self.smith_result)
        self.assertEquals(race.total_votes, 2000)
