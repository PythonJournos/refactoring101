#!/usr/bin/env python
import csv
from collections import defaultdict
from decimal import Decimal, getcontext


def parse_and_clean(path):
    """Parse downloaded results file and perform various data clean-ups


    RETURNS:

        Nested dictionary keyed first by race, then candidate.
        Candidate value is an array of dicts containing county level results.

    """
    # Create reader for ingesting CSV as array of dicts
    reader = csv.DictReader(open(path, 'rb'))

    # Normally, accessing a non-existent dictionary key would raise a KeyError.
    # Use defaultdict to automatically create non-existent keys with an empty dictionary as the default value.
    # See https://pydocs2cn.readthedocs.org/en/latest/library/collections.html#defaultdict-objects
    results = defaultdict(dict)

    # Initial data clean-up
    #import ipdb;ipdb.set_trace()
    for row in reader:
        # Perform some data clean-ups and conversions
        row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]
        row['party_clean'] = clean_party(row['party'])
        row['office_clean'], row['office_slug'], row['district'] = clean_office(row['office'])
        row['votes'] = int(row['votes'])

        # Store county-level results uusing unique keys for race and candidates
        race_key = (row['office_slug'], row['district'])
        # Use party in case multiple candidates have same last name
        cand_key = (row['party_clean'], row['last_name'])
        # Below, setdefault initializes empty dict and list for the respective keys if they don't already exist.
        race = results[race_key]
        race.setdefault(cand_key, []).append(row)

    return results

def clean_party(party):
    party = party.strip().upper()
    if party.startswith('GOP'):
        party_clean = 'REP'
    elif party.startswith('DEM'):
        party_clean = 'DEM'
    else:
        party_clean = party
    return party_clean

def clean_office(office):
    if 'Pres' in office:
        office_clean = office.strip()
        office_slug = 'president'
        district = ''
    elif 'Rep' in office:
        office_clean = 'U.S. House of Representatives'
        office_slug = 'us-house'
        district = int(office.split('-')[-1])
    else:
        office_clean = office.strip()
        office_slug = office.strip().replace('.', '').replace(' ', '-').lower()
        district = ''
    return office_clean, office_slug, district

