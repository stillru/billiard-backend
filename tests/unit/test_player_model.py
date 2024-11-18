from backend.models.player import Player
import logging

from backend.extensions import db

logger = logging.getLogger(__name__)
"""
#TODO: Переписать
def test_new_user(app):
"""
# GIVEN a User model
# WHEN a new User is created
# THEN check the email, hashed_password, and role fields are defined correctly
"""
    user = User("John Doe", "patkennedy79@gmail.com", "FlaskIsAwesome")
    logger.debug(user)
    assert user.email == "patkennedy79@gmail.com"
    assert user.password_hash != "FlaskIsAwesome"


def test_new_player(client):
    user = User("John Doe", "patkennedy79@gmail.com", "FlaskIsAwesome")
    player = Player(user.id, 1, 1)
    logger.debug(player)
    assert player is not None
"""
