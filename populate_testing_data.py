from werkzeug.security import generate_password_hash
from app import app
from models import Player, Tag, Game, Play
from extensions import db

with app.app_context():
    db.create_all()

    # Генерация хешей паролей
    users = [
        Player(
            username="user1",
            email="user1@example.com",
            password_hash=generate_password_hash("password1"),
        ),
        Player(
            username="user2",
            email="user2@example.com",
            password_hash=generate_password_hash("password2"),
        ),
        Player(
            username="user3",
            email="user3@example.com",
            password_hash=generate_password_hash("password3"),
        ),
        Player(
            username="user4",
            email="user4@example.com",
            password_hash=generate_password_hash("password4"),
        ),
        Player(
            username="user5",
            email="user5@example.com",
            password_hash=generate_password_hash("password5"),
        ),
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()
