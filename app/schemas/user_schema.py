from app.models import User
from marshmallow import validate, validates, fields, Schema, post_load, ValidationError

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))
    dni = fields.Int(required=True, validate=validate.Range(min=1))
    gender = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(max=50))
    address = fields.Str(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=200))
    role_type = fields.Str(required=True, validate=validate.Length(max=50))

    @validates('dni')
    def validate_dni(self, value):
        if value <= 0:
            raise ValidationError('DNI must be a positive number')
        if len(str(value)) < 8:
            raise ValidationError('DNI must have at least 8 digits')
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)