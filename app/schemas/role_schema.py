from app.models import Role
from marshmallow import fields, Schema, post_load, validate

class RoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))

    @post_load
    def make_role(self, data, **kwargs):
        return Role(**data)