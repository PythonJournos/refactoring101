
class Race(object):

    def __init__(self, date, raw_office):
        self.date = date
        self.office, self.district = self.__clean_office(raw_office)

    # Private methods
    def __clean_office(self, office):
        if 'Rep' in office:
            office_clean = 'U.S. House of Representatives'
            district = int(office.split('-')[-1])
        else:
            office_clean = office.strip()
            district = ''
        return office_clean, district


class Candidate(object):

    def __init__(self, raw_name, party):
        self.last_name, self.first_name = [name.strip() for name in raw_name.split(",")]
        self.party = self.__clean_party(party)
        self.county_results = {}
        self.votes = 0

    def add_votes(self, county, votes):
        self.county_results[county] = votes
        self.votes += votes

    # Private methods
    def __clean_party(self, party):
        party = party.strip().upper()
        if party.startswith('GOP'):
            party_clean = 'REP'
        elif party.startswith('DEM'):
            party_clean = 'DEM'
        else:
            party_clean = party
        return party_clean
