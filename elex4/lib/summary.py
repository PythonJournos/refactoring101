from collections import defaultdict
from operator import itemgetter


def summarize(results):
    """Triggers winner assignments and formats data for output.

    RETURNS:

        Dictionary of results

    """
    summary = {}

    for race_key, race in results.items():
        cands = []
        # Call our new assign_winner method
        race.assign_winner()
        # Loop through Candidate instances and extract a dictionary 
        # of target values. Basically, we're throwing away county-level
        # results since we don't need those for the summary report
        for cand in race.candidates.values():
            # Remove lower-level county results
            # This is a dirty little trick to botainfor easily obtaining
            # a dictionary of candidate attributes.
            info = cand.__dict__.copy()
            # Remove county results
            info.pop('county_results')
            cands.append(info)

        summary[race_key] = {
            'all_votes': race.total_votes,
            'date': race.date,
            'office': race.office,
            'district': race.district,
            'candidates': cands,
        }

    return summary

