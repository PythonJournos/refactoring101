
class Candidate(object):

    def __init__(self, raw_name):
        self.last_name, self.first_name = [name.strip() for name in raw_name.split(",")]
