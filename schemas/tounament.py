from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.tounament import TournamentParticipant, Tournament
from schemas.game import GameSchema
from schemas.season import SeasonSchema
from schemas.player import PlayerSchema


class TournamentParticipantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TournamentParticipant
        load_instance = True

    # Включаем данные о игроке и турнире
    player = fields.Nested(PlayerSchema)
    # tournament = fields.Nested(TournamentSchema)


class TournamentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tournament
        load_instance = True

    # Включаем связанные игры, участников и сезон в схему турнира
    games = fields.List(fields.Nested(GameSchema))
    participants = fields.List(fields.Nested(TournamentParticipantSchema))
    season = fields.Nested(SeasonSchema)
