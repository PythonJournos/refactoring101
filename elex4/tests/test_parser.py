from os.path import dirname, join
from unittest import TestCase

from elex4.lib.parser import parse_and_clean


class TestParser(TestCase):

    def test_name_parsing(self):
        "Parser should split full candidate name into first and last names"
        path = join(dirname(__file__), 'sample_results.csv')
        results = parse_and_clean(path)
        race = results['President']
        smith = [cand for cand in race.candidates.values() if cand.last_name == 'Smith'][0]
        self.assertEqual(smith.first_name, 'Joe')
        self.assertEqual(smith.last_name, 'Smith')
