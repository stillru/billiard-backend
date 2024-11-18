from extensions import db


class Club(db.Model):
    __tablename__ = "clubs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    table_count = db.Column(db.Integer, nullable=True, default=0)
    games_played = db.Column(db.Integer, nullable=True, default=0)
    price_per_hour = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    top_players = db.Column(db.String, nullable=True)

    photos = db.relationship("Photo", back_populates="club")
    games = db.relationship("Game", back_populates="club")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)

    club = db.relationship("Club", back_populates="photos")
