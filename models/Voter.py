from models.User import User
class Voter(User):
    def __init__(self, tc_no, name, password, city):
        super().__init__(tc_no, name, password)
        self.__city = city
        self.__has_voted_president = False
        self.__has_voted_mayor = False

    def get_city(self):
        return self.__city

    def get_has_voted_president(self):
        return self.__has_voted_president

    def get_has_voted_mayor(self):
        return self.__has_voted_mayor

    def mark_voted_president(self):
        self.__has_voted_president = True

    def mark_voted_mayor(self):
        self.__has_voted_mayor = True