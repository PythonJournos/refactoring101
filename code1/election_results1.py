#!/usr/bin/env python
"""
A monstrosity of an election results script. Bundles together waaaay too much 
functionality in a single module.
"""
import csv
import datetime
import urllib
from decimal import Decimal, getcontext
from operator import itemgetter
from collections import defaultdict
from os.path import abspath, dirname, join
from urllib import urlretrieve

# Set precision for all Decimals
getcontext().prec = 2

# Download CSV of fake Virginia election results from GDocs
url = "https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv"

# Download the file to the root project directory /path/to/refactorin101/
# NOTE: This will only download the file if it doesn't already exist
# This approach is simplified for demo purposes. In a real-life application,
# you'd likely have a considerable amount of additional code
# to appropriately handle HTTP timeouts, 404s, and other real-world scenarios.
# For example, you might retry a request several times after a timeout, and then
# send an email alert that the site is non-responsive.
filename = join(dirname(dirname(abspath(__file__))), 'fake_va_elec_results.csv')
urllib.urlretrieve(url, filename)

# Create reader for ingesting CSV as array of dicts
reader = csv.DictReader(open(filename, 'rb'))

# Normally, accessing a non-existent dictionary key would raise a KeyError.
# Use defaultdict to automatically create non-existent keys with an empty dictionary as the default value.
# See https://pydocs2cn.readthedocs.org/en/latest/library/collections.html#defaultdict-objects
results = defaultdict(dict)

# Initial data clean-up
for row in reader:
    # Parse name into first and last
    row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]

    # Standardize party abbreviations
    party = row['party'].strip().upper()
    if party.startswith('GOP'):
        party_clean = 'REP'
    elif party.startswith('DEM'):
        party_clean = 'DEM'
    else:
        party_clean = party
    row['party_clean'] = party_clean

    # Standardize Office and add slug and district
    office = row['office']
    if 'Pres' in office:
        row['office_clean'] = office.strip()
        row['office_slug'] = 'president'
        row['district'] = ''
    elif 'Rep' in office:
        row['office_clean'] = 'U.S. Representative'
        row['office_slug'] = 'us-house'
        row['district'] = int(office.split('-')[-1])
    else:
        row['office_clean'] = office.strip()
        row['office_slug'] = office.strip().replace(' ', '-')
        row['district'] = ''

    # Convert total votes to an integer
    row['votes'] = int(row['votes'])

    # Create unique keys for race and candidates to store county-level results
    race_key = (row['office_slug'], row['district'])
    # Use party in case multiple candidates have same last name
    cand_key = (row['party_clean'], row['last_name'])

    # Below, setdefault initializes empty dict and list for the respective keys if they don't already exist.
    race = results[race_key]
    race.setdefault(cand_key, []).append(row)


# Create a new set of summary results that includes each candidate's
# statewide total votes, % of vote, winner flag, margin of victory, tie_race flag
summary = defaultdict(dict)

for race_key, cand_results in results.items():
    all_votes = 0
    tie_race = ''
    cand_totals = []
    for cand_key, results in cand_results.items():
        # Populate a new candidate dict using one set of county results
        cand = results[0].copy()
        # Remove all non-candidate entries such as votes, office, district, etc.
        [cand.pop(key) for key in cand.keys() if key not in ('candidate', 'first_name', 'last_name', 'party', 'party_clean')]
        # Calculate candidate total votes
        cand_statewide_total= sum([result['votes'] for result in results])
        cand['votes'] = cand_statewide_total
        cand_totals.append(cand)
        # Add cand totals to racewide vote count
        all_votes += cand_statewide_total

    # sort cands from highest to lowest vote count
    sorted_cands = sorted(cand_totals, key=itemgetter('votes'), reverse=True)

    # Determine vote pct for each candiate
    for cand in sorted_cands:
        vote_pct = (Decimal(cand['votes']) / Decimal(all_votes)) * 100
        cand['vote_pct'] = "%s" %  vote_pct.to_eng_string()

    # Determine winner, if any, and assign margin of victory
    first = sorted_cands[0]
    second = sorted_cands[1]

    if first['votes'] == second['votes']:
        tie_race = 'X'
    else:
        first['winner'] = 'X'
        mov = (Decimal(first['votes'] - second['votes']) / all_votes) * 100
        first['margin_of_vic'] = "%s" % mov.to_eng_string()

    # Get race metadata from one set of results
    result = cand_results.values()[0][0]
    summary[race_key] = {
        'all_votes': all_votes,
        'tie_race': tie_race,
        'date': result['date'],
        'county': result['county'],
        'office': result['office_clean'],
        'office_slug': result['office_slug'],
        'district': result['district'],
        'candidates': sorted_cands,
    }


# Output CSV of results
outfile = join(dirname(abspath(__file__)), 'summary_results.csv')
with open(outfile, 'wb') as fh:
    fieldnames = [
        'date',
        'office_slug',
        'district',
        'last_name',
        'first_name',
        'party_clean',
        'county',
        'all_votes',
        'votes',
        'vote_pct',
        'winner',
        'margin_of_vic',
        'tie_race',
    ]
    writer = csv.DictWriter(fh, fieldnames, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for race, results in summary.items():
        cands = results.pop('candidates')
        for cand in cands:
            meta = results.copy()
            meta.update(cand)
            writer.writerow(meta)
