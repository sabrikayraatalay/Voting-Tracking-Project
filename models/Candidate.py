
class Candidate:
    def __init__(self, candidate_id, name, party, position, city=None):
        self.__candidate_id = candidate_id
        self.__name = name
        self.__party = party
        self.__position = position

        if self.__position.lower() == "president":
            self.__city = None
        else:
            self.__city = city

        self.__vote_count = 0

    def get_candidate_id(self):
        return self.__candidate_id

    def get_name(self):
        return self.__name

    def get_party(self):
        return self.__party

    def get_position(self):
        return self.__position

    def get_city(self):
        return self.__city

    def get_vote_count(self):
        return self.__vote_count

    def set_name(self, name):
        self.__name = name

    def set_party(self, party):
        self.__party = party

    def set_position(self, position):
        self.__position = position

    def set_city(self, city):
        if self.__position.lower() != "president":
            self.__city = city
        else:
            self.__city = None

    def add_vote(self):
        self.__vote_count += 1

    def __str__(self):
        location = None
        if self.__city is not None:
            location = self.__city
        return f"[{self.__party}] {self.__name} - {self.__position} ({location})"