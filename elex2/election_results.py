"""
In this second pass at the election_results.py script, we chop up the code into
functions and add a few tests.

USAGE:

    python election_results.py

OUTPUT:

    summary_results.csv

"""
import csv
import urllib
from operator import itemgetter
from collections import defaultdict
from os.path import dirname, join


def main():
    # Download CSV of fake Virginia election results to root of project
    path = join(dirname(dirname(__file__)), 'fake_va_elec_results.csv')
    download_results(path)
    # Process data
    results = parse_and_clean(path)
    summary = summarize(results)
    write_csv(summary)


#### PRIMARY FUNCS ####
### These funcs perform the major steps of our application ###

def download_results(path):
    """Download CSV of fake Virginia election results from GDocs"""
    url = "https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=csv"
    urllib.urlretrieve(url, path)

def parse_and_clean(path):
    """Parse downloaded results file and perform various data clean-ups


    RETURNS:

        Nested dictionary keyed by race, then candidate.
        Candidate value is an array of dicts containing county level results.

    """
    # Create reader for ingesting CSV as array of dicts
    reader = csv.DictReader(open(path, 'rb'))

    # Use defaultdict to automatically create non-existent keys with an empty dictionary as the default value.
    # See https://pydocs2cn.readthedocs.org/en/latest/library/collections.html#defaultdict-objects
    results = defaultdict(dict)

    # Initial data clean-up
    for row in reader:
        # Parse name into first and last
        row['last_name'], row['first_name'] = [name.strip() for name in row['candidate'].split(',')]
        # Convert total votes to an integer
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


def summarize(results):
    """Tally votes for Races and candidates and assign winner flag.

    RETURNS:

        Dictionary of results

    """
    summary = defaultdict(dict)

    for race_key, cand_results in results.items():
        all_votes = 0
        cands = []
        for cand_key, results in cand_results.items():
            # Populate a new candidate dict using one set of county results
            cand = {
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'party': results[0]['party'],
                'winner': '',
            }
            # Calculate candidate total votes
            cand_total_votes = sum([result['votes'] for result in results])
            cand['votes'] = cand_total_votes
            # Add cand totals to racewide vote count
            all_votes += cand_total_votes
            # And stash the candidate's data
            cands.append(cand)

        # sort cands from highest to lowest vote count
        sorted_cands = sorted(cands, key=itemgetter('votes'), reverse=True)

        # Determine winner, if any
        first = sorted_cands[0]
        second = sorted_cands[1]

        if first['votes'] != second['votes']:
            first['winner'] = 'X'

        # Get race metadata from one set of results
        result = cand_results.values()[0][0]
        # Add results to output
        summary[race_key] = {
            'all_votes': all_votes,
            'date': result['date'],
            'office': result['office'],
            'district': result['district'],
            'candidates': sorted_cands,
        }

    return summary


def write_csv(summary):
    """Generates CSV from summary election results data

    CSV is written to 'summary_results.csv' file, inside same directory
    as this module.

    """
    outfile = join(dirname((__file__)), 'summary_results.csv')
    with open(outfile, 'wb') as fh:
        # Limit output to cleanly parsed, standardized values
        fieldnames = [
            'date',
            'office',
            'district',
            'last_name',
            'first_name',
            'party',
            'all_votes',
            'votes',
            'winner',
        ]
        writer = csv.DictWriter(fh, fieldnames, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for race, results in summary.items():
            cands = results.pop('candidates')
            for cand in cands:
                results.update(cand)
                writer.writerow(results)


# Q: What on earth is this __name__ == __main__ thing?
# A: Syntax that lets you execute a module as a script.
# http://docs.python.org/2/tutorial/modules.html#executing-modules-as-scripts
if __name__ == '__main__':
    main()
