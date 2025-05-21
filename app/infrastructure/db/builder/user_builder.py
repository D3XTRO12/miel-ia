from ..dataclass.user import User

class UserBuilder:
    def __init__(self, dni, email, last_name, name, password):
        self.user = User()
        self.user.dni = dni
        self.user.email = email
        self.user.last_name = last_name
        self.user.name = name
        self.user.password = password

    def build(self):
        return self.user
