from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from backend.models.club import Club, Photo


class PhotoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Photo
        load_instance = True


class ClubSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Club
        load_instance = True

    id = fields.Integer(load_only=True)

    photos = fields.List(fields.Nested(PhotoSchema))

    """
    @validates("latitude")
    def validate_latitude_id(self, value):
        if value is None:
            raise ValidationError("No latitude for club")


    @validates("longitude")
    def validate_longitude_id(self, value):
        if value is None:
            raise ValidationError("No longitude for club")
    """
