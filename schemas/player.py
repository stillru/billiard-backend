import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from models.player import Player


class PlayerSchema(SQLAlchemySchema):
    class Meta:
        model = Player
        load_instance = True

    id = auto_field(dump_only=True)
    name = auto_field(required=True)
