class Party:
    def __init__(self, party_id, name, abbreviation):
        self.__party_id = party_id
        self.__name = name
        self.__abbreviation = abbreviation

    def get_party_id(self):
        return self.__party_id

    def get_name(self):
        return self.__name

    def get_abbreviation(self):
        return self.__abbreviation

    def __str__(self):
        return f"{self.__name} [{self.__abbreviation}]"