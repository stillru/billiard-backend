from extensions import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)
    played_games = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    user = db.relationship("User", back_populates="player_id")
    tournament_participants = db.relationship(
        "TournamentParticipant", back_populates="player"
    )
    matches_as_player1 = db.relationship(
        "Match", foreign_keys="Match.player1_id", back_populates="player1_relation"
    )
    matches_as_player2 = db.relationship(
        "Match", foreign_keys="Match.player2_id", back_populates="player2_relation"
    )
    events = db.relationship("Event", back_populates="player", overlaps="event_records")
