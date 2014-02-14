#!/usr/bin/env python
import csv
from collections import defaultdict


def parse_and_clean(path):
    """Parse downloaded results file and perform various data clean-ups


    RETURNS:

        Nested dictionary keyed first by race, then candidate.
        Candidate value is an array of dicts containing county level results.

    """
    # Create reader for ingesting CSV as array of dicts
    reader = csv.DictReader(open(path, 'rb'))

    # Use defaultdict to automatically create non-existent keys with an empty dictionary as the default value.
    # See https://pydocs2cn.readthedocs.org/en/latest/library/collections.html#defaultdict-objects
    results = defaultdict(dict)

    # Initial data clean-up
    for row in reader:
        # Perform some data clean-ups and conversions
        row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]
        row['votes'] = int(row['votes'])

        # Store county-level results by slugified office and district (if there is one), 
        # then by candidate party and raw name
        race_key = row['office'] 
        if row['district']:
            race_key += "-%s" % row['district']
        # Create unique candidate key from party and name, in case multiple candidates have same
        cand_key = "-".join((row['party'], row['candidate']))
        # Below, setdefault initializes empty dict and list for the respective keys if they don't already exist.
        race = results[race_key]
        race.setdefault(cand_key, []).append(row)

    return results
