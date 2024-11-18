import marshmallow as ma

from backend.schemas import PlayerSchema


class PlaySchema(ma.Schema):
    id = ma.fields.Integer()
    game_id = ma.fields.Integer()
    game_type = ma.fields.Integer()
    start_time = ma.fields.DateTime()
    end_time = ma.fields.DateTime()
    winner_id = ma.fields.Integer()
    winner = ma.fields.Nested(PlayerSchema)
