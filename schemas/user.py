import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
    new_player = ma.fields.Boolean()
