class Election:

    def __init__(self, title):
        self.__title = title
        self.__candidates = []
        self.__voters = []

    def get_title(self):
        return self.__title

    def get_all_candidates(self):
        return self.__candidates

    def register_candidate(self, candidate):
        self.__candidates.append(candidate)

    def register_voter(self, voter):
        self.__voters.append(voter)

    def remove_candidate(self, candidate_id):
        for candidate in self.__candidates:
            if candidate.get_candidate_id() == candidate_id:
                self.__candidates.remove(candidate)
                return True
        return False
    