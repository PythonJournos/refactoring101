from unittest import TestCase

from .election_results import clean_office, clean_party, percent


class TestDataCleaners(TestCase):

    def test_clean_office_prez(self):
        self.assertEquals(clean_office('President'), ('President', 'president', ''))

    def test_clean_office_rep(self):
        self.assertEquals(clean_office('U.S. Rep - 1'), ('U.S. House of Representatives', 'us-house', 1))

    def test_clean_office_other(self):
        self.assertEquals(clean_office('U.S. Senate'), ('U.S. Senate', 'us-senate', ''))

    def test_clean_party_gop(self):
        self.assertEquals(clean_party('GOP'), 'REP')

    def test_clean_party_dem(self):
        self.assertEquals(clean_party('Democratic'), 'DEM')

    def test_clean_party_others(self):
        self.assertEquals(clean_party('Green'), 'GREEN')



class TestPercentFunc(TestCase):

    def test_percent(self):
        "test_percent returns percentage as string"
        self.assertEquals(percent(50, 100), '50')
