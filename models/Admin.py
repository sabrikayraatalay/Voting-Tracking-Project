from models.Voter import Voter

class Admin(Voter):
    # DÜZELTME: 'city' parametresi eklendi
    def __init__(self, tc_no, name, password, city, admin_role="General"):
        # DÜZELTME: 'city' parametresi miras alınan Voter sınıfına gönderildi
        super().__init__(tc_no, name, password, city)
        self.__admin_role = admin_role

    def get_admin_role(self):
        return self.__admin_role

    def set_admin_role(self, role):
        self.__admin_role = role

    def __str__(self):
        return f"[ADMIN] {self.get_name()} - Role: {self.__admin_role}"