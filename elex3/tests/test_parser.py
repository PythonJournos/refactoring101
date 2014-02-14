from os.path import dirname, join
from unittest import TestCase

from elex3.lib.parser import parse_and_clean


class TestParser(TestCase):

    def test_name_parsing(self):
        "Parser should split full candidate name into first and last names"
        path = join(dirname(__file__), 'sample_results.csv')
        results = parse_and_clean(path)
        race_key = 'President'
        cand_key = 'GOP-Smith, Joe'
        # Get one county result
        smith = results[race_key][cand_key][0]
        self.assertEqual(smith['first_name'], 'Joe')
        self.assertEqual(smith['last_name'], 'Smith')
