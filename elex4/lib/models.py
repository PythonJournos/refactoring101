from operator import attrgetter

class Race(object):

    def __init__(self, date, office, district):
        self.date = date
        self.office = office
        self.district = district
        self.total_votes = 0
        self.candidates = {}

    def add_result(self, result):
        self.total_votes += result['votes']
        candidate = self.__get_or_create_candidate(result)
        candidate.add_votes(result['county'], result['votes'])

    def assign_winner(self):
        # sort cands from highest to lowest vote count
        sorted_cands = sorted(self.candidates.values(), key=attrgetter('votes'), reverse=True)

        # Determine winner, if any
        first = sorted_cands[0]
        second = sorted_cands[1]

        if first.votes != second.votes:
            first.winner = 'X'


    # Private methods
    def __get_or_create_candidate(self, result):
        key = (result['party'], result['candidate'])
        try:
            candidate = self.candidates[key]
        except KeyError:
            candidate = Candidate(result['candidate'], result['party'])
            self.candidates[key] = candidate
        return candidate


class Candidate(object):

    def __init__(self, raw_name, party):
        self.last_name, self.first_name = self.__parse_name(raw_name)
        self.party = party
        self.county_results = {}
        self.votes = 0
        self.winner = ''

    def add_votes(self, county, votes):
        self.county_results[county] = votes
        self.votes += votes

    # Private method
    def __parse_name(self, raw_name):
        return [name.strip() for name in raw_name.split(",")]
