
class Candidate(object):

    def __init__(self, raw_name, party):
        self.last_name, self.first_name = [name.strip() for name in raw_name.split(",")]
        self.party = self.__clean_party(party)

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
