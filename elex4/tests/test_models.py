from unittest import TestCase

from elex4.lib.models import Candidate

class TestCandidate(TestCase):

    def test_candidate_name(self):
        "Candidates should have first_name and last_name attributes"
        cand = Candidate("Smith, Joe")
        self.assertEquals(cand.first_name, "Joe")
        self.assertEquals(cand.last_name, "Smith")
