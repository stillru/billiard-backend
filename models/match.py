from enum import Enum as PyEnum

from extensions import db


class MatchStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    player2_id = db.Column(db.Integer, db.ForeignKey("players.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game_type = db.Column(db.String)
    match_date = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Enum(MatchStatus), default=MatchStatus.IN_PROGRESS)

    events = db.relationship("Event", back_populates="match")
    player1_relation = db.relationship(
        "Player", foreign_keys=[player1_id], back_populates="matches_as_player1"
    )
    player2_relation = db.relationship(
        "Player", foreign_keys=[player2_id], back_populates="matches_as_player2"
    )
    winner = db.relationship("Player", foreign_keys=[winner_id])
    game = db.relationship("Game", back_populates="matches")
