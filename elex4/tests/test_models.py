from unittest import TestCase

from elex4.lib.models import Candidate

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
