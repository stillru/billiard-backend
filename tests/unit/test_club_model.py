import logging

from backend.extensions import db
from backend.models.club import Club
from backend.schemas.club import ClubSchema


def test_club_model(app):
    club_schema = ClubSchema()
    club_instance = Club(name="Meridian", address="Beograd, Serbija")
    club_data = club_schema.dump(club_instance)
    loaded_club = club_schema.load(
        club_data, session=db.session
    )  # Add session if needed
    logging.info(club_data)
    assert loaded_club.name == "Meridian"
    assert club_data["name"] == "Meridian"


def test_club_model_wrong(app):
    club_schema = ClubSchema()
    club_instance = Club(name="Meridian", address="Beograd, Serbija", table_count=34)
    club_data = club_schema.dump(club_instance)
    loaded_club = club_schema.load(
        club_data, session=db.session
    )  # Add session if needed
    logging.info(club_data)
    assert loaded_club.name == "Meridian"
    assert club_data["name"] == "Meridian"
