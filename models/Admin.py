from models.Voter import  Voter
class Admin(Voter):
    def __init__(self, tc_no, name, password, admin_role="General"):
        super().__init__(tc_no, name, password)
        self.__admin_role = admin_role

    def get_admin_role(self):
        return self.__admin_role

    def set_admin_role(self, role):
        self.__admin_role = role

    def __str__(self):
        return f"[ADMIN] {self.get_name()} - Role: {self.__admin_role}"


