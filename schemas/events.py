import logging
import marshmallow as ma
from marshmallow import post_load, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from models.events import (
    GlobalEvent,
    Event,
    HitBallEventData,
    BallPottedEventData,
    FoulEventData,
)
from models.user import User


class GlobalEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GlobalEvent
        load_instance = True

    event_type = ma.fields.String(required=True)
    data = ma.fields.Dict(allow_none=True)
    state = ma.fields.String(allow_none=True)
    status = ma.fields.Integer(allow_none=True)

    @post_load
    def combine_fields(self, data, **kwargs):
        event_type = data.get("event_type")

        # Validate event_type
        if event_type not in [
            "start_game",
            "player_scored",
            "end_game",
            "start_play",
            "update_play",
            "end_play",
            "register_user",
            "register_player",
        ]:
            raise ValidationError(f"'{event_type}' is not a valid event type.")

        event_data = data.get("data", {})

        # Process specific event types
        if event_type == "start_game":
            player1_id = event_data.get("player1_id")
            player2_id = event_data.get("player2_id")
            player1 = User.query.filter_by(id=player1_id).first()
            player2 = User.query.filter_by(id=player2_id).first()
            if not player1 or not player2:
                raise ValidationError("Player IDs must be valid and existing users.")
            data["description"] = (
                f"{player1.name} and {player2.name} are starting a game..."
            )

        # Add additional processing for other event types as needed
        elif event_type in ["start_play", "register_player"]:
            logging.debug(data)
        return data


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True


class HitBallEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HitBallEventData
        load_instance = True

    ball_number = ma.fields.Integer(required=True)
    description = ma.fields.String()
    pocket_id = ma.fields.Integer()


class BallPottedEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BallPottedEventData
        load_instance = True

    ball_number = ma.fields.Integer(required=True)
    pocket_id = ma.fields.Integer(required=True)
    description = ma.fields.String()
    write = ma.fields.String()


class FoulEventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FoulEventData
        load_instance = True

    reason = ma.fields.String(required=True)
    description = ma.fields.String()
