#!/usr/bin/env python
"""
A monstrosity of an election results script. Generates statewide results for races, 
based on county results.

This module bundles together way too much functionality and is near impossible to test,
beyond eye-balling results.

USAGE:

    python election_results.py


OUTPUT:

    Generates summary_results.csv


"""
import csv
import datetime
import urllib
from decimal import Decimal, getcontext
from operator import itemgetter
from collections import defaultdict
from os.path import abspath, dirname, join
from urllib import urlretrieve


def main():
    fname = 'fake_va_elec_results.csv'
    path = join(dirname(dirname(abspath(__file__))), fname)
    download_results(path)
    results = parse_and_clean(path)
    summary = summarize(results)
    write_csv(summary)


# HELPER FUNCS
# Set precision for all Decimals
getcontext().prec = 2

def percent(part, total):
    pct = (Decimal(part) / Decimal(total)) * 100
    return "%s" %  pct.to_eng_string()

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


# PRIMARY FUNCS
def download_results(path):
    """Download CSV of fake Virginia election results from GDocs

    Downloads the file to the root of the repo (/path/to/refactoring101/).

    NOTE: This will only download the file if it doesn't already exist
    This approach is simplified for demo purposes. In a real-life application,
    you'd likely have a considerable amount of additional code
    to appropriately handle HTTP timeouts, 404s, and other real-world scenarios.
    For example, you might retry a request several times after a timeout, and then
    send an email alert that the site is non-responsive.

    """
    url = "https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv"
    urllib.urlretrieve(url, path)


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
    for row in reader:
        # Parse name into first and last
        row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]

        # Standardize party abbreviations
        row['party_clean'] = clean_party(row['party'])


        # Add clean Office name, slug and district
        row['office_clean'], row['office_slug'], row['district'] = clean_office(row['office'])

        # Convert total votes to an integer
        row['votes'] = int(row['votes'])

        # Create unique keys for race and candidates to store county-level results
        race_key = (row['office_slug'], row['district'])
        # Use party in case multiple candidates have same last name
        cand_key = (row['party_clean'], row['last_name'])

        # Below, setdefault initializes empty dict and list for the respective keys if they don't already exist.
        race = results[race_key]
        race.setdefault(cand_key, []).append(row)

    return results


def summarize(results):
    """
    Create a new set of summary results that includes each candidate's
    statewide total votes, % of vote, winner flag, margin of victory, tie_race flag
    """
    summary = defaultdict(dict)

    for race_key, cand_results in results.items():
        all_votes = 0
        tie_race = ''
        cand_totals = []
        for cand_key, results in cand_results.items():
            # Populate a new candidate dict using one set of county results
            cand = {
                'candidate': results[0]['candidate'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'party': results[0]['party'],
                'party_clean': results[0]['party_clean'],
                'winner': '',
                'margin_of_vic': '',
            }
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
            cand['vote_pct'] = percent(cand['votes'], all_votes)

        # Determine winner, if any, and assign margin of victory
        first = sorted_cands[0]
        second = sorted_cands[1]

        if first['votes'] == second['votes']:
            tie_race = 'X'
        else:
            first['winner'] = 'X'
            first['margin_of_vic'] = percent(first['votes'] - second['votes'], all_votes)

        # Get race metadata from one set of results
        result = cand_results.values()[0][0]
        summary[race_key] = {
            'all_votes': all_votes,
            'tie_race': tie_race,
            'date': result['date'],
            'office': result['office_clean'],
            'office_slug': result['office_slug'],
            'district': result['district'],
            'candidates': sorted_cands,
        }

    return summary


def write_csv(summary):
    """Generates CSV from summary election results data

    CSV is written to 'summary_results.csv' file, inside same directory
    as this module.

    """
    outfile = join(dirname(abspath(__file__)), 'summary_results.csv')
    with open(outfile, 'wb') as fh:
        # Limit output to cleanly parsed, standardized values
        fieldnames = [
            'date',
            'office_slug',
            'district',
            'last_name',
            'first_name',
            'party_clean',
            'all_votes',
            'votes',
            'vote_pct',
            'winner',
            'margin_of_vic',
            'tie_race',
        ]
        writer = csv.DictWriter(fh, fieldnames, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        #import ipdb;ipdb.set_trace()
        for race, results in summary.items():
            cands = results.pop('candidates')
            for cand in cands:
                results.update(cand)
                writer.writerow(results)



if __name__ == '__main__':
    main()
