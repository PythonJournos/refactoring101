#!/usr/bin/env python
from collections import defaultdict
from operator import itemgetter


def summarize(results):
    """Tally votes for Races and candidates and assign winners.

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
        summary[race_key] = {
            'all_votes': all_votes,
            'date': result['date'],
            'office': result['office'],
            'district': result['district'],
            'candidates': sorted_cands,
        }

    return summary

