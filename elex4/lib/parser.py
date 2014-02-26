#!/usr/bin/env python
import csv
from collections import defaultdict

from elex4.lib.models import Race


def parse_and_clean(path):
    """Parse downloaded results file.


    RETURNS:

        A dictionary containing race key and Race instances as values.

    """
    # Create reader for ingesting CSV as array of dicts
    reader = csv.DictReader(open(path, 'rb'))

    results = {}

    # Initial data clean-up
    for row in reader:
        # Convert votes to integer
        row['votes'] = int(row['votes'])

        # Store races by slugified office and district (if there is one)
        race_key = row['office'] 
        if row['district']:
            race_key += "-%s" % row['district']

        try:
            race = results[race_key]
        except KeyError:
            race = Race(row['date'], row['office'], row['district'])
            results[race_key] = race

        race.add_result(row)

    return results
