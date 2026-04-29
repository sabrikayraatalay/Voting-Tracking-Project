class User: #Base class

    def __init__(self, tc_no, name, password):
        self.__tc_no = tc_no
        self.__name = name
        self.__password = password

    def get_tc_no(self):
        return self.__tc_no

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def set_name(self, name):
        self.__name = name

    def set_password(self, password):
        self.__password = password

    def __str__(self):
        return f"User: {self.__name} (TC: {self.__tc_no})"