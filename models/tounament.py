import enum

from extensions import db


class TournamentPhase(enum.Enum):
    REGISTRATION = "Registration"  # Регистрация
    GROUP_STAGE = "Group Stage"  # Групповой этап
    KNOCKOUT = "Knockout"  # Нокаут
    FINAL = "Final"  # Финал
    COMPLETED = "Completed"  # Завершен


class TournamentType(enum.Enum):
    ELIMINATION = "Elimination"
    ROUND_ROBIN = "Round Robin"
    SWISS = "Swiss"


class TournamentParticipant(db.Model):
    __tablename__ = "tournament_participants"
    tournament_id = db.Column(
        db.Integer, db.ForeignKey("tournaments.id"), primary_key=True
    )
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), primary_key=True)

    player = db.relationship("Player", back_populates="tournament_participants")
    tournament = db.relationship("Tournament", back_populates="participants")


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    tournament_type = db.Column(db.Enum(TournamentType), nullable=False)  # Тип турнира
    prize_pool = db.Column(db.Float, nullable=True)  # Призовой фонд
    organizer = db.Column(db.String, nullable=False)  # Учредитель турнира
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)  # Дата начала
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)  # Дата окончания
    player_count = db.Column(
        db.Integer, nullable=False, default=0
    )  # Количество игроков
    phase = db.Column(
        db.Enum(TournamentPhase), nullable=False, default=TournamentPhase.REGISTRATION
    )
    games = db.relationship("Game", back_populates="tournament")
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=True)
    season = db.relationship("Season", back_populates="tournaments")
    participants = db.relationship("TournamentParticipant", back_populates="tournament")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )
