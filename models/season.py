from extensions import db


class Season(db.Model):
    __tablename__ = "season"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    games = db.relationship("Game", back_populates="season")
    tournaments = db.relationship("Tournament", back_populates="season")
