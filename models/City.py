class City:
    def __init__(self, city_id, name, region):
        self.__city_id = city_id
        self.__name = name
        self.__region = region

    def get_city_id(self):
        return self.__city_id

    def get_name(self):
        return self.__name

    def get_region(self):
        return self.__region

    def __str__(self):
        return f"{self.__name} ({self.__region})"