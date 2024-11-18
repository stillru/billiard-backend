from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from models.match import Match


class MatchSchema(SQLAlchemySchema):
    class Meta:
        model = Match
        load_instance = True

    id = auto_field(dump_only=True)
    player1_id = auto_field(required=False)
    player2_id = auto_field(required=False)
    winner_id = auto_field(required=False, allow_none=True)  # Allow None for winner_id

    @validates("player1_id")
    def validate_player1_id(self, value):
        if value is None:
            raise ValidationError("player1_id must not be null.")

    @validates("player2_id")
    def validate_player2_id(self, value):
        if value is None:
            raise ValidationError("player2_id must not be null.")

    @validates("winner_id")
    def validate_winner_id(self, value, **kwargs):
        if value is not None:  # Allow None as it represents an undefined winner.
            if value not in [self.context["player1_id"], self.context["player2_id"]]:
                raise ValidationError(
                    "winner_id must be either player1_id or player2_id."
                )
