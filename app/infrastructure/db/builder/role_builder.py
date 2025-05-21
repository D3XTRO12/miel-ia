from ..dataclass.role import Role

class RoleBuilder:
    def __init__(self, name):
        self.role = Role()
        self.role.name = name

    def build(self):
        return self.role
