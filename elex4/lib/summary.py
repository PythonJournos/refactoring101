#!/usr/bin/env python
from collections import defaultdict
from decimal import Decimal, getcontext
from operator import itemgetter


# HELPER FUNC
# Set precision for all Decimals
getcontext().prec = 2

def percent(part, total):
    pct = (Decimal(part) / Decimal(total)) * 100
    return "%s" %  pct.to_eng_string()

def summarize(results):
    """
    Create a new set of summary results that includes each candidate's
    statewide total votes, % of vote, winner flag, margin of victory, tie_race flag

    RETURNS:

        Dictionary of results

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
            'district': result['district'],
            'candidates': sorted_cands,
        }

    return summary

