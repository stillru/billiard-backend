from extensions import db


class WinReason(db.Model):
    __tablename__ = "win_reason"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
