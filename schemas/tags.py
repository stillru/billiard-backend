import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.news import Tag


class TagSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True

    id = ma.fields.Int(dump_only=True)
    name = ma.fields.String()
