class Election:
    def __init__(self, title, status="Active"):
        self.__title = title
        self.__status = status
        self.__candidates = []
        self.__voters = []

    def get_title(self):
        return self.__title

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def add_candidate(self, candidate):
        self.__candidates.append(candidate)

    def set_candidates(self, candidate_list):
        self.__candidates = candidate_list

    def get_candidates(self):
        return self.__candidates

    def get_total_votes(self):
        """Tüm adayların oylarını toplayarak toplam katılımı hesaplar."""
        return sum(c.get_vote_count() for c in self.__candidates)

    def __str__(self):
        return f"Election: {self.__title} ({self.__status}) - {len(self.__candidates)} Candidates"