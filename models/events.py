from enum import Enum as PyEnum

from extensions import db


class EventType(PyEnum):
    HIT_BALL = "hit_ball"
    BALL_POTTED = "BALL_POTTED"
    FOUL = "foul"
    TURN_END = "turn_end"
    GAME_WIN = "game_win"


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(
        db.Integer, db.ForeignKey("matches.id", ondelete="CASCADE"), nullable=False
    )
    event_type = db.Column(db.Enum(EventType), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    match = db.relationship("Match", back_populates="events")
    player = db.relationship(
        "Player", back_populates="events", overlaps="event_records"
    )


class HitBallEventData(db.Model):
    __tablename__ = "hit_ball_event_data"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    ball_number = db.Column(db.Integer, nullable=False)
    event = db.relationship("Event", backref="hit_ball_data")


class BallPottedEventData(db.Model):
    __tablename__ = "ball_potted_event_data"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    ball_number = db.Column(db.Integer, nullable=False)
    pocket_id = db.Column(db.Integer, nullable=False)  # Идентификатор лузы

    event = db.relationship("Event", backref="ball_potted_data")


class FoulEventData(db.Model):
    __tablename__ = "foul_event_data"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    reason = db.Column(db.String(255), nullable=False)

    event = db.relationship("Event", backref="foul_data")


class GlobalEvent(db.Model):
    __tablename__ = "all_events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
