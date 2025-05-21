from ..dataclass.user_role import UserRole

class UserRoleBuilder:
    def __init__(self, role_id, user_id):
        self.user_role = UserRole()
        self.user_role.role_id = role_id
        self.user_role.user_id = user_id

    def build(self):
        return self.user_role
