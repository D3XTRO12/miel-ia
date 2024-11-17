from app.models import UserRole
from marshmallow import fields, Schema, post_load

class UserRoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    role_id = fields.UUID(required=True)

    @post_load
    def make_user_role(self, data, **kwargs):
        return UserRole(**data)